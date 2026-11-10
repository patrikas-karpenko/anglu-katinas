// chat.js – what happens in the browser
const $ = (id) => document.getElementById(id);
const chat = $("chat");
const form = $("form");
const input = $("input");
const cat = $("cat");
const bubble = $("bubble");
const sendButton = $("send");
const courseSelect = $("course");
const lessonSelect = $("lesson");
const scoreBox = $("score");
const helpers = $("helpers");

let ui = {};   // the words on the page (buttons, headings) in the course's language

// 0. The teacher's settings, saved in this browser
const DEFAULTS = {
  mode: "drill",                                              // "drill" or "chat"
  types: { word: true, fill: true, translate: true, listen: true },
  count: 12,                                                  // exercises per round
  strict: true,                                               // check capitals and punctuation
  speak: true,                                                // say the right answer aloud
  focus: "",                                                  // instruction for William
};

function loadSettings() {
  try {
    const saved = JSON.parse(localStorage.getItem("teacher-settings") || "{}");
    return { ...DEFAULTS, ...saved, types: { ...DEFAULTS.types, ...(saved.types || {}) } };
  } catch {
    return { ...DEFAULTS };
  }
}
let settings = loadSettings();

// Has this browser met William before? Open the page with ?new to make him introduce himself again.
if (location.search.includes("new")) localStorage.removeItem("met-william");
let firstTime = !localStorage.getItem("met-william");

// 1. Draw William
const EYES = { normal: "o   o", happy: "^   ^", think: "-   o", wink: "^   -" };

function drawCat(mood) {
  cat.textContent = [
    "    /\\_____/\\",
    `   /  ${EYES[mood]}  \\`,
    "  ( ==  ^  == )",
    "   )         (     (",
    "  (           )     )",
    " ( (  )   (  ) )   /",
    "(__(__)___(__)__)_/",
  ].join("\n");
}

drawCat("normal");

// 2. William's tricks: a speech bubble and a flip
function say(text, ms = 3000) {
  bubble.textContent = text;
  bubble.classList.add("show");
  setTimeout(() => bubble.classList.remove("show"), ms);
}

function flip() {
  cat.classList.remove("flip");
  void cat.offsetWidth;            // restart the animation if it is already running
  cat.classList.add("flip");
  drawCat("happy");
  setTimeout(() => { cat.classList.remove("flip"); drawCat("wink"); }, 1100);
  setTimeout(() => drawCat("normal"), 2000);
}

cat.addEventListener("click", flip);   // click William and he flips

// Test button: makes William flip, so you can check the animation without answering 5 questions
$("flip-test").addEventListener("click", () => {
  flip();
  say(ui.perfect || "Miau!", 2000);
});

// 3. The score next to William: every right answer adds 1. At 5/5 he flips and it starts again at 0/5.
const GOAL = 5;
let points = 0;

function showScore() {
  scoreBox.textContent = `${points}/${GOAL}`;
  scoreBox.classList.remove("bump");
  void scoreBox.offsetWidth;       // restart the little "bump" animation
  scoreBox.classList.add("bump");
}

function addPoint() {
  points += 1;
  showScore();
  if (points === GOAL) {
    flip();
    say(ui.perfect, 3000);
    setTimeout(() => { points = 0; showScore(); }, 2500);
  }
}

// 4. Reading aloud: the browser says English words and sentences
const canSpeak = "speechSynthesis" in window;
let englishVoice = null;

function pickVoice() {
  const voices = speechSynthesis.getVoices();
  englishVoice = voices.find((v) => v.lang === "en-GB") || voices.find((v) => v.lang.startsWith("en")) || null;
}
if (canSpeak) {
  pickVoice();
  speechSynthesis.onvoiceschanged = pickVoice;   // some browsers load the voices a bit later
}

function speak(text) {
  if (!canSpeak || !text) return;
  speechSynthesis.cancel();                       // stop whatever it was saying
  const sentence = new SpeechSynthesisUtterance(text.replace(/…/g, ""));
  sentence.lang = "en-GB";
  if (englishVoice) sentence.voice = englishVoice;
  sentence.rate = 0.85;                           // a little slower than normal
  speechSynthesis.speak(sentence);
}

function speakButton(text) {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "speak";
  b.textContent = "🔊";
  b.title = ui.listen;
  b.hidden = !canSpeak;
  b.addEventListener("click", () => speak(text));
  return b;
}

