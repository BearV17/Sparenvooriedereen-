# SparenVoorIedereen (SVI)

Schoolproject bij Capabel Onderwijs — **Blokopdracht 3.1**  
Opleiding Software developer: sparen bij de bank.

Systeem waarmee SparenVoorIedereen renteberekeningen uitvoert en spaarders hun geld kunnen beheren.

Startdatum systeem: **1 januari 2025**.

## Inhoud van de repo

```
docs/
  01_vragen_opdrachtgever.md
  02_business_requirements.md
  03_plan_van_aanpak.md
  04_functioneel_ontwerp.md
  05_technisch_ontwerp.md
  06_code_review.md
  07_reflectie_starr.md
src/
  bank.py              # startpunt (inloggen + menu)
  rente.py             # renteberekeningen en saldoklassen
  database.py          # SQLite-opslag
data/
  svi.db               # wordt automatisch aangemaakt
login.py               # oorspronkelijke inlog-oefening
```

## Starten

Vereist: Python 3.10 of hoger. Geen extra packages.

```bash
python3 src/bank.py
```

Demo-account (alleen voor testdoeleinden):

- gebruikersnaam: `admin`
- pincode: `1234`
- startsaldo: € 12.500,00

## Wat het systeem kan

- Inloggen (max. 3 pogingen)
- Geld storten en opnemen
- Saldo opvragen
- Opgebouwde rente dit kwartaal
- Verkregen rente dit jaar (t/m laatste kwartaal)
- Rente-overzicht laatste 12 maanden
- Transactieoverzicht (vanaf startdatum of eigen periode)
- Dagelijkse rente simuleren (handig voor testdata)

## Aannames (zie ook vragen aan opdrachtgever)

De saldoklasse-percentages uit de opdracht worden behandeld als **correctie** op de basisrente voor spaarders (1,80% per 1-1-2025).  
Boven € 1.000.000 wordt geen rente berekend.

Zie `docs/01_vragen_opdrachtgever.md` voor open punten.
