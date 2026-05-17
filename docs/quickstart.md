# Quickstart - Installation in 5 Minuten

Diese Kurzanleitung fuehrt dich durch die wichtigsten Schritte. Fuer Details siehe `README.md`.

## Voraussetzung

Zugriff auf das `/config/`-Verzeichnis deines Home Assistant (z.B. via **File Editor** Add-on, **Studio Code Server** Add-on, **Samba**, **SSH** oder **Visual Studio Code Remote**).

## 1. Package-Verzeichnis aktivieren

In `configuration.yaml` einmalig diese Zeilen am Anfang ergaenzen (falls nicht vorhanden):

```yaml
homeassistant:
  packages: !include_dir_named packages
```

Verzeichnis anlegen falls nicht vorhanden:

```bash
mkdir -p /config/packages
mkdir -p /config/python_scripts
mkdir -p /config/blueprints/automation/wm2026
```

## 2. Drei Dateien kopieren

```text
ha-wm-2026/packages/wm2026.yaml
    -> /config/packages/wm2026.yaml

ha-wm-2026/python_scripts/wm2026_bracket.py
    -> /config/python_scripts/wm2026_bracket.py

ha-wm-2026/blueprints/automation/wm2026_notifications.yaml
    -> /config/blueprints/automation/wm2026/wm2026_notifications.yaml
```

## 3. HA neu starten

`Einstellungen -> System -> Reparieren -> 3-Punkte-Menue -> Konfiguration neu laden`
oder
`Einstellungen -> System -> Neu starten`

## 4. Dashboard hinzufuegen

`Einstellungen -> Dashboards -> Dashboard hinzufuegen -> Neues Dashboard von Grund auf`

Name: `WM 2026` | Icon: `mdi:soccer`

Dashboard oeffnen -> Bleistift (oben rechts) -> 3-Punkte-Menue -> **Raw-Konfigurations-Editor** -> kompletten Inhalt durch Inhalt von `dashboards/wm2026_dashboard.yaml` ersetzen.

## 5. Lieblings-Team auswaehlen

Im neuen Dashboard ganz oben in der "Einstellungen"-Karte das gewuenschte Team waehlen (Standard: `GER`).

Nach Aenderung dauert es bis zu 30 Min, bis der Bracket-Sensor das uebernimmt (oder manuell aktualisieren: `Entwicklerwerkzeuge -> Aktionen -> homeassistant.update_entity -> sensor.wm_2026_bracket`).

## 6. Push-Notifications (optional)

`Einstellungen -> Automatisierungen -> Blueprints` -> Blueprint **"WM 2026 - Push-Benachrichtigungen"** waehlen -> Automation erstellen.

Felder ausfuellen:
- **Benachrichtigungs-Service:** dein Mobile-App-Service, z.B. `notify.mobile_app_meinphone`
- **Tagesvorschau aktivieren:** EIN
- Andere nach Geschmack

Speichern - fertig.

## Fertig!

Heute (vor WM-Start) zeigt das Dashboard "Naechster Spieltag" mit Countdown bis zum Eroeffnungsspiel. Waehrend der WM rotiert die Anzeige automatisch auf die jeweils aktuellen Spiele.
