# Anglų katinas 🐱

A terminal-style English practice app for Lithuanian students with special educational needs (A1 → B1).
A local Qwen model (through [Ollama](https://ollama.com)) talks to the student; an ASCII cat keeps them company.
Everything runs on your own computer – no accounts, no cloud, student data never leaves the machine.

It is a **drilling and reinforcement tool**, not a replacement for the teacher.

## How a student uses it

1. **First session – diagnostic.** The student types their name, names the cat, says what they like
   (horses, Roblox…), and takes a short test (A1 → A2 → B1). Instructions are in Lithuanian.
   The test stops early once a level is clearly too hard, so nobody struggles through B1 questions.
2. **Every session after that – a short lesson.** The app picks the next topic the student hasn't
   mastered, shows the rule in Lithuanian with examples built around their interests, then drills:
   fill-in-the-blank, multiple choice, word order and translation. Wrong answers get the correct
   sentence plus a short Lithuanian explanation ("Nedidelė klaidelė: …") and come back once at the end.
   Two old mistakes are repeated in every lesson. The lesson ends with a 3-message chat in English,
   where the model corrects mistakes in Lithuanian.
3. Progress is remembered per student in `data/<name>.json`.

Student commands: `nežinau` (I don't know), `kartoti` (repeat), `pagalba` (help), `pabaiga` (end),
`salto` / `pamaitinti`. Click **[▶]** on any English line to hear it read aloud.

**Teacher report:** open <http://localhost:8000/teacher> – level, mastery per topic, lessons,
latest mistakes, the diagnostic answers, and anything the safety filter stopped.

## Setup (Windows + VS Code)

1. Install **Python 3** from <https://www.python.org/downloads/>. Tick "Add python.exe to PATH".
2. In VS Code: **File → Open Folder…** → this project.
3. **Model – choose one:**
   - **Online API (easiest):** copy `.env.example` to a new file called `.env` and paste your
     Alibaba Cloud (Model Studio) key after `LLM_API_KEY=`. Nothing else to install.
     `.env` is git-ignored – never upload it to GitHub.
   - **Offline:** install Ollama from <https://ollama.com/download>, then run `ollama pull qwen3:8b`.
     Used automatically when `.env` has no key.
4. Run it in one of three ways:
   - **Terminal → Run Build Task** (Ctrl+Shift+B), or
   - in the VS Code terminal: `py server.py`, or
   - double-click `start.bat`.

The browser opens at <http://localhost:8000>. Stop the app with Ctrl+C in the terminal.

## Setup (Linux / macOS)

```bash
# 1. Ollama + model (once)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:8b

# 2. Run (Python 3.9+, no packages needed)
./start.sh            # or: python3 server.py
```

The browser opens at <http://localhost:8000>. Without Ollama the exercises still work;
only the explanations, examples and chat are skipped (built-in Lithuanian rules are shown instead).

### Choosing the model
Edit `config.json`:

| setting | meaning |
|---|---|
| `model` | `qwen3:8b` (default, ~5 GB). Weaker computer: `qwen3:4b`. Strong GPU: `qwen3:14b` writes better Lithuanian. |
| `think` | `false` turns off Qwen3's slow "thinking". Use `null` for models without that switch. |
| `max_level` | `A1`, `A2` or `B1` |
| `drill_items`, `review_items`, `chat_turns` | lesson length |

## Safety

Two locks:
1. The model's system prompt forbids sex, romance, private/reproductive body parts, puberty,
   politics, war, religion, drugs, alcohol, weapons, violence; it must not ask for personal details or secrets.
2. `safety.py` filters **what the student types before the model sees it** and **what the model writes
   before the student sees it** (English + Lithuanian + common Russian swearing). Blocked input gets
   "Apie tai mes čia nekalbame. Grįžkime prie anglų kalbos!"; blocked model output is replaced by
   built-in text. If the student writes something that sounds like distress, they get a kind message
   pointing to a trusted adult and Vaikų linija (116 111), and it appears in the teacher report.

The answers themselves are checked by code, not by the model, so the model can't mark a wrong answer correct.
Add words to the lists in `safety.py` if something slips through.

## Changing the content

All topics, Lithuanian rules and exercises are in `curriculum.py` (35 topics, ~210 exercises).
Add a topic with `topic(...)` and exercises with `fill`, `choose`, `tr` (translate) and `order`.

## Files

```
server.py       web server, lesson logic, model calls, student memory
curriculum.py   topics, rules, exercises, diagnostic test
checker.py      answer checking (forgiving about capitals, apostrophes, small typos)
safety.py       content filter
static/         terminal UI, ASCII cat, teacher page
data/           student progress (git-ignored – never commit it)
```
