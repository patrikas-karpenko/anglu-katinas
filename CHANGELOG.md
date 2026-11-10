# Changelog – William (English for Lithuanian students)

Newest changes first. "Still to do" at the bottom is the plan for what comes next.

## 2026-11-10 (later) – Fix: hint / "Nežinau" buttons seemed stuck
- After a mistake (while the student copies the right answer) both buttons did nothing. Now 💡 shows
  the answer again, and 🤷 shows it once more and moves on to the next exercise.
- In the short pause between exercises, the buttons (and Enter) acted on the next, not-yet-shown
  question. They now wait until it appears.
- "Nežinau" on a sentence step when William had no example skipped silently. Now he says "Gerai,
  einame toliau." first.

## 2026-11-10 (afternoon) – Smaller word lists, word → sentence drills
**Smaller word lists**
- Every book lesson with more than 8 words is split into parts of at most 8. For example, 3A (36
  words) is now 5 parts.
- Book 1 has 70 parts and book 2 has 58. No book words were dropped.
- Each part keeps the lesson's grammar.
- In the lesson menu, the parts are grouped under their book lesson ("3A · Wild animals · Laukiniai
  gyvūnai" → "Laukiniai gyvūnai 1/5"). Set the size with `MAX_WORDS` in `tools/build_pe.py`.

**Words, then a sentence**
- A round now goes: word, word → **make a sentence with them**, word, word → sentence, … then 2
  fill-in-the-gap exercises and 1 translation for the grammar.
- One of the word drills is sometimes a dictation instead.
- The sentence step ("Dabar sudaryk sakinį su žodžiu „elephant“ arba „giraffe“") shows the lesson's
  grammar pattern.
- The code checks the sentence: the lesson word is there (any form: elephants, dancing), at least 3
  words, a capital letter, end punctuation and apostrophes.
- William checks the grammar. If it's wrong, he gives the corrected sentence and why (in
  Lithuanian), and the student copies it. A sentence that isn't OK for school gets "try again".
- On the sentence step:
  - 💡 shows the pattern and sentence starters ("I like … / I can see … / This is …").
  - 🤷 Nežinau gives an example sentence from William to copy.
- Teacher settings: a new on/off for "Sakinių kūrimas su žodžiais", and the exercise number is now
  the most per round (default 15).

## 2026-11-10 – Drills, code-checked answers, teacher settings, reading aloud

**Drill-focused lessons (new default)**
- A lesson is now: the lesson card → William opens it in 1–2 Lithuanian sentences → a round of
  short exercises made by the code (`drills.py`), not by William.
- Five exercise types:
  - word (LT → EN)
  - phrase (LT → EN, e.g. "Iš kur tu esi?" → "Where are you from?")
  - fill in the gap
  - sentence translation
  - listening/dictation
- Easy exercises come first and harder ones later.
- After a round, the exercises that went wrong come back once ("Dar kartą tie, kurie nepavyko").
- Then a summary appears ("Iš pirmo karto teisingai: 9 iš 12") with a **Dar kartą** button.
- Helper buttons: 💡 **Užuomina** (first letters: "c__ s___"), 🤷 **Nežinau** (shows the answer) and
  🔊 **Klausyti** (repeats the dictation).
- After a mistake or "Nežinau", the student writes the right answer once ("Dabar parašyk teisingai:").

**Answers checked by code (`checker.py`)**
- First it checks the words, ignoring capitals and punctuation. "I'm" = "I am" and "can't" =
  "cannot". British and American spelling both count (colour/color), and so do numbers (8 = eight).
