"""Drill exercises for every grammar point.
F: fill-in sentence with ___ (hint in brackets) | answer / other answer
T: Lithuanian sentence | English answer / other correct English answer"""

RAW = {
"freq": """
F: I ___ walk to school. (visada) | always
F: She is ___ late. (niekada) | never
F: We ___ play football after school. (dažnai) | often
F: My brother ___ reads comics. (kartais) | sometimes
F: They are ___ happy on Fridays. (paprastai) | usually
T: Aš visada valgau pusryčius. | I always eat breakfast. / I always have breakfast.
T: Jis niekada nežiūri televizoriaus. | He never watches TV. / He never watches television.
T: Mes dažnai einame į parką. | We often go to the park.
""",
"can": """
F: I ___ swim. (moku) | can
F: She ___ play the guitar. (nemoka) | can't / cannot
F: ___ you dance? (ar moki) | Can
F: Can you dive? – Yes, I ___. | can
F: Can he speak Spanish? – No, he ___. | can't / cannot
T: Aš moku šokti. | I can dance.
T: Ji nemoka nardyti. | She can't dive.
T: Ar tu moki groti gitara? | Can you play the guitar?
""",
"like_ing": """
F: I love ___. (dance) | dancing
F: My sister likes ___ books. (read) | reading
F: He doesn't like ___ up early. (get) | getting
F: We hate ___ in cold water. (swim) | swimming
F: I can't stand ___ sudoku. (do) | doing
T: Aš mėgstu šokti. | I like dancing. / I love dancing.
T: Mano brolis nemėgsta skaityti. | My brother doesn't like reading.
T: Mes labai mėgstame plaukti. | We love swimming.
""",
"what_like": """
F: What ___ your friend like? (is / does) | is
F: What ___ she look like? (is / does) | does
F: She's got ___ hair. (garbanoti) | curly
F: What is he like? – He's very ___. (draugiškas) | friendly
F: What does he look like? – He's got a ___. (barzda) | beard
T: Koks tavo draugas? | What's your friend like?
T: Kaip ji atrodo? | What does she look like?
T: Ji turi ilgus plaukus. | She's got long hair. / She has long hair.
""",
"pres_cont": """
F: I ___ reading a book now. (am / is / are) | am
F: She is ___ TV. (watch) | watching
F: They ___ playing football. (am / is / are) | are
F: We are ___ a cake. (make) | making
F: ___ you listening? (am / is / are) | Are
T: Aš dabar skaitau. | I'm reading now. / Now I'm reading.
T: Jis dabar žaidžia futbolą. | He's playing football now. / Now he's playing football.
T: Ką tu darai? | What are you doing?
""",
"there_is": """
F: There ___ a lamp on the desk. (is / are) | is
F: There ___ two beds in my room. (is / are) | are
F: ___ there a garage? (is / are) | Is
F: There ___ any posters. (isn't / aren't) | aren't
F: Are there any chairs? – Yes, there ___. | are
T: Mano kambaryje yra lova. | There's a bed in my room.
T: Virtuvėje yra dvi kėdės. | There are two chairs in the kitchen.
T: Ar yra vonia? | Is there a bath?
""",
"a_some_any": """
F: There's ___ armchair. (a / an) | an
F: There's ___ sofa. (a / an) | a
F: There are ___ books on the desk. (some / any) | some
F: Are there ___ posters? (some / any) | any
F: There aren't ___ pictures. (some / any) | any
T: Yra fotelis ir kelios kėdės. | There's an armchair and some chairs.
T: Ar yra plakatų? | Are there any posters?
T: Nėra lempos. | There isn't a lamp.
""",
"possessives": """
F: This is ___ bag. (mano) | my
F: The bag is ___. (mano) | mine
F: Is this ___ pen? (tavo) | your
F: Whose is it? – It's ___. (jos) | hers
F: That's ___ bike. (jo) | his
T: Tai mano knyga. | This is my book. / That is my book. / It is my book.
T: Kieno tai? | Whose is it? / Whose is this?
T: Tas dviratis yra jo. | That bike is his.
""",
"want": """
F: I ___ a new book. (want / wants) | want
F: She ___ to go to the pet shop. (want / wants) | wants
F: We want ___ go to the bookshop. | to
F: Do you ___ to come? (want / wants) | want
F: He doesn't want ___ play. | to
T: Aš noriu naujo kamuolio. | I want a new ball.
T: Ji nori eiti į knygyną. | She wants to go to the bookshop.
T: Ar nori eiti į parką? | Do you want to go to the park?
""",
"comp_short": """
F: An elephant is ___ than a giraffe. (big) | bigger
F: A snail is ___ than a snake. (slow) | slower
F: A giraffe is ___ than a horse. (tall) | taller
F: My cat is ___ than my dog. (small) | smaller
F: A buffalo is ___ than a lizard. (heavy) | heavier
T: Dramblys didesnis už žirafą. | An elephant is bigger than a giraffe. / The elephant is bigger than the giraffe.
T: Sraigė lėtesnė už gyvatę. | A snail is slower than a snake. / The snail is slower than the snake.
T: Žirafa aukštesnė už strutį. | A giraffe is taller than an ostrich. / The giraffe is taller than the ostrich.
""",
"sup_short": """
F: The cheetah is the ___ animal. (fast) | fastest
F: This is the ___ pet in the competition. (small) | smallest
F: The giraffe is the ___ animal. (tall) | tallest
F: My hamster is the ___. (cute) | cutest
F: This is the ___ snake. (long) | longest
T: Gepardas yra greičiausias gyvūnas. | The cheetah is the fastest animal.
T: Mano katė yra mažiausia. | My cat is the smallest.
T: Kuris gyvūnas yra didžiausias? | Which animal is the biggest?
""",
"qwords": """
F: ___ do bees live? (kur) | Where
F: ___ legs has a spider got? (kiek) | How many
F: ___ is your birthday? (kada) | When
F: ___ is your favourite insect? (koks) | What
F: ___ do you like butterflies? (kodėl) | Why
T: Kur gyvena skruzdėlės? | Where do ants live?
T: Kiek kojų turi voras? | How many legs has a spider got? / How many legs does a spider have?
T: Kas tai? | What is it? / What is this? / What is that?
""",
"comp_long": """
F: Skiing is ___ dangerous than skating. (labiau) | more
F: Scuba diving is the ___ exciting sport. (labiausiai) | most
F: This book is ___ than that one. (good) | better
F: Rowing is ___ than sailing. (difficult) | more difficult
F: This is the ___ day of my life! (bad) | worst
T: Buriavimas brangesnis už irklavimą. | Sailing is more expensive than rowing.
T: Tai įdomiausia sporto šaka. | It's the most exciting sport. / This is the most exciting sport.
T: Ledo ritulys geresnis už futbolą. | Ice hockey is better than football.
""",
"adverbs": """
F: The turtle walks ___. (slow) | slowly
F: The rabbit runs ___. (quick) | quickly
F: Please write ___. (careful) | carefully
F: She plays the guitar very ___. (good) | well
F: He runs very ___. (fast) | fast
T: Vėžlys eina lėtai. | The turtle walks slowly. / The turtle goes slowly.
T: Triušis bėga greitai. | The rabbit runs fast. / The rabbit runs quickly.
T: Ji gerai žaidžia. | She plays well.
""",
"past_be": """
F: She ___ a champion in 2020. (was / were) | was
F: We ___ at home yesterday. (was / were) | were
F: They ___ at school. (wasn't / weren't) | weren't
F: ___ he famous? (was / were) | Was
F: Were you happy? – Yes, I ___. | was
T: Vakar aš buvau namie. | I was at home yesterday. / Yesterday I was at home.
T: Jie buvo čempionai. | They were champions.
T: Ar tu buvai mokykloje? | Were you at school?
""",
"past_pos_neg": """
F: We ___ by train. (travel) | travelled / traveled
F: They ___ to the beach. (go) | went
F: I ___ go to the lake. (neiginys) | didn't
F: She ___ a boat on the river. (see) | saw
F: We ___ in a campsite. (stay) | stayed
T: Mes nuvykome į paplūdimį. | We went to the beach.
T: Aš nevažiavau traukiniu. | I didn't go by train. / I didn't travel by train.
T: Jie aplankė ūkį. | They visited a farm. / They visited the farm.
""",
"past_wh": """
F: Where ___ you go? (did / do) | did
F: What did they ___ at the club? (do) | do
F: When did she ___? (arrive) | arrive
F: ___ did you play? (ką) | What
F: Who did you ___ there? (meet) | meet
T: Kur tu nuėjai? | Where did you go?
T: Ką jūs veikėte? | What did you do?
T: Kada jie atvyko? | When did they arrive? / When did they come?
""",
"past_yn": """
F: ___ you pack your jeans? (did) | Did
F: Did she take a coat? – No, she ___. | didn't
F: Did you wear a hat? – Yes, I ___. | did
F: Did they ___ their boots? (bring) | bring
F: ___ he buy a T-shirt? (did) | Did
T: Ar tu susidėjai džinsus? | Did you pack your jeans?
T: Ar ji pasiėmė paltą? | Did she take a coat? / Did she take her coat?
T: Taip, pasiėmė. | Yes, she did.
""",
"pc_vs_ps": """
F: I usually ___ cereal for breakfast. (eat / am eating) | eat
F: Look! He ___ a pancake now. (eats / is eating) | is eating
F: We ___ soup every Monday. (have / are having) | have
F: What ___ you cooking now? (do / are) | are
F: She ___ meat. She's a vegetarian. (doesn't eat / isn't eating) | doesn't eat
T: Paprastai aš valgau sriubą. | I usually eat soup. / I usually have soup.
T: Dabar aš valgau blynus. | I'm eating pancakes now. / Now I'm eating pancakes. / I'm having pancakes now.
T: Ką tu dabar gamini? | What are you cooking now? / What are you making now?
""",
"past_irregular": """
F: We ___ some cheese. (eat) | ate
F: I ___ a souvenir. (buy) | bought
F: She ___ a photo. (take) | took
F: They ___ hot chocolate. (drink) | drank
F: He ___ a recipe. (write) | wrote
T: Mes nusipirkome suvenyrą. | We bought a souvenir.
T: Aš išgėriau karšto šokolado. | I drank hot chocolate. / I drank some hot chocolate.
T: Ji pagamino jogurtą. | She made a yoghurt. / She made yoghurt.
""",
"imperatives": """
F: ___ the eggs. (išmaišyk) | Mix
F: ___ the cheese. (sutarkuok) | Grate
F: ___ the salt. (įdėk) | Add
F: ___ open the oven! (nedaryk) | Don't
F: ___ the sugar. (pasverk) | Weigh
T: Supjaustyk obuolį. | Cut up the apple. / Cut the apple.
T: Nevalgyk masės! | Don't eat the mixture!
T: Įdėk jogurtą į dubenį. | Put the yoghurt in a bowl. / Put the yoghurt in the bowl.
""",
"have_got": """
F: I ___ got a big bedroom. (have / has) | have
F: She ___ got a sister. (have / has) | has
F: ___ you got a pet? (have / has) | Have
F: He ___ got a dog. (neiginys) | hasn't
F: Have they got a car? – Yes, they ___. | have
T: Aš turiu brolį. | I've got a brother. / I have a brother.
T: Ar tu turi šunį? | Have you got a dog? / Do you have a dog?
T: Ji neturi katės. | She hasn't got a cat. / She doesn't have a cat.
""",
"pronouns": """
F: I like ___. (jį) | him
F: She helps ___ every day. (mus) | us
F: Can you help ___? (man) | me
F: Is this surfboard yours? – Yes, it's ___. (mano) | mine
F: I can see ___. (juos) | them
T: Ji mums padeda. | She helps us.
T: Aš ją pažįstu. | I know her.
T: Ar ši knyga tavo? | Is this book yours? / Is this your book?
""",
"ps_freq": """
F: She usually ___ glasses. (wear) | wears
F: My friend ___ ever plays sport. (beveik niekada) | hardly
F: We ___ go to the cinema. (kartais) | sometimes
F: He ___ his teeth every morning. (brush) | brushes
F: I ___ late for school. (niekada nebūnu) | am never / 'm never
T: Ji paprastai nešioja akinius. | She usually wears glasses.
T: Mano draugas beveik niekada nesportuoja. | My friend hardly ever plays sport. / My friend hardly ever does sport.
T: Aš dažnai skaitau knygas. | I often read books.
""",
"ps_pc_stative": """
F: I ___ you. (understand / am understanding) | understand
F: We usually live in a city, but now we ___ in a tent. (live / are living) | are living
F: She ___ a new phone. (wants / is wanting) | wants
F: Look! They ___ in the rainforest. (walk / are walking) | are walking
F: Do you ___ the answer? (know / knowing) | know
T: Aš tave suprantu. | I understand you.
T: Aš ilgiuosi savo draugų. | I miss my friends.
T: Dabar mes gyvename palapinėje. | We're living in a tent now. / Now we're living in a tent.
""",
"past_regular": """
F: It ___ all day yesterday. (rain) | rained
F: We ___ at home. (stay) | stayed
F: The rain ___ at five o'clock. (stop) | stopped
F: I ___ to find my umbrella. (try) | tried
F: They ___ a film. (watch) | watched
T: Vakar visą dieną lijo. | It rained all day yesterday. / Yesterday it rained all day.
T: Mes likome namie. | We stayed at home. / We stayed home.
T: Jie žiūrėjo filmą. | They watched a film. / They watched a movie.
""",
"there_was": """
F: There ___ a storm last night. (was / were) | was
F: There ___ a lot of clouds. (was / were) | were
F: ___ there a rainbow? (was / were) | Was
F: There ___ any snow. (wasn't / weren't) | wasn't
F: Were there any people? – No, there ___. | weren't
T: Vakar buvo audra. | There was a storm yesterday. / Yesterday there was a storm.
T: Buvo daug debesų. | There were a lot of clouds. / There were lots of clouds. / There were many clouds.
T: Ar buvo vaivorykštė? | Was there a rainbow?
""",
"prep_time": """
F: It snowed ___ January. (in / on / at) | in
F: We met ___ Saturday. (in / on / at) | on
F: The film starts ___ seven o'clock. (in / on / at) | at
F: I get up early ___ the morning. (in / on / at) | in
F: My birthday is ___ the fifth of May. (in / on / at) | on
T: Sausį snigo. | It snowed in January.
T: Susitikome šeštadienį. | We met on Saturday.
T: Pamoka prasideda aštuntą valandą. | The lesson starts at eight o'clock. / The lesson begins at eight o'clock.
""",
"past_questions": """
F: ___ they find the tribe? (did) | Did
F: He ___ take any medicine. (neiginys) | didn't
F: Did you ___ the jungle? (see) | see
F: ___ they scared? (was / were) | Were
F: Did she help them? – Yes, she ___. | did
T: Ar jie rado gentį? | Did they find the tribe?
T: Jis negėrė vaistų. | He didn't take any medicine. / He didn't take the medicine.
T: Ar jūs bijojote? | Were you scared? / Were you frightened?
""",
"qwords_past": """
F: ___ did the earthquake happen? (kada) | When
F: It happened three years ___. (prieš) | ago
F: First we ran, ___ we hid. (tada) | then
F: ___ did they go? (kur) | Where
F: ___, we were safe. (galiausiai) | Finally
T: Kada tai įvyko? | When did it happen?
T: Prieš dvejus metus. | Two years ago.
T: Kur jūs buvote? | Where were you?
""",
"countables": """
F: I've got two ___. (banana) | bananas
F: There are three ___ in the bag. (potato) | potatoes
F: I'd like ___ apple. (a / an) | an
F: We need two ___. (tomato) | tomatoes
F: Can I have some ___, please? (rice / rices) | rice
T: Aš turiu du bananus. | I've got two bananas. / I have two bananas.
T: Pienas yra sveikas. | Milk is healthy. / Milk is good for you.
T: Aš noriu obuolio. | I want an apple. / I'd like an apple.
""",
"some_any": """
F: Can I have ___ juice, please? (some / any) | some
F: There isn't ___ cheese. (some / any) | any
F: Have you got ___ eggs? (some / any) | any
F: I bought ___ bread. (some / any) | some
F: We haven't got ___ milk. (some / any) | any
T: Mes neturime duonos. | We haven't got any bread. / We don't have any bread.
T: Ar turi kiaušinių? | Have you got any eggs? / Do you have any eggs?
T: Aš nupirkau sūrio. | I bought some cheese.
""",
"how_much": """
F: How ___ sugar do you eat? (much / many) | much
F: How ___ apples are there? (much / many) | many
F: I don't eat ___ sweets. (much / many) | many
F: There isn't ___ water. (much / many) | much
F: She drinks a ___ of milk. (daug) | lot
T: Kiek obuolių tu turi? | How many apples have you got? / How many apples do you have?
T: Kiek vandens tu išgeri? | How much water do you drink?
T: Aš valgau daug vaisių. | I eat a lot of fruit. / I eat lots of fruit.
""",
"will_future": """
F: People ___ have robots at home. (will / won't) | will
F: We ___ use keyboards. (neiginys) | won't
F: ___ we live on Mars? (will) | Will
F: I think it ___ rain tomorrow. (will / won't) | will
F: Will cars fly? – No, they ___. | won't
T: Žmonės turės robotus. | People will have robots.
T: Mes nenaudosime klaviatūrų. | We won't use keyboards.
T: Ar rytoj lis? | Will it rain tomorrow?
""",
"going_to": """
F: I'm ___ to make a video. (go) | going
F: She ___ going to buy a drone. (am / is / are) | is
F: ___ they going to play? (am / is / are) | Are
F: We are going ___ visit our grandparents. | to
F: I'm not going ___ watch TV. | to
T: Aš ketinu sukurti vaizdo įrašą. | I'm going to make a video.
T: Ar jie ketina pirkti droną? | Are they going to buy a drone?
T: Ji ketina žaisti futbolą. | She's going to play football.
""",
"will_decisions": """
F: It's dark. I ___ switch on the light. (will) | will / 'll
F: I'm thirsty. – I ___ get you some water. (will) | will / 'll
F: The phone is ringing. I ___ answer it. (will) | will / 'll
F: I ___ play the next level! (will) | will / 'll
F: It's cold. I ___ close the window. (will) | will / 'll
T: Įjungsiu šviesą. | I'll switch on the light. / I'll turn on the light.
T: Aš tau padėsiu. | I'll help you.
T: Žaisiu kitą lygį. | I'll play the next level.
""",
"comp_all": """
F: The tower is ___ than the cathedral. (tall) | taller
F: The museum is ___ than the park. (interesting) | more interesting
F: The park isn't ___ big as the stadium. | as
F: The bridge is as old ___ the palace. | as
F: This square is ___ than that one. (beautiful) | more beautiful
T: Bokštas aukštesnis už katedrą. | The tower is taller than the cathedral.
T: Parkas nėra toks didelis kaip stadionas. | The park isn't as big as the stadium.
T: Muziejus įdomesnis už parką. | The museum is more interesting than the park.
""",
"sup_all": """
F: This is the ___ hill. (high) | highest
F: It's the ___ view. (beautiful) | most beautiful
F: This is the ___ day of the holiday! (good) | best
F: The village is the ___ place. (quiet) | quietest
F: That was the ___ film. (bad) | worst
T: Tai aukščiausia kalva. | This is the highest hill. / It's the highest hill.
T: Tai gražiausias vaizdas. | It's the most beautiful view. / This is the most beautiful view.
T: Kuri vieta geriausia? | Which place is the best?
""",
"articles": """
F: There's ___ aquarium near the port. (a / an) | an
F: There's a café. ___ café is next to the bank. (A / The) | The
F: Look at ___ moon! (a / the) | the
F: I saw ___ dolphin in the harbour. (a / an) | a
F: My uncle is ___ engineer. (a / an) | an
T: Netoli uosto yra akvariumas. | There's an aquarium near the port.
T: Akvariumas yra priešais rotušę. | The aquarium is opposite the town hall.
T: Mano mama yra mokytoja. | My mum is a teacher. / My mother is a teacher.
""",
"should": """
F: You ___ switch off your phone. (reikėtų) | should
F: You ___ sleep in. (nereikėtų) | shouldn't
F: ___ I wear a coat? (should) | Should
F: He should ___ to bed early. (go) | go
F: We ___ eat so many sweets. (nereikėtų) | shouldn't
T: Tau reikėtų išjungti telefoną. | You should switch off your phone. / You should turn off your phone.
T: Tau nereikėtų pramiegoti. | You shouldn't sleep in.
T: Ką man reikėtų daryti? | What should I do?
""",
"must": """
F: You ___ cross the road carefully. (privalai) | must
F: You ___ feed the animals. (negalima) | mustn't
F: We ___ be quiet in the library. (privalome) | must
F: You ___ run near the pool. (negalima) | mustn't
F: Students must ___ their homework. (do) | do
T: Tu privalai būti atsargus. | You must be careful.
T: Negalima šerti gyvūnų. | You mustn't feed the animals.
T: Mes privalome eiti lėtai. | We must walk slowly. / We must go slowly.
""",
"have_to": """
F: I ___ to tidy my room. (have / has) | have
F: She ___ to get up early. (have / has) | has
F: We don't ___ to wear a uniform. | have
F: He ___ have to do homework today. (neiginys) | doesn't
F: Do you have ___ go now? | to
T: Man reikia susitvarkyti kambarį. | I have to tidy my room.
T: Mums nebūtina dėvėti uniformos. | We don't have to wear a uniform.
T: Ar tau reikia anksti keltis? | Do you have to get up early?
""",
}


def parse():
    ex = {}
    for gid, block in RAW.items():
        items = []
        for line in block.strip().splitlines():
            kind, rest = line.split(": ", 1)
            q, answers = rest.split(" | ")
            a = [x.strip() for x in answers.split(" / ")]
            if kind == "F":
                items.append({"type": "fill", "q": q.strip(), "a": a})
            else:
                items.append({"type": "translate", "lt": q.strip(), "a": a})
        ex[gid] = items
    return ex


EX = parse()
