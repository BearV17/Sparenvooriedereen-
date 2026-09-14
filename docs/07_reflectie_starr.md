# Reflectie (STARR) — eigen bijdrage

Zelfreflectie als beginnend beroepsbeoefenaar. Model: Situatie, Taak, Actie, Resultaat, Reflectie.

## Situatie

We kregen blokopdracht 3.1: een spaarsysteem voor SparenVoorIedereen, van requirements tot een werkend onderdeel in een scrumteam. De renteregels in de achtergrondinformatie waren deels tegenstrijdig (basisrente 1,80% versus negatieve klassepercentages). De repo bevatte al een eenvoudig `login.py`.

## Taak

Mijn taak was de opdracht structureren, ontbrekende regels expliciet maken, ontwerpdocumenten opleveren en een werkende kern bouwen (inloggen, mutaties, rente, overzichten) die later met teamonderdelen samen kan.

## Actie

- Eerst de opdrachtregel voor regel langs en een vragenlijst voor de opdrachtgever gemaakt.
- Aannames vastgelegd zodat we wél konden ontwerpen.
- Business requirements, plan van aanpak, functioneel en technisch ontwerp kort gehouden (A4-limiet).
- Bestaande login niet weggegooid maar uitgebreid: hash, database, menu.
- Rente in een aparte module gezet zodat een teamgenoot die kan reviewen zonder de UI te hoeven kennen.
- Na een interne review pincode uit de broncode gehaald en queries geparameteriseerd.

## Resultaat

Er staat een startbaar programma (`python3 src/bank.py`) plus de gevraagde documenten in `docs/`. De tien klantacties uit de opdracht zijn bereikbaar. Open punt blijft de officiële duiding van de saldoklassen; die staat in de vragenlijst. Samenvoegen met andere teamleden kan via dezelfde tabellen en functienamen.

Wat goed ging: opsplitsen in lagen en aannames opschrijven.  
Wat beter kon: eerder een klein testdatum-scenario (hele kwartaal doordraaien) automatiseren in plaats van handmatig in het menu.

## Reflectie

Ik heb geleerd dat “de opdrachtgever vragen” geen zwakte is maar onderdeel van B1-K1-W1: zonder scherpe regels bouw je de verkeerde rente. Volgende keer begin ik met één gezamenlijk datamodel op papier vóór iemand code schrijft, zodat mergen minder schuurt. Planning poker had ik eerder moeten gebruiken om de rentemodule niet te onderschatten (klassen + schrikkeljaar + kwartaalgrens).
