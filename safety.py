"""Safety filter. Runs on everything the student types BEFORE it reaches the
model, and on everything the model writes BEFORE the student sees it.
The model also gets strict rules in its system prompt; this is the second lock.

Add words to the lists below if you notice something slipping through.
Patterns are matched against lower-case text with Lithuanian letters
simplified (ž->z, ū->u ...), so write them without diacritics.
"""
import re
import unicodedata

# word starts (\b + stem). Keep stems long enough to avoid innocent words.
BLOCK = {
    "sexual": [
        r"sex", r"seks", r"porn", r"nude", r"naked", r"nuog", r"penis", r"vagin", r"genital",
        r"lytin", r"makst", r"testic", r"boob", r"dick\b", r"cock\b", r"condom",
        r"prezervatyv", r"pregnan", r"nescia", r"nescium", r"menstru", r"puberty", r"brendim",
        r"orgasm", r"erotic", r"erotik", r"horny", r"myletis", r"kiss", r"boyfriend", r"girlfriend",
        r"onlyfans", r"bybi", r"pimpal", r"pyzd", r"pizd", r"pist(i|u|uos)\b", r"pisk", r"krusys\b",
    ],
    "politics": [
        r"politi", r"president", r"prezident", r"election", r"rinkim", r"vote\b", r"voting",
        r"balsav", r"parliament", r"seim(as|o|e|ui|u)\b", r"partij", r"putin", r"trump", r"zelensk", r"nauseda",
        r"biden", r"government", r"vyriausyb", r"ministr", r"nato\b", r"war\b", r"wars\b",
        r"kar(as|o|e|a|u|ai|uose)\b", r"protest", r"nazi", r"nacist",
    ],
    "harmful": [
        r"drugs?\b", r"narkot", r"cocain", r"kokain", r"heroin", r"weed\b", r"marihuan", r"alcohol",
        r"alkohol", r"vodka", r"degtin", r"beer\b", r"alus\b", r"cigar", r"vape", r"rukyt", r"gun\b",
        r"guns\b", r"ginkl", r"bomb", r"murder", r"nuzud", r"kill", r"terror", r"blood", r"krauj",
        r"suicid", r"savizud",
    ],
    "rude": [
        r"fuck", r"shit", r"bitch", r"asshole", r"bastard", r"wtf\b", r"blet", r"blyat", r"bliat",
        r"nachui", r"nahui", r"chuj", r"huj", r"kurv", r"debil", r"idiot", r"durn",
    ],
}

# Signs that the student is upset or not safe. These are NOT blocked silently:
# the student gets a kind answer and the teacher sees it in the report.
DISTRESS = [
    r"noriu mirt", r"nenoriu gyvent", r"nusizud", r"save nuzud", r"mane musa", r"mane skriaud",
    r"is manes tycio", r"tyciojasi", r"bijau namo", r"kill myself", r"want to die",
    r"hurts me", r"hits me", r"bullied", r"bully", r"man labai liudna", r"esu labai liudn",
]

_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "@": "a", "$": "s"})


def simplify(text):
    t = unicodedata.normalize("NFKD", (text or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return t.translate(_LEET)


_BLOCK_RE = {cat: re.compile(r"\b(" + "|".join(p for p in pats) + ")") for cat, pats in BLOCK.items()}
_DISTRESS_RE = re.compile("|".join(DISTRESS))


def check_input(text):
    """Returns None if fine, else 'distress' or the category that was hit."""
    t = simplify(text)
    if _DISTRESS_RE.search(t):
        return "distress"
    for cat, rx in _BLOCK_RE.items():
        if rx.search(t):
            return cat
    return None


def output_ok(text):
    t = simplify(text)
    return not any(rx.search(t) for rx in _BLOCK_RE.values())


REPLIES = {
    "distress": ("Atrodo, kad tau dabar sunku. Tai labai svarbu. Pasakyk apie tai savo mokytojui "
                 "arba suaugusiajam, kuriuo pasitiki. Gali nemokamai paskambinti į Vaikų liniją: 116 111."),
    "rude": "Kalbėkime gražiai. Grįžkime prie anglų kalbos!",
    "default": "Apie tai mes čia nekalbame. Grįžkime prie anglų kalbos!",
}


def reply_for(category):
    return REPLIES.get(category, REPLIES["default"])
