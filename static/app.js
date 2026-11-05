"use strict";
/* Anglų katinas – terminal front end */

const $ = (id) => document.getElementById(id);
const out = $("out"), inp = $("inp"), term = $("term");

const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* ignore */ } },
};

const state = {
  slug: null, name: null, catName: "Murkis", busy: false,
  mood: "normal", full: 70, typing: store.get("typing", true), voice: store.get("voice", false),
};

/* ------------------------------------------------------------- the cat */
const FACES = {
  normal: ["o   o", " ^ "], blink: ["-   -", " ^ "], happy: ["^   ^", " w "],
  sad: ["o   o", " ~ "], think: ["o   O", " . "], eat1: ["^   ^", " O "],
  eat2: ["^   ^", " o "], hungry: ["u   u", " o "], wink: ["^   -", " w "],
};

let wag = false;
function catArt(face) {
  const [eyes, mouth] = FACES[face] || FACES.normal;
  const t = wag ? ["      )", "     ("] : ["     (", "      )"];
  return [
    "    /\\_____/\\",
    `   /  ${eyes}  \\`,
    `  ( == ${mouth} == )`,
    "   )         (" + t[0],
    "  (           )" + t[1],
    " ( (  )   (  ) )   /",
    "(__(__)___(__)__)_/",
  ].join("\n");
}

let faceTimer = null;
function face(f, ms) {
  $("cat").textContent = catArt(f);
  clearTimeout(faceTimer);
  if (ms) faceTimer = setTimeout(() => face(restFace()), ms);
}
function restFace() { return state.full < 30 ? "hungry" : "normal"; }

function wrap(text, width) {
  const words = String(text).split(/\s+/), lines = [];
  let cur = "";
  for (const w of words) {
    if ((cur + " " + w).trim().length > width) { if (cur) lines.push(cur); cur = w; }
    else cur = (cur + " " + w).trim();
  }
  if (cur) lines.push(cur);
  return lines.length ? lines : [""];
}

let bubbleTimer = null;
function say(text, ms = 6000) {
  if (!text) return;
  const lines = wrap(text, 22);
  const w = Math.max(...lines.map((l) => l.length));
  const tail = Math.max(1, Math.floor((w + 2) / 2) - 1);
  $("bubble").textContent = [
    " " + "_".repeat(w + 2),
    ...lines.map((l) => "| " + l.padEnd(w) + " |"),
    " " + "-".repeat(tail) + "\\_/" + "-".repeat(Math.max(0, w + 2 - tail - 3)),
  ].join("\n");
  clearTimeout(bubbleTimer);
  if (ms) bubbleTimer = setTimeout(() => { $("bubble").textContent = ""; }, ms);
}

function anim(cls) {
  const el = $("catwrap");
  el.classList.remove("flip", "bounce", "shake");
  void el.offsetWidth;
  el.classList.add(cls);
  return new Promise((r) => setTimeout(() => { el.classList.remove(cls); r(); }, cls === "flip" ? 1150 : 550));
}

function setMood(m) {
  state.mood = m;
  if (m === "happy") { face("happy", 1800); anim("bounce"); }
  else if (m === "sad") { face("sad", 2200); anim("shake"); }
  else if (m === "think") face("think", 2000);
  else if (m === "eat") eat();
  else face(restFace());
}

// wag the tail
setInterval(() => {
  const cur = $("cat").textContent;
  for (const f of Object.keys(FACES)) {
    if (cur === catArt(f)) { wag = !wag; $("cat").textContent = catArt(f); return; }
  }
}, 900);

// blink now and then
setInterval(() => {
  const cur = $("cat").textContent;
  if (cur === catArt("normal") || cur === catArt("hungry")) {
    face("blink");
    setTimeout(() => face(restFace()), 160);
  }
}, 3800);

const FLIP_LINES = ["Wheee!", "Look at me!", "Ta-da!", "Again? Meow!", "I can fly!"];
let flipping = false;
async function flip() {
  if (flipping) return;
  flipping = true;
  face("happy");
  say(FLIP_LINES[Math.floor(Math.random() * FLIP_LINES.length)], 2500);
  await anim("flip");
  face("wink", 900);
  flipping = false;
}

function hearts(n = 4) {
  for (let i = 0; i < n; i++) {
    const h = document.createElement("span");
    h.className = "heart";
    h.textContent = i % 2 ? "♥" : "<3";
    h.style.left = 35 + Math.random() * 30 + "%";
    h.style.animationDelay = i * 0.18 + "s";
    $("hearts").appendChild(h);
    setTimeout(() => h.remove(), 2200);
  }
}

