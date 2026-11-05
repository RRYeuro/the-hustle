"""
The Hustle bot. One file, everything in it.

Slash commands
  /setup       (admin)  Build and decorate the server: icon, emojis, channels, rules, gallery, posts.
  /update      (admin)  Post a patch note and ping the Hustle Tester role.
  /play                 Link to the game.
  /build                What build is live on the website right now.
  /bug                  Pop-up form -> posts a bug report to #hustle-bugs.
  /feedback             Pop-up form -> posts to #hustle-feedback.
  /idea                 Pop-up form -> posts to #hustle-ideas with vote buttons.
  /score                Pop-up form -> posts to #hustle-high-scores and saves it.
  /leaderboard          Top 10 saved scores.
  /character            Shows one of the 6 characters.
  /tip                  A random street tip.

Automatic
  - Watches the live game page. When the Build number changes it posts to #hustle-patch-notes
    with the newest commit message and pings Hustle Tester.
  - A "Get the Tester role" button in #welcome.
  - Shows the live Build number as the bot's status.

Run:  see README.md
"""
import asyncio
import io
import json
import os
import random
import re
import sys
import time

import aiohttp
import discord
from discord import app_commands
from discord.ext import tasks

try:
    from PIL import Image
except ImportError:  # pillow is only needed for /setup
    Image = None

HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.environ.get("DISCORD_TOKEN", "")
GUILD_ID = int(os.environ.get("GUILD_ID", "1567836539134939270"))
GAME_URL = os.environ.get("GAME_URL", "https://rryeuro.github.io/the-hustle/")
GAME_REPO = os.environ.get("GAME_REPO", "RRYeuro/the-hustle")
ART = os.environ.get("ART_DIR", os.path.join(HERE, "hustle_art"))
STATE_FILE = os.environ.get("STATE_FILE", os.path.join(HERE, "state.json"))
GAME = "The Hustle: No Days Off"

RED, GREEN, GOLD, DARK = 0xE74C3C, 0x2ECC71, 0xF1C40F, 0x2B2D31
TESTER = "Hustle Tester"

CH = {
    "play": "hustle-play", "notes": "hustle-patch-notes", "feedback": "hustle-feedback",
    "bugs": "hustle-bugs", "ideas": "hustle-ideas", "scores": "hustle-high-scores",
    "welcome": "welcome", "rules": "rules", "ann": "announcements",
    "crew": "meet-the-crew", "blocks": "the-blocks", "whips": "whips-and-safes",
}

BLOCKS = ["Eastside", "Southpark", "The Bottom", "Westgate", "Northline", "Downtown"]
CARS = [
    ("beater", "Old Buick", "$2,500", "Rust and a loud muffler, but the trunk is big."),
    ("civic", "Honda Civic", "$6,000", "Clean, quiet, gets you around."),
    ("charger", "Dodge Charger", "$14,000", "Rep +2. People notice this one."),
    ("tahoe", "Chevy Tahoe", "$28,000", "Rep +3. Room for everything."),
    ("rover", "Range Rover", "$60,000", "Rep +6. Top of the lot."),
]
SAFES = [
    ("0", "Small safe", "$800", "+30 safe space. Cash, drugs and guns that can't get jacked."),
    ("1", "Floor safe", "$4,000", "+80 safe space."),
    ("2", "Vault room", "$15,000", "+200 safe space."),
]
EMOJI_DRUGS = {"loud": "weed", "bars": "xans", "snow": "coke", "kicks": "molly", "percs": "percs", "phones": "lean"}
GUN_EMOJIS = ["pistol", "draco", "glizzy", "smitty", "switchy", "rifle", "shotgun", "micro", "revolver", "baby"]
RULES = [
    ("1. Respect everybody", "Honest feedback is welcome. Being mean is not."),
    ("2. No spam or ads", "Keep it about the game and the server."),
    ("3. Nothing illegal or hateful", "No hate, harassment, or real-life illegal stuff."),
    ("4. It's a game", "Keep real people and real crimes out of it."),
    ("5. Bugs go in #hustle-bugs", "Use /bug so I can fix them fast."),
]
TIPS = [
    "Cash in your safe at home can't get jacked, raided or busted. Strict parents can't find it either.",
    "A recruited plug stops selling to you. Keep your big plug connect if you want the good prices.",
    "Plugs only give you trust once a day per deal, so don't waste trips buying tiny amounts.",
    "Serving the Js on a crew's block with a drug they don't carry won't start beef.",
    "Strung-out customers skip the I'm open blast. Serving them is a risk.",
    "Weed customers who get top-quality weed 5 times in a row become potheads and text you more.",
    "Talk 8 or higher can talk your parents out of kicking you out.",
    "A lawyer on call means the next bust costs you nothing.",
    "Big plugs almost always have good product, but not always. Test when you can.",
    "Cash on you gets noticed by strict parents. Get a job for cover, and stash the rest.",
    "Doing chores while grounded takes a day off the grounding.",
    "High-trust plugs will sometimes text you drugs they don't normally carry. Those are hot, so heat goes up.",
]

