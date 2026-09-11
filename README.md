# Český editor s druhým názorem

Obecný skill pro přirozenější češtinu. Funguje samostatně v AI asistentovi; volitelný Python skript požádá o další redakci Gemini a porovná čísla a odkazy. Nejde o ověření faktů ani detektor AI.

## Začněte zde

Stáhněte celý repozitář přes **Code → Download ZIP**. Složku přejmenujte na `cestina-editor` a zkopírujte ji do `.claude/skills/` ve svém projektu (nebo `~/.claude/skills/` pro všechny projekty). Zachovejte skripty a příklady vedle SKILL.md. Potom napište:

> Použijte cestina-editor na tento text. Vykáme více čtenářům. Zachovejte význam a vypište podstatné změny: [váš text]

V jiném asistentovi přiložte SKILL.md a text; možnosti spouštění skriptů závisejí na prostředí.

## Bez API klíče

Python 3.10 nebo novější, bez dalších balíčků. Příkazy spouštějte ve složce tohoto repozitáře.

```sh
mkdir -p output
python3 scripts/review.py examples/vstup.txt --tone vykání --prompt-only --output output/zadani.txt
```

Zadání můžete předat druhému asistentovi sami. Ukázka `examples/odpoved.json` je ručně připravená a fiktivní, nikoli výsledek živého API testu. Offline kontrola:

```sh
python3 scripts/review.py examples/vstup.txt --check-response examples/odpoved.json --output output/kontrola.json
```

## Volitelně automaticky přes Gemini

Vytvořte vlastní klíč v [Google AI Studio](https://aistudio.google.com/apikey). Nastavte `GEMINI_API_KEY` bezpečně v prostředí a `GEMINI_MODEL` na model dostupný ve vašem účtu, který podporuje strukturovaný výstup. Klíč nedávejte do textu, příkazové historie ani Gitu. Skript nečte `.env` ani jiné projekty.

```sh
python3 scripts/review.py examples/vstup.txt --tone vykání --send-to-gemini --output output/gemini.json
```

Tento příkaz odešle **obsah vybraného souboru** službě Google a může čerpat placenou API kvótu. Posílejte jen text, který tam chcete zpracovat. Síťová cesta používá [Gemini generateContent](https://ai.google.dev/api/generate-content); model není pevně zadaný, protože dostupnost se mění.

Výstup obsahuje návrh textu, změny, otázky a `audit_warnings`. Kód ukončení 0 = dokončeno, 1 = chyba, 2 = uložený návrh vyžaduje kontrolu změněných čísel či odkazů. Existující soubory se nepřepisují. Kontrola nenajde všechny změny významu a může upozornit i na neškodnou úpravu formátu. Návrh vždy přečtěte.

## Ověření

```sh
python3 -m unittest discover -s tests -v
```

Testy používají pouze fiktivní texty a simulované API. Živý API přístup vyžaduje vlastní klíč; úspěch offline testu nedokládá dostupnost konkrétního modelu. Výstupy ukládejte do ignorované složky `output/`.
