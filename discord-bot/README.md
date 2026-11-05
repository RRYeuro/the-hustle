# The Hustle bot

One bot for the whole server: setup, rules, gallery, update pings, bug/feedback/idea forms, leaderboard.

## First time (Chromebook Linux terminal)
    git clone https://github.com/RRYeuro/the-hustle.git
    cd the-hustle/discord-bot
    ./run.sh

## Every time after
    cd the-hustle/discord-bot && ./run.sh     # pulls the newest bot code itself

In Discord an admin types `/setup` once. Members use /bug /feedback /idea /score /leaderboard /character /tip /play /build.
Admins use `/update` for a manual patch note. New builds are announced automatically while the bot is running.

The bot is only online while run.sh is running. Always-on update pings come from the GitHub Action (.github/workflows/discord.yml) using a channel webhook.
Never paste the token anywhere except the terminal prompt. Reset it in the Developer Portal if it leaks.
