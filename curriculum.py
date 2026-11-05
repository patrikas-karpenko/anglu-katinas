"""
Curriculum: A1 -> B1 topics, Lithuanian rules, exercise bank and diagnostic test.

Everything here is written by hand, so the checking of answers never depends on
the language model. Add topics or exercises freely: the app picks them up.

Exercise types
  fill      – sentence with ___ ; student types the missing word(s)
  choose    – multiple choice ; student types a letter (a/b/c) or the word
  translate – Lithuanian word -> English word
  order     – put the words in the right order
"""

LEVELS = ["A1", "A2", "B1"]


def fill(q, *answers):
    return {"type": "fill", "q": q, "a": list(answers)}


def choose(q, options, answer):
    return {"type": "choose", "q": q, "opts": list(options), "a": [answer]}


def tr(lt, *answers):
    return {"type": "translate", "q": lt, "a": list(answers)}


def order(sentence):
    return {"type": "order", "q": sentence, "a": [sentence]}


def topic(id, level, title_lt, focus_en, rule_lt, examples, items):
    return {"id": id, "level": level, "title": title_lt, "focus": focus_en,
            "rule": rule_lt, "examples": examples, "items": items}


TOPICS = [
    # ------------------------------------------------------------------ A1
    topic("a1_colors", "A1", "Spalvos", "colours (vocabulary)",
          "Spalvos angliškai: red – raudona, blue – mėlyna, green – žalia, yellow – geltona, "
          "pink – rožinė, purple – violetinė, black – juoda, white – balta, brown – ruda, grey – pilka.",
          ["My cat is black.", "I like pink and purple.", "The horse is brown."],
          [tr("raudona", "red"), tr("rožinė", "pink"), tr("violetinė", "purple"),
           tr("ruda", "brown"), choose("The sky is ___.", ["blue", "pink", "black"], "blue"),
           fill("Snow is ___. (balta)", "white"), choose("Grass is ___.", ["red", "green", "white"], "green")]),

    topic("a1_animals", "A1", "Gyvūnai", "animals (vocabulary)",
          "Gyvūnai angliškai: cat – katė, dog – šuo, horse – arklys, rat – žiurkė, "
          "bird – paukštis, fish – žuvis, rabbit – triušis, cow – karvė.",
          ["I have a dog.", "The horse is big.", "My rat is small."],
          [tr("arklys", "horse"), tr("žiurkė", "rat"), tr("šuo", "dog"), tr("paukštis", "bird"),
           choose("A ___ says 'meow'.", ["cat", "dog", "horse"], "cat"),
           tr("triušis", "rabbit"), fill("A ___ lives in water. (žuvis)", "fish")]),

    topic("a1_be", "A1", "am / is / are", "the verb to be: am / is / are",
          "Veiksmažodis „būti“ (to be): I am, you are, he / she / it is, we / they are. "
          "Pvz.: I am 13. She is my sister. They are my dogs.",
          ["I am happy.", "She is my sister.", "They are my cats."],
          [fill("I ___ 13 years old.", "am"), fill("My cat ___ black.", "is"),
           fill("We ___ friends.", "are"), choose("They ___ my sisters.", ["am", "is", "are"], "are"),
           fill("Pipsius ___ a rat.", "is"), order("My horse is big"),
           choose("You ___ my friend.", ["am", "is", "are"], "are")]),

    topic("a1_possessive_adj", "A1", "my / your / his / her", "possessive adjectives: my, your, his, her, our, their",
          "Kieno? my – mano, your – tavo, his – jo, her – jos, our – mūsų, their – jų. "
          "Pvz.: He is my father. His name is Andrius.",
          ["His name is Tom.", "Her cat is white.", "Our house is big."],
          [fill("He is my father. ___ name is Andrius.", "his"),
           fill("She is my sister. ___ name is Ana.", "her"),
           choose("I have a cat. ___ cat is grey.", ["My", "I", "Me"], "My"),
           fill("They have a dog. ___ dog is big. (jų)", "their"),
           tr("mano", "my"),
           choose("Is this ___ book, Tom?", ["you", "your", "he"], "your")]),

    topic("a1_family", "A1", "Šeima", "family words (vocabulary)",
          "Šeima angliškai: mother / mum – mama, father / dad – tėtis, sister – sesuo, "
          "brother – brolis, parents – tėvai, grandmother – močiutė, grandfather – senelis.",
          ["I have two sisters.", "My mum is kind.", "My dad is tall."],
          [tr("mama", "mother", "mum", "mom", "mummy"), tr("tėtis", "father", "dad", "daddy"),
           tr("sesuo", "sister"), tr("brolis", "brother"), tr("tėvai", "parents"),
           tr("močiutė", "grandmother", "granny", "grandma", "gran")]),

    topic("a1_articles", "A1", "a / an", "articles a and an",
          "Prieš vieną daiktą rašome a arba an. „an“ – kai žodis prasideda balse (a, e, i, o, u): "
          "an apple, an egg. Kitais atvejais – „a“: a cat, a horse.",
          ["I have a cat.", "This is an apple.", "It is an egg."],
          [fill("___ apple", "an"), fill("___ dog", "a"),
           choose("I have ___ orange.", ["a", "an"], "an"), choose("She has ___ horse.", ["a", "an"], "a"),
           fill("It is ___ elephant.", "an"), fill("This is ___ pencil.", "a")]),

    topic("a1_plurals", "A1", "Daugiskaita", "plural nouns: -s, -es, irregular plurals",
          "Kai daiktų daug, dažniausiai pridedame -s: cat – cats, dog – dogs. "
          "Po s, sh, ch, x pridedame -es: box – boxes. Išimtys: child – children, mouse – mice, man – men.",
          ["I have two cats.", "There are three boxes.", "The children are happy."],
          [fill("one cat, two ___", "cats"), fill("one box, three ___", "boxes"),
           fill("one horse, five ___", "horses"),
           choose("one child, two ___", ["childs", "children", "childes"], "children"),
           fill("one rat, many ___", "rats"), fill("one mouse, two ___", "mice")]),

    topic("a1_numbers", "A1", "Skaičiai", "numbers 1-20 (vocabulary)",
          "Skaičiai: one 1, two 2, three 3, four 4, five 5, six 6, seven 7, eight 8, nine 9, ten 10, "
          "eleven 11, twelve 12, thirteen 13, fourteen 14, fifteen 15, twenty 20.",
          ["I am thirteen.", "I have two sisters.", "I have three pets."],
          [tr("trylika", "thirteen", "13"), tr("septyni", "seven", "7"),
           fill("I have ___ sisters. (2)", "two"), tr("dvidešimt", "twenty", "20"),
           fill("5 + 5 = ___ (žodžiu)", "ten"), tr("dvylika", "twelve", "12")]),

    topic("a1_have", "A1", "have / has", "have / has for possession",
          "Turėti: I / you / we / they have, he / she / it has. "
          "Pvz.: I have a dog. She has two sisters. Klausimas: Do you have a cat?",
          ["I have a rat.", "She has a horse.", "We have a big house."],
          [fill("I ___ a cat.", "have"), fill("She ___ two sisters.", "has"),
           choose("My dog ___ big ears.", ["have", "has"], "has"), fill("We ___ a big house.", "have"),
           choose("___ you have a pet?", ["Do", "Does", "Are"], "Do"), order("He has a horse")]),

    topic("a1_this_that", "A1", "this / that / these / those", "this, that, these, those",
          "this – šis (arti, vienas), that – tas (toli, vienas), "
          "these – šie (arti, daug), those – tie (toli, daug).",
          ["This is my pen.", "That horse is fast.", "These are my cats."],
          [choose("___ is my pen. (arti, vienas)", ["This", "These"], "This"),
           choose("___ are my cats. (arti, daug)", ["This", "These"], "These"),
           fill("Look at ___ horse over there! (toli, vienas)", "that"),
           fill("___ dogs over there are big. (toli, daug)", "those"),
           choose("Is ___ your bag? (arti, vienas)", ["this", "these"], "this"),
           fill("___ are my books. (arti, daug)", "these")]),

    topic("a1_possessive_s", "A1", "Kieno? ('s)", "possessive 's (my father's name)",
          "Kieno daiktas? Pridedame 's: father's name – tėčio vardas, Ana's cat – Anos katė. "
          "Kai žodis jau baigiasi -s (parents), rašome tik apostrofą: my parents' house.",
          ["My father's name is Andrius.", "This is Ana's cat.", "My sister's bag is pink."],
          [fill("My ___ name is Andrius. (father)", "father's"),
           fill("This is ___ cat. (Ana)", "ana's"),
           choose("My ___ car is red.", ["mother", "mother's", "mothers"], "mother's"),
           order("My sister's name is Ema"),
           fill("It is the ___ toy. (dog)", "dog's"),
           choose("My ___ names are Rita and Tomas.", ["parents", "parents'", "parent"], "parents'")]),

    topic("a1_food", "A1", "Maistas", "food and drink (vocabulary)",
          "Maistas: apple – obuolys, bread – duona, milk – pienas, water – vanduo, "
          "cheese – sūris, ice cream – ledai, chicken – vištiena, cake – tortas.",
          ["I like ice cream.", "I drink milk.", "This apple is red."],
          [tr("obuolys", "apple", "an apple"), tr("duona", "bread"), tr("pienas", "milk"),
           tr("vanduo", "water"), tr("sūris", "cheese"), tr("ledai", "ice cream", "ice-cream")]),

    topic("a1_present_simple", "A1", "Esamasis laikas (I like / she likes)", "present simple, third person -s",
          "Esamasis paprastasis laikas – tai, kas vyksta dažnai ar visada. I / you / we / they like. "
          "He / she / it likes – pridedame -s! Pvz.: I like horses. She likes art.",
          ["I like horses.", "She likes art.", "My dog plays every day."],
          [fill("I ___ horses. (like)", "like"), fill("She ___ pizza. (like)", "likes"),
           choose("My dog ___ every day.", ["play", "plays"], "plays"),
           fill("They ___ to school. (go)", "go"), fill("He ___ TV. (watch)", "watches"),
           order("She likes art")]),

    topic("a1_present_neg_q", "A1", "don't / doesn't, Do...? / Does...?", "present simple negatives and questions",
          "Neiginys: I don't like… / He doesn't like… (po doesn't veiksmažodis be -s!). "
          "Klausimas: Do you like…? Does she like…?",
          ["I don't like milk.", "Does she like horses?", "He doesn't play football."],
          [fill("I ___ like milk. (ne)", "don't", "do not"),
           fill("She ___ like rats. (ne)", "doesn't", "does not"),
           choose("___ you like music?", ["Do", "Does"], "Do"),
           choose("___ he play Roblox?", ["Do", "Does"], "Does"),
           choose("She doesn't ___ fish.", ["like", "likes"], "like"),
           order("Do you like horses")]),

    topic("a1_school", "A1", "Mokykla", "school things (vocabulary)",
          "Mokykla: pencil – pieštukas, pen – rašiklis, book – knyga, teacher – mokytojas, "
          "bag – kuprinė, art – dailė, notebook – sąsiuvinis.",
          ["I like art.", "My bag is purple.", "This is my pencil."],
          [tr("pieštukas", "pencil", "a pencil"), tr("knyga", "book", "a book"),
           tr("mokytojas", "teacher", "a teacher"), tr("kuprinė", "bag", "backpack", "schoolbag", "school bag"),
           tr("dailė", "art"), tr("sąsiuvinis", "notebook", "exercise book")]),

    topic("a1_can", "A1", "can / can't", "can / can't for ability",
          "can – galiu, moku. can't – negaliu, nemoku. Po can veiksmažodis be -s: She can swim (ne „swims“). "
          "Klausimas: Can you draw?",
          ["I can draw.", "Horses can run fast.", "A fish can't walk."],
          [fill("I ___ draw. (galiu)", "can"), fill("A fish ___ walk. (negali)", "can't", "cannot", "can not"),
           choose("She can ___.", ["rides", "ride", "riding"], "ride"),
           choose("___ you swim?", ["Can", "Do", "Are"], "Can"),
           order("Horses can run fast"), fill("Birds ___ fly.", "can")]),

    topic("a1_there_is", "A1", "there is / there are", "there is / there are",
          "There is – yra (vienas daiktas). There are – yra (daug daiktų). "
          "Pvz.: There is a cat in the room. There are two dogs.",
          ["There is a horse in the field.", "There are three cats.", "Is there a dog?"],
          [fill("There ___ a horse in the field.", "is"), fill("There ___ three cats.", "are"),
           choose("There ___ two books on the table.", ["is", "are"], "are"),
           choose("There ___ an apple.", ["is", "are"], "is"),
           fill("___ there a dog in your house?", "is"), order("There is a bird")]),

    topic("a1_prepositions", "A1", "Kur? in / on / under", "prepositions of place: in, on, under, next to, behind",
          "Kur? in – viduje, on – ant, under – po, next to – šalia, behind – už.",
          ["The cat is in the box.", "The book is on the table.", "The dog is under the bed."],
          [choose("The cat is ___ the box. (viduje)", ["in", "on", "under"], "in"),
           choose("The book is ___ the table. (ant)", ["in", "on", "under"], "on"),
           choose("The dog is ___ the bed. (po)", ["in", "on", "under"], "under"),
           fill("The horse is ___ the tree. (šalia)", "next to"),
           fill("My bag is ___ the chair. (už)", "behind"), tr("ant", "on")]),

    topic("a1_days", "A1", "Savaitės dienos", "days of the week (vocabulary)",
          "Savaitės dienos: Monday – pirmadienis, Tuesday – antradienis, Wednesday – trečiadienis, "
          "Thursday – ketvirtadienis, Friday – penktadienis, Saturday – šeštadienis, Sunday – sekmadienis. "
          "Angliškai jas rašome iš didžiosios raidės.",
          ["Today is Monday.", "I play on Saturday.", "I like Friday."],
          [tr("pirmadienis", "monday"), tr("trečiadienis", "wednesday"), tr("penktadienis", "friday"),
           tr("šeštadienis", "saturday"), tr("sekmadienis", "sunday"), tr("antradienis", "tuesday")]),

    # ------------------------------------------------------------------ A2
    topic("a2_present_continuous", "A2", "Kas vyksta dabar? (-ing)", "present continuous: am/is/are + -ing",
          "Esamasis eigos laikas – kas vyksta DABAR: am / is / are + veiksmažodis su -ing. "
          "Pvz.: I am drawing. She is playing Roblox.",
          ["I am drawing now.", "She is reading.", "The horse is running."],
          [fill("I ___ drawing now.", "am"), fill("She is ___ a book now. (read)", "reading"),
           choose("They ___ playing now.", ["is", "are"], "are"),
           fill("The horse is ___. (run)", "running"),
           choose("Look! The cat ___.", ["sleeps", "is sleeping"], "is sleeping"),
           order("He is swimming")]),

    topic("a2_was_were", "A2", "was / were", "past of to be: was / were",
          "„Būti“ praeityje: I / he / she / it was, you / we / they were. "
          "Pvz.: I was at home yesterday. They were happy.",
          ["I was at home.", "We were tired.", "It was cold."],
          [fill("I ___ at school yesterday.", "was"), fill("We ___ tired.", "were"),
           choose("She ___ sick last week.", ["was", "were"], "was"),
           choose("The dogs ___ hungry.", ["was", "were"], "were"),
           fill("___ you at home yesterday?", "were"), fill("It ___ cold yesterday.", "was")]),

    topic("a2_past_regular", "A2", "Būtasis laikas (-ed)", "past simple of regular verbs (-ed)",
          "Būtasis laikas (taisyklingi veiksmažodžiai): pridedame -ed. play – played, watch – watched, "
          "like – liked. Pvz.: Yesterday I played Roblox.",
          ["Yesterday I played Roblox.", "She watched a film.", "We visited Granny."],
          [fill("Yesterday I ___ Roblox. (play)", "played"), fill("She ___ a film last night. (watch)", "watched"),
           fill("We ___ our grandmother. (visit)", "visited"),
           choose("I ___ my room yesterday.", ["clean", "cleaned"], "cleaned"),
           fill("He ___ to music. (listen)", "listened"), fill("They ___ in the park. (walk)", "walked")]),

    topic("a2_past_irregular", "A2", "Netaisyklingi veiksmažodžiai", "past simple of irregular verbs (went, ate, saw...)",
          "Netaisyklingi veiksmažodžiai turi savo formą: go – went, have – had, see – saw, eat – ate, "
          "make – made, do – did. Juos reikia išmokti mintinai.",
          ["I went to the shop.", "We ate pizza.", "She saw a horse."],
          [fill("Yesterday I ___ to the shop. (go)", "went"), fill("We ___ pizza. (eat)", "ate"),
           fill("She ___ a horse. (see)", "saw"), fill("I ___ a cake. (make)", "made"),
           choose("He ___ a dog when he was small.", ["have", "had", "haved"], "had"),
           fill("I ___ my homework. (do)", "did")]),

    topic("a2_past_neg_q", "A2", "didn't / Did...?", "past simple negatives and questions with did",
          "Neiginys praeityje: didn't + veiksmažodis be pakeitimų: I didn't go. "
          "Klausimas: Did you go? Po did veiksmažodis be -ed!",
          ["I didn't go to school.", "Did you see the film?", "She didn't watch TV."],
          [fill("I ___ go to school yesterday. (ne)", "didn't", "did not"),
           choose("___ you see the film?", ["Did", "Do", "Were"], "Did"),
           choose("She didn't ___ TV.", ["watch", "watched"], "watch"),
           fill("We didn't ___ pizza. (eat)", "eat"),
           choose("Did he ___ home?", ["go", "went"], "go"),
           order("Did you ride a horse")]),

    topic("a2_object_pronouns", "A2", "me / him / her / them", "object pronouns: me, you, him, her, us, them",
          "Ką? Kam? me – mane / man, you – tave / tau, him – jį / jam, her – ją / jai, us – mus, them – juos. "
          "Pvz.: I like her. Help me!",
          ["Help me, please!", "I like her.", "I love them."],
          [fill("Can you help ___? (man)", "me"), fill("I like ___. (jį)", "him"),
           fill("She loves ___. (juos)", "them"),
           choose("This is my sister. I love ___.", ["she", "her"], "her"),
           fill("Call ___ tomorrow! (mus)", "us"), choose("Give the book to ___.", ["I", "me"], "me")]),

    topic("a2_comparatives", "A2", "bigger / more beautiful", "comparatives: -er than / more ... than",
          "Lyginame du daiktus. Trumpi žodžiai: + -er + than: big – bigger than, fast – faster than. "
          "Ilgi žodžiai: more + žodis: more beautiful. Išimtys: good – better, bad – worse.",
          ["A horse is bigger than a dog.", "Art is more interesting than maths.", "Summer is better than winter."],
          [fill("A horse is ___ than a dog. (big)", "bigger"), fill("A cat is ___ than a rat. (fast)", "faster"),
           choose("This film is ___ than that film.", ["good", "better", "gooder"], "better"),
           fill("Art is ___ interesting than maths.", "more"),
           fill("My sister is ___ than me. (tall)", "taller"),
           choose("Winter is ___ than summer.", ["colder", "more cold"], "colder")]),

    topic("a2_superlatives", "A2", "the biggest / the best", "superlatives: the -est / the most / the best",
          "Pats didžiausias, geriausias: the + -est: the biggest, the fastest. "
          "Ilgi žodžiai: the most beautiful. Išimtys: good – the best, bad – the worst.",
          ["The elephant is the biggest animal.", "This is the best day!", "She is the tallest girl."],
          [fill("The elephant is ___ animal. (big)", "the biggest"),
           fill("This is ___ day of my life! (good)", "the best"),
           choose("She is ___ girl in the class.", ["the tallest", "the taller"], "the tallest"),
           fill("It is ___ beautiful horse.", "the most"),
           fill("Who is ___ in your family? (old)", "the oldest"),
           choose("This is ___ film ever!", ["the worst", "the baddest"], "the worst")]),

    topic("a2_some_any", "A2", "some / any", "some and any",
          "some – šiek tiek, keli (teigiamuose sakiniuose). any – kokių nors, jokių (klausimuose ir neiginiuose). "
          "Pvz.: I have some apples. Do you have any pets? I don't have any milk.",
          ["I have some apples.", "Do you have any pets?", "We don't have any milk."],
          [fill("I have ___ apples.", "some"), fill("Do you have ___ pets?", "any"),
           fill("We don't have ___ milk.", "any"),
           choose("There are ___ cats in the garden.", ["some", "any"], "some"),
           choose("Is there ___ water?", ["some", "any"], "any"), fill("She wants ___ water.", "some")]),

    topic("a2_going_to", "A2", "going to (planai)", "be going to for plans",
          "Planai ateičiai: am / is / are + going to + veiksmažodis. "
          "Pvz.: I am going to draw a horse. She is going to visit her grandmother.",
          ["I am going to draw a horse.", "We are going to play.", "She is going to ride."],
          [fill("I am ___ to watch a film.", "going"), fill("She ___ going to ride a horse.", "is"),
           choose("They are going ___ play Roblox.", ["to", "for"], "to"),
           fill("We are going to ___ pizza. (eat)", "eat"), order("I am going to draw"),
           fill("___ you going to come?", "are")]),

    topic("a2_frequency", "A2", "always / never / sometimes", "adverbs of frequency and their position",
          "Kaip dažnai? always – visada, usually – dažniausiai, often – dažnai, sometimes – kartais, "
          "never – niekada. Jie eina prieš veiksmažodį: I always play. Bet po am / is / are: She is never late.",
          ["I always feed my cat.", "I sometimes draw.", "She is never late."],
          [tr("niekada", "never"), tr("visada", "always"), tr("kartais", "sometimes"),
           fill("I ___ eat breakfast. (visada)", "always"), order("I always feed my cat"),
           order("She is never late")]),

    # ------------------------------------------------------------------ B1
    topic("b1_past_continuous", "B1", "was / were + -ing", "past continuous",
          "Būtasis eigos laikas: was / were + -ing – kas vyko tam tikru momentu praeityje. "
          "Pvz.: I was drawing when my mum called.",
          ["I was drawing at five.", "They were playing.", "She was sleeping."],
          [fill("I ___ drawing at 5 o'clock.", "was"), fill("They ___ playing when it started to rain.", "were"),
           fill("She was ___ when I came. (sleep)", "sleeping"),
           choose("We ___ watching TV.", ["was", "were"], "were"),
           choose("What ___ you doing at 8?", ["was", "were"], "were"),
           fill("The horse was ___ in the field. (run)", "running")]),

    topic("b1_present_perfect", "B1", "have + seen / done", "present perfect: have/has + past participle, ever",
          "Esamasis atliktinis laikas: have / has + trečioji forma (seen, been, done, eaten). "
          "Naudojame kalbėdami apie patirtį: I have seen this film. Have you ever ridden a horse?",
          ["I have seen this film.", "She has been to Riga.", "Have you ever ridden a horse?"],
          [fill("I have ___ this film. (see)", "seen"), fill("She ___ been to London.", "has"),
           choose("Have you ever ___ a horse?", ["rode", "ridden"], "ridden"),
           fill("We have ___ our homework. (do)", "done"), fill("___ you ever eaten sushi?", "have"),
           choose("He has ___ his phone.", ["lost", "lose"], "lost")]),

    topic("b1_will", "B1", "will / won't", "will for predictions, promises and quick decisions",
          "will – ateitis: spėjimai, pažadai, staigūs sprendimai. I will help you. It will rain tomorrow. "
          "Neiginys: won't (= will not).",
          ["I will help you.", "It will rain tomorrow.", "She won't come."],
          [fill("I think it ___ rain tomorrow.", "will"), fill("I ___ help you. (pažadas)", "will"),
           choose("She ___ come. She is sick.", ["will", "won't"], "won't"),
           choose("Will you ___ me?", ["help", "helps"], "help"), order("I will call you"),
           fill("They ___ be late. (nebus)", "won't", "will not")]),

    topic("b1_first_conditional", "B1", "If ..., ... will", "first conditional",
          "Pirmasis sąlygos sakinys: If + esamasis laikas, will + veiksmažodis. "
          "If it rains, I will stay at home. Po „if“ NErašome will!",
          ["If it rains, I will stay at home.", "If you study, you will pass.", "If I am tired, I will sleep."],
          [fill("If it ___, I will stay home. (rain)", "rains"),
           fill("If you study, you ___ pass the test.", "will"),
           choose("If she ___ the bus, she will be late.", ["miss", "misses", "will miss"], "misses"),
           fill("If we are hungry, we will ___ pizza. (eat)", "eat"),
           choose("If it is sunny, we ___ to the park.", ["go", "will go"], "will go"),
           order("If I am tired I will sleep")]),

    topic("b1_should_must", "B1", "should / must / mustn't", "should, must, mustn't",
          "should – patarimas (reikėtų): You should sleep more. must – privaloma: You must stop at a red light. "
          "mustn't – draudžiama: You mustn't run here.",
          ["You should sleep more.", "You must wear a helmet.", "You mustn't run here."],
          [fill("You look tired. You ___ go to bed. (patarimas)", "should"),
           fill("You ___ wear a helmet when you ride a horse. (privaloma)", "must"),
           choose("You ___ touch the fire! It is dangerous.", ["mustn't", "should"], "mustn't"),
           fill("You ___ eat more fruit. (patarimas)", "should"),
           choose("Students ___ listen to the teacher.", ["must", "mustn't"], "must"),
           fill("You ___ shout in the library. (draudžiama)", "mustn't", "must not")]),
]

