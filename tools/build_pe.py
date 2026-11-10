"""Build course/project-explore-1.json and course/project-explore-2.json.
Usage (from the project folder): python tools/build_pe.py course
Edit the words in pe1.py / pe2.py, grammar in grammar_lt.py, exercises in exercises_lt.py, then run this.
It refuses to build if a sentence is missing its capital letter or end punctuation."""
import json
import sys

sys.path.insert(0, sys.path[0])
from grammar_lt import G  # noqa: E402
from exercises_lt import EX  # noqa: E402
import pe1  # noqa: E402
import pe2  # noqa: E402

out = sys.argv[1]

INSTRUCTIONS = (
    "The student is a Lithuanian school student (about 10-13 years old) and may have special educational needs. "
    "Speak to the student in simple, short, correct Lithuanian. English is only for the words, examples and practice. "
    "Keep English sentences very short and simple. "
    "Start every correction with 'Nedidelė klaidelė:', then show the correct English sentence and explain the mistake "
    "in one short Lithuanian sentence. "
    "Always ask the student to answer in a full sentence ('My cat is brown.', not 'brown'). "
    "Be warm and patient; praise effort. "
    "Ordinary body parts (head, arm, knee) are fine when the lesson needs them; never talk about private parts, romance, "
    "dating, alcohol, violence or anything really scary. Monsters and ghosts from the lesson are fine, in a fun way. "
    "Never ask for personal details such as addresses, phone numbers, school names or passwords."
)

UI = {
    "lesson": "Pamoka", "you_will_learn": "Išmoksi:", "new_words": "Nauji žodžiai", "grammar": "Gramatika",
    "placeholder": "Rašyk Williamui…", "send": "Siųsti", "perfect": "Puiku! 5 iš 5!",
    "start": "Labas! Pradėkime pamoką.",
    "no_server": "Miau… serveris neatsako. Ar jis paleistas?",
    "no_model": "Miau… negaliu prisijungti prie savo „smegenų“. Patikrink LLM_API_KEY.",
    # drills
    "q_word": "Kaip angliškai „{lt}“?", "q_phrase": "Kaip pasakyti angliškai: „{lt}“",
    "q_fill": "Įrašyk, kas trūksta:", "q_translate": "Išversk į anglų kalbą:",
    "q_listen": "Klausyk ir parašyk, ką girdi.",
    "exercise": "Pratimas", "review": "Dar kartą tie, kurie nepavyko:",
    "praise": ["Puiku!", "Teisingai!", "Šaunu!", "Labai gerai!", "Taip!"],
    "also_right": "Taip pat galima: {a}", "inner_punct": "Nepamiršk skyrybos ženklų: {a}",
    "hyphen": "Rašoma su brūkšneliu: {a}",
    "almost": "Beveik!", "try_again": "Parašyk dar kartą.", "copy": "Dabar parašyk teisingai:",
    "mistake": "Nedidelė klaidelė:", "correct_is": "teisingai būtų „{a}“.", "answer_is": "Atsakymas: {a}",
    "spelling": "rašyba – rašoma „{w}“.",
    "start_capital": "Sakinys prasideda didžiąja raide.",
    "i_capital": "Žodis „I“ (aš) visada rašomas didžiąja raide.",
    "proper_capital": "Žodis „{w}“ rašomas didžiąja raide.",
    "acronym": "„{w}“ rašoma didžiosiomis raidėmis.",
    "end_dot": "Sakinio gale reikia taško (.).", "end_question": "Klausimo gale reikia klaustuko (?).",
    "is_question": "Tai klausimas – gale reikia klaustuko (?).",
    "not_question": "Tai ne klausimas – gale reikia taško (.).",
    "apostrophe": "Trūksta apostrofo: {w}.",
    "round_done": "Pratimai baigti! Iš pirmo karto teisingai: {n} iš {total}.", "again": "Dar kartą",
    "dont_know": "Nežinau", "hint": "Užuomina", "listen": "Klausyti", "teacher": "Mokytojui",
    "focus_on": "Mokytojo tema: {f}",
    # teacher settings
    "t_title": "Mokytojo nustatymai", "t_mode": "Režimas", "t_drill": "Pratimai",
    "t_chat": "Pokalbis su Williamu", "t_types": "Pratimų tipai", "t_word": "Žodžiai ir frazės",
    "t_fill": "Užpildyk tarpą", "t_translate": "Sakinių vertimas", "t_listen": "Klausymas (diktantas)",
    "t_count": "Pratimų skaičius", "t_strict": "Tikrinti didžiąsias raides ir skyrybą",
    "t_speak": "Ištarti teisingą atsakymą balsu", "t_focus": "Nurodymas Williamui (nebūtina)",
    "t_focus_ph": "Pvz.: spalvos su present simple", "t_save": "Išsaugoti", "t_cancel": "Atšaukti",
}


