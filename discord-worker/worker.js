// The Hustle: always-on Discord commands on a free Cloudflare Worker.
// No bot connection needed. Discord sends every slash command, button and form here.
//
// Settings (Worker > Settings > Variables and Secrets):
//   DISCORD_PUBLIC_KEY  (text)    Developer Portal > General Information > Public Key
//   DISCORD_TOKEN       (secret)  the bot token (only used to post messages and give roles)
//   GUILD_ID            (text)    1567836539134939270
// Optional: KV namespace binding named HUSTLE (for /score and /leaderboard).

const GAME_URL = "https://rryeuro.github.io/the-hustle/";
const GAME = "The Hustle: No Days Off";
const RAW = "https://raw.githubusercontent.com/RRYeuro/the-hustle/main/discord-bot/hustle_art/";
const API = "https://discord.com/api/v10";
const RED = 0xe74c3c, GREEN = 0x2ecc71, GOLD = 0xf1c40f;
const TESTER = "Hustle Tester";
const AREAS = [
  ["Money Testers", "💸", 0x2ECC71, "cost of living, Expenses tab, dirty and clean cash, laundering, businesses and upgrades"],
  ["Street Testers", "🔌", 0xE67E22, "plugs, Big plug outcomes, crew, upkeep, wars, your own gang"],
  ["Heat Testers", "🚔", 0xE74C3C, "heat, raids, cops, house arrest, on the run, prison, parole"],
  ["Rap Testers", "🎤", 0x9B59B6, "songs, shows, tours, merch, the three labels, your own label, buyouts"],
  ["Life Testers", "🏠", 0x3498DB, "parents, school, kids, girlfriend, friends, cars, homes, jewelry, clothes, block party"],
];
const areaMenu = () => ({ type: 1, components: AREAS.map(([n, e]) => ({ type: 2, style: 2, label: n.replace(" Testers", ""), emoji: { name: e }, custom_id: "hustle:area:" + n })) });
const CH = { bugs: "hustle-bugs", feedback: "hustle-feedback", ideas: "hustle-ideas", scores: "hustle-high-scores", notes: "hustle-patch-notes" };

const PICK_ROLES = [
  [TESTER, "Get pinged on every new build"], ["Phone Player", "I play on my phone"], ["Laptop Player", "I play on a laptop or Chromebook"],
  ["Main: Slick", "Slick is my guy"], ["Main: Tank", "Tank is my guy"], ["Main: Shade", "Shade is my guy"],
  ["Main: Val", "Val is my girl"], ["Main: Casper", "Casper is my guy"], ["Main: Lucky", "Lucky is my guy"],
];
const CHARS = [
 {
  "id": "slick",
  "name": "Slick",
  "role": "The Talker",
  "story": "Jalen \"Slick\" Moore. Started rapping about stealing cars, and the songs were not made up. He could get into anything on four wheels and talk his way out of any stop, until the one he could not. Did three years, came home with a rap name and a plug list, and now he talks his way into every deal.",
  "perk": "Knows 2 plugs from the jump and they trust him. +20% odds when talking price."
 },
 {
  "id": "tank",
  "name": "Tank",
  "role": "The Fallen Star",
  "story": "Darius \"Tank\" Coleman. Star running back on a full ride, scouts at every game, headed to the league. Tore his knee up in the championship game and it was over. Tried the 9-to-5, got let go, and missed the love he used to get on Friday nights. The streets still know his name, so he started trapping.",
  "perk": "Knows 1 plug. People still know his name: starts with 15 rep, +10 strength and a soldier. Bad knee: worse at running away."
 },
 {
  "id": "shade",
  "name": "Shade",
  "role": "The Ghost",
  "story": "Andre \"Shade\" Wallace. His songs are all over the city, but nobody has seen his face. No interviews, no pictures, no shows. People argue about who he really is. That mystery is the reason nobody can pin anything on him.",
  "perk": "Always watching: knows 3 plugs and can spot fakes. Heat builds half as fast. Gets away from cops way more."
 },
 {
  "id": "val",
  "name": "Val",
  "role": "The Boss Lady",
  "story": "Valentina \"Val\" Reyes. Ran the register at her family's taqueria since she was twelve and learned the back door moves more money than the front. When her dad got sick, she took over everything.",
  "perk": "Knows 2 plugs. Runs it like a business: the Js pay her 10% more and her workers never steal."
 },
 {
  "id": "country",
  "name": "Casper",
  "role": "Raised by the Block",
  "story": "Cody \"Casper\" Walsh. Only white boy on Eastside growing up. His mom worked doubles, so the block raised him: the corner store fed him, the older homies taught him. Everybody knows Casper, and he ain't going nowhere.",
  "perk": "Knows 1 plug. The block raised him: every crew starts out respecting him, and staying cool with cops is easier."
 },
 {
  "id": "lucky",
  "name": "Lucky",
  "role": "The Rich Girl",
  "story": "Keisha \"Lucky\" Grant. Gated community, private school, daddy's money. She started rapping and nobody took her seriously because she never struggled. Now she is out here to prove she is real, and she is spending her trust fund to do it.",
  "perk": "Only plug she knows is her ex, Tre. Starts with the most cash, and things just fall her way: double the odds on every card drop."
 }
];
const TIPS = [
  "Cash in your safe at home can't get jacked, raided or busted. Strict parents can't find it either.",
  "A recruited plug stops selling to you. Keep your big plug connect if you want the good prices.",
  "Plugs only give you trust once a day per deal, so don't waste trips buying tiny amounts.",
  "Strung-out customers skip the I'm open blast. Serving them is a risk.",
  "Weed customers who get top-quality weed 5 times in a row become potheads and text you more.",
  "Talk 8 or higher can talk your parents out of kicking you out.",
  "A lawyer on call means the next bust costs you nothing.",
  "Big plugs almost always have good product, but not always. Test when you can.",
  "Cash on you gets noticed by strict parents. Get a job for cover, and stash the rest.",
  "Doing chores while grounded takes a day off the grounding. You have to be at the house.",
  "Talk 4 lets you haggle with plugs. A stolen car is free but runs hot.",
  "Selling back to the plug you just bought from pays at most 85% of what you paid.",
];