TOPIC_BY_ID = {t["id"]: t for t in TOPICS}


def topics_up_to(max_level):
    allowed = LEVELS[: LEVELS.index(max_level) + 1]
    return [t for t in TOPICS if t["level"] in allowed]


# ---------------------------------------------------------------- diagnostic
# Each block is one level. The test stops early if a block goes badly,
# so a beginner never has to struggle through B1 questions.
def d(topic_id, item):
    item = dict(item)
    item["topic"] = topic_id
    return item


DIAGNOSTIC = [
    {"level": "A1", "stop_if_wrong": 5, "items": [
        d("a1_colors", tr("geltona", "yellow")),
        d("a1_animals", tr("arklys", "horse")),
        d("a1_be", choose("I ___ 13 years old.", ["am", "is", "are"], "am")),
        d("a1_possessive_adj", choose("He is my father. ___ name is Tom.", ["He", "His", "Her"], "His")),
        d("a1_articles", choose("It is ___ apple.", ["a", "an"], "an")),
        d("a1_plurals", choose("one cat, two ___", ["cat", "cats"], "cats")),
        d("a1_have", choose("She ___ a dog.", ["have", "has"], "has")),
        d("a1_present_simple", choose("My sister ___ music.", ["like", "likes"], "likes")),
        d("a1_present_neg_q", choose("___ you like pizza?", ["Do", "Does", "Are"], "Do")),
        d("a1_can", choose("I can ___.", ["swim", "swims", "swimming"], "swim")),
        d("a1_there_is", choose("There ___ three cats.", ["is", "are"], "are")),
        d("a1_prepositions", choose("The cat is ___ the box. (viduje)", ["in", "on", "under"], "in")),
    ]},
    {"level": "A2", "stop_if_wrong": 4, "items": [
        d("a2_present_continuous", choose("Look! She ___ now.", ["dances", "is dancing", "dance"], "is dancing")),
        d("a2_was_were", choose("We ___ at home yesterday.", ["was", "were"], "were")),
        d("a2_past_regular", fill("Yesterday I ___ Roblox. (play)", "played")),
        d("a2_past_irregular", choose("Yesterday we ___ to the zoo.", ["go", "went", "goed"], "went")),
        d("a2_past_neg_q", choose("___ you see the film yesterday?", ["Do", "Did", "Was"], "Did")),
        d("a2_comparatives", choose("A horse is ___ than a cat.", ["big", "bigger", "biggest"], "bigger")),
        d("a2_superlatives", choose("It is ___ day of the year!", ["the best", "the better", "the good"], "the best")),
        d("a2_going_to", choose("I am going ___ draw.", ["to", "for", "at"], "to")),
    ]},
    {"level": "B1", "stop_if_wrong": 3, "items": [
        d("b1_present_perfect", choose("I have ___ this film.", ["saw", "seen", "see"], "seen")),
        d("b1_will", choose("I think it ___ rain tomorrow.", ["will", "is", "does"], "will")),
        d("b1_first_conditional", choose("If it ___, we will stay at home.", ["rains", "will rain"], "rains")),
        d("b1_should_must", choose("You look tired. You ___ go to bed.", ["should", "mustn't", "can't"], "should")),
        d("b1_past_continuous", choose("I ___ drawing when you called.", ["was", "were", "am"], "was")),
        d("a2_some_any", choose("Do you have ___ pets?", ["some", "any"], "any")),
    ]},
]
