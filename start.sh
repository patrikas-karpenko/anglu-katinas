#!/usr/bin/env bash
# Starts Anglų katinas. Usage: ./start.sh
cd "$(dirname "$0")"
MODEL=$(python3 -c "import json;print(json.load(open('config.json'))['model'])")
if command -v ollama >/dev/null 2>&1; then
  curl -s http://localhost:11434/api/tags >/dev/null 2>&1 || (ollama serve >/dev/null 2>&1 &) ; sleep 1
  ollama list | grep -q "^${MODEL%%:*}" || ollama pull "$MODEL"
else
  echo "Ollama not found – exercises will work, explanations and chat won't. See README."
fi
exec python3 server.py