let eating = false;
async function eat(serverLine) {
  if (eating) return;
  eating = true;
  const fish = $("fish");
  fish.classList.remove("go"); void fish.offsetWidth; fish.classList.add("go");
  face("eat1");
  await new Promise((r) => setTimeout(r, 900));
  for (let i = 0; i < 6; i++) {
    face(i % 2 ? "eat2" : "eat1");
    await new Promise((r) => setTimeout(r, 180));
  }
  face("happy", 1500);
  hearts();
  if (serverLine) say(serverLine, 3500);
  eating = false;
}

async function feed() {
  if (!state.slug) { eat("Yum! Thank you!"); return; }
  const r = await api("/api/feed", { slug: state.slug });
  if (!r) return;
  updateStats(r.stats);
  if (r.mood === "eat") eat(r.bubble);
  else { say(r.bubble, 3000); face("happy", 1500); }
}

$("flipBtn").onclick = flip;
$("feedBtn").onclick = feed;
$("cat").onclick = flip;

/* ------------------------------------------------------------- stats */
function updateStats(s) {
  if (!s) return;
  state.full = s.full;
  state.catName = s.cat || state.catName;
  const n = Math.round(s.full / 10);
  const bar = "#".repeat(n) + "-".repeat(10 - n);
  const low = s.full < 30 ? " low" : "";
  $("stats").innerHTML =
    `<span class="s-key">katinas :</span> ${esc(state.catName)}\n` +
    `<span class="s-key">sotumas :</span> <span class="s-bar${low}">[${bar}]</span>\n` +
    `<span class="s-key">žvaigždės:</span> <span class="s-star">★ ${s.stars}</span>\n` +
    `<span class="s-key">lygis   :</span> ${esc(s.level)}\n` +
    (s.topic ? `<span class="s-key">tema    :</span> ${esc(s.topic)}` : "");
  if (s.full < 30 && Math.random() < 0.3) say("I am hungry... Feed me, please!", 4000);
}

/* ------------------------------------------------------------- terminal */
const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const scroll = () => { term.scrollTop = term.scrollHeight; };

const SPEAK_KINDS = new Set(["cat", "q", "ex", "fix", "ok"]);

function speakable(m) {
  let t = m.t;
  if (m.k === "fix") t = t.replace(/^Teisingai:\s*/, "");
  if (m.k === "ok") t = t.replace(/\+1.*$/, "");
  if (m.k === "q") {
    t = t.replace(/\([^)]*\)/g, "").replace(/_{2,}/g, " blank ");
    if (t.includes(" / ")) return null;          // word-order exercise: don't give it away
  }
  return t.trim();
}

