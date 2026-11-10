# William – anglų kalbos treniruoklis (Project Explore)

Katinas William padeda lietuviams mokiniams treniruoti anglų kalbą. Du kursai pagal *Project Explore 1* ir
*Project Explore 2* (Oxford): 53 vadovėlio pamokos, padalytos į trumpas dalis (ne daugiau kaip 8 žodžiai),
žodžiai ir frazės su vertimu į lietuvių kalbą, gramatika paaiškinta lietuviškai.

## Kaip vyksta pamoka
1. Pamokos kortelė: nauji žodžiai ir gramatika (🔊 – paklausyti, kaip skamba).
2. William trumpai lietuviškai pristato pamoką.
3. Pratimai: du žodžiai → sakinys su jais → dar du žodžiai → sakinys … , tada „įrašyk, kas trūksta“
   ir sakinio vertimas. Kartais vietoj žodžio – diktantas.
   Atsakymus tikrina programa: žodžius, didžiąsias raides, skyrybos ženklus ir apostrofus.
   Jei klaida tikra (pvz., *like / likes*), William lietuviškai paaiškina kodėl.
4. Mygtukai: 💡 Užuomina, 🤷 Nežinau, 🔊 Klausyti.
5. Pabaigoje dar kartą kartojami nepavykę pratimai ir parodomas rezultatas.

Taškų skaitiklis šalia Williamo: už kiekvieną teisingą atsakymą +1, pasiekus 5/5 William apsiverčia ore.
William prisistato tik pirmą kartą (adreso gale `?new` – prisistatys iš naujo).

## Mokytojui (⚙ viršuje dešinėje)
- Režimas: **Pratimai** arba **Pokalbis su Williamu**.
- Kokie pratimai, kiek jų, ar tikrinti didžiąsias raides ir skyrybą, ar ištarti atsakymą balsu.
- **Nurodymas Williamui**, pvz., „spalvos su present simple“ – William sukurs papildomų pratimų šia tema.
Nustatymai išsaugomi šiame kompiuteryje.

## Paleisti (GitHub Codespaces)
1. Pridėk modelio raktą kaip Codespaces paslaptį `LLM_API_KEY`
   (GitHub → Settings → Codespaces → Secrets) ir leisk šiam repozitorijui ją naudoti.
2. Codespace terminale:
   ```
   pip install -r requirements.txt
   uvicorn app:app --reload --port 8000
   ```
3. Atidaryk 8000 prievadą skiltyje **Ports**.

## Sandara
- `app.py` – serveris. `checker.py` – tikrina atsakymus. `drills.py` – sudaro pratimus.
- `static/` – puslapis.
- `course/project-explore-1.json`, `course/project-explore-2.json` – kursai.
- `tools/` – kursų duomenys (žodžiai, gramatika, pratimai). Pakeitus juos: `python tools/build_pe.py course`.
- `CHANGELOG.md` – kas ir kada pakeista, ką dar reikia padaryti.

Niekada nekelk vadovėlių PDF ar `.env` failo su raktu į GitHub.
