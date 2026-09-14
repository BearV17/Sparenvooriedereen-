#!/usr/bin/env python3
"""SparenVoorIedereen — klantportaal (CLI)."""

from __future__ import annotations

import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Zorg dat src/ importeerbaar is bij `python3 src/bank.py`
sys.path.insert(0, str(Path(__file__).resolve().parent))

import database as db
import rente

STARTDATUM = date(2025, 1, 1)
MAX_POGINGEN = 3


def parse_datum(tekst: str) -> date:
    return datetime.strptime(tekst.strip(), "%Y-%m-%d").date()


def euro(bedrag: float) -> str:
    return f"€ {bedrag:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def vraag_datum(prompt: str) -> date:
    while True:
        raw = input(prompt).strip()
        try:
            dag = parse_datum(raw)
            if dag < STARTDATUM:
                print(f"Datum ligt voor de startdatum ({STARTDATUM}).")
                continue
            return dag
        except ValueError:
            print("Gebruik formaat JJJJ-MM-DD, bijvoorbeeld 2025-03-31.")


def vraag_bedrag(prompt: str) -> float:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            bedrag = float(raw)
        except ValueError:
            print("Voer een getal in.")
            continue
        if bedrag <= 0:
            print("Bedrag moet groter zijn dan 0.")
            continue
        return round(bedrag, 2)


def inloggen() -> dict | None:
    print("=== SparenVoorIedereen — beveiligd inloggen ===")
    print(f"Systeemstartdatum: {STARTDATUM}")
    for poging in range(1, MAX_POGINGEN + 1):
        naam = input("Gebruikersnaam: ").strip()
        pin = input("Pincode: ").strip()
        rij = db.zoek_klant(naam, pin)
        if rij:
            print(f"\nInloggen geslaagd. Welkom {rij['naam']}.")
            return dict(rij)
        over = MAX_POGINGEN - poging
        print(f"Onjuist. Je hebt nog {over} poging(en) over.")
        print("-" * 34)
    print("\nSysteem geblokkeerd. Neem contact op met de bank.")
    return None


def toon_saldo(sessie: dict) -> None:
    rekening = db.haal_rekening(sessie["rekening_id"])
    print(f"IBAN:  {rekening['iban']}")
    print(f"Saldo: {euro(rekening['saldo'])}")


def storten(sessie: dict, dag: date) -> None:
    bedrag = vraag_bedrag("Te storten bedrag: ")
    nieuw = db.mutatie(sessie["rekening_id"], "storting", bedrag, "Storting", dag)
    print(f"Gestort: {euro(bedrag)}. Nieuw saldo: {euro(nieuw)}.")


def opnemen(sessie: dict, dag: date) -> None:
    bedrag = vraag_bedrag("Op te nemen bedrag: ")
    try:
        nieuw = db.mutatie(sessie["rekening_id"], "opname", bedrag, "Opname", dag)
    except ValueError as fout:
        print(fout)
        return
    print(f"Opgenomen: {euro(bedrag)}. Nieuw saldo: {euro(nieuw)}.")


def bereken_rente_voor_dag(rekening_id: int, dag: date) -> float:
    rekening = db.haal_rekening(rekening_id)
    saldo = float(rekening["saldo"])
    tarief = db.tarief_op(dag)
    basis = float(tarief["spaarder_pct"])
    pct = rente.effectief_percentage(saldo, basis)
    bedrag = rente.dagelijkse_rente(saldo, basis, dag)
    db.sla_rente_dag_op(rekening_id, dag, saldo, pct, bedrag)
    return bedrag


def simuleer_rente(sessie: dict) -> None:
    print("Simuleer dagelijkse rente tot en met een datum (testhulp).")
    einde = vraag_datum("Einddatum (JJJJ-MM-DD): ")
    dag = STARTDATUM
    totaal = 0.0
    dagen = 0
    while dag <= einde:
        totaal += bereken_rente_voor_dag(sessie["rekening_id"], dag)
        dagen += 1
        dag += timedelta(days=1)
    print(f"{dagen} dag(en) berekend. Som dagrente: {euro(totaal)}.")
    if rente.is_kwartaaleinde(einde):
        _keer_kwartaal_uit(sessie["rekening_id"], einde)


def _keer_kwartaal_uit(rekening_id: int, einde: date) -> None:
    q = rente.kwartaal_van(einde)
    start, _ = rente.kwartaal_grenzen(einde.year, q)
    bedrag = db.som_rente(rekening_id, start, einde)
    db.schrijf_rente_bij(
        rekening_id,
        round(bedrag, 2),
        einde,
        f"Kwartaalrente {einde.year}-Q{q}",
    )
    print(f"Kwartaalrente {einde.year}-Q{q} bijgeschreven: {euro(bedrag)}.")


