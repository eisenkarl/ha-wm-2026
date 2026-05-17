#!/bin/bash
# ===================================================================
# WM 2026 - Halbautomatisches Installations-Skript
# ===================================================================
# Voraussetzung: lokal in HA-Container/-OS ausfuehrbar (z.B. via SSH).
# Kopiert die drei zentralen Dateien an die richtigen Stellen unter /config.
# Aenderungen an configuration.yaml musst du selbst vornehmen (siehe README).
# ===================================================================
set -e

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HA_CONFIG="${HA_CONFIG:-/config}"

echo "==> WM 2026 Installer"
echo "    Quelle: $SRC_DIR"
echo "    Ziel:   $HA_CONFIG"
echo

if [ ! -d "$HA_CONFIG" ]; then
  echo "FEHLER: $HA_CONFIG nicht gefunden. Bitte HA_CONFIG-Variable setzen, z.B.:"
  echo "  HA_CONFIG=/usr/share/hassio/homeassistant ./install.sh"
  exit 1
fi

echo "==> Verzeichnisse anlegen..."
mkdir -p "$HA_CONFIG/packages"
mkdir -p "$HA_CONFIG/python_scripts"
mkdir -p "$HA_CONFIG/blueprints/automation/wm2026"

echo "==> Dateien kopieren..."
cp -v "$SRC_DIR/packages/wm2026.yaml" "$HA_CONFIG/packages/wm2026.yaml"
cp -v "$SRC_DIR/python_scripts/wm2026_bracket.py" "$HA_CONFIG/python_scripts/wm2026_bracket.py"
cp -v "$SRC_DIR/blueprints/automation/wm2026_notifications.yaml" \
   "$HA_CONFIG/blueprints/automation/wm2026/wm2026_notifications.yaml"

chmod +x "$HA_CONFIG/python_scripts/wm2026_bracket.py"

echo
echo "==> Installation abgeschlossen."
echo
echo "Naechste Schritte:"
echo "  1. configuration.yaml ergaenzen falls noch nicht geschehen:"
echo
echo "     homeassistant:"
echo "       packages: !include_dir_named packages"
echo
echo "  2. Home Assistant neu starten."
echo "  3. Dashboard manuell erstellen (siehe dashboards/wm2026_dashboard.yaml)."
echo "  4. Blueprint-Automation einrichten (optional, siehe README)."
