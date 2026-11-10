#!/usr/bin/env python3
"""
Anglų katinas – a terminal-style English drilling app for special-needs learners.

Start it with:  python server.py   (Windows: py server.py)
The language model comes from an online API (key in LLM_API_KEY) or from a local Ollama.
Student progress is kept in ./data/<name>.json on this computer.
"""
import datetime
import json
import os
import random
import re
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import checker
import curriculum as CUR
import safety

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
STATIC = BASE / "static"

DEFAULTS = {
    "cat_name": "William",
    "ollama_url": "http://localhost:11434",
    "model": "qwen3:8b",
    "think": False,
    "temperature": 0.4,
    "timeout": 120,
    "port": 8000,
    "open_browser": True,
    "max_level": "B1",
    "drill_items": 6,        # new exercises per lesson
    "review_items": 2,       # old mistakes repeated per lesson
    "chat_turns": 3,         # short conversation at the end (0 = off)
    "full_sentences": "encourage",   # "encourage" = bonus stars, "require" = must write the sentence
    "show_student_names": True,      # list known students on the start screen
}


# ------------------------------------------------------------------ settings
def load_dotenv():
    """Read KEY=VALUE lines from .env. Real environment variables (e.g. Codespaces secrets) win."""
    f = BASE / ".env"
    if not f.exists():
        return
    for line in f.read_text("utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.split(" #")[0].strip().strip('"').strip("'"))


def load_config():
    load_dotenv()
    cfg = dict(DEFAULTS)
    f = BASE / "config.json"
    if f.exists():
        cfg.update(json.loads(f.read_text("utf-8")))
    key = os.environ.get("LLM_API_KEY", "").strip()
    groq = key.startswith("gsk_")                         # Groq keys start with gsk_
    cfg["api_key"] = key
    cfg["api_url"] = os.environ.get("LLM_BASE_URL", "").strip() or (
        "https://api.groq.com/openai/v1" if groq else "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
    if key:
        cfg["model"] = os.environ.get("LLM_MODEL", "").strip() or ("qwen/qwen3.8-27b" if groq else "qwen-flash")
    cfg["teacher_pin"] = os.environ.get("TEACHER_PIN", "").strip()
    if os.environ.get("PORT"):
        cfg["port"] = int(os.environ["PORT"])
    if os.environ.get("CODESPACES"):                      # no local browser in Codespaces
        cfg["open_browser"] = False
    return cfg


CFG = load_config()
CAT = CFG["cat_name"]
LOCK = threading.Lock()
SESSIONS = {}
MASTERED = 0.8

PRAISE = ["Great job!", "Super!", "Well done!", "Purr-fect!", "Yes! Correct!", "Excellent!",
          "You are a star!", "Brilliant!", "Good thinking!"]
ENCOURAGE = ["You can do it!", "Let's try again!", "Mistakes help us learn!", "Good try!"]
YUM = ["Yum yum! Thank you!", "Mmm, fish! I love fish!", "Nom nom nom!", "Thank you! Purrr..."]


def now_iso():
    return datetime.datetime.now().isoformat(timespec="seconds")


def log(*a):
    print("[katinas]", *a, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ student files
def slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", safety.simplify(name)).strip("-")
    return s[:40] or "mokinys"


def load_profile(sl):
    f = DATA / f"{sl}.json"
    if not f.exists():
        return None
    p = json.loads(f.read_text("utf-8"))
    p.setdefault("plan", {"topics": [], "note": ""})
    return p


def save_profile(p):
    DATA.mkdir(exist_ok=True)
    f = DATA / f"{p['slug']}.json"
    tmp = f.with_suffix(".tmp")
    tmp.write_text(json.dumps(p, ensure_ascii=False, indent=1), "utf-8")
    tmp.replace(f)


def all_students():
    DATA.mkdir(exist_ok=True)
    out = []
    for f in sorted(DATA.glob("*.json")):
        p = json.loads(f.read_text("utf-8"))
        out.append({"slug": p["slug"], "name": p["name"], "level": p.get("level"),
                    "sessions": len(p["sessions"]), "alerts": len(p["alerts"])})
    return out


def new_profile(name):
    return {
        "name": name, "slug": slug(name), "created": now_iso(), "interests": "",
        "diagnostic_done": False, "level": None, "diagnostic": None,
        "topics": {}, "mistakes": [], "log": [], "sessions": [], "alerts": [],
        "plan": {"topics": [], "note": ""},
        "stars": 0, "cat": {"full": 70, "t": time.time(), "fed": 0},
    }


def topic_state(p, tid):
    return p["topics"].setdefault(tid, {"score": 0.0, "tries": 0, "correct": 0, "last": None})


def record(p, tid, value):
    st = topic_state(p, tid)
    st["score"] = round(st["score"] * 0.8 + 0.2 * value, 3)
    st["tries"] += 1
    st["correct"] += 1 if value >= 1 else 0
    st["last"] = now_iso()


def fullness(p):
    c = p["cat"]
    hours = (time.time() - c.get("t", time.time())) / 3600
    return max(0, min(100, int(c.get("full", 70) - hours * 4)))


def item_key(it):
    return it["topic"] + "|" + it["q"]


def add_mistake(p, it):
    key = item_key(it)
    for m in p["mistakes"]:
        if m["key"] == key:
            m["n"] += 1
            return
    clean = {k: v for k, v in it.items() if k in ("type", "q", "a", "opts", "topic")}
    p["mistakes"].append({"key": key, "item": clean, "n": 1})
    p["mistakes"] = p["mistakes"][-60:]


def remove_mistake(p, it):
    p["mistakes"] = [m for m in p["mistakes"] if m["key"] != item_key(it)]


def stats(p, s=None):
    return {"name": p["name"], "cat": CAT, "stars": p["stars"], "level": p.get("level") or "?",
            "full": fullness(p), "topic": (s or {}).get("title", "")}


# ------------------------------------------------------------------ language model
def llm(messages, json_mode=False, max_tokens=300):
    try:
        text = _llm_api(messages, json_mode, max_tokens) if CFG["api_key"] \
            else _llm_ollama(messages, json_mode, max_tokens)
    except Exception as e:  # noqa: BLE001
        log("model error:", e)
        return None
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S).strip()
    return text or None


def _llm_api(messages, json_mode, max_tokens):
    body = {"model": CFG["model"], "messages": messages, "temperature": CFG["temperature"],
            "max_tokens": max_tokens}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    if "dashscope" in CFG["api_url"]:
        body["enable_thinking"] = False            # Qwen: answer directly, no slow "thinking"
    if "groq.com" in CFG["api_url"] and "qwen" in CFG["model"].lower():
        body["reasoning_effort"] = "none"          # same on Groq

    def send(b):
        req = urllib.request.Request(CFG["api_url"].rstrip("/") + "/chat/completions",
                                     data=json.dumps(b).encode(),
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + CFG["api_key"],
                                              "User-Agent": "anglu-katinas/1.0"})
        with urllib.request.urlopen(req, timeout=CFG["timeout"]) as r:
            return json.loads(r.read())

    try:
        data = send(body)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", "replace")
        if e.code != 400 or not ("reasoning" in err or "thinking" in err):
            raise RuntimeError(f"API {e.code}: {err[:300]}") from None
        body.pop("reasoning_effort", None)         # model without that switch: try again without it
        body.pop("enable_thinking", None)
        data = send(body)
    return data["choices"][0]["message"].get("content") or ""


def _llm_ollama(messages, json_mode, max_tokens):
    body = {"model": CFG["model"], "messages": messages, "stream": False,
            "options": {"temperature": CFG["temperature"], "num_predict": max_tokens}}
    if json_mode:
        body["format"] = "json"
    if CFG.get("think") is not None:
        body["think"] = CFG["think"]

    def send(b):
        req = urllib.request.Request(CFG["ollama_url"].rstrip("/") + "/api/chat", data=json.dumps(b).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=CFG["timeout"]) as r:
            return json.loads(r.read())

    try:
        data = send(body)
    except urllib.error.HTTPError:
        body.pop("think", None)
        data = send(body)
    return (data.get("message") or {}).get("content") or ""


_API_OK = None


def model_status():
    global _API_OK
    if CFG["api_key"]:
        if _API_OK is None:                        # test the key once
            _API_OK = llm([{"role": "user", "content": "Say OK."}], max_tokens=5) is not None
        return {"ollama": True, "installed": _API_OK, "model": CFG["model"], "api": True}
    try:
        req = urllib.request.Request(CFG["ollama_url"].rstrip("/") + "/api/tags")
        with urllib.request.urlopen(req, timeout=5) as r:
            names = [m.get("name", "") for m in json.loads(r.read()).get("models", [])]
    except Exception:  # noqa: BLE001
        return {"ollama": False, "installed": False, "model": CFG["model"]}
    want = CFG["model"] if ":" in CFG["model"] else CFG["model"] + ":latest"
    return {"ollama": True, "installed": want in names, "model": CFG["model"]}


def clean_out(text, fallback):
    """Last check on anything the model wrote before the student sees it."""
    if not text:
        return fallback
    text = re.sub(r"[*#_`]+", "", text).strip()
    if not safety.output_ok(text):
        log("blocked model output:", text[:200])
        return fallback
    return text


def system_prompt(p):
    known = [CUR.TOPIC_BY_ID[t]["focus"] for t, st in p["topics"].items()
             if st["score"] >= MASTERED and t in CUR.TOPIC_BY_ID][:12]
    weak = [CUR.TOPIC_BY_ID[t]["focus"] for t, st in p["topics"].items()
            if st["tries"] and st["score"] < 0.5 and t in CUR.TOPIC_BY_ID][:8]
    recent = "; ".join(f'"{m["ans"]}" instead of "{m["correct"]}"' for m in p["log"][-4:])
    note = (p.get("plan") or {}).get("note", "").strip()
    teacher = f"\nTEACHER'S INSTRUCTION (follow it): {note}\n" if note else ""
    return f"""You are {CAT}, a kind cartoon cat who helps a Lithuanian school student practise English.
You are a practice helper. You do not replace the student's real teacher.

STUDENT
- Name: {p['name']}. English level: about {p.get('level') or 'A1'} (beginner).
- The student has special educational needs. Everything must be short, clear and calm.
- Likes: {p.get('interests') or 'animals, colours, games'}.
- Knows well: {', '.join(known) or 'not much yet'}.
- Needs more practice: {', '.join(weak) or 'unknown'}.
- Recent mistakes: {recent or 'none'}.
{teacher}
STYLE
- English must be very simple (A1-A2): short sentences, common words. Max 3 sentences.
- Always encourage the student to answer in FULL SENTENCES ("My cat is brown.", not just "brown").
- When you write Lithuanian, write simple and correct Lithuanian.
- Be warm and encouraging. Never call the student bad, slow or stupid.
- Plain text only. No markdown, no emojis, no lists.

SAFETY RULES - NEVER BREAK THESE
- Never talk about sex, romance, dating, kissing, private or reproductive body parts, puberty or pregnancy.
- Never talk about politics, politicians, elections, war, religion, drugs, alcohol, smoking, weapons,
  violence, crime, horror or other scary or adult topics.
- Never ask for addresses, phone numbers, school names, passwords, photos or social media.
  Never ask the student to keep a secret. Never suggest meeting anyone.
- If the student brings up one of these topics, do not discuss it. Say only:
  "Apie tai mes čia nekalbame. Grįžkime prie anglų kalbos!" and go back to the lesson.
- If the student seems sad, scared or hurt, tell them kindly in Lithuanian to talk to their teacher
  or a trusted adult.
- Stay on English learning. Topics you may use: animals, pets, horses, colours, food, family,
  school, art, hobbies, games, weather, days, the house."""


def parse_json(text):
    if not text:
        return None
    try:
        return json.loads(text)
    except ValueError:
        m = re.search(r"\{.*\}", text, flags=re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except ValueError:
                return None
    return None


# ------------------------------------------------------------------ messages
def M(kind, text):
    return {"k": kind, "t": text}


def render_item(it, n, total):
    head = "[dar kartą]" if it.get("key_seen") else \
        f"[{n}/{total}]" + (" (kartojimas)" if it.get("review") else "")
    if it["type"] == "fill":
        return [M("lt", f"{head} Įrašyk trūkstamą žodį – arba parašyk visą sakinį (+2 ★):"), M("q", it["q"])]
    if it["type"] == "choose":
        opts = "    ".join(f"{checker.LETTERS[i]}) {o}" for i, o in enumerate(it["opts"]))
        return [M("lt", f"{head} Pasirink: parašyk raidę – arba visą sakinį (+2 ★):"), M("q", it["q"]),
                M("opt", opts)]
    if it["type"] == "translate":
        f = checker.frame(it)
        if f:
            return [M("lt", f"{head} Kaip angliškai „{it['q']}“? Parašyk visą sakinį (+2 ★):"), M("q", f)]
        return [M("lt", f"{head} Kaip angliškai „{it['q']}“?")]
    return [M("lt", f"{head} Sudėliok sakinį iš šių žodžių:"), M("q", it["display"])]


def reply(p, s, msgs, mood="normal", bubble=None, done=False):
    return {"messages": msgs, "mood": mood, "bubble": bubble, "done": done,
            "stats": stats(p, s), "slug": p["slug"]}


HELP = [
    M("lt", "Kaip atsakyti:"),
    M("lt", "  • Geriausia – parašyk visą sakinį, pvz.: My cat is brown. Gausi 2 ★!"),
    M("lt", "  • Jei yra variantai a), b), c) – gali parašyti raidę."),
    M("lt", "  • Jei nežinai – parašyk „nežinau“. Tai visai nieko tokio!"),
    M("lt", "  • „kartoti“ – parodysiu klausimą dar kartą."),
    M("lt", "  • „pabaiga“ – baigsime pamoką. „keisti“ – kitas mokinys."),
    M("lt", "  • Paspausk ant [▶] ir išgirsi, kaip skamba angliškai."),
]


# ------------------------------------------------------------------ session start
def start(name):
    name = re.sub(r"\s+", " ", name or "").strip()[:30]
    if not name or not re.search(r"\w", name) or safety.check_input(name):
        return {"error": "name"}
    sl = slug(name)
    p = load_profile(sl) or new_profile(name)
    save_profile(p)
    s = {"slug": sl, "llm_ok": model_status()["installed"], "started": now_iso()}
    SESSIONS[sl] = s
    if not p["diagnostic_done"]:
        return start_diagnostic(p, s)
    return start_lesson(p, s)


# ------------------------------------------------------------------ diagnostic (1st session)
def start_diagnostic(p, s):
    s["phase"] = "interests"
    out = [M("lt", f"Labas, {p['name']}! Aš esu katinas {CAT} ir padėsiu tau mokytis anglų kalbos."),
           M("lt", "Ką tu labiausiai mėgsti? Parašyk kelis žodžius (pvz.: arkliai, piešimas, Roblox).")]
    return reply(p, s, out, "happy", f"Hello, {p['name']}! I am {CAT}.")


def begin_test(p, s):
    s.update(phase="diag", bi=0, ii=0, wrong=0, results=[])
    out = [
        M("lt", "Dabar atliksime trumpą testą. Tai ne kontrolinis – pažymių nebus!"),
        M("lt", "Aš tik noriu sužinoti, ką tu jau moki, kad žinočiau, ko mokytis toliau."),
        *HELP[:4],
        M("sys", ""),
    ]
    return out + diag_item(s)


def diag_item(s):
    block = CUR.DIAGNOSTIC[s["bi"]]
    it = checker.prepare(block["items"][s["ii"]])
    s["item"] = it
    total = sum(len(b["items"]) for b in CUR.DIAGNOSTIC)
    n = sum(len(b["items"]) for b in CUR.DIAGNOSTIC[: s["bi"]]) + s["ii"] + 1
    return render_item(it, n, total)


def answer_diag(p, s, text):
    it = s["item"]
    v, _ = checker.check(it, text)
    good = v in ("ok", "near")
    s["results"].append({"topic": it["topic"], "q": it["q"], "ans": text, "ok": good})
    if not good:
        s["wrong"] += 1
        add_mistake(p, it)
    else:
        p["stars"] += 1
    out = [M("ok", random.choice(["Teisingai!", "Puiku!", "Taip!"]))] if good else \
          [M("sys", random.choice(["Ačiū! Einame toliau.", "Gerai, kitas klausimas.", "Nieko tokio, toliau!"]))]
    save_profile(p)
    block = CUR.DIAGNOSTIC[s["bi"]]
    s["ii"] += 1
    # stop the block early once it is clearly too hard – no need to struggle on
    if s["ii"] >= len(block["items"]) or s["wrong"] >= block["stop_if_wrong"]:
        stop = s["wrong"] >= block["stop_if_wrong"] or s["bi"] + 1 >= len(CUR.DIAGNOSTIC) \
            or CUR.DIAGNOSTIC[s["bi"] + 1]["level"] not in CUR.LEVELS[: CUR.LEVELS.index(CFG["max_level"]) + 1]
        s.setdefault("blocks", []).append({"level": block["level"], "wrong": s["wrong"],
                                           "passed": s["wrong"] < block["stop_if_wrong"]})
        if stop:
            return finish_diag(p, s, out)
        s.update(bi=s["bi"] + 1, ii=0, wrong=0)
        out.append(M("lt", "Puikiai sekasi! Dabar bus šiek tiek sunkesni klausimai."))
    out += diag_item(s)
    return reply(p, s, out, "happy" if good else "normal", random.choice(PRAISE) if good else None)


def finish_diag(p, s, out):
    passed = [b["level"] for b in s["blocks"] if b["passed"]]
    p["level"] = passed[-1] if passed else "A1 (pradžia)"
    for t in CUR.topics_up_to(CFG["max_level"]):
        topic_state(p, t["id"])["score"] = 0.85 if t["level"] in passed else 0.0
    for r in s["results"]:
        st = topic_state(p, r["topic"])
        st["score"] = max(st["score"], 0.5) if r["ok"] else 0.2
    p["diagnostic"] = {"date": now_iso(), "blocks": s["blocks"], "results": s["results"]}
    p["diagnostic_done"] = True
    good = [r for r in s["results"] if r["ok"]]
    p["sessions"].append({"date": now_iso(), "type": "diagnostika", "topic": "-",
                          "correct": len(good), "total": len(s["results"])})
    knows = list(dict.fromkeys(CUR.TOPIC_BY_ID[r["topic"]]["title"] for r in good))[:4]
    todo = list(dict.fromkeys(CUR.TOPIC_BY_ID[r["topic"]]["title"] for r in s["results"] if not r["ok"]))[:4]
    save_profile(p)
    s["phase"] = "done"
    out += [M("sys", ""), M("head", "Testas baigtas!"),
            M("lt", f"Ačiū, {p['name']}! Teisingai atsakei į {len(good)} iš {len(s['results'])} klausimų.")]
    if knows:
        out.append(M("lt", "Tu jau moki: " + ", ".join(knows) + "."))
    if todo:
        out.append(M("lt", "Kartu pasimokysime: " + ", ".join(todo) + "."))
    out += [M("lt", "Dabar gali pamaitinti katiną arba paspausti „Salto“ – jis apsivers ore!"),
            M("lt", "Jei nori iškart pradėti pirmą pamoką, parašyk „toliau“.")]
    return reply(p, s, out, "happy", "You did it!", done=True)


# ------------------------------------------------------------------ lessons
def choose_topic(p):
    topics = CUR.topics_up_to(CFG["max_level"])
    for t in topics:
        if topic_state(p, t["id"])["score"] < MASTERED:
            return t
    return min(topics, key=lambda t: topic_state(p, t["id"])["last"] or "")   # all learned: review


def lesson_topics(p):
    """The teacher's chosen topics if there is a plan, otherwise the next topic to learn."""
    chosen = [CUR.TOPIC_BY_ID[x] for x in (p.get("plan") or {}).get("topics", []) if x in CUR.TOPIC_BY_ID]
    return chosen or [choose_topic(p)]


def start_lesson(p, s):
    topics = lesson_topics(p)
    ids = [t["id"] for t in topics]
    pools = []
    for t in topics:
        items = [dict(i, topic=t["id"]) for i in t["items"]]
        random.shuffle(items)
        pools.append(items)
    queue, i = [], 0
    while len(queue) < CFG["drill_items"] and any(pools):       # take turns from each chosen topic
        if pools[i % len(pools)]:
            queue.append(pools[i % len(pools)].pop())
        i += 1
    others = [m["item"] for m in p["mistakes"] if m["item"]["topic"] not in ids]
    random.shuffle(others)
    queue += [dict(x, review=True) for x in others[: CFG["review_items"]]]
    title = " + ".join(t["title"] for t in topics)
    focus = " + ".join(t["focus"] for t in topics)
    s.update(phase="drill", topics=ids, title=title, focus=focus, queue=[checker.prepare(x) for x in queue],
             pos=0, first_try=0, retry=False, requeued=set(), turns=0, want_full=False)
    s["total"] = len(s["queue"])
    note = (p.get("plan") or {}).get("note", "").strip()

    last = next((x["topic"] for x in reversed(p["sessions"]) if x.get("type") == "pamoka"), None)
    greet = None
    if s["llm_ok"]:
        greet = llm([{"role": "system", "content": system_prompt(p)},
                     {"role": "user", "content":
                      f"Say hello to {p['name']} in one or two very short, happy English sentences. "
                      f"{'Last time we practised: ' + last + '. ' if last else ''}"
                      f"Today we practise: {focus}. Write nothing else."}], max_tokens=80)
        s["llm_ok"] = greet is not None
    greet = clean_out(greet, f"Hello, {p['name']}! I am happy to see you. Let's learn English!")

    examples = None
    if s["llm_ok"]:
        raw = llm([{"role": "system", "content": system_prompt(p)},
                   {"role": "user", "content":
                    f"Write exactly 3 very short, simple English example sentences for: {focus}. "
                    f"{'Follow the teacher: ' + note + '. ' if note else ''}"
                    f"Use things the student likes ({p.get('interests') or 'animals'}). "
                    f"Max 8 words each. One sentence per line. No numbers, no translation, nothing else."}],
                  max_tokens=90)
        lines = [re.sub(r"^\s*[-•\d.)]+\s*", "", x).strip() for x in (raw or "").splitlines() if x.strip()]
        if len(lines) >= 2 and all(len(x.split()) <= 12 for x in lines[:3]) \
                and all(safety.output_ok(x) for x in lines[:3]):
            examples = lines[:3]
    examples = examples or [e for t in topics for e in t["examples"]][:3]

    out = [M("cat", greet), M("sys", ""), M("head", f"Šiandienos tema: {title}")]
    out += [M("lt", t["rule"]) for t in topics]
    out += [M("lt", "Pavyzdžiai:"), *[M("ex", e) for e in examples], M("sys", ""),
            M("lt", "Dabar – pratimai! Rašyk visus sakinius – už juos gausi 2 ★. Nežinai? Parašyk „nežinau“.")]
    out += render_item(s["queue"][0], 1, s["total"])
    return reply(p, s, out, "happy", f"Hello, {p['name']}!")


def explain(p, s, it, ans, t):
    fallback = "Pažiūrėk į taisyklę: " + t["rule"]
    if not s["llm_ok"]:
        return fallback
    q = it.get("display") or it["q"]
    text = llm([{"role": "system", "content": system_prompt(p)},
                {"role": "user", "content":
                 f"Exercise: {q}\nStudent's answer: {ans}\nCorrect answer: {checker.correct_text(it)}\n"
                 f"Grammar rule (Lithuanian): {t['rule']}\n\n"
                 "In Lithuanian, explain the mistake in 1 or 2 very short, simple sentences for a child "
                 "with special needs. Be kind. Do not repeat the whole rule. Write only the explanation."}],
               max_tokens=120)
    if text is None:
        s["llm_ok"] = False
    text = clean_out(text, fallback)
    return text if len(text) < 400 else fallback


def answer_drill(p, s, text):
    it = s["queue"][s["pos"]]
    t = CUR.TOPIC_BY_ID[it["topic"]]
    v, tip = checker.check(it, text)
    full = v == "ok" and checker.is_full(it, text)

    if v == "near" and not s["retry"]:
        s["retry"] = True
        return reply(p, s, [M("lt", "Beveik! Pažiūrėk atidžiai ir pabandyk dar kartą.")], "think", "Almost!")
    if v == "ok" and not full and it["type"] != "order" and CFG["full_sentences"] == "require" \
            and not s["want_full"]:
        s["want_full"] = True
        return reply(p, s, [M("ok", "Teisingas žodis!"),
                            M("lt", "Dabar parašyk visą sakinį, pvz.: " + checker.correct_text(it))],
                     "happy", "Full sentence, please!")

    out, mood, bubble = [], "happy", None
    if v == "ok":
        value = 0.5 if s["retry"] else 1.0
        if not s["retry"] and not it.get("key_seen"):
            s["first_try"] += 1
        bubble = random.choice(PRAISE)
        if full:
            p["stars"] += 2
            out.append(M("ok", f"{bubble} Visas sakinys!  +2 ★"))
        else:
            p["stars"] += 1
            out.append(M("ok", f"{bubble}  +1 ★"))
            if it["type"] != "order":
                out.append(M("fix", "Visas sakinys: " + checker.correct_text(it)))
                out.append(M("lt", "Kitą kartą parašyk visą sakinį – gausi 2 ★!"))
        if tip:
            out.append(M("lt", tip))
        if it.get("review"):
            remove_mistake(p, it)
    else:
        value = 0.0
        mood, bubble = "sad", random.choice(ENCOURAGE)
        if v == "dontknow":
            out += [M("lt", "Nieko tokio! Pažiūrėk:"), M("fix", "Teisingai: " + checker.correct_text(it)),
                    M("lt", t["rule"])]
        else:
            out += [M("fix", "Teisingai: " + checker.correct_text(it)),
                    M("lt", "Nedidelė klaidelė: " + explain(p, s, it, text, t))]
        add_mistake(p, it)
        p["log"].append({"date": now_iso(), "topic": it["topic"], "q": it.get("display") or it["q"],
                         "ans": text[:80], "correct": checker.correct_text(it)})
        p["log"] = p["log"][-100:]
        k = item_key(it)
        if k not in s["requeued"] and len(s["requeued"]) < 3:   # try it again at the end (max 3)
            s["requeued"].add(k)
            s["queue"].append(dict(it, key_seen=True))
    record(p, it["topic"], value)
    s["retry"] = s["want_full"] = False
    s["pos"] += 1
    save_profile(p)

    if s["pos"] < len(s["queue"]):
        out += [M("sys", "")] + render_item(s["queue"][s["pos"]], s["pos"] + 1, s["total"])
        return reply(p, s, out, mood, bubble)
    return start_chat(p, s, out)


# ------------------------------------------------------------------ short conversation
def chat_system(p, s):
    return system_prompt(p) + f"""

NOW: SHORT CONVERSATION PRACTICE. Today's grammar/words: {s['focus']}.
Ask simple questions that make the student use today's grammar or words in a full sentence.
Answer ONLY with a JSON object with exactly these keys:
"klaida": if the student's last message has a real grammar or word mistake, explain it in ONE short, simple
  Lithuanian sentence. Ignore capital letters, full stops and tiny typos. If there is no real mistake: "".
  If the student answered with only one or two words, kindly ask (in Lithuanian) for a full sentence.
  If the student wrote in Lithuanian, gently ask them (in Lithuanian) to try in English.
"pataisyta": the student's answer as a correct, full English sentence, or "" if it was already a correct
  full sentence.
"atsakymas": your reply in very simple English: one short friendly reaction and one short question. Max 20 words."""


def start_chat(p, s, out):
    if not s["llm_ok"] or CFG["chat_turns"] <= 0:
        return finish_lesson(p, s, out)
    s.update(phase="chat", turns=0)
    s["chat"] = [{"role": "system", "content": chat_system(p, s)},
                 {"role": "user", "content": f"(Start the conversation. Ask {p['name']} one simple question.)"}]
    data = parse_json(llm(s["chat"], json_mode=True, max_tokens=150))
    q = clean_out((data or {}).get("atsakymas", ""), "")
    if not q:
        return finish_lesson(p, s, out)
    s["chat"].append({"role": "assistant", "content": json.dumps({"klaida": "", "pataisyta": "", "atsakymas": q})})
    out += [M("sys", ""), M("head", "Pratimai baigti! Dabar trumpai pasikalbėkime angliškai."),
            M("lt", "Atsakyk visu sakiniu."), M("cat", q)]
    return reply(p, s, out, "happy", "Let's talk!")


def answer_chat(p, s, text):
    s["turns"] += 1
    last = s["turns"] >= CFG["chat_turns"]
    s["chat"].append({"role": "user", "content": text})
    msgs = list(s["chat"])
    if last:
        msgs.append({"role": "system", "content":
                     'This is the last message of the lesson. In "atsakymas" do NOT ask a question: '
                     "say something kind and say goodbye."})
    data = parse_json(llm(msgs, json_mode=True, max_tokens=180)) or {}
    out = []
    klaida = clean_out(str(data.get("klaida") or ""), "")
    fixed = clean_out(str(data.get("pataisyta") or ""), "")
    ans = clean_out(str(data.get("atsakymas") or ""), "")
    if fixed and checker.norm(fixed) == checker.norm(text):
        klaida = fixed = ""                       # the model "corrected" a correct sentence
    if klaida:
        out.append(M("lt", "Nedidelė klaidelė: " + klaida))
    if fixed:
        out.append(M("fix", "Teisingai: " + fixed))
        p["log"].append({"date": now_iso(), "topic": s["topics"][0], "q": "(pokalbis)", "ans": text[:80],
                         "correct": fixed})
    if ans:
        out.append(M("cat", ans))
        s["chat"].append({"role": "assistant", "content": json.dumps(
            {"klaida": klaida, "pataisyta": fixed, "atsakymas": ans}, ensure_ascii=False)})
    if last or not ans:
        return finish_lesson(p, s, out)
    save_profile(p)
    return reply(p, s, out, "sad" if klaida else "happy", None if klaida else random.choice(PRAISE))


def finish_lesson(p, s, out):
    done_items = min(s["pos"], len(s["queue"]))
    original = len([i for i in s["queue"][:done_items] if not i.get("key_seen")])
    p["sessions"].append({"date": now_iso(), "type": "pamoka", "topic": s["title"],
                          "correct": s["first_try"], "total": original})
    save_profile(p)
    s["phase"] = "done"
    learned = all(topic_state(p, t)["score"] >= MASTERED for t in s["topics"])
    out += [M("sys", ""), M("head", "Pamoka baigta! Puikiai padirbėjai!"),
            M("lt", f"Iš pirmo karto teisingai: {s['first_try']} iš {original}. Žvaigždučių iš viso: {p['stars']} ★"),
            M("lt", f"„{s['title']}“ – jau išmokta, kitą kartą eisime toliau!" if learned
              else f"„{s['title']}“ dar pakartosime kitą kartą."),
            M("lt", "Iki kito karto! Jei nori dar vienos pamokos, parašyk „toliau“.")]
    return reply(p, s, out, "happy", "Bye-bye! See you!", done=True)


# ------------------------------------------------------------------ dispatcher
def answer(sl, text):
    p, s = load_profile(sl), SESSIONS.get(sl)
    if not p or not s:
        return {"error": "session"}
    text = (text or "").strip()[:300]
    low = safety.simplify(text).strip(" /.!")

    if s.get("phase") == "done":
        return start(p["name"])
    if not text:
        return reply(p, s, [M("lt", "Parašyk atsakymą ir paspausk Enter.")])

    hit = safety.check_input(text)
    if hit:
        p["alerts"].append({"date": now_iso(), "type": hit, "text": text[:120]})
        p["alerts"] = p["alerts"][-50:]
        save_profile(p)
        msgs = [M("lt", safety.reply_for(hit))]
        if s.get("phase") in ("drill", "diag"):
            it = s["queue"][s["pos"]] if s["phase"] == "drill" else s["item"]
            msgs += [M("lt", "Pabandykime šį klausimą:"), M("q", it.get("display") or it["q"])]
        return reply(p, s, msgs, "normal" if hit == "distress" else "think")

    if low in ("pagalba", "help"):
        return reply(p, s, HELP)
    if low in ("pabaiga", "baigti", "stop", "exit"):
        if s.get("phase") in ("drill", "chat"):
            return finish_lesson(p, s, [])
        s["phase"] = "done"
        return reply(p, s, [M("lt", "Gerai, baigiame. Iki kito karto!")], "happy", "Bye-bye!", done=True)
    if low in ("kartoti", "pakartok", "repeat"):
        if s.get("phase") == "drill":
            return reply(p, s, render_item(s["queue"][s["pos"]], s["pos"] + 1, s["total"]))
        if s.get("phase") == "diag":
            return reply(p, s, diag_item(s))

    phase = s.get("phase")
    if phase == "interests":
        p["interests"] = text[:100]
        save_profile(p)
        return reply(p, s, [M("lt", "Šaunu! Tai panaudosiu pamokose.")] + begin_test(p, s), "happy", "Cool!")
    if phase == "diag":
        return answer_diag(p, s, text)
    if phase == "drill":
        return answer_drill(p, s, text)
    if phase == "chat":
        return answer_chat(p, s, text)
    return start(p["name"])


def feed(sl):
    p = load_profile(sl)
    if not p:
        return {"error": "session"}
    before = fullness(p)
    if before >= 95:
        return reply(p, SESSIONS.get(sl), [], "happy", "I am full! Thank you!")
    p["cat"] = {"full": min(100, before + 25), "t": time.time(), "fed": p["cat"].get("fed", 0) + 1}
    save_profile(p)
    return reply(p, SESSIONS.get(sl), [], "eat", random.choice(YUM))


# ------------------------------------------------------------------ teacher
def report(sl):
    p = load_profile(sl)
    if not p:
        return {"error": "not found"}
    rows = []
    for t in CUR.topics_up_to(CFG["max_level"]):
        st = p["topics"].get(t["id"], {"score": 0, "tries": 0, "correct": 0, "last": None})
        rows.append({"id": t["id"], "level": t["level"], "title": t["title"], **st})
    return {"profile": p, "topics": rows, "mastered": MASTERED}


def save_plan(data):
    if CFG["teacher_pin"] and data.get("pin", "") != CFG["teacher_pin"]:
        return {"error": "pin"}
    p = load_profile(data.get("slug", ""))
    if not p:
        return {"error": "not found"}
    topics = [t for t in data.get("topics", []) if t in CUR.TOPIC_BY_ID]
    p["plan"] = {"topics": topics, "note": str(data.get("note", ""))[:300], "date": now_iso()}
    save_profile(p)
    return {"ok": True, "plan": p["plan"]}


# ------------------------------------------------------------------ http
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(STATIC), **kw)

    def log_message(self, *a):
        pass

    def send_json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/status":
            return self.send_json({**model_status(), "max_level": CFG["max_level"], "cat": CAT,
                                   "pin": bool(CFG["teacher_pin"])})
        if u.path == "/api/students":
            return self.send_json(all_students())
        if u.path == "/api/names":                 # start screen: names only
            names = [x["name"] for x in all_students()] if CFG["show_student_names"] else []
            return self.send_json(names)
        if u.path == "/api/topics":
            return self.send_json([{"id": t["id"], "level": t["level"], "title": t["title"]}
                                   for t in CUR.topics_up_to(CFG["max_level"])])
        if u.path == "/api/report":
            return self.send_json(report(parse_qs(u.query).get("name", [""])[0]))
        if u.path in ("/teacher", "/mokytojas"):
            self.path = "/teacher.html"
        return super().do_GET()

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            data = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self.send_json({"error": "bad json"}, 400)
        path = urlparse(self.path).path
        with LOCK:
            if path == "/api/start":
                return self.send_json(start(data.get("name", "")))
            if path == "/api/answer":
                return self.send_json(answer(data.get("slug", ""), data.get("text", "")))
            if path == "/api/feed":
                return self.send_json(feed(data.get("slug", "")))
            if path == "/api/plan":
                return self.send_json(save_plan(data))
        self.send_json({"error": "not found"}, 404)


def main():
    for stream in (sys.stdout, sys.stderr):      # Windows consoles: show Lithuanian letters safely
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    st = model_status()
    url = f"http://localhost:{CFG['port']}"
    print(f"\n  Anglų katinas veikia:  {url}\n  Mokytojo puslapis:     {url}/teacher\n")
    if st.get("api"):
        print(f"  Modelis: {CFG['model']} per API ({CFG['api_url']})" if st["installed"] else
              "  ! API raktas neveikia – patikrink LLM_API_KEY")
    elif not st["ollama"]:
        print("  ! Nėra API rakto (LLM_API_KEY) ir nėra Ollama. Žr. README.")
    elif not st["installed"]:
        print(f"  ! Modelis neįdiegtas. Paleisk:  ollama pull {CFG['model']}")
    if not st["installed"]:
        print("    (Pratimai veiks ir be modelio, bet nebus paaiškinimų ir pokalbių.)\n")
    default_host = "0.0.0.0" if os.environ.get("CODESPACES") else "127.0.0.1"
    srv = ThreadingHTTPServer((os.environ.get("HOST", default_host), CFG["port"]), Handler)
    if CFG["open_browser"]:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  Iki!")


if __name__ == "__main__":
    main()