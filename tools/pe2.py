"""Project Explore 2 – lessons (code, title, Lithuanian title, grammar ids, words 'english = lietuviškai')."""

LESSONS = [
("Intro A", "Moving house", "Persikraustymas", ["have_got", "like_ing"], """
box – boxes = dėžė – dėžės
family – families = šeima – šeimos
shelf – shelves = lentyna – lentynos
person – people = žmogus – žmonės
child – children = vaikas – vaikai
man – men = vyras – vyrai
woman – women = moteris – moterys
tooth – teeth = dantis – dantys
foot – feet = pėda – pėdos
flight = skrydis
front door = lauko durys
leave = išvykti
visitor = svečias
I can't stand … = Negaliu pakęsti …
Finally! = Pagaliau!
I hope so. = Tikiuosi.
Ooh, exciting! = Oho, kaip įdomu!
Weird! = Keista!
"""),
("Intro B", "Neighbours", "Kaimynai", ["can", "pronouns"], """
January = sausis
February = vasaris
March = kovas
April = balandis
May = gegužė
June = birželis
July = liepa
August = rugpjūtis
September = rugsėjis
October = spalis
November = lapkritis
December = gruodis
first = pirmas
second = antras
third = trečias
twentieth = dvidešimtas
twenty-first = dvidešimt pirmas
surf = plaukti banglente
surfboard = banglentė
cook a meal = gaminti valgį
play squash = žaisti skvošą
I guess so. = Turbūt taip.
"""),
("1A", "New friends", "Nauji draugai", ["ps_freq"], """
tall = aukštas
quite tall = gana aukštas
medium height = vidutinio ūgio
quite small = gana žemas
long = ilgas
medium length = vidutinio ilgio
straight = tiesus
wavy = banguotas
curly = garbanotas
dark = tamsus
fair = šviesus
freckles = strazdanos
glasses = akiniai
beard = barzda
tan = įdegis
smile = šypsena
friendly = draugiškas
funny = juokingas
kind = geras, malonus
nice = mielas
clever = protingas
sporty = sportiškas
hardly ever = beveik niekada
"""),
("1B", "New school", "Nauja mokykla", ["pres_cont"], """
art = dailė
biology = biologija
chemistry = chemija
English = anglų kalba
geography = geografija
history = istorija
IT = informacinės technologijos
maths = matematika
PE = kūno kultūra
physics = fizika
timetable = tvarkaraštis
coursebook = vadovėlis
notebook = sąsiuvinis
dictionary = žodynas
pen = rašiklis
ruler = liniuotė
ring binder = segtuvas
paint = dažai
tablet = planšetė
clock = laikrodis
bookshelf = knygų lentyna
pinboard = skelbimų lenta
projector = projektorius
interactive whiteboard = interaktyvi lenta
waste-paper basket = šiukšlių dėžė
"""),
("1C", "New home", "Nauji namai", ["ps_pc_stative"], """
know = žinoti
understand = suprasti
believe = tikėti
need = reikėti
want = norėti
miss = ilgėtis
huge = didžiulis
amazing = nuostabus
rainforest = atogrąžų miškas
wildlife = laukinė gamta
way of life = gyvenimo būdas
"""),
("1D", "Getting on", "Sutariame", [], """
Can I …? = Ar galiu …?
Could I …? = Ar galėčiau …?
May I …, please? = Ar galėčiau …? (labai mandagiai)
Go right ahead. = Prašom, pirmyn.
Of course. = Žinoma.
Sure. = Žinoma.
No problem. = Jokių problemų.
I'm sorry, no. = Atsiprašau, ne.
I'm sorry, that's not possible. = Atsiprašau, tai neįmanoma.
Want to join us? = Nori prisijungti?
Can I tag along? = Ar galiu eiti kartu?
A little bit. = Truputį.
Awesome! = Šaunu!
"""),
("2A", "What's the weather like?", "Koks oras?", ["past_regular", "there_was", "prep_time"], """
sunny = saulėta
cloudy = debesuota
windy = vėjuota
foggy = rūkas, rūkuota
stormy = audringa
wet = lietinga, šlapia
hot = karšta
warm = šilta
cold = šalta
freezing = labai šalta
to rain = lyti
to snow = snigti
hailing = kruša
rainbow = vaivorykštė
yesterday = vakar
last week = praeitą savaitę
"""),
("2B", "The lost tribe", "Pasiklydusi gentis", ["past_be", "past_irregular", "past_questions"], """
tribe = gentis
jungle = džiunglės
thunderstorm = perkūnija
frightened = išsigandęs
be scared = bijoti
illness = liga
medicine = vaistai
take care of = rūpintis
translator = vertėjas
freedom = laisvė
improve = pagerinti
"""),
("2C", "Young survivors", "Jaunieji išgyvenusieji", ["qwords_past"], """
avalanche = lavina
earthquake = žemės drebėjimas
flood = potvynis
hurricane = uraganas
lightning = žaibas
snowstorm = pūga
tornado = tornadas
tsunami = cunamis
volcanic eruption = ugnikalnio išsiveržimas
survive = išgyventi
ago = prieš (laiką)
then = tada
after that = po to
later = vėliau
finally = galiausiai
"""),
("2D", "It all went wrong!", "Viskas nepavyko!", [], """
Oh no! = O ne!
Bad luck! = Nepasisekė!
Poor you! = Vargšelis!
Never mind! = Nieko tokio!
It really doesn't matter. = Tai visai nesvarbu.
Sorry about that. = Atsiprašau dėl to.
That's a real shame! = Labai gaila!
It's not funny! = Nejuokinga!
Exactly! = Būtent!
brave = drąsus
mud = purvas
sleeping bag = miegmaišis
"""),
("3A", "Food and drink", "Maistas ir gėrimai", ["countables"], """
banana = bananas
grape = vynuogė
strawberry = braškė
carrot = morka
potato = bulvė
tomato = pomidoras
egg = kiaušinis
cheese = sūris
chicken = vištiena
fish = žuvis
ham = kumpis
lamb = ėriena
pasta = makaronai
rice = ryžiai
sandwich = sumuštinis
crisps = traškučiai
chocolate = šokoladas
milk = pienas
tea = arbata
coffee = kava
fruit juice = vaisių sultys
lemonade = limonadas
cola = kola
"""),
("3B", "Going shopping", "Apsipirkimas", ["some_any"], """
a bag of = maišelis
a bar of = plytelė, batonėlis
a bowl of = dubenėlis
a box of = dėžutė
a can of = skardinė
a carton of = pakelis (kartoninis)
a cup of = puodelis
a glass of = stiklinė
a kilo of = kilogramas
a loaf of = kepalas
a packet of = pakelis
a plate of = lėkštė
a pot of = indelis
a slice of = riekė
a tin of = konservų skardinė
"""),
("3C", "Eating well", "Sveikai maitinamės", ["how_much"], """
healthy = sveikas
unhealthy = nesveikas
snack = užkandis
cereal = dribsniai
smoothie = vaisių kokteilis
soft drink = gaivusis gėrimas
fizzy = gazuotas
sugary = su daug cukraus
home-made = naminis
portion = porcija
regularly = reguliariai
skip breakfast = praleisti pusryčius
"""),
("3D", "Eating out", "Valgome ne namie", [], """
Can you …? = Ar gali …?
Could you …, please? = Ar galėtum …, prašau?
Happy to. = Mielai.
No, I can't. I'm sorry. = Ne, negaliu. Atsiprašau.
Sorry, I can't at the moment. = Atsiprašau, dabar negaliu.
Sounds good! = Skamba gerai!
Like what? = Pavyzdžiui?
barbecue = kepsninė, iškyla su kepsniais
"""),
("4A", "Online", "Internete", ["will_future"], """
go online = prisijungti prie interneto
Wi-Fi = belaidis internetas
wireless router = belaidis maršrutizatorius
laptop = nešiojamasis kompiuteris
keyboard = klaviatūra
printer = spausdintuvas
scanner = skeneris
camera = kamera
charger = kroviklis
touchscreen = jutiklinis ekranas
games console = žaidimų konsolė
password = slaptažodis
download = atsisiųsti
upload = įkelti
post = paskelbti
blog = tinklaraštis
vlog = vaizdo tinklaraštis
social media site = socialinis tinklas
virus = virusas
"""),
("4B", "Great ideas", "Puikios idėjos", ["going_to"], """
smartphone = išmanusis telefonas
smartwatch = išmanusis laikrodis
earphones = ausinukai
e-reader = elektroninė skaityklė
drone = dronas
3D printer = 3D spausdintuvas
electric car = elektromobilis
driverless car = savavaldis automobilis
virtual reality headset = virtualios realybės akiniai
gadget = prietaisas
invention = išradimas
inventor = išradėjas
"""),
("4C", "Computer games", "Kompiuteriniai žaidimai", ["will_decisions"], """
character = veikėjas
mission = misija
decision = sprendimas
level = lygis
boss = bosas
shield = skydas
laser = lazeris
hide = slėptis
remote control = nuotolinio valdymo pultas
hard drive = kietasis diskas
"""),
("4D", "First-time vlogger", "Pirmasis vaizdo įrašas", [], """
Can I help you? = Ar galiu tau padėti?
I'll help you with that. = Aš tau padėsiu.
Let me help you with that. = Leisk man padėti.
Sure, we'll help. = Žinoma, padėsime.
That's great, thanks! = Puiku, ačiū!
That's really kind of you. = Labai malonu iš tavo pusės.
Why don't you ask Mike to help? = Kodėl nepaprašai Mike'o pagalbos?
You should … = Tau reikėtų …
All set, everyone? = Visi pasiruošę?
And … action! = Ir … veiksmas!
"""),
("5A", "In the city", "Mieste", ["comp_all"], """
art gallery = meno galerija
bridge = tiltas
cathedral = katedra
clock = laikrodis
fountain = fontanas
monument = paminklas
museum = muziejus
palace = rūmai
park = parkas
river = upė
square = aikštė
stadium = stadionas
station = stotis
statue = statula
tower = bokštas
tunnel = tunelis
"""),
("5B", "In the country", "Kaime", ["sup_all"], """
hill = kalva
field = laukas
village = kaimas
farm = ūkis
forest = miškas
harbour = uostas
dolphin = delfinas
view = vaizdas
far = toli
ordinary = paprastas
"""),
("5C", "Out and about", "Po miestą", ["articles"], """
behind = už
between = tarp
in front of = priešais
in the middle of = viduryje
near = netoli
next to = šalia
on the corner = ant kampo
opposite = priešais (kitoje pusėje)
over = virš
through = per, pro
aquarium = akvariumas
newsagent's = spaudos kioskas
tourist office = turizmo informacijos centras
town hall = rotušė
port = uostas
"""),
("5D", "A tour of the city", "Ekskursija po miestą", [], """
Excuse me, how do I find the nearest …? = Atsiprašau, kaip rasti artimiausią …?
Excuse me, could you tell me how to get to …, please? = Atsiprašau, gal galite pasakyti, kaip nueiti iki …?
Go up this street. = Eikite šia gatve.
Turn left at the end of the road. = Gatvės gale sukite į kairę.
Turn right. = Sukite į dešinę.
Can you see that … over there? = Ar matote tą … ten?
Certainly. = Žinoma.
Thanks a lot. = Labai ačiū.
You're welcome. = Prašom.
I'm not from around here. = Aš ne vietinis.
Thanks anyway! = Vis tiek ačiū!
Easy peasy. = Vieni niekai.
"""),
("6A", "Problems", "Problemos", ["should"], """
wake up = pabusti
sleep in = ilgiau pamiegoti
look at = žiūrėti į
look for = ieškoti
pick up = pakelti
put down = padėti
put on = užsidėti, apsivilkti
take off = nusiimti, nusivilkti
switch on = įjungti
switch off = išjungti
turn up = pagarsinti
turn down = pritildyti
advice = patarimas
"""),
("6B", "Rules", "Taisyklės", ["must"], """
quickly = greitai
slowly = lėtai
loudly = garsiai
quietly = tyliai
happily = laimingai
sadly = liūdnai
nicely = gražiai
badly = blogai
carefully = atsargiai
carelessly = neatsargiai
safely = saugiai
dangerously = pavojingai
well = gerai
fast = greitai
cross the road = pereiti gatvę
feed the animals = šerti gyvūnus
rule = taisyklė
"""),
("6C", "Dilemmas", "Dilemos", ["have_to"], """
dilemma = dilema
tidy my room = susitvarkyti kambarį
do homework = daryti namų darbus
wear a uniform = dėvėti uniformą
get up early = anksti keltis
rucksack = kuprinė
engine = variklis
breathe = kvėpuoti
"""),
("6D", "Go on. Give it a try!", "Nagi, pabandyk!", [], """
Come on, you can do it. = Nagi, tu gali!
Don't give up! = Nepasiduok!
Go on. Give it a try. = Pirmyn, pabandyk.
I think you should do it. = Manau, kad turėtum tai padaryti.
What have you got to lose? = Ką tu prarasi?
You really must do it. = Tu būtinai turi tai padaryti.
I'll think about it. = Pagalvosiu.
See? I told you! = Matai? Sakiau!
Too late! = Per vėlu!
embarrassed = susigėdęs
presentation = pristatymas
raincoat = lietpaltis
"""),
]