// ---------- helpers
const hex = (s) => Uint8Array.from(s.match(/../g).map((h) => parseInt(h, 16)));
async function verify(req, body, pub) {
  const sig = req.headers.get("x-signature-ed25519"), ts = req.headers.get("x-signature-timestamp");
  if (!sig || !ts) return false;
  const data = new TextEncoder().encode(ts + body);
  for (const alg of ["Ed25519", "NODE-ED25519"]) {
    try {
      const key = await crypto.subtle.importKey("raw", hex(pub), alg === "Ed25519" ? { name: "Ed25519" } : { name: alg, namedCurve: alg }, false, ["verify"]);
      return await crypto.subtle.verify(alg === "Ed25519" ? "Ed25519" : alg, key, hex(sig), data);
    } catch (e) { /* try the next name */ }
  }
  return false;
}
const json = (o) => new Response(JSON.stringify(o), { headers: { "content-type": "application/json" } });
const say = (content, extra = {}) => json({ type: 4, data: { content, flags: 64, ...extra } });
const embedReply = (embed, extra = {}) => json({ type: 4, data: { embeds: [embed], ...extra } });
const rest = (env, method, path, body) =>
  fetch(API + path, { method, headers: { Authorization: "Bot " + env.DISCORD_TOKEN, "Content-Type": "application/json", "User-Agent": "HustleWorker (the-hustle, 1.0)" }, body: body ? JSON.stringify(body) : undefined });

let cacheCh, cacheRoles;
async function channels(env) { if (!cacheCh) cacheCh = await (await rest(env, "GET", `/guilds/${env.GUILD_ID}/channels`)).json(); return cacheCh; }
async function roles(env, fresh) { if (!cacheRoles || fresh) cacheRoles = await (await rest(env, "GET", `/guilds/${env.GUILD_ID}/roles`)).json(); return cacheRoles; }
async function chan(env, key) { const l = await channels(env); return (Array.isArray(l) ? l : []).find((c) => c.name === CH[key]); }
async function role(env, name) { let l = await roles(env); let r = l.find((x) => x.name === name); if (!r) { l = await roles(env, true); r = l.find((x) => x.name === name); } return r; }
const isAdmin = (i) => (BigInt(i.member?.permissions || "0") & 8n) === 8n;
const opt = (i, n) => (i.data.options || []).find((o) => o.name === n)?.value;
const field = (i, id) => { for (const row of i.data.components || []) for (const c of row.components || []) if (c.custom_id === id) return (c.value || "").trim(); return ""; };
const input = (id, label, style, max, required, ph) => ({ type: 1, components: [{ type: 4, custom_id: id, label, style, max_length: max, required, placeholder: ph }] });
const who = (i) => i.member?.nick || i.member?.user?.global_name || i.member?.user?.username || "someone";