function speak(text) {
  if (!text || !("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-GB";
  u.rate = 0.85;
  const v = speechSynthesis.getVoices().find((x) => /^en(-|_)GB/i.test(x.lang)) ||
            speechSynthesis.getVoices().find((x) => /^en/i.test(x.lang));
  if (v) u.voice = v;
  speechSynthesis.speak(u);
}

async function printMsg(m) {
  const div = document.createElement("div");
  div.className = "line k-" + m.k;
  out.appendChild(div);
  let prefix = "", text = m.t || "";
  if (m.k === "cat") prefix = `<span class="who">${esc(state.catName)}&gt;</span> `;
  if (m.k === "q") prefix = "» ";
  if (m.k === "ex") prefix = "• ";
  if (m.k === "head") { text = `== ${text} ==`; }
  div.innerHTML = prefix;
  const span = document.createElement("span");
  div.appendChild(span);

  if (state.typing && text.length) {
    const step = text.length > 160 ? 4 : 2;
    for (let i = 0; i < text.length; i += step) {
      span.textContent = text.slice(0, i + step);
      scroll();
      await sleep(14);
    }
  }
  span.textContent = text;

  const st = SPEAK_KINDS.has(m.k) ? speakable(m) : null;
  if (st) {
    const b = document.createElement("button");
    b.className = "say";
    b.type = "button";
    b.title = "Klausyti";
    b.textContent = "[▶]";
    b.onclick = () => speak(st);
    div.appendChild(b);
    if (state.voice && (m.k === "cat" || m.k === "q")) speak(st);
  }
  scroll();
}

async function printAll(msgs) {
  for (const m of msgs || []) await printMsg(m);
}

function echo(text) {
  const div = document.createElement("div");
  div.className = "line k-user";
  div.innerHTML = `<span class="ps">${esc(ps1())}</span> ${esc(text)}`;
  out.appendChild(div);
  scroll();
}

function ps1() {
  const who = state.name ? state.name.toLowerCase().replace(/\s+/g, "-") : "svečias";
  return `${who}@anglu ~>`;
}

let spin = null;
function thinking(on) {
  if (on) {
    const div = document.createElement("div");
    div.className = "line spinner";
    div.id = "spin";
    out.appendChild(div);
    const frames = ["|", "/", "-", "\\"];
    let i = 0;
    spin = setInterval(() => { div.textContent = `${state.catName} galvoja ${frames[i++ % 4]}`; scroll(); }, 120);
    face("think");
  } else {
    clearInterval(spin);
    const s = $("spin");
    if (s) s.remove();
  }
}

async function api(path, body) {
  try {
    const r = await fetch(path, {
      method: body ? "POST" : "GET",
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    });
    return await r.json();
  } catch (e) {
    await printMsg({ k: "err", t: "Nepavyko susisiekti su programa. Ar serveris įjungtas? (python3 server.py)" });
    return null;
  }
}

function lock(on) {
  state.busy = on;
  inp.disabled = on;
  if (!on) inp.focus();
}

async function handle(r) {
  if (!r) return;
  if (r.error) {
    if (r.error === "name") await printMsg({ k: "lt", t: "Parašyk savo vardą raidėmis, pavyzdžiui: Evelina." });
    else if (r.error === "session") { await printMsg({ k: "lt", t: "Pradėkime iš naujo." }); return begin(state.name); }
    return;
  }
  if (r.slug) state.slug = r.slug;
  updateStats(r.stats);
  if (r.mood) setMood(r.mood);
  if (r.bubble) say(r.bubble);
  await printAll(r.messages);
}

async function begin(name) {
  lock(true);
  thinking(true);
  const r = await api("/api/start", { name });
  thinking(false);
  if (r && !r.error) {
    state.name = r.stats.name;
    $("ps1").textContent = ps1();
    $("tbTitle").textContent = `~ : ${state.name.toLowerCase()} — anglų katinas`;
  }
  await handle(r);
  lock(false);
}

$("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  if (state.busy) return;
  const text = inp.value.trim();
  inp.value = "";
  if (!text) return;
  echo(text);
  const low = text.toLowerCase();
  if (low === "salto" || low === "/flip") return flip();
  if (low === "pamaitinti" || low === "/feed") return feed();
  if (low === "clear" || low === "valyti") { out.innerHTML = ""; return; }

  if (!state.slug) return begin(text);

  lock(true);
  thinking(true);
  const r = await api("/api/answer", { slug: state.slug, text });
  thinking(false);
  await handle(r);
  lock(false);
});

term.addEventListener("click", () => { if (!window.getSelection().toString()) inp.focus(); });

/* ------------------------------------------------------------- settings */
function applyFont(px) {
  px = Math.max(14, Math.min(30, px));
  document.documentElement.style.setProperty("--fs", px + "px");
  store.set("fs", px);
}
applyFont(store.get("fs", 19));
$("fontUp").onclick = () => applyFont(store.get("fs", 19) + 2);
$("fontDown").onclick = () => applyFont(store.get("fs", 19) - 2);

function labels() {
  $("animBtn").textContent = "rašymas: " + (state.typing ? "įj." : "išj.");
  $("voiceBtn").textContent = "balsas: " + (state.voice ? "įj." : "išj.");
}
$("animBtn").onclick = () => { state.typing = !state.typing; store.set("typing", state.typing); labels(); };
$("voiceBtn").onclick = () => { state.voice = !state.voice; store.set("voice", state.voice); labels(); };
labels();
if ("speechSynthesis" in window) speechSynthesis.getVoices();

/* ------------------------------------------------------------- boot */
(async function boot() {
  face("normal");
  lock(true);
  const st = await api("/api/status");
  const lines = [
    "Anglų katinas 1.0  —  tty1",
    "[ OK ] Katinėlis pabudo",
    "[ OK ] Pratimai įkelti (A1–" + (st ? st.max_level : "B1") + ")",
  ];
  let warn = null;
  if (st && st.api && !st.installed) warn = "[WARN] API raktas neveikia – veiks tik pratimai (patikrink .env)";
  else if (!st || !st.ollama) warn = "[WARN] Nėra modelio – veiks tik pratimai (be paaiškinimų)";
  else if (!st.installed) warn = `[WARN] Modelis ${st.model} neįdiegtas – veiks tik pratimai`;
  else lines.push(`[ OK ] Modelis ${st.model} paruoštas${st.api ? " (API)" : ""}`);
  for (const l of lines) {
    const div = document.createElement("div");
    div.className = "line k-boot";
    div.innerHTML = l.replace("[ OK ]", '<span class="okk">[ OK ]</span>');
    out.appendChild(div);
    await sleep(state.typing ? 220 : 0);
  }
  if (warn) {
    const div = document.createElement("div");
    div.className = "line k-boot";
    div.innerHTML = `<span class="warn">${esc(warn)}</span>`;
    out.appendChild(div);
  }
  await printMsg({ k: "sys", t: "" });
  say("Hello! What is your name?", 0);
  face("happy", 1500);
  await printMsg({ k: "cat", t: "Hello! What is your name?" });
  await printMsg({ k: "lt", t: "Labas! Kuo tu vardu? Parašyk savo vardą ir paspausk Enter." });
  updateStats({ full: 70, stars: 0, level: "?", cat: state.catName });
  lock(false);
})();
