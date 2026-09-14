# Gerichte vragen aan de opdrachtgever

Opdracht: SparenVoorIedereen — Blokopdracht 3.1  
Doel: ontbrekende businessregels verduidelijken voordat ontwerp en bouw starten.

## Rente en saldoklassen

1. Zijn de percentages per saldoklasse (-0,25%, 0%, -0,15%, enz.) **absolute rentes**, of **correcties** op de basisrente van 1,80% voor spaarders?
2. Geldt de basisrente van 1,80% voor élke klasse, of alleen als voorbeeldtarief per 1 januari 2025?
3. Wordt rente over het **eindsaldo van de dag** berekend, ook als er die dag is gestort of opgenomen?
4. Wordt kwartaalrente automatisch bijgeschreven op het saldo, of alleen zichtbaar tot de klant die opvraagt?
5. Als het tarief tussentijds wijzigt: geldt het nieuwe percentage vanaf die kalenderdag, of pas vanaf het volgende kwartaal?
6. Wordt in een schrikkeljaar élke dag door 366 gedeeld, of alleen 29 februari?

## Transacties en rekeningen

7. Mag het saldo onder € 0,00 komen? Zo nee: blokkeren we de opname of laten we een deelopname toe?
8. Zijn er min/max-bedragen voor storten en opnemen?
9. Mag een klant meerdere spaarrekeningen hebben?
10. Hoe identificeren we een rekening (rekeningnummer, IBAN, intern id)?

## Klanten en beveiliging

11. Hoe wordt een nieuwe klant aangemeld? Alleen medewerker, of ook zelfregistratie?
12. Is inloggen met gebruikersnaam + pincode voldoende, of is extra authenticatie verplicht?
13. Wat gebeurt er na 3 foute pogingen: tijdelijke blokkade, permanente blokkade, of handmatige reset door de bank?
14. Moeten pincodes versleuteld worden opgeslagen (hash), of is dat voor deze opdracht nog niet verplicht?

## Bankzijde

15. Moet het systeem het **bankkapitaal** en de 75%-buffer bijhouden, of is dat alleen achtergrondinformatie?
16. Moet een medewerker de rentepercentages kunnen wijzigen in het systeem?

## Rapportages

17. Is “rente laatste 12 maanden” per kalendermaand of een schuivend venster vanaf vandaag?
18. Welke gegevens mag een klant van zichzelf zien, en welke alleen een medewerker?

## Voorgestelde aannames tot antwoord

Tot de opdrachtgever anders besluit werken we met:

- saldoklasse-percentages als correctie op 1,80%;
- geen negatief saldo;
- één spaarrekening per klant;
- pincode gehashed opslaan;
- na 3 foute pogingen sessie weigeren;
- kwartaalrente wordt bijgeschreven op het saldo;
- tariefwijziging geldt vanaf de ingangsdatum per dag;
- bankkapitaal/buffer is buiten scope van het klantportaal.