async function readBuild() {
  try { const t = await (await fetch(GAME_URL, { cf: { cacheTtl: 0 } })).text(); return (t.match(/const BUILD='(v\d+)'/) || [])[1] || null; } catch (e) { return null; }
}

// ---------- slash commands
async function command(i, env, ctx) {
  const n = i.data.name;
  if (n === "play") return embedReply({ title: "Play " + GAME, url: GAME_URL, description: GAME_URL, color: RED });
  if (n === "tip") return say("💡 " + TIPS[Math.floor(Math.random() * TIPS.length)], { flags: 0 });
  if (n === "build") { const b = await readBuild(); return say(b ? `Live build: **${b}**` : "Couldn't read the live build right now.", { flags: 0 }); }
  if (n === "character") {
    const id = opt(i, "who") === "casper" ? "country" : opt(i, "who");
    const c = CHARS.find((x) => x.id === id);
    if (!c) return say("Couldn't find that character.");
    return embedReply({ title: `${c.name}: ${c.role}`, description: c.story, color: RED, thumbnail: { url: `${RAW}portraits/${c.id}.jpg` }, fields: [{ name: "Perk", value: c.perk || "None" }] });
  }
  if (n === "bug") return json({ type: 9, data: { custom_id: "m:bug", title: "Report a bug", components: [
    input("build", "Build number (main menu)", 1, 12, false, "v165"), input("device", "Device and browser", 1, 60, true, "Phone Safari, Chromebook Chrome..."),
    input("what", "What happened?", 2, 900, true), input("expected", "What should have happened?", 2, 500, false)] } });
  if (n === "feedback") return json({ type: 9, data: { custom_id: "m:feedback", title: "Tell me what you think", components: [
    input("liked", "What did you like?", 2, 700, false), input("notliked", "What didn't you like or got confusing?", 2, 700, false), input("want", "What should I add next?", 2, 500, false)] } });
  if (n === "idea") return json({ type: 9, data: { custom_id: "m:idea", title: "Suggest an idea", components: [input("title", "Short title", 1, 80, true), input("body", "The idea", 2, 900, true)] } });
  if (n === "score") return json({ type: 9, data: { custom_id: "m:score", title: "Post your run", components: [
    input("char", "Character", 1, 20, true, "Slick, Tank, Shade, Val, Casper, Lucky"), input("days", "Days survived", 1, 6, true, "120"),
    input("cash", "Biggest bag (cash)", 1, 12, true, "250000"), input("note", "How did it end? (optional)", 1, 120, false)] } });
  if (n === "leaderboard") {
    if (!env.HUSTLE) return say("The leaderboard storage isn't set up yet.");
    const rows = JSON.parse((await env.HUSTLE.get("scores")) || "[]").slice(0, 10);
    if (!rows.length) return say("No runs posted yet. Use /score.", { flags: 0 });
    return embedReply({ title: "Leaderboard", color: GOLD, description: rows.map((r, k) => `**${k + 1}.** ${r.user} · ${r.char} · $${r.cash.toLocaleString("en-US")} · ${r.days.toLocaleString("en-US")} days`).join("\n") });
  }
  // admin commands
  if (["update", "award", "roles"].includes(n) && !isAdmin(i)) return say("Admins only.");
  if (n === "update") {
    const ch = await chan(env, "notes"); if (!ch) return say("No #hustle-patch-notes channel found. Run /setup on the bot first.");
    const r = await role(env, TESTER), ping = opt(i, "ping") !== false;
    await rest(env, "POST", `/channels/${ch.id}/messages`, { content: ping && r ? `<@&${r.id}>` : undefined, allowed_mentions: { roles: ping && r ? [r.id] : [] },
      embeds: [{ title: opt(i, "title"), description: `${opt(i, "text")}\n\n[Play the newest build](${GAME_URL})`, color: RED }] });
    return say(`Posted in <#${ch.id}>.`);
  }
  if (n === "award") {
    const uid = opt(i, "member"), r = await role(env, opt(i, "role"));
    if (!r) return say("That role doesn't exist yet. Run /setup on the bot first.");
    const res = await rest(env, "PUT", `/guilds/${env.GUILD_ID}/members/${uid}/roles/${r.id}`);
    return res.ok ? say(`<@${uid}> is now **${r.name}**.`, { flags: 0, allowed_mentions: { parse: [] } }) : say("Move my role above that role in Server Settings > Roles.");
  }
  if (n === "roles") {
    const cr = await (await rest(env, "GET", `/channels/${i.channel_id}`)).json();
    if (/tester/i.test(cr.name || "")) {
      await rest(env, "POST", `/channels/${i.channel_id}/messages`, { embeds: [{ title: "🧪 TESTER SIGN-UP: pick your area", color: RED,
        description: "The Hustle is getting a full test run before release. Pick the part of the game you'll own. Tap a button to join, tap again to leave. I want 2 testers on each area.\n\n" + AREAS.map(([nm, e, , d]) => `${e} **${nm}**: ${d}`).join("\n") + "\n\nPlay your area hard. Try to break it. Post bugs in your role's channel with a screenshot and what you did right before. Check the version first (hard refresh if it's old)." }], components: [areaMenu()] });
      return say("Posted the tester sign-up.");
    }
    await rest(env, "POST", `/channels/${i.channel_id}/messages`, { embeds: [{ title: "Pick your roles", description: "Use the menu below. You can change it any time.", color: GREEN }], components: [roleMenu()] });
    return say("Posted.");
  }
  return say("I don't know that command yet. Try /play or /tip.");
}
const roleMenu = () => ({ type: 1, components: [{ type: 3, custom_id: "hustle:roles", placeholder: "Pick your roles (this replaces your picks)", min_values: 0, max_values: PICK_ROLES.length, options: PICK_ROLES.map(([l, d]) => ({ label: l, description: d, value: l })) }] });

