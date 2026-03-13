#!/usr/bin/env bash
set -euo pipefail
echo '🔧 irsanai-nexus-repo Setup'
command -v git &>/dev/null || { echo "'git' nicht gefunden"; exit 1; }
command -v python3 &>/dev/null || { echo "'python3' nicht gefunden"; exit 1; }
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q || true
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo '⚠️  .env aus .env.example erstellt — bitte Werte eintragen!'
fi
mkdir -p /tmp/irsanai-nexus-work reports_output
echo '🚀 Setup abgeschlossen!'