// 5. Put a message on the screen (with a 🔊 button if there is English to listen to)
function addMessage(who, text, speakText) {
  const div = document.createElement("div");
  div.className = "msg " + who;   // "msg me", "msg william" ...
  div.textContent = text;         // textContent, never innerHTML: typed text can't break the page
  if (speakText) div.appendChild(speakButton(speakText));
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function busy(on) {
  sendButton.disabled = on;
  for (const b of helpers.querySelectorAll("button")) b.disabled = on;
  drawCat(on ? "think" : "normal");
}

const pick = (list) => list[Math.floor(Math.random() * list.length)];

// 6. William talks: in drill mode he opens the lesson, in chat mode he teaches the whole lesson
const history = [];   // the conversation so far. The model remembers nothing, so we send all of it every time.

async function askWilliam() {
  busy(true);
  let data;
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course: courseSelect.value,
        lesson: Number(lessonSelect.value),
        messages: history,
        first_time: firstTime,
        mode: settings.mode,
        focus: settings.focus,
      }),
    });
    data = await response.json();
    if (firstTime && response.ok) {        // William has introduced himself: never again
      firstTime = false;
      localStorage.setItem("met-william", "yes");
    }
  } catch (error) {
    data = { reply: ui.no_server, mark: null };
  }

  history.push({ role: "assistant", content: data.reply });
  addMessage("william", data.reply);
  busy(false);
  drawCat("happy");
  setTimeout(() => drawCat("normal"), 1500);
  if (data.mark === "right") addPoint();   // chat mode: William said the answer was right
  input.focus();
}

// 7. Drills: the code gives the exercises and checks the answers
let round = null;   // { items, i, attempt, copying, firstTry, missed, reviewing, total }

async function startRound() {
  busy(true);
  input.disabled = false;
  let items = [];
  try {
    const response = await fetch("/api/drill", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course: courseSelect.value,
        lesson: Number(lessonSelect.value),
        types: settings.types,
        count: settings.count,
        focus: settings.focus,
      }),
    });
    items = (await response.json()).items || [];
  } catch (error) {
    addMessage("william", ui.no_server);
  }
  busy(false);
  if (!items.length) return;
  round = { items, i: 0, attempt: 1, copying: false, firstTry: 0, missed: [], reviewing: false, total: items.length };
  helpers.hidden = false;
  showItem();
}

const current = () => (round ? round.items[round.i] : null);

function stripHint(q) {                       // "I ___ swim. (moku)" -> "I ___ swim."
  return q.endsWith(")") ? q.slice(0, q.lastIndexOf(" (")) : q;
}

function rightAnswer(item) {                  // the answer as a whole sentence
  return item.type === "fill" ? stripHint(item.q).replace("___", item.a[0]) : item.a[0];
}

function questionText(item) {
  if (item.type === "word") return ui.q_word.replace("{lt}", item.lt);
  if (item.type === "phrase") return ui.q_phrase.replace("{lt}", item.lt);
  if (item.type === "fill") return `${ui.q_fill}\n${item.q}`;
  if (item.type === "translate") return `${ui.q_translate}\n${item.lt}`;
  return ui.q_listen;
}

function showItem() {
  const item = current();
  round.attempt = 1;
  round.copying = false;
  const counter = round.reviewing ? "" : `${ui.exercise} ${round.i + 1}/${round.total}\n`;
  addMessage("william task", counter + questionText(item), item.type === "listen" ? item.say : null);
  if (item.type === "listen") speak(item.say);
  $("listen-btn").hidden = item.type !== "listen";
  input.focus();
}

function missed(item) {
  if (!round.reviewing && !round.missed.includes(item)) round.missed.push(item);
}

function nextItem() {
  round.i += 1;
  if (round.i < round.items.length) {
    setTimeout(showItem, 700);
  } else if (!round.reviewing && round.missed.length) {   // once more, the ones that went wrong
    round.reviewing = true;
    round.items = round.items.concat(round.missed);
    addMessage("william", ui.review);
    setTimeout(showItem, 700);
  } else {
    finishRound();
  }
}

function finishRound() {
  helpers.hidden = true;
  const text = ui.round_done.replace("{n}", round.firstTry).replace("{total}", round.total);
  const div = addMessage("william result", text);
  const again = document.createElement("button");
  again.type = "button";
  again.className = "again";
  again.textContent = ui.again;
  again.addEventListener("click", () => { again.remove(); startRound(); });
  div.appendChild(again);
  chat.scrollTop = chat.scrollHeight;  // show the button too
  round = null;
  input.disabled = true;               // wait for "Dar kartą"
}