def parse_words(block):
    words = []
    for line in block.strip().splitlines():
        en, lt = line.split(" = ", 1)
        words.append({"text": en.strip(), "meaning": lt.strip()})
    return words


def grammar(gid):
    name, explain, pattern, examples = G[gid]
    return {"id": gid, "name": name, "explain": explain, "pattern": pattern,
            "examples": [{"text": e, "meaning": m} for e, m in examples], "requires": [],
            "exercises": EX[gid]}


# ---- checks: every sentence starts with a capital letter and ends with . ? or ! ----
END = (".", "?", "!")
problems = []


def is_sentence(s):
    return (s[:1].isupper() or s[:1].isdigit()) and s.endswith(END)


def check_data():
    assert set(EX) == set(G), set(G) ^ set(EX)
    for gid, items in EX.items():
        for it in items:
            if it["type"] == "fill":
                q = it["q"]
                if q.count("___") != 1:
                    problems.append(f"{gid}: one ___ needed: {q}")
                sentence = q.rsplit(" (", 1)[0] if q.endswith(")") else q
                if not sentence.endswith(END):
                    problems.append(f"{gid}: fill sentence must end with punctuation: {q}")
                for a in it["a"]:
                    filled = sentence.replace("___", a)
                    if not filled[:1].isupper():
                        problems.append(f"{gid}: filled sentence starts small: {filled}")
            else:
                if not is_sentence(it["lt"]):
                    problems.append(f"{gid}: Lithuanian sentence: {it['lt']}")
                for a in it["a"]:
                    if not is_sentence(a):
                        problems.append(f"{gid}: answer not a sentence: {a}")
        for e, m in G[gid][3]:
            if not (is_sentence(e) and is_sentence(m)):
                problems.append(f"{gid}: example: {e} / {m}")
    for book in (pe1, pe2):
        for code, *_rest, block in book.LESSONS:
            for w in parse_words(block):
                t = w["text"]
                # a phrase that starts with a capital letter must end like a sentence (or with …)
                if " " in t and t[:1].isupper() and not t.endswith(END + ("…",)) and not t.startswith(("I can't stand", "I don't feel")):
                    problems.append(f"{code}: phrase without end punctuation: {t}")
                if t.endswith(END) and not t[:1].isupper():
                    problems.append(f"{code}: sentence without capital: {t}")
    if problems:
        print("\n".join(problems))
        sys.exit(1)


check_data()


def course(cid, name, book, lessons):
    c = {
        "id": cid, "name": name,
        "target_language": "English", "learner_language": "Lithuanian",
        "format_example": "cat – katė", "restrict_vocabulary": False,
        "instructions": INSTRUCTIONS, "ui": UI,
        "source": f"Lesson order, vocabulary and grammar follow {book} (Oxford University Press). "
                  "Lithuanian meanings and explanations written for this app.",
        "practice_links": [], "lessons": [],
    }
    for i, (code, title, title_lt, gids, block) in enumerate(lessons, 1):
        c["lessons"].append({"id": i, "title": f"{code} · {title}", "title_learner": title_lt,
                             "words": parse_words(block), "grammar": [grammar(g) for g in gids]})
    path = f"{out}/{cid}.json"
    json.dump(c, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path, len(c["lessons"]), "lessons,", sum(len(l["words"]) for l in c["lessons"]), "words,",
          sum(len(l["grammar"]) for l in c["lessons"]), "grammar points")


course("project-explore-1", "Project Explore 1", "Project Explore 1", pe1.LESSONS)
course("project-explore-2", "Project Explore 2", "Project Explore 2", pe2.LESSONS)
