#!/bin/bash
# Starts the bot. Asks for the token once and keeps it in .token (never uploaded: it is in .gitignore).
cd "$(dirname "$0")"
git pull -q 2>/dev/null
pip install -q --break-system-packages -r requirements.txt
if [ ! -s .token ]; then
  read -p "Bot token (right-click or Ctrl+Shift+V to paste): " T
  echo "$T" > .token; chmod 600 .token
fi
export DISCORD_TOKEN="$(cat .token)"
python3 bot.py