// ---------- buttons and menus
async function component(i, env) {
  const uid = i.member.user.id, mine = new Set(i.member.roles || []);
  if (i.data.custom_id === "hustle:tester") {
    const r = await role(env, TESTER); if (!r) return say("The role doesn't exist yet. An admin needs to run /setup.");
    const has = mine.has(r.id);
    const res = await rest(env, has ? "DELETE" : "PUT", `/guilds/${env.GUILD_ID}/members/${uid}/roles/${r.id}`);
    if (!res.ok) return say("I can't hand out that role yet. An admin needs to drag my role above 'Hustle Tester' in Server Settings > Roles.");
    return say(has ? "Tester role removed. You won't get update pings." : "You're a Hustle Tester now. You'll get update pings.");
  }
  if (i.data.custom_id.startsWith("hustle:area:")) {
    const nm = i.data.custom_id.slice(12), a = AREAS.find((x) => x[0] === nm); if (!a) return say("That area isn't set up.");
    let r = await role(env, nm);
    if (!r) { const cr = await rest(env, "POST", `/guilds/${env.GUILD_ID}/roles`, { name: nm, color: a[2], mentionable: true }); if (cr.ok) { r = await cr.json(); cacheRoles = null; } }
    if (!r) return say("I couldn't make that role. An admin needs to drag my role to the top in Server Settings > Roles.");
    const has = mine.has(r.id);
    const res = await rest(env, has ? "DELETE" : "PUT", `/guilds/${env.GUILD_ID}/members/${uid}/roles/${r.id}`);
    if (!res.ok) return say("I can't hand out that role yet. An admin needs to drag my role to the top in Server Settings > Roles.");
    return say(has ? `You left ${nm}.` : `You're a ${nm.replace(/s$/, "")} now. Test your area hard and post bugs in your channel.`);
  }
  if (i.data.custom_id === "hustle:roles") {
    const all = await roles(env, true), want = new Set(i.data.values || []), pickable = new Set(PICK_ROLES.map((x) => x[0]));
    let failed = false;
    for (const r of all) {
      if (!pickable.has(r.name)) continue;
      const has = mine.has(r.id), should = want.has(r.name);
      if (has === should) continue;
      const res = await rest(env, should ? "PUT" : "DELETE", `/guilds/${env.GUILD_ID}/members/${uid}/roles/${r.id}`);
      if (!res.ok) failed = true;
    }
    return say(failed ? "I can't hand out some of those roles yet. An admin needs to drag my role to the top in Server Settings > Roles." : "Roles updated: " + ([...want].join(", ") || "none"));
  }
  return say("That button isn't set up.");
}

