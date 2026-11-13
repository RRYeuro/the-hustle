#!/bin/bash
# ./deploy.sh "msg [silent]"  -> pushes the-hustle to GitHub Pages (main)
set -e
R=/home/claude/the-hustle; MSG="${1:?need a commit message}"
mkdir -p $R/dev
cp /home/claude/ideas.md /home/claude/game-status.md /home/claude/art-prompts-all.md /home/claude/art-list-all.html /home/claude/deploy.sh /home/claude/tools/*.py /home/claude/tools/skin27.html $R/dev/ 2>/dev/null || true
cp /tmp/claude-0/t_*.py $R/dev/ 2>/dev/null || true
H=$(md5sum $R/index.html | cut -c1-8)
sed -i "s/const CACHE='hustle-[0-9a-f]*'/const CACHE='hustle-$H'/" $R/sw.js
git -C $R add -A
git -C $R commit -q -m "$MSG

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0114ktvoKANi5fD5UtBz3Qjb"
git -C $R -c push.negotiate=true push -q origin HEAD:main
git -C $R log --oneline -1
