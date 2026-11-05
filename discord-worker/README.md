# Always-on Discord commands (Cloudflare Worker)

Paste `worker.js` into a free Cloudflare Worker. Commands, buttons and forms then work 24/7 with no bot running.
Set DISCORD_PUBLIC_KEY, DISCORD_TOKEN (secret), GUILD_ID and a KV binding named HUSTLE, then paste the Worker URL
into the Discord Developer Portal as the Interactions Endpoint URL.

/setup still lives in discord-bot/bot.py. While the Interactions Endpoint URL is set, Discord sends interactions only to the Worker,
so to run /setup: clear the URL in the portal, run the bot, run /setup, stop the bot, put the URL back.