# ---------------------------------------------------------------- state
_state = {"build": None, "scores": []}


def load_state():
    global _state
    try:
        with open(STATE_FILE) as f:
            _state.update(json.load(f))
    except (OSError, ValueError):
        pass


def save_state():
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(_state, f)
    except OSError:
        pass


# ---------------------------------------------------------------- helpers
def art(*parts):
    p = os.path.join(ART, *parts)
    return p if os.path.exists(p) else None


def fpath(p, name):
    return discord.File(p, filename=name)


def chan(guild, key):
    name = CH[key]
    return discord.utils.find(lambda c: c.name == name, guild.text_channels)


def tester_role(guild):
    return discord.utils.find(lambda r: r.name == TESTER, guild.roles)


def is_admin(inter: discord.Interaction):
    return inter.user.guild_permissions.administrator or inter.user.id == getattr(inter.guild, "owner_id", 0)


async def fetch_build(session):
    try:
        async with session.get(GAME_URL, timeout=aiohttp.ClientTimeout(total=20),
                               headers={"Cache-Control": "no-cache"}) as r:
            txt = await r.text()
        m = re.search(r"const BUILD='(v\d+)'", txt)
        return m.group(1) if m else None
    except Exception:
        return None


async def latest_commit_line(session):
    try:
        async with session.get(f"https://api.github.com/repos/{GAME_REPO}/commits/main",
                               timeout=aiohttp.ClientTimeout(total=20)) as r:
            data = await r.json()
        msg = data["commit"]["message"].split("\n")[0].strip()
        return msg or None
    except Exception:
        return None


async def channel_empty(ch):
    try:
        async for _ in ch.history(limit=1):
            return False
    except discord.Forbidden:
        return False
    return True


async def send_embed(ch, embed, files=None, pin=False, content=None, roles=False):
    msg = await ch.send(content=content, embed=embed, files=files or [],
                        allowed_mentions=discord.AllowedMentions(roles=roles))
    if pin:
        try:
            await msg.pin()
        except discord.HTTPException:
            pass
    await asyncio.sleep(0.6)
    return msg


# ---------------------------------------------------------------- forms
class BugForm(discord.ui.Modal, title="Report a bug"):
    build = discord.ui.TextInput(label="Build number (main menu)", placeholder="v161", max_length=12, required=False)
    device = discord.ui.TextInput(label="Device and browser", placeholder="Phone Safari, Chromebook Chrome...", max_length=60)
    what = discord.ui.TextInput(label="What happened?", style=discord.TextStyle.paragraph, max_length=900)
    expected = discord.ui.TextInput(label="What should have happened?", style=discord.TextStyle.paragraph,
                                    max_length=500, required=False)

    async def on_submit(self, inter: discord.Interaction):
        ch = chan(inter.guild, "bugs")
        if not ch:
            return await inter.response.send_message("I can't find #hustle-bugs. Ask an admin to run /setup.", ephemeral=True)
        e = discord.Embed(title="Bug report", description=str(self.what), color=RED)
        e.add_field(name="Build", value=str(self.build) or "?", inline=True)
        e.add_field(name="Device", value=str(self.device), inline=True)
        if str(self.expected):
            e.add_field(name="Expected", value=str(self.expected), inline=False)
        e.set_footer(text=f"From {inter.user.display_name}")
        msg = await ch.send(embed=e)
        await msg.add_reaction("🐛")
        await inter.response.send_message(f"Sent to {ch.mention}. Thank you.", ephemeral=True)


