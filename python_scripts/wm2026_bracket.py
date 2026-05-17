#!/usr/bin/env python3
"""WM 2026 vollstaendiger Turnierbaum-Fetcher fuer Home Assistant.

Liefert ein kompaktes JSON ueber stdout mit:
- Gruppen-Tabellen (Standings) der 12 WM-Gruppen
- Gruppenspiele pro Gruppe (72 Spiele)
- KO-Phase: Sechzehntel-, Achtel-, Viertel-, Halbfinale + Spiel um Platz 3 + Finale (32 Spiele)

Wird vom HA command_line-Sensor aufgerufen, alle 30 Minuten.
Datenquelle: ESPN inoffizielle JSON-API (kein Key noetig).

Lizenz: MIT
"""

import json
import sys
import urllib.request
from datetime import datetime, timezone

# ESPN-API hat ein 100-Events-Limit je Aufruf, daher zwei Calls
GROUP_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"
    "?dates=20260611-20260627"
)
KO_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"
    "?dates=20260628-20260720"
)
STANDINGS_URL = (
    "https://site.web.api.espn.com/apis/v2/sports/soccer/fifa.world/standings"
)

KO_ROUNDS = [
    "round-of-32",
    "round-of-16",
    "quarterfinals",
    "semifinals",
    "3rd-place-match",
    "final",
]

# Lieblings-Team kann via Env-Variable oder CLI-Arg gesetzt werden.
# Default: GER (Deutschland). Beispiele: AUT, SUI, ITA, BRA, ARG, ESP, ENG, FRA, NED, USA
FAV_TEAM = "GER"
if len(sys.argv) > 1 and sys.argv[1].strip():
    FAV_TEAM = sys.argv[1].strip().upper()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "HomeAssistant-WM2026/1.1"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def stat_get(stats, name, default=0):
    for s in stats:
        if s.get("name") == name:
            return s.get("value", default)
    return default


def parse_standings(data, fav_abbr):
    groups = {}
    team_to_group = {}
    for child in data.get("children", []):
        gname = child.get("name", "").replace("Group ", "").strip() or "?"
        entries = child.get("standings", {}).get("entries", [])
        rows = []
        for e in entries:
            team = e.get("team", {})
            stats = e.get("stats", [])
            abbr = team.get("abbreviation", "?")
            team_to_group[abbr] = gname
            rows.append({
                "rank": int(stat_get(stats, "rank", 0)),
                "team": team.get("displayName", "?"),
                "abbr": abbr,
                "played": int(stat_get(stats, "gamesPlayed", 0)),
                "won": int(stat_get(stats, "wins", 0)),
                "draw": int(stat_get(stats, "ties", 0)),
                "loss": int(stat_get(stats, "losses", 0)),
                "gf": int(stat_get(stats, "pointsFor", 0)),
                "ga": int(stat_get(stats, "pointsAgainst", 0)),
                "gd": int(stat_get(stats, "pointDifferential", 0)),
                "pts": int(stat_get(stats, "points", 0)),
                "favorite": abbr == fav_abbr,
            })
        rows.sort(key=lambda r: (r["rank"] or 99, -r["pts"], -r["gd"]))
        groups[gname] = rows
    return groups, team_to_group


def compact_event(e, fav_abbr):
    c = e["competitions"][0]
    competitors = c.get("competitors", [])
    home = next((t for t in competitors if t.get("homeAway") == "home"), {})
    away = next((t for t in competitors if t.get("homeAway") == "away"), {})

    def team_info(t):
        team = t.get("team", {}) if t else {}
        return {
            "name": team.get("displayName", "TBD"),
            "abbr": team.get("abbreviation", "?"),
            "score": int(t.get("score", 0)) if t and t.get("score") not in (None, "") else 0,
            "winner": t.get("winner", False) if t else False,
        }

    status = c.get("status", {}).get("type", {})
    status_name = status.get("name", "")
    home_info = team_info(home)
    away_info = team_info(away)
    return {
        "date": e["date"],
        "short": e.get("shortName", ""),
        "home": home_info,
        "away": away_info,
        "city": c.get("venue", {}).get("address", {}).get("city", ""),
        "status": status.get("description", "?"),
        "is_final": status_name == "STATUS_FULL_TIME",
        "is_live": status_name in ("STATUS_IN_PROGRESS", "STATUS_HALFTIME"),
        "favorite": home_info["abbr"] == fav_abbr or away_info["abbr"] == fav_abbr,
    }


def main():
    events = []
    errors = []
    for url, label in [(GROUP_URL, "group"), (KO_URL, "ko")]:
        try:
            data = fetch(url)
            events.extend(data.get("events", []))
        except Exception as e:
            errors.append(f"{label}: {e}")

    try:
        standings_data = fetch(STANDINGS_URL)
        groups, team_to_group = parse_standings(standings_data, FAV_TEAM)
    except Exception as e:
        groups, team_to_group = {}, {}
        errors.append(f"standings: {e}")

    group_matches = {g: [] for g in groups}
    ko_matches = {r: [] for r in KO_ROUNDS}

    for e in events:
        season = e.get("season", {})
        slug = season.get("slug", "")
        compact = compact_event(e, FAV_TEAM)
        if slug == "group-stage":
            grp = team_to_group.get(compact["home"]["abbr"]) or team_to_group.get(compact["away"]["abbr"])
            if grp:
                group_matches.setdefault(grp, []).append(compact)
        elif slug in KO_ROUNDS:
            ko_matches[slug].append(compact)

    for g in group_matches:
        group_matches[g].sort(key=lambda m: m["date"])
    for r in ko_matches:
        ko_matches[r].sort(key=lambda m: m["date"])

    out = {
        "count": len(events),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "favorite_team": FAV_TEAM,
        "groups": groups,
        "group_matches": group_matches,
        "ko_matches": ko_matches,
    }
    if errors:
        out["errors"] = errors
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