- Then capitals and punctuation, when the teacher's "strict" setting is on (the default):
  - capital letter at the start of a sentence
  - "I" always capital
  - names, countries, months and other capitalized words
  - TV/UK in capitals
  - . or ? at the end, and ? for questions
  - apostrophes (Im → I'm)
- Missing commas get a gentle note but still count as right.
- A capitals or punctuation slip, or a spelling slip (freindly → friendly), gets one more try.
- A real mistake (like/likes, is/are, a/an) shows the right answer, and William explains why in one
  Lithuanian sentence. The code decides it is wrong; William only explains, so he can't mark a wrong
  answer right.
- On a fill-in-the-gap exercise, the student can type just the missing word or the whole sentence.
- Other English words with the same Lithuanian meaning are accepted too (gražus → beautiful or
  pretty), with a note.
- The input box no longer auto-capitalizes or spell-checks, so it can't hide the student's mistakes.

**Exercise bank**
- 336 hand-written exercises: 5 fill-in-the-gap and 3 sentence translations for each of the 42
  grammar points, plus all the words and phrases of every lesson.
- The data is built with `tools/build_pe.py`. The build refuses to finish if any sentence is missing
  its capital letter or end punctuation.

**Teacher settings (⚙ button, top right)**
- Mode:
  - **Pratimai** (drills, default)
  - **Pokalbis su Williamu** (William teaches in the chat, now told to be drill-style: little talk,
    lots of practice)
- Exercise types on/off, exercises per round, strict capitals/punctuation on/off, and saying the
  right answer aloud on/off.
- **Instruction for William**, e.g. "spalvos su present simple":
  - William writes extra exercises for it. The code keeps only the ones it can check: a single gap,
    capitals and punctuation present.
  - The instruction is shown above the chat.
- Settings are saved in the browser (per computer).

**Reading aloud**
- 🔊 next to every word and grammar example on the card, and next to William's answers.
- Dictation exercises: the browser says a word or sentence, and the student writes it.
- After each answer the right English answer is said aloud (can be switched off).
- It uses the browser's own voice (British English if there is one), so it's free and no sound is
  sent anywhere.

**Capitals and punctuation in the data and in William's replies**
- William's instructions now say every sentence starts with a capital letter and ends with . ? or !
- School subjects are now written the normal English way (art, maths, history; English, IT and PE
  keep their capitals). Music room, Science lab and Science workshop are lowercase too, and "Wi-fi"
  is now "Wi-Fi".

**Files**
- New: `checker.py`, `drills.py`, `tools/` (the course data and the build script), `CHANGELOG.md`.
- Changed: `app.py` (new `/api/drill` and `/api/check`, mode and focus in `/api/chat`, page texts with
  English defaults), `static/*`, the course files.

## 2026-11-09 (evening) – William keeps going, test button
- William stopped after praising an answer. He is now told to always ask the next question in the
  same message.
- 🐱 **Salto!** test button makes William flip.

## 2026-11-09 – Project Explore curriculum
- The English File course was replaced with **Project Explore 1** and **Project Explore 2**: 53
  lessons in the books' order, with core words and phrases from the workbook word lists, Lithuanian
  meanings and grammar explained in Lithuanian.
- A score badge next to William: +1 for each right answer, a flip at 5/5, then back to 0/5.
- The lesson starts in Lithuanian. William introduces himself only the first time (open the page with
  `?new` to see it again).

## 2026-11-09 (earlier) – Lithuanian version as its own project
- The same engine as the Chinese tutor; every `course/*.json` file becomes a course in the menu.
- All instructions and corrections are in Lithuanian, and the student is asked for full sentences.

## Still to do
- **Lesson stages:** the server only sends William the last 20 messages, so in chat mode he can lose
  track of long lessons. Drill mode doesn't have this problem.
- **Split long lessons** (20–36 words) into parts for SEN students.
- **Safety filter in code** for what students type and what William says (the first app had one).
- **Diagnostic test** on the first session.
- **Student profiles and progress** (postponed). Feeding William comes with these.
- **Pronunciation (IPA)** for the words. The scans were too poor to copy it.
- **Student reads aloud** (speech recognition). Chrome sends the recording to Google, so check
  privacy first.
- **Privacy before school use:** no names in messages, a data agreement with the model provider, and
  a DPIA.
- Bring the Chinese tutor up to date with this engine.