class FeedbackForm(discord.ui.Modal, title="Tell me what you think"):
    liked = discord.ui.TextInput(label="What did you like?", style=discord.TextStyle.paragraph, max_length=700, required=False)
    notliked = discord.ui.TextInput(label="What didn't you like or got confusing?", style=discord.TextStyle.paragraph,
                                    max_length=700, required=False)
    want = discord.ui.TextInput(label="What should I add next?", style=discord.TextStyle.paragraph, max_length=500, required=False)

    async def on_submit(self, inter: discord.Interaction):
        ch = chan(inter.guild, "feedback")
        if not ch:
            return await inter.response.send_message("I can't find #hustle-feedback. Ask an admin to run /setup.", ephemeral=True)
        e = discord.Embed(title="Feedback", color=GREEN)
        for name, v in (("Liked", self.liked), ("Didn't like", self.notliked), ("Wants next", self.want)):
            if str(v).strip():
                e.add_field(name=name, value=str(v), inline=False)
        if not e.fields:
            return await inter.response.send_message("You left everything blank.", ephemeral=True)
        e.set_footer(text=f"From {inter.user.display_name}")
        await ch.send(embed=e)
        await inter.response.send_message(f"Sent to {ch.mention}. Thank you.", ephemeral=True)


class IdeaForm(discord.ui.Modal, title="Suggest an idea"):
    title_ = discord.ui.TextInput(label="Short title", max_length=80)
    body = discord.ui.TextInput(label="The idea", style=discord.TextStyle.paragraph, max_length=900)

    async def on_submit(self, inter: discord.Interaction):
        ch = chan(inter.guild, "ideas")
        if not ch:
            return await inter.response.send_message("I can't find #hustle-ideas. Ask an admin to run /setup.", ephemeral=True)
        e = discord.Embed(title=str(self.title_), description=str(self.body), color=GOLD)
        e.set_footer(text=f"From {inter.user.display_name}")
        msg = await ch.send(embed=e)
        for em in ("👍", "👎"):
            await msg.add_reaction(em)
        await inter.response.send_message(f"Posted in {ch.mention}. Vote with the thumbs.", ephemeral=True)


class ScoreForm(discord.ui.Modal, title="Post your run"):
    character = discord.ui.TextInput(label="Character", placeholder="Slick, Tank, Shade, Val, Casper, Lucky", max_length=20)
    days = discord.ui.TextInput(label="Days survived", placeholder="120", max_length=6)
    cash = discord.ui.TextInput(label="Biggest bag (cash)", placeholder="250000", max_length=12)
    note = discord.ui.TextInput(label="How did it end? (optional)", max_length=120, required=False)

    async def on_submit(self, inter: discord.Interaction):
        try:
            days = int(re.sub(r"[^\d]", "", str(self.days)) or "0")
            cash = int(re.sub(r"[^\d]", "", str(self.cash)) or "0")
        except ValueError:
            return await inter.response.send_message("Days and cash need to be numbers.", ephemeral=True)
        rec = {"user": inter.user.display_name, "uid": inter.user.id, "char": str(self.character)[:20],
               "days": days, "cash": cash, "note": str(self.note), "t": int(time.time())}
        _state["scores"].append(rec)
        _state["scores"] = sorted(_state["scores"], key=lambda r: r["cash"], reverse=True)[:200]
        save_state()
        ch = chan(inter.guild, "scores")
        if ch:
            e = discord.Embed(title=f"{inter.user.display_name} posted a run", color=GOLD)
            e.add_field(name="Character", value=rec["char"])
            e.add_field(name="Days", value=f"{days:,}")
            e.add_field(name="Bag", value=f"${cash:,}")
            if rec["note"]:
                e.add_field(name="How it ended", value=rec["note"], inline=False)
            await ch.send(embed=e)
        await inter.response.send_message("Saved. Check /leaderboard.", ephemeral=True)


class TesterButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get the Hustle Tester role", style=discord.ButtonStyle.success, custom_id="hustle:tester")
    async def give(self, inter: discord.Interaction, button: discord.ui.Button):
        role = tester_role(inter.guild)
        if not role:
            return await inter.response.send_message("The role doesn't exist yet. An admin needs to run /setup.", ephemeral=True)
        if role in inter.user.roles:
            try:
                await inter.user.remove_roles(role)
            except discord.Forbidden:
                return await inter.response.send_message("Move my role above 'Hustle Tester' in Server Settings > Roles first.", ephemeral=True)
            return await inter.response.send_message("Tester role removed. You won't get update pings.", ephemeral=True)
        try:
            await inter.user.add_roles(role)
        except discord.Forbidden:
            return await inter.response.send_message(
                "I can't hand out that role yet. An admin needs to drag my role above 'Hustle Tester' in Server Settings > Roles.",
                ephemeral=True)
        await inter.response.send_message("You're a Hustle Tester now. You'll get update pings.", ephemeral=True)


# ---------------------------------------------------------------- characters
def load_chars():
    p = art("chars.json")
    try:
        with open(p) as f:
            return json.load(f)
    except Exception:
        return []


# ---------------------------------------------------------------- server setup
def square(path, size, mode="icon"):
    im = Image.open(path).convert("RGBA" if mode == "emoji" else "RGB")
    w, h = im.size
    s = min(w, h)
    left = (w - s) // 2
    im = im.crop((left, 0 if mode == "emoji" else (h - s) // 2, left + s, (0 if mode == "emoji" else (h - s) // 2) + s)).resize((size, size))
    b = io.BytesIO()
    im.save(b, "PNG")
    return b.getvalue()


async def build_server(guild: discord.Guild, dry: bool, say, refresh_icon: bool = False):
    me = guild.me
    title = art("titleart", "titleart.jpg")
    if Image is None:
        say("Pillow isn't installed, so I'll skip the icon and emojis.")
    icon = art("icon.png")
    if icon and (refresh_icon or not guild.icon):
        say("server icon")
        if not dry:
            with open(icon, "rb") as f:
                await guild.edit(icon=f.read(), reason="Hustle setup")
    if Image:
        have = {e.name for e in guild.emojis}
        wanted = []
        for cid, nm in (("slick", "slick"), ("tank", "tank"), ("shade", "shade"), ("val", "val"),
                        ("country", "casper"), ("lucky", "lucky")):
            p = art("portraits", cid + ".jpg")
            if p:
                wanted.append((f"hustle_{nm}", p))
        for gid, nm in EMOJI_DRUGS.items():
            p = art("drugpics", gid + ".jpg")
            if p:
                wanted.append((f"drug_{nm}", p))
        for g in GUN_EMOJIS:
            p = art("gunpics", g + ".jpg")
            if p:
                wanted.append((f"gun_{g}", p))
        room = guild.emoji_limit - len(guild.emojis)
        added = 0
        for name, p in wanted:
            if name in have or room <= 0:
                continue
            added += 1
            if not dry:
                try:
                    await guild.create_custom_emoji(name=name, image=square(p, 128, "emoji"), reason="Hustle setup")
                    room -= 1
                except discord.HTTPException as e:
                    say(f"emoji {name} failed: {e}")
                await asyncio.sleep(1.0)
        say(f"{added} emoji to add")

    roles = {r.name: r for r in guild.roles}
    if TESTER not in roles:
        say(f"role {TESTER}")
        if not dry:
            await guild.create_role(name=TESTER, colour=discord.Colour(GREEN), mentionable=True, reason="Hustle setup")

    async def get_cat(name, position=None):
        cat = discord.utils.find(lambda c: c.name.lower() == name.lower(), guild.categories)
        if cat:
            return cat
        say(f"category {name}")
        if dry:
            return None
        kw = {"position": position} if position is not None else {}
        return await guild.create_category(name, reason="Hustle setup", **kw)

    async def get_chan(cat, key, topic, readonly):
        name = CH[key]
        c = discord.utils.find(lambda x: x.name == name, guild.text_channels)
        if c:
            return c
        say(f"channel #{name}")
        if dry:
            return None
        ow = {}
        if readonly:
            ow[guild.default_role] = discord.PermissionOverwrite(send_messages=False, add_reactions=True)
            ow[me] = discord.PermissionOverwrite(send_messages=True, attach_files=True, embed_links=True)
        return await guild.create_text_channel(name, category=cat, topic=topic, overwrites=ow, reason="Hustle setup")

    start = await get_cat("START HERE", 0)
    welcome = await get_chan(start, "welcome", "What this server is and how to play.", True)
    rules = await get_chan(start, "rules", "Short rules. Keep it cool.", True)
    ann = await get_chan(start, "ann", "Big news about the game.", True)
    game = await get_cat("THE HUSTLE (GAME)")
    play = await get_chan(game, "play", "Link to the newest build.", True)
    notes = await get_chan(game, "notes", "What changed in each build.", True)
    fb = await get_chan(game, "feedback", "What did you like or not like? Be honest, this is my first game.", False)
    bugs = await get_chan(game, "bugs", "Found a bug? Use /bug.", False)
    ideas = await get_chan(game, "ideas", "Ideas for the game. Use /idea.", False)
    scores = await get_chan(game, "scores", "How far did you get? Use /score.", False)
    gal = await get_cat("GALLERY")
    crew = await get_chan(gal, "crew", "The 6 playable characters.", True)
    blocks = await get_chan(gal, "blocks", "Where it all goes down.", True)
    whips = await get_chan(gal, "whips", "Cars and safes you can buy.", True)
    if dry:
        return

    if welcome and await channel_empty(welcome):
        e = discord.Embed(
            title=f"Welcome to {GAME}",
            description=("A street-hustle life sim. Pick a block, find your plugs, build your bag, and try to make it to "
                         "the top. Inspired by Trapper RPG and BitLife.\n\nI made this myself and it is my **first try**, "
                         f"so your feedback means a lot.\n\n**[Play it here]({GAME_URL})**\nWorks on a phone or a laptop. "
                         "The main menu shows a Build number so you can tell if you have the newest one."),
            color=RED)
        files = []
        if title:
            files = [fpath(title, "title.jpg")]
            e.set_image(url="attachment://title.jpg")
        e.add_field(name="Commands", value="`/play` `/bug` `/feedback` `/idea` `/score` `/leaderboard` `/character` `/tip` `/build`", inline=False)
        e.add_field(name="Update pings", value="Press the button below to get pinged on every new build.", inline=False)
        m = await welcome.send(embed=e, files=files, view=TesterButton())
        try:
            await m.pin()
        except discord.HTTPException:
            pass
    if rules and await channel_empty(rules):
        e = discord.Embed(title="Server rules", color=GOLD)
        for t, d in RULES:
            e.add_field(name=t, value=d, inline=False)
        await send_embed(rules, e, pin=True)
    if ann and await channel_empty(ann):
        e = discord.Embed(title="The server is open",
                          description=f"**{GAME}** is playable right now.\n[Play it]({GAME_URL})\n\nBugs: `/bug`. Ideas: `/idea`.",
                          color=GREEN)
        await send_embed(ann, e)
    if play and await channel_empty(play):
        e = discord.Embed(title=f"Play {GAME}", url=GAME_URL,
                          description="If the Build number on the main menu looks old, reopen the app or hard refresh. "
                                      "New builds can take 10 to 20 minutes to show up.", color=RED)
        files = []
        if title:
            files = [fpath(title, "t.jpg")]
            e.set_image(url="attachment://t.jpg")
        await send_embed(play, e, files=files, pin=True)
    if notes and await channel_empty(notes):
        e = discord.Embed(title="Patch notes", description="New builds get posted here automatically.", color=DARK)
        await send_embed(notes, e, pin=True)
    if bugs and await channel_empty(bugs):
        e = discord.Embed(title="Found a bug?", description="Type `/bug` and fill in the form. It posts here.", color=RED)
        await send_embed(bugs, e, pin=True)
    if fb and await channel_empty(fb):
        e = discord.Embed(title="Tell me what you think", description="Type `/feedback` and fill in the form. What was fun, what was confusing, what should I add?", color=GREEN)
        await send_embed(fb, e, pin=True)
    if crew and await channel_empty(crew):
        for c in load_chars():
            p = art("portraits", c["id"] + ".jpg")
            e = discord.Embed(title=f"{c['name']}: {c['role']}", description=c["story"], color=RED)
            e.add_field(name="Perk", value=c.get("perk") or "None", inline=False)
            files = []
            if p:
                files = [fpath(p, "p.jpg")]
                e.set_thumbnail(url="attachment://p.jpg")
            await send_embed(crew, e, files=files)
    if blocks and await channel_empty(blocks):
        for i, nm in enumerate(BLOCKS):
            p = art("blockart", f"{i}.jpg")
            if p:
                e = discord.Embed(title=nm, color=DARK)
                e.set_image(url="attachment://b.jpg")
                await send_embed(blocks, e, files=[fpath(p, "b.jpg")])
    if whips and await channel_empty(whips):
        for key, nm, cost, sub in CARS:
            p = art("carpics", key + ".jpg")
            if p:
                e = discord.Embed(title=f"{nm}  ·  {cost}", description=sub, color=GOLD)
                e.set_image(url="attachment://c.jpg")
                await send_embed(whips, e, files=[fpath(p, "c.jpg")])
        for key, nm, cost, sub in SAFES:
            p = art("safepics", key + ".jpg")
            if p:
                e = discord.Embed(title=f"{nm}  ·  {cost}", description=sub, color=GREEN)
                e.set_image(url="attachment://s.jpg")
                await send_embed(whips, e, files=[fpath(p, "s.jpg")])
    if welcome and guild.system_channel != welcome:
        try:
            await guild.edit(system_channel=welcome, reason="Hustle setup")
        except discord.HTTPException:
            pass


# ---------------------------------------------------------------- the bot
class HustleBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        self.members_on = os.environ.get("MEMBER_INTENT") == "1"
        intents.members = self.members_on
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.http_session = None

    async def setup_hook(self):
        self.http_session = aiohttp.ClientSession()
        self.add_view(TesterButton())
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        try:
            await self.tree.sync(guild=guild)
        except discord.Forbidden:
            print("\nCan't register slash commands (Missing Access). Re-invite the bot with BOTH scopes: "
                  "bot + applications.commands (Developer Portal > OAuth2 > URL Generator), and make sure "
                  "GUILD_ID is the server the bot is in. The bot will keep running without slash commands.\n")
        self.watch_build.start()

    async def close(self):
        if self.http_session:
            await self.http_session.close()
        await super().close()

    async def on_ready(self):
        print(f"Logged in as {self.user} (server {GUILD_ID})")

    async def on_member_join(self, member: discord.Member):
        ch = chan(member.guild, "welcome")
        if ch:
            await ch.send(f"Welcome {member.mention}. Read #rules, then try the game: {GAME_URL}")

    @tasks.loop(minutes=10)
    async def watch_build(self):
        build = await fetch_build(self.http_session)
        if not build:
            return
        await self.change_presence(activity=discord.Game(name=f"The Hustle {build}"))
        old = _state.get("build")
        if old == build:
            return
        _state["build"] = build
        save_state()
        if old is None:
            return  # first run: just remember it
        guild = self.get_guild(GUILD_ID)
        ch = chan(guild, "notes") if guild else None
        if not ch:
            return
        line = await latest_commit_line(self.http_session)
        role = tester_role(guild)
        e = discord.Embed(title=f"{build} is live", color=RED,
                          description=(line + "\n\n" if line and line.lower() != "game update" else "") + f"[Play the newest build]({GAME_URL})")
        await ch.send(content=role.mention if role else None, embed=e,
                      allowed_mentions=discord.AllowedMentions(roles=True))

    @watch_build.before_loop
    async def _wait(self):
        await self.wait_until_ready()


client = HustleBot()
tree = client.tree
CHARS = ["slick", "tank", "shade", "val", "casper", "lucky"]


@tree.command(name="setup", description="Admin: build and decorate the server for The Hustle.")
@app_commands.describe(dry_run="Only list what it would do", refresh_icon="Replace the server icon with the newest one")
async def cmd_setup(inter: discord.Interaction, dry_run: bool = False, refresh_icon: bool = False):
    if not is_admin(inter):
        return await inter.response.send_message("Admins only.", ephemeral=True)
    await inter.response.defer(ephemeral=True, thinking=True)
    lines = []
    try:
        await build_server(inter.guild, dry_run, lines.append, refresh_icon)
    except discord.Forbidden as e:
        return await inter.followup.send(f"Missing a permission. Give me Administrator. ({e})", ephemeral=True)
    head = "Dry run, nothing changed:" if dry_run else "Done:"
    body = "\n".join("• " + x for x in lines) or "Everything already exists."
    await inter.followup.send(f"{head}\n{body}"[:1900], ephemeral=True)


@tree.command(name="update", description="Admin: post a patch note and ping Hustle Testers.")
@app_commands.describe(title="Like: Build v162", text="What changed", ping="Ping the Hustle Tester role")
async def cmd_update(inter: discord.Interaction, title: str, text: str, ping: bool = True):
    if not is_admin(inter):
        return await inter.response.send_message("Admins only.", ephemeral=True)
    ch = chan(inter.guild, "notes")
    if not ch:
        return await inter.response.send_message("No #hustle-patch-notes. Run /setup first.", ephemeral=True)
    role = tester_role(inter.guild)
    e = discord.Embed(title=title, description=f"{text}\n\n[Play the newest build]({GAME_URL})", color=RED)
    await ch.send(content=role.mention if (ping and role) else None, embed=e,
                  allowed_mentions=discord.AllowedMentions(roles=True))
    await inter.response.send_message(f"Posted in {ch.mention}.", ephemeral=True)


@tree.command(name="play", description="Link to the game.")
async def cmd_play(inter: discord.Interaction):
    e = discord.Embed(title=f"Play {GAME}", url=GAME_URL, description=GAME_URL, color=RED)
    await inter.response.send_message(embed=e)


@tree.command(name="build", description="What build is live on the website right now?")
async def cmd_build(inter: discord.Interaction):
    await inter.response.defer()
    b = await fetch_build(client.http_session)
    await inter.followup.send(f"Live build: **{b}**" if b else "Couldn't read the live build right now.")


@tree.command(name="bug", description="Report a bug.")
async def cmd_bug(inter: discord.Interaction):
    await inter.response.send_modal(BugForm())


@tree.command(name="feedback", description="Tell me what you think of the game.")
async def cmd_feedback(inter: discord.Interaction):
    await inter.response.send_modal(FeedbackForm())


@tree.command(name="idea", description="Suggest something for the game.")
async def cmd_idea(inter: discord.Interaction):
    await inter.response.send_modal(IdeaForm())


@tree.command(name="score", description="Post how far you got.")
async def cmd_score(inter: discord.Interaction):
    await inter.response.send_modal(ScoreForm())


@tree.command(name="leaderboard", description="Top 10 biggest bags.")
async def cmd_leaderboard(inter: discord.Interaction):
    rows = _state.get("scores", [])[:10]
    if not rows:
        return await inter.response.send_message("No runs posted yet. Use /score.")
    lines = [f"**{i + 1}.** {r['user']} · {r['char']} · ${r['cash']:,} · {r['days']:,} days" for i, r in enumerate(rows)]
    await inter.response.send_message(embed=discord.Embed(title="Leaderboard", description="\n".join(lines), color=GOLD))


@tree.command(name="character", description="Show one of the 6 characters.")
@app_commands.choices(who=[app_commands.Choice(name=n.title(), value=n) for n in CHARS])
async def cmd_character(inter: discord.Interaction, who: app_commands.Choice[str]):
    cid = "country" if who.value == "casper" else who.value
    c = next((x for x in load_chars() if x["id"] == cid), None)
    if not c:
        return await inter.response.send_message("Couldn't find that character.", ephemeral=True)
    e = discord.Embed(title=f"{c['name']}: {c['role']}", description=c["story"], color=RED)
    e.add_field(name="Perk", value=c.get("perk") or "None", inline=False)
    p = art("portraits", cid + ".jpg")
    if p:
        e.set_thumbnail(url="attachment://p.jpg")
        return await inter.response.send_message(embed=e, file=fpath(p, "p.jpg"))
    await inter.response.send_message(embed=e)


@tree.command(name="tip", description="A random street tip.")
async def cmd_tip(inter: discord.Interaction):
    await inter.response.send_message(f"💡 {random.choice(TIPS)}")


if __name__ == "__main__":
    if not TOKEN:
        print("Set DISCORD_TOKEN first. See README.md.")
        sys.exit(1)
    load_state()
    client.run(TOKEN)