// ---------- forms
async function modal(i, env) {
  const id = i.data.custom_id, name = who(i);
  const post = async (key, payload) => {
    const ch = await chan(env, key); if (!ch) return null;
    const res = await rest(env, "POST", `/channels/${ch.id}/messages`, payload); return res.ok ? { ch, msg: await res.json() } : null;
  };
  if (id === "m:bug") {
    const r = await post("bugs", { embeds: [{ title: "Bug report", description: field(i, "what"), color: RED, footer: { text: "From " + name },
      fields: [{ name: "Build", value: field(i, "build") || "?", inline: true }, { name: "Device", value: field(i, "device"), inline: true },
        ...(field(i, "expected") ? [{ name: "Expected", value: field(i, "expected") }] : [])] }] });
    if (!r) return say("I can't find #hustle-bugs. Ask an admin to run /setup.");
    await rest(env, "PUT", `/channels/${r.ch.id}/messages/${r.msg.id}/reactions/${encodeURIComponent("🐛")}/@me`);
    return say(`Sent to <#${r.ch.id}>. Thank you.`);
  }
  if (id === "m:feedback") {
    const f = [["Liked", "liked"], ["Didn't like", "notliked"], ["Wants next", "want"]].filter(([, k]) => field(i, k)).map(([n2, k]) => ({ name: n2, value: field(i, k) }));
    if (!f.length) return say("You left everything blank.");
    const r = await post("feedback", { embeds: [{ title: "Feedback", color: GREEN, fields: f, footer: { text: "From " + name } }] });
    return r ? say(`Sent to <#${r.ch.id}>. Thank you.`) : say("I can't find #hustle-feedback. Ask an admin to run /setup.");
  }
  if (id === "m:idea") {
    const r = await post("ideas", { embeds: [{ title: field(i, "title"), description: field(i, "body"), color: GOLD, footer: { text: "From " + name } }] });
    if (!r) return say("I can't find #hustle-ideas. Ask an admin to run /setup.");
    for (const e of ["👍", "👎"]) await rest(env, "PUT", `/channels/${r.ch.id}/messages/${r.msg.id}/reactions/${encodeURIComponent(e)}/@me`);
    return say(`Posted in <#${r.ch.id}>. Vote with the thumbs.`);
  }
  if (id === "m:score") {
    const days = parseInt(field(i, "days").replace(/\D/g, "") || "0", 10), cash = parseInt(field(i, "cash").replace(/\D/g, "") || "0", 10);
    const rec = { user: name, uid: i.member.user.id, char: field(i, "char").slice(0, 20), days, cash, note: field(i, "note"), t: Date.now() };
    if (env.HUSTLE) { const all = JSON.parse((await env.HUSTLE.get("scores")) || "[]"); all.push(rec); all.sort((a, b) => b.cash - a.cash); await env.HUSTLE.put("scores", JSON.stringify(all.slice(0, 200))); }
    await post("scores", { embeds: [{ title: `${name} posted a run`, color: GOLD, fields: [
      { name: "Character", value: rec.char, inline: true }, { name: "Days", value: days.toLocaleString("en-US"), inline: true }, { name: "Bag", value: "$" + cash.toLocaleString("en-US"), inline: true },
      ...(rec.note ? [{ name: "How it ended", value: rec.note }] : [])] }] });
    return say(env.HUSTLE ? "Saved. Check /leaderboard." : "Posted. (Leaderboard storage isn't set up yet.)");
  }
  return say("That form isn't set up.");
}

export default {
  async fetch(req, env, ctx) {
    if (req.method !== "POST") return new Response("The Hustle bot is up.");
    const body = await req.text();
    if (!(await verify(req, body, env.DISCORD_PUBLIC_KEY || ""))) return new Response("bad signature", { status: 401 });
    const i = JSON.parse(body);
    try {
      if (i.type === 1) return json({ type: 1 });
      if (i.type === 2) return await command(i, env, ctx);
      if (i.type === 3) return await component(i, env);
      if (i.type === 5) return await modal(i, env);
    } catch (e) { return say("Something broke on my end. Try again in a minute."); }
    return say("Unsupported.");
  },
};
