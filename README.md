# WM 2026 - Home Assistant Integration

Eine komplette Home-Assistant-Lösung zur Verfolgung der FIFA Fussball-Weltmeisterschaft 2026 (USA / Kanada / Mexiko, 11. Juni - 19. Juli 2026).

## Features

- **Tagesübersicht** aller WM-Spiele (heute oder nächster Spieltag)
- **Komplette Gruppenphase** - alle 12 Gruppen (A-L) mit Live-Tabellen und allen 72 Spielen
- **Komplette KO-Phase** - Sechzehntelfinale, Achtelfinale, Viertelfinale, Halbfinale, Spiel um Platz 3, Finale
- **Lieblings-Team-Tracker** mit freier Auswahl aus allen 48 Teams (Standard: Deutschland)
- **Live-Ergebnisse** und automatische **Sieger-Hervorhebung** während laufender Spiele
- **Push-Benachrichtigungen** (optional, via Blueprint):
  - Tägliche Vorschau (Uhrzeit wählbar)
  - Anpfiff-Reminder 10 Min vor Lieblings-Team-Spiel
  - Halbzeit + Schlusspfiff Live-Updates
- **Keine API-Keys nötig** - nutzt die öffentliche ESPN-JSON-API

## Voraussetzungen

- Home Assistant **2024.6** oder neuer (für Blueprint Auto-Discovery & input_select)
- `python3` im HA Core Container (standardmässig vorhanden)
- Optional: **Mobile App Companion** für Push-Benachrichtigungen

## Installation

### Schritt 1: Package-Support aktivieren (einmalig)

In deiner `configuration.yaml` ergänzen (falls noch nicht vorhanden):

```yaml
homeassistant:
  packages: !include_dir_named packages
```

Dann `/config/packages/` Verzeichnis erstellen falls noch nicht da.

### Schritt 2: Dateien kopieren

| Quelldatei (aus diesem Repo) | Ziel in deinem HA |
|---|---|
| `packages/wm2026.yaml` | `/config/packages/wm2026.yaml` |
| `python_scripts/wm2026_bracket.py` | `/config/python_scripts/wm2026_bracket.py` |
| `blueprints/automation/wm2026_notifications.yaml` | `/config/blueprints/automation/wm2026/wm2026_notifications.yaml` |

**Hinweis Python-Skript-Pfad:** Die HA-Komponente `python_scripts` (Sandbox) ist **nicht** gemeint. Der Pfad `/config/python_scripts/` wird hier nur als Ablage genutzt, das Skript wird via `command_line` ausgeführt. Du kannst auch einen anderen Pfad wählen, dann musst du im `command_line`-Block in `wm2026.yaml` den Pfad anpassen.

```bash
chmod +x /config/python_scripts/wm2026_bracket.py
```

### Schritt 3: HA neustarten

`Einstellungen -> System -> Reparieren -> Neu starten` oder via Terminal:

```bash
ha core restart
```

### Schritt 4: Konfiguration überprüfen

Nach dem Neustart prüfen ob die Sensoren existieren:

`Entwicklerwerkzeuge -> Zustände`

Suche nach:
- `sensor.wm_2026_api` (Roh-API)
- `sensor.wm_2026_bracket` (Komplett-Bracket via Python-Skript)
- `sensor.wm_2026_spiele_heute`
- `sensor.wm_2026_naechster_spieltag`
- `sensor.wm_2026_lieblings_team_naechstes_spiel`
- `input_select.wm_2026_favorite_team`

### Schritt 5: Dashboard einrichten

`Einstellungen -> Dashboards -> Dashboard hinzufügen -> "Neues Dashboard von Grund auf"`

Name z.B. `WM 2026`, Icon `mdi:soccer`.

Neues Dashboard öffnen -> Stift -> 3-Punkte-Menü -> **Raw-Konfigurations-Editor** -> kompletten Inhalt durch `dashboards/wm2026_dashboard.yaml` ersetzen.

### Schritt 6 (optional): Push-Benachrichtigungen aktivieren

`Einstellungen -> Automatisierungen & Szenen -> Blueprints -> Automatisierung erstellen`

Wähle **"WM 2026 - Push-Benachrichtigungen"** aus der Liste und konfiguriere:

- **Benachrichtigungs-Service:** z.B. `notify.mobile_app_meinphone`
- **Uhrzeit Tagesvorschau:** z.B. `08:00:00`
- **Tagesvorschau / Anpfiff-Reminder / Live-Updates:** je nach Wunsch ein/aus

## Konfiguration

### Lieblings-Team ändern

Im HA-UI:

`Einstellungen -> Geräte & Dienste -> Helfer -> WM 2026 Lieblings-Team`

Oder direkt im Dashboard, dort steht die Auswahl ganz oben.

Verfügbare Teams sind die 49 vorkonfigurierten WM-Teilnehmer (Drei-Buchstaben-Code, z.B. `GER`, `AUT`, `SUI`, `BRA`, `ARG`...). Bei Bedarf kannst du die Liste in `packages/wm2026.yaml` unter `input_select` erweitern oder anpassen.

### Update-Intervall

Standardmässig:
- **Tagesübersicht** (REST-API): alle 5 Minuten
- **Kompletter Bracket** (Python-Skript): alle 30 Minuten

Anpassbar in `packages/wm2026.yaml` über `scan_interval`.

### Manuelles Update erzwingen

`Entwicklerwerkzeuge -> Aktionen -> homeassistant.update_entity -> sensor.wm_2026_bracket`

## Datenquelle

Diese App nutzt die inoffizielle ESPN-JSON-API (`site.api.espn.com`). Diese ist öffentlich erreichbar und benötigt keine Authentifizierung. Bitte fair nutzen - Standard-Polling-Intervalle nicht unter 5 Min setzen.

ESPN ist nicht Teil dieses Projekts und übernimmt keine Garantie für die Datenverfügbarkeit. Falls die API zwischenzeitlich nicht erreichbar ist, behält der Sensor seinen letzten Stand.

## Troubleshooting

### Sensoren bleiben auf `unknown` / `unavailable`

1. Logs prüfen: `Einstellungen -> System -> Protokolle` nach "wm_2026" filtern
2. Python-Skript manuell testen über SSH/Terminal:
   ```bash
   python3 /config/python_scripts/wm2026_bracket.py GER
   ```
   Sollte JSON ausgeben. Falls Fehler: Internet-Zugang aus HA Core Container prüfen.
3. ESPN-API direkt testen:
   ```bash
   curl https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard
   ```

### Konfiguration ungültig nach Installation

- Sicherstellen dass `packages: !include_dir_named packages` in `configuration.yaml` steht
- Datei muss exakt unter `/config/packages/wm2026.yaml` liegen
- YAML-Einrückung prüfen (`Einstellungen -> System -> Reparieren -> Konfiguration prüfen`)

### Push-Benachrichtigungen kommen nicht an

- Mobile App Companion installiert und in HA registriert?
- Korrekter notify-Service eingetragen? (`Entwicklerwerkzeuge -> Aktionen -> "notify."` durchsuchen)
- Im Blueprint die jeweilige Funktion aktiviert?

## Lizenz

MIT - siehe `LICENSE`. Frei für private und kommerzielle Nutzung.

## Mitwirken

Pull Requests willkommen. Issues bitte mit:
- HA-Version
- Sensor-State der betroffenen Entity
- Auszug aus den Logs

## Credits

- **ESPN** für die öffentliche Sport-Daten-API
- **Home Assistant Community** für die hervorragende Plattform
