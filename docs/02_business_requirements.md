# Business requirements — SparenVoorIedereen

**Project:** Spaarsysteem SVI  
**Opdrachtgever:** SparenVoorIedereen / docent Capabel  
**Document:** maximaal 1 A4  
**Versie:** 1.0  
**Startdatum systeem:** 1 januari 2025

## 1. Doel

SVI wil spaarders inzicht geven in saldo, transacties en rente, en intern renteberekening automatiseren. Het systeem ondersteunt dagelijkse renteberekening per saldoklasse, kwartaaluitkering en raadplegen van historie.

## 2. Belanghebbenden

| Rol        | Belang                                      |
|------------|---------------------------------------------|
| Spaarder   | Storten, opnemen, saldo en rente inzien     |
| Medewerker | Klant ondersteunen, rente tarieven beheren  |
| Bank       | Correcte rente, bufferregel, audittrail     |

## 3. Functionele eisen

**F1 Inloggen**  
Klant logt in met gebruikersnaam en pincode. Maximaal 3 pogingen per sessie.

**F2 Storten**  
Klant stort een positief bedrag. Saldo en transactie worden direct bijgewerkt.

**F3 Opnemen**  
Klant neemt een positief bedrag op, alleen als het saldo toereikend is.

**F4 Saldo opvragen**  
Klant ziet het actuele saldo.

**F5 Rente dit kwartaal**  
Klant ziet de nog niet (of al) uitgekeerde rente van het lopende kwartaal.

**F6 Rente dit jaar**  
Klant ziet de tot en met het laatste afgesloten kwartaal uitgekeerde rente.

**F7 Rente 12 maanden**  
Klant ziet een maandoverzicht van berekende rente over de laatste 12 maanden.

**F8 Transactieoverzicht**  
Klant ziet transacties vanaf 1-1-2025 of tussen twee zelf gekozen datums.

**F9 Dagelijkse renteberekening**  
Aan het einde van de dag: `rente = saldo × (percentage_saldoklasse / dagen_in_jaar)`.  
Normaaljaar 365 dagen, schrikkeljaar 366. Rente is per kwartaal uitkeerbaar en tarieven zijn wijzigbaar.

**F10 Tarieflogica**  
Spaardersrente is 0,25 procentpunt lager dan het percentage waarmee de bank geld wegzet.  
Per 1-1-2025: bank 2,05%, spaarder 1,80%.  
Saldoklassen (correctie op basisrente, aanname tot nader order):

| Saldo                 | Correctie | Effectief (bij 1,80%) |
|-----------------------|-----------|------------------------|
| € 0 – € 10.000        | −0,25%    | 1,55%                  |
| € 10.000 – € 25.000   | 0%        | 1,80%                  |
| € 25.000 – € 50.000   | −0,15%    | 1,65%                  |
| € 50.000 – € 100.000  | −0,25%    | 1,55%                  |
| € 100.000 – € 1.000.000 | −0,50%  | 1,30%                  |
| boven € 1.000.000     | geen rente| 0%                     |

**F11 Bankbuffer (niet in klantportaal)**  
De bank zet geld weg boven 75% van haar kapitaal. Tot 75% is een verplichte buffer.

## 4. Niet-functionele eisen

- Gebruiksvriendelijk menu, bedragen in euro’s met 2 decimalen.
- Gegevens duurzaam opslaan (database), transacties niet stilzwijgend wijzigen.
- Pincodes niet in platte tekst bewaren.
- SQL-injectie voorkomen (parameters).
- Code leesbaar, testbaar en later samenvoegbaar in een scrumteam.

## 5. Buiten scope (deze opdracht)

Zelfregistratie, meerdere rekeningen per klant, overboekingen tussen klanten, mobiele app, koppeling DNB-rapportages.

## 6. Acceptatie

Het systeem is acceptabel als een ingelogde tesklant alle acties F2–F8 kan uitvoeren, rente volgens F9/F10 wordt berekend, en mislukte opnames/logins netjes worden geweigerd.
