# Changelog

Alle nennenswerten Aenderungen an diesem Projekt werden hier dokumentiert.

## [1.3.0] - 2026-05-17

### Hinzugefuegt / Added
- Mehrsprachigkeit: Deutsch (de) + Englisch (en) per `input_select.wm_2026_language` umschaltbar
- Vollstaendige i18n im Dashboard (Titel, Tabellen-Header, Phasen-Namen) und im Blueprint
- `t` (Translation-Dict) als Attribut am Bracket-Sensor
- README.en.md fuer englischsprachige User
- Badge "i18n: de | en" im README

### Geaendert / Changed
- Python-Skript akzeptiert zweites Argument fuer Sprache (`de`/`en`)
- Blueprint-Texte sind jetzt bilingual und holen sich Strings dynamisch aus dem Sensor
- Bracket-Refresh-Automation triggert nun auch bei Sprachwechsel

## [1.2.1] - 2026-05-17

### Behoben
- Lieblings-Team-Wechsel war erst nach bis zu 30 Minuten sichtbar (command_line scan_interval)
- Neue Automation `wm2026_refresh_on_team_change` aktualisiert den Bracket-Sensor sofort beim Team-Wechsel

## [1.2.0] - 2026-05-17

### Hinzugefuegt
- Nationalflaggen-Bilder fuer alle Teams (via flagcdn.com)
- FIFA-3-Buchstaben zu ISO-3166-2 Mapping mit 200+ Eintraegen
- `iso2_map` und `favorite_iso2` Attribute am Bracket-Sensor
- UK-Sonderfaelle: ENG=gb-eng, SCO=gb-sct, WAL=gb-wls, NIR=gb-nir

### Geaendert
- `input_select.wm_2026_favorite_team`: `initial:` entfernt - HA merkt sich nun den zuletzt gewaehlten Wert ueber Restarts hinweg
- Dashboard-Karten zeigen jetzt Flag-PNGs neben jedem Team-Namen

## [1.0.1] - 2026-05-17

### Hinzugefuegt
- Logo (logo.png) und Icon (icon.png) für Repo + HACS
- Badges im README (Release, License, HA-Version, HACS)

## [1.0.0] - 2026-05-17

### Hinzugefuegt
- Initiale Veroeffentlichung
- HA Package `wm2026.yaml` mit REST/Template/Command-Line-Sensoren
- Python-Skript `wm2026_bracket.py` fuer kompletten Bracket
- Lieblings-Team frei waehlbar via `input_select.wm_2026_favorite_team`
- Blueprint fuer Push-Benachrichtigungen (Tagesvorschau, Anpfiff, Halbzeit, Schlusspfiff)
- Beispiel-Dashboard mit Tagesuebersicht, Gruppenphase, KO-Phase
- README mit Installations-Anleitung
- HACS-kompatible Struktur (`hacs.json`)
- MIT-Lizenz
