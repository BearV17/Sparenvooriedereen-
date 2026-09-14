# Functioneel ontwerp — SparenVoorIedereen

Max. 2 A4. Indeling volgens Software developer, hoofdstuk 2.3.

## 1. Inleiding

Dit ontwerp vertaalt de business requirements naar de werking van het spaarsysteem: wie doet wat, hoe ziet de interactie eruit, en welke processen het systeem ondersteunt. Doelgroep: opdrachtgever, team en latere bouwers.

## 2. Systeemfunctionaliteiten

Het systeem is een beveiligd klantportaal (eerste versie: tekstmenu) met:

1. Inloggen
2. Geld storten
3. Geld opnemen
4. Saldo opvragen
5. Opgebouwde rente dit kwartaal
6. Verkregen rente dit jaar
7. Renteoverzicht laatste 12 maanden
8. Transactieoverzicht (vanaf startdatum of periode)
9. (Systeem) dagelijkse rente berekenen / simuleren

Een medewerker wijzigt in een latere versie tarieven. Dat zit nu alleen in de gegevenslaag.

## 3. Gebruikersinteractie

Na succesvol inloggen ziet de klant een menu. Elke actie vraagt alleen de noodzakelijke invoer (bedrag of datums), toont een bevestiging en keert terug naar het menu. Fouten (verkeerde pin, te hoog opnamebedrag, ongeldige datum) krijgen een duidelijke melding zonder technische details.

### Wireframes — drie klantacties

Lesopdracht 2.3 (inlog / saldo) is het startpunt. Uitgewerkt voor storten, rente en transacties.

```
[Inloggen]                      [Storten]                       [Rente dit kwartaal]
+----------------------+        +----------------------+        +----------------------+
| SVI - Inloggen       |        | SVI - Storten        |        | SVI - Rente          |
| Gebruikersnaam [   ] |        | Huidig saldo €12500  |        | Kwartaal: 2025-Q1    |
| Pincode        [   ] |        | Bedrag     [     ]   |        | Dagen berekend: 31   |
| [Inloggen]           |        | [Bevestigen] [Terug] |        | Opgebouwd: € 19,32   |
| Poging 1 van 3       |        | Boeking direct zicht-|        | Basisrente: 1,80%    |
+----------------------+        | baar in transacties  |        | Klasse: 10k-25k 0%   |
                                +----------------------+        +----------------------+
```

## 4. Diagrammen

### 4.1 Use-case diagram

```
                    SparenVoorIedereen
        +--------------------------------------+
        |  UC1 Inloggen                        |
        |  UC2 Geld storten                    |
 Klant -|  UC3 Geld opnemen                    |
        |  UC4 Saldo opvragen                  |
        |  UC5 Rente kwartaal opvragen         |
        |  UC6 Rente jaar opvragen             |
        |  UC7 Rente 12 maanden opvragen       |
        |  UC8 Transacties opvragen            |
        +--------------------------------------+
 Medewerker -- UC9 Tarief wijzigen (later)
 Systeem    -- UC10 Dagelijkse renteberekening
```

### 4.2 Klassendiagram (functioneel)

```
Klant            Rekening              Transactie
- id             - id                  - id
- naam           - iban                - type (stort/opname/rente)
- gebruikersnaam - saldo               - bedrag
- pincode_hash   - klant_id            - saldo_na
+ inloggen()     + storten()           - datum
                 + opnemen()
                 + saldo_tonen()       RenteDag
Tarief           + rente_overzicht()   - datum
- vanaf          + transacties()       - saldo
- bank_pct                             - percentage
- spaarder_pct                         - bedrag
```

## 5. Processen

**Storten/opnemen:** controle invoer → saldo bijwerken → transactie opslaan → bevestiging.

**Dagelijkse rente:** bepaal dagen in jaar → bepaal saldoklasse van eindsaldo → (basis + correctie) / dagen × saldo → regel opslaan. Op de laatste dag van het kwartaal wordt het totaal bijgeschreven als transactie type `rente`.

**Overzichten:** filter op rekening + periode, som of lijst tonen.

## 6. Technische overwegingen (functioneel niveau)

- Eén rekening per klant in deze versie.
- Bedragen als decimalen met 2 cijfers (centen).
- Systeemklok of testdatum; productie zou einde-dag-batch draaien.
- Geen negatief saldo.
- Interface later vervangbaar door webschermen; de use-cases blijven gelijk.