def rente_kwartaal(sessie: dict, dag: date) -> None:
    q = rente.kwartaal_van(dag)
    start, einde = rente.kwartaal_grenzen(dag.year, q)
    einde = min(einde, dag)
    bedrag = db.som_rente(sessie["rekening_id"], start, einde)
    rekening = db.haal_rekening(sessie["rekening_id"])
    tarief = db.tarief_op(dag)
    pct = rente.effectief_percentage(float(rekening["saldo"]), float(tarief["spaarder_pct"]))
    print(f"Kwartaal {dag.year}-Q{q} ({start} t/m {einde})")
    print(f"Opgebouwde rente: {euro(bedrag)}")
    print(f"Huidig effectief tarief bij dit saldo: {pct:.2f}%")


def rente_jaar(sessie: dict, dag: date) -> None:
    q = rente.kwartaal_van(dag)
    if q == 1:
        print("Er is dit jaar nog geen kwartaal afgesloten.")
        return
    start = date(dag.year, 1, 1)
    _, einde_laatste = rente.kwartaal_grenzen(dag.year, q - 1)
    bedrag = db.som_rente_transacties(sessie["rekening_id"], start, einde_laatste)
    print(
        f"Verkregen rente {dag.year} t/m Q{q - 1} "
        f"(tot {einde_laatste}): {euro(bedrag)}"
    )


def rente_12_maanden(sessie: dict, dag: date) -> None:
    start = date(dag.year - 1, dag.month, 1)
    if start < STARTDATUM:
        start = STARTDATUM
    rijen = db.rente_per_maand(sessie["rekening_id"], start, dag)
    if not rijen:
        print("Nog geen dagrentes berekend. Gebruik eerst optie 8.")
        return
    print(f"Rente per maand van {start} t/m {dag}:")
    for rij in rijen:
        print(f"  {rij['maand']}: {euro(rij['totaal'])}")


def toon_transacties(sessie: dict) -> None:
    print("1. Vanaf startdatum tot nu")
    print("2. Eigen periode")
    keuze = input("Keuze: ").strip()
    start = STARTDATUM
    einde = None
    if keuze == "2":
        start = vraag_datum("Startdatum (JJJJ-MM-DD): ")
        einde = vraag_datum("Einddatum (JJJJ-MM-DD): ")
        if einde < start:
            print("Einddatum ligt voor de startdatum.")
            return
    rijen = db.transacties(sessie["rekening_id"], start, einde)
    if not rijen:
        print("Geen transacties in deze periode.")
        return
    print(f"{'Datum':<12} {'Type':<10} {'Bedrag':>12} {'Saldo na':>12}  Omschrijving")
    for rij in rijen:
        print(
            f"{rij['datum']:<12} {rij['type']:<10} "
            f"{euro(rij['bedrag']):>12} {euro(rij['saldo_na']):>12}  "
            f"{rij['omschrijving']}"
        )


def menu(sessie: dict) -> None:
    systeemdag = date.today()
    if systeemdag < STARTDATUM:
        systeemdag = STARTDATUM
    while True:
        print("\n=== Menu ===")
        print(f"(rekendag: {systeemdag})")
        print("1. Saldo opvragen")
        print("2. Geld storten")
        print("3. Geld opnemen")
        print("4. Opgebouwde rente dit kwartaal")
        print("5. Verkregen rente dit jaar (t/m laatste kwartaal)")
        print("6. Renteoverzicht laatste 12 maanden")
        print("7. Transactieoverzicht")
        print("8. Simuleer dagelijkse rente (testhulp)")
        print("9. Rekendag instellen")
        print("0. Uitloggen")
        keuze = input("Keuze: ").strip()
        if keuze == "1":
            toon_saldo(sessie)
        elif keuze == "2":
            storten(sessie, systeemdag)
        elif keuze == "3":
            opnemen(sessie, systeemdag)
        elif keuze == "4":
            rente_kwartaal(sessie, systeemdag)
        elif keuze == "5":
            rente_jaar(sessie, systeemdag)
        elif keuze == "6":
            rente_12_maanden(sessie, systeemdag)
        elif keuze == "7":
            toon_transacties(sessie)
        elif keuze == "8":
            simuleer_rente(sessie)
        elif keuze == "9":
            systeemdag = vraag_datum("Nieuwe rekendag (JJJJ-MM-DD): ")
        elif keuze == "0":
            print("Uitgelogd. Tot ziens.")
            break
        else:
            print("Onbekende keuze.")


def main() -> None:
    db.initialiseer()
    sessie = inloggen()
    if sessie:
        menu(sessie)


if __name__ == "__main__":
    main()
