#!/bin/bash
# ./deploy.sh "msg [silent]"  -> pushes the-hustle to GitHub Pages (main)
set -e
R=/home/claude/the-hustle; MSG="${1:?need a commit message}"
mkdir -p $R/dev
mkdir -p $R/dev/skins $R/dev/tests
cp /home/claude/game-status.md /home/claude/art-prompts-all.md /home/claude/art-list-all.html /home/claude/deploy.sh /home/claude/tools/*.py $R/dev/ 2>/dev/null || true
# ideas.md: the repo copy (dev/ideas.md) is the master; never overwrite it from /home/claude
cp $R/dev/ideas.md /home/claude/ideas.md 2>/dev/null || true
# feature source copies: every tools/skinN.html whose script is in index.html
for f in /home/claude/tools/skin*.html; do n=$(basename $f .html); grep -q "id=\"${n}js\"" $R/index.html && cp $f $R/dev/skins/; done
rm -f $R/zz_*.html
cp /tmp/claude-0/t_*.py $R/dev/tests/ 2>/dev/null || true
python3 -I /home/claude/tools/extract.py
python3 -I /home/claude/tools/codemap.py
H=$(md5sum $R/index.html | cut -c1-8)
sed -i "s/const CACHE='hustle-[0-9a-f]*'/const CACHE='hustle-$H'/" $R/sw.js
git -C $R add -A
git -C $R commit -q -m "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0114ktvoKANi5fD5UtBz3Qjb"
git -C $R -c push.negotiate=true push -q origin HEAD:main
git -C $R log --oneline -1
