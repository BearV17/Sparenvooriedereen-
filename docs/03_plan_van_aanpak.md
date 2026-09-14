# Plan van aanpak — SparenVoorIedereen

Template: Projectmanagement, project opstarten.

## 1. Opdracht

Ontwerp en realiseer (onderdelen van) een spaarsysteem voor SVI: requirements, functioneel ontwerp, technisch ontwerp en een werkend programmadeel in een scrumteam.

## 2. Doel en resultaat

- Business requirements + dit plan
- Functioneel ontwerp (rapport + diagrammen + UI-schetsen)
- Technisch ontwerp (database, berekeningen, beveiliging)
- Werkende component + code-review + STARR-reflectie

## 3. Afbakening

**Wel:** klantacties uit de opdracht, rentelogica, lokale SQLite-opslag, CLI-interface.  
**Niet:** productiehosting, echte bankkoppeling, volledige web-UI.

## 4. Aanpak

Waterval voor deel 1–3 (requirements → FO → TO). Scrum/Kanban voor deel 4 (bouwen, reviewen, integreren).

## 5. Planning (4–5 dagdelen)

| Dagdeel | Onderdeel              | Resultaat                         |
|---------|------------------------|-----------------------------------|
| 1       | Deel 1 Requirements    | Vragen, BR-document, dit plan     |
| 2       | Deel 2 Functioneel     | Diagrammen, wireframes, FO-rapport|
| 3       | Deel 3 Technisch       | Databaseschema, TO-rapport        |
| 4       | Deel 4 Sprint + code   | Eigen component, review           |
| 5       | Integratie + reflectie | Samengevoegd systeem, STARR       |

## 6. Organisatie

Groep 2–3 studenten voor ontwerp. Scrumteam kan anders zijn; ieder programmeert een eigen onderdeel. Beoordeling is individueel op de eigen component.

Voorgestelde taakverdeling bouw:

- Lid A: inloggen + sessie + beveiliging
- Lid B: storten/opnemen/saldo + transacties
- Lid C: renteberekening + overzichten

## 7. Communicatie en voortgang

- Kanban-board (lesopdracht 7.1)
- Planning poker voor inschatting (lesopdracht 7.2)
- Korte stand-up per werksessie
- Ontbrekende info direct bij de docent toetsen

## 8. Kwaliteit

- Geen O-scores op het beoordelingsformulier
- Code-review kruislings
- Samen testen na merge
- Documenten binnen de A4-limieten

## 9. Risico’s

| Risico                         | Aanpak                                      |
|--------------------------------|---------------------------------------------|
| Onduidelijke renteregels       | Vragenlijst + vastgelegde aannames          |
| Onderdelen sluiten niet aan    | Eerst datamodel en functienamen afspreken   |
| Tijdtekort integratie          | Klein werkend pad eerst (login + saldo)     |

## 10. Deliverables (Google Drive / GitHub)

Business requirements, plan van aanpak, functioneel ontwerp, technisch ontwerp, templates, eigen code, feedback code-review, STARR-reflectie.