async function answerItem(text) {
  const item = current();
  busy(true);
  let r;
  try {
    const response = await fetch("/api/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course: courseSelect.value,
        item,
        answer: text,
        strict: settings.strict,
        explain: !round.copying && round.attempt === 1,
      }),
    });
    r = await response.json();
  } catch (error) {
    busy(false);
    addMessage("william", ui.no_server);
    return;
  }
  busy(false);

  // a) The student is copying the right answer after a mistake
  if (round.copying) {
    if (r.result === "right") addMessage("william", pick(ui.praise));
    else addMessage("william", ui.answer_is.replace("{a}", r.expected), r.expected);
    return nextItem();
  }

  // b) Right!
  if (r.result === "right") {
    if (round.attempt === 1 && !round.reviewing) round.firstTry += 1;
    addMessage("william good", r.message, r.expected);
    if (settings.speak) speak(r.expected);
    addPoint();
    return nextItem();
  }

  // c) Only capitals, punctuation or spelling: one more try
  if ((r.result === "form" || r.result === "spelling") && round.attempt === 1) {
    round.attempt = 2;
    addMessage("william", `${r.message}\n${ui.try_again}`);
    return;
  }

  // d) A real mistake (or the second try didn't work): show the answer, the student writes it once
  let reply = r.message;
  if (r.result !== "wrong") reply += "\n" + ui.answer_is.replace("{a}", r.expected);
  if (r.explain) reply += "\n" + r.explain;
  addMessage("william", `${reply}\n${ui.copy}`, r.expected);
  if (settings.speak) speak(r.expected);
  missed(item);
  round.copying = true;
}

// Helper buttons
function hintFor(text) {                     // "can't swim" -> "c____ s___"
  return text.replace(/[A-Za-z]+/g, (w) => w[0] + "_".repeat(w.length - 1));
}

$("hint-btn").addEventListener("click", () => {
  const item = current();
  if (!item || round.copying) return;
  addMessage("william", "💡 " + hintFor(item.a[0]));
  input.focus();
});

$("dontknow-btn").addEventListener("click", () => {
  const item = current();
  if (!item || round.copying) return;
  addMessage("me", ui.dont_know);
  const answer = rightAnswer(item);
  addMessage("william", `${ui.answer_is.replace("{a}", answer)}\n${ui.copy}`, answer);
  if (settings.speak) speak(answer);
  missed(item);
  round.copying = true;
  input.focus();
});

$("listen-btn").addEventListener("click", () => {
  const item = current();
  if (item && item.say) speak(item.say);
  input.focus();
});

// 8. When you press Send
form.addEventListener("submit", async (event) => {
  event.preventDefault();          // stop the browser from reloading the page
  const text = input.value.trim();
  if (!text || sendButton.disabled) return;

  input.value = "";
  addMessage("me", text);
  if (settings.mode === "drill") {
    if (current()) await answerItem(text);
    return;
  }
  history.push({ role: "user", content: text });
  await askWilliam();
});

// 9. The lesson card: everything new in this lesson, built from the course file
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function showCard(lesson) {
  const card = el("section", "card");
  card.appendChild(el("h2", "", lesson.title));
  card.appendChild(el("p", "subtitle", lesson.title_learner));

  if (lesson.grammar.length) {
    const goals = lesson.grammar.map((g) => g.name).join(" · ");
    card.appendChild(el("p", "goals", `${ui.you_will_learn} ${goals}`));
  }

  if (lesson.words.length) {
    card.appendChild(el("h3", "", ui.new_words));
    const table = el("table", "words");
    for (const w of lesson.words) {
      const row = el("tr");
      const listen = el("td", "listen");
      listen.appendChild(speakButton(w.text));
      row.appendChild(listen);
      row.appendChild(el("td", "text", w.text));
      if (w.pron) row.appendChild(el("td", "pron", w.pron));   // only if the course has pronunciation
      row.appendChild(el("td", "meaning", w.meaning));
      table.appendChild(row);
    }
    card.appendChild(table);
  }

  if (lesson.grammar.length) {
    card.appendChild(el("h3", "", ui.grammar));
    for (const g of lesson.grammar) {
      const box = el("div", "grammar");
      box.appendChild(el("p", "g-name", g.name));
      box.appendChild(el("p", "g-explain", g.explain));
      box.appendChild(el("p", "g-pattern", g.pattern));
      for (const ex of g.examples.slice(0, 2)) {
        const parts = [ex.text, ex.pron, ex.meaning].filter(Boolean);
        const line = el("p", "g-example", parts.join("  –  "));
        line.prepend(speakButton(ex.text));
        box.appendChild(line);
      }
      card.appendChild(box);
    }
  }

  chat.appendChild(card);
}

