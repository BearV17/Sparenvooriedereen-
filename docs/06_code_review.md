# Code-review

Beoordeling van de eigen component en van het werk van een teamgenoot, zoals gevraagd in deel 4.

## Reviewchecklist

- Werkt de code zoals bedoeld?
- Is de code duidelijk en goed gestructureerd?
- Zijn er verbeteringen mogelijk?

---

## Review op `login.py` (bestaande startcode)

**Reviewer:** teamgenoot  
**Datum:** sprint deel 4

### Wat werkt

- Loop stopt bij succes (`break`).
- Pogingen worden afgeteld tot 3.
- Duidelijke meldingen in het Nederlands.

### Verbeterpunten (doorgevoerd in `src/bank.py`)

1. Pincode stond in platte tekst in de bron. Nu hash in de database.
2. Gebruikersgegevens hard coded; nu tabel `klant`.
3. Na inloggen gebeurde nog niets. Nu volgt het bankmenu.
4. Geen scheiding tussen UI en data. Nu `bank.py` / `database.py` / `rente.py`.

### Aanpassingen na review

- Inloggen gekoppeld aan SQLite.
- Max. 3 pogingen behouden.
- Sessie bewaart `klant_id` en `rekening_id` zodat overzichten alleen eigen data tonen.

---

## Review op rentemodule (`src/rente.py`)

**Reviewer:** teamgenoot

| Criterium        | Oordeel | Opmerking                                      |
|------------------|---------|------------------------------------------------|
| Werkt zoals bedoeld | Ja    | Klassengrenzen en schrikkeljaar gedekt         |
| Structuur        | Ja      | Pure functies, makkelijk te testen             |
| Verbetering      | Wens    | Later: Decimal i.p.v. float voor geld          |

Feedback verwerkt: grenzen documenteren (`10_000` hoort bij de tweede klasse: ondergrens inclusief, bovengrens exclusief behalve de laatste).

---

## Reviewformulier (leeg, voor inleveren eigen teamgenoot)

- Reviewer:
- Bestand / component:
- Werkt de code zoals bedoeld?
- Is de code duidelijk en gestructureerd?
- Verbeterpunten:
- Aanpassingen doorgevoerd: ja / nee
