# Technisch ontwerp — SparenVoorIedereen

Max. 2–3 A4. Indeling volgens Software developer, hoofdstuk 4.5.

## 1. Inleiding

Dit document beschrijft hoe het functioneel ontwerp technisch wordt gerealiseerd: gegevensopslag, componenten, kernberekeningen en beveiliging. Implementatie: Python 3 + SQLite.

## 2. Onderdelen van het systeem

| Component     | Bestand        | Verantwoordelijkheid                          |
|---------------|----------------|-----------------------------------------------|
| Presentatie   | `src/bank.py`  | Inloggen, menu, invoervalidatie, uitvoer      |
| Domein        | `src/rente.py` | Saldoklasse, dag-/kwartaal-/jaarRente         |
| Persistentie  | `src/database.py` | Tabellen, queries, demo-data               |
| Database      | `data/svi.db`  | SQLite-bestand                                |

Stroom: gebruiker → `bank.py` → `database.py` / `rente.py` → SQLite.

## 3. Databaseschema

```
klant (id PK, naam, gebruikersnaam UNIQUE, pincode_hash, aangemaakt_op)
        |
        | 1-1
        v
rekening (id PK, klant_id FK, iban UNIQUE, saldo, geopend_op)
        |
        | 1-n
        +---> transactie (id PK, rekening_id FK, type, bedrag, saldo_na, omschrijving, datum)
        |
        +---> rente_dag (id PK, rekening_id FK, datum, saldo, percentage, bedrag)
                         UNIQUE (rekening_id, datum)

tarief (id PK, geldig_vanaf UNIQUE, bank_pct, spaarder_pct)
```

Relaties: een klant heeft één rekening; een rekening heeft veel transacties en veel dagrentes. Tarieven zijn historisch: de rij met de hoogste `geldig_vanaf` ≤ de rekeningsdatum geldt.

## 4. Belangrijke berekeningen

### 4.1 Effectief rentepercentage

```
basis = spaarderspercentage op die dag          # 1-1-2025: 1,80
correctie = klasse_correctie(saldo)
als saldo > 1_000_000: effectief = 0
anders: effectief = basis + correctie
```

Klassen: 0–10k −0,25; 10–25k 0; 25–50k −0,15; 50–100k −0,25; 100k–1M −0,50.

### 4.2 Dagelijkse rente

```
dagen = 366 als schrikkeljaar(jaar) anders 365
dag_rente = saldo × (effectief / 100) / dagen
```

Afgerond op 2 decimalen bij tonen; intern 4 decimalen om optelfouten per kwartaal te beperken.

### 4.3 Kwartaal- en jaarrente

Kwartaal Q1=jan–mrt, Q2=apr–jun, Q3=jul–sep, Q4=okt–dec.  
Rente dit kwartaal = som `rente_dag` in het lopende kwartaal.  
Rente dit jaar t/m laatste kwartaal = som bijgeschreven rentetransacties in afgesloten kwartalen van het jaar.  
12 maanden = som per kalendermaand over de laatste 12 volle maanden t.o.v. de testdatum.

## 5. Beveiligingsmaatregelen

- **Toegangscontrole:** sessie pas na juiste combinatie gebruikersnaam + pincode. Maximaal 3 pogingen; daarna geen menu.
- **Opslag pincode:** SHA-256-hash, geen platte tekst in de database. (Productie: beter Argon2/bcrypt + salt; hier bewust eenvoudig voor de opleiding.)
- **SQL:** uitsluitend parameterized queries, geen string-concatenatie van gebruikersinvoer.
- **Autorisatie:** een klant ziet alleen de eigen rekening (filter op `rekening_id` uit de sessie).
- **Integriteit:** opname geweigerd als `bedrag > saldo`; bedragen > 0; datums gevalideerd.
- **Audittrail:** elke mutatie krijgt een transactieregel; geen UPDATE op historische bedragen.
- **Configuratie:** demo-pincode alleen in seed-script documenteren, niet hardcoded in queries.

## 6. Technische beperkingen

- Single-user CLI, geen gelijktijdige schrijfacties.
- Systeemdatum simuleerbaar voor toetsen van 2025-rente.
- Geen netwerk-API in deze versie.

## 7. Testdata

Klant `admin` / pincode `1234`, IBAN `NL00SVI0000000001`, startsaldo € 12.500, tarief vanaf 2025-01-01: bank 2,05% / spaarder 1,80%.