// 10. Teacher settings
function teacherForm() {
  const f = $("teacher-form");
  f.innerHTML = "";
  f.appendChild(el("h2", "", ui.t_title));

  const mode = el("fieldset");
  mode.appendChild(el("legend", "", ui.t_mode));
  for (const [value, label] of [["drill", ui.t_drill], ["chat", ui.t_chat]]) {
    const l = el("label");
    const r = el("input");
    r.type = "radio"; r.name = "mode"; r.value = value; r.checked = settings.mode === value;
    l.append(r, " " + label);
    mode.appendChild(l);
  }
  f.appendChild(mode);

  const types = el("fieldset");
  types.appendChild(el("legend", "", ui.t_types));
  for (const t of ["word", "fill", "translate", "listen"]) {
    const l = el("label");
    const c = el("input");
    c.type = "checkbox"; c.name = "type-" + t; c.checked = settings.types[t];
    l.append(c, " " + ui["t_" + t]);
    types.appendChild(l);
  }
  f.appendChild(types);

  const count = el("label", "row");
  const n = el("input");
  n.type = "number"; n.name = "count"; n.min = 3; n.max = 40; n.value = settings.count;
  count.append(ui.t_count + " ", n);
  f.appendChild(count);

  for (const [name, label] of [["strict", ui.t_strict], ["speak", ui.t_speak]]) {
    const l = el("label", "row");
    const c = el("input");
    c.type = "checkbox"; c.name = name; c.checked = settings[name];
    l.append(c, " " + label);
    f.appendChild(l);
  }

  const focus = el("label", "focus");
  focus.append(ui.t_focus);
  const area = el("textarea");
  area.name = "focus"; area.rows = 2; area.maxLength = 300; area.placeholder = ui.t_focus_ph; area.value = settings.focus;
  focus.appendChild(area);
  f.appendChild(focus);

  // "Save" comes first, so pressing Enter saves (CSS shows it on the right)
  const buttons = el("div", "dialog-buttons");
  const save = el("button", "", ui.t_save);
  save.value = "save";
  const cancel = el("button", "secondary", ui.t_cancel);
  cancel.value = "cancel";
  buttons.append(save, cancel);
  f.appendChild(buttons);
}

$("teacher-btn").addEventListener("click", () => {
  teacherForm();
  $("teacher").showModal();
});

$("teacher").addEventListener("close", () => {
  if ($("teacher").returnValue !== "save") return;
  const field = (name) => $("teacher-form").elements.namedItem(name);
  settings = {
    mode: field("mode").value,
    types: Object.fromEntries(["word", "fill", "translate", "listen"].map((t) => [t, field("type-" + t).checked])),
    count: Math.min(40, Math.max(3, Number(field("count").value) || 12)),
    strict: field("strict").checked,
    speak: field("speak").checked,
    focus: field("focus").value.trim(),
  };
  localStorage.setItem("teacher-settings", JSON.stringify(settings));
  startLesson();                    // start again with the new settings
});

// 11. Start a lesson: card first, then William opens it, then the exercises
async function startLesson() {
  chat.innerHTML = "";             // clear the screen
  history.length = 0;              // forget the old conversation
  round = null;
  helpers.hidden = true;
  input.disabled = false;
  points = 0;                      // new lesson, new score
  scoreBox.textContent = `0/${GOAL}`;
  localStorage.setItem("course", courseSelect.value);
  localStorage.setItem("lesson-" + courseSelect.value, lessonSelect.value);

  const response = await fetch(`/api/courses/${courseSelect.value}/lessons/${lessonSelect.value}`);
  const data = await response.json();
  ui = data.ui;
  input.placeholder = ui.placeholder;
  sendButton.textContent = ui.send;
  $("teacher-btn").title = ui.teacher;
  $("hint-btn").textContent = "💡 " + ui.hint;
  $("listen-btn").textContent = "🔊 " + ui.listen;
  $("dontknow-btn").textContent = "🤷 " + ui.dont_know;

  showCard(data.lesson);           // the handout first...
  if (settings.focus) addMessage("focus", ui.focus_on.replace("{f}", settings.focus));
  await askWilliam();              // ...then William opens the lesson...
  if (settings.mode === "drill") {
    await startRound();            // ...and the exercises start
  } else {
    chat.scrollTop = 0;            // chat mode: start reading at the top of the card
  }
}

// 12. Fill the lesson menu for the chosen course
async function loadLessons() {
  const response = await fetch(`/api/courses/${courseSelect.value}/lessons`);
  const lessons = await response.json();
  lessonSelect.innerHTML = "";
  for (const lesson of lessons) {
    const option = document.createElement("option");
    option.value = lesson.id;
    option.textContent = `${lesson.title} · ${lesson.title_learner}`;
    lessonSelect.appendChild(option);
  }
  lessonSelect.value = localStorage.getItem("lesson-" + courseSelect.value) || lessons[0].id;
  await startLesson();
}

// 13. Fill the course menu (hidden when there is only one course)
async function loadCourses() {
  const response = await fetch("/api/courses");
  const courses = await response.json();
  for (const course of courses) {
    const option = document.createElement("option");
    option.value = course.id;
    option.textContent = course.name;
    courseSelect.appendChild(option);
  }
  courseSelect.hidden = courses.length < 2;
  const saved = localStorage.getItem("course");
  if (courses.some((c) => c.id === saved)) courseSelect.value = saved;
  await loadLessons();
}

courseSelect.addEventListener("change", loadLessons);
lessonSelect.addEventListener("change", startLesson);
loadCourses();
