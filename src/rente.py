"""Renteberekening SparenVoorIedereen.

Aanname (zie docs/01_vragen_opdrachtgever.md):
de klassepercentages zijn correcties op de basisrente voor spaarders.
"""

from __future__ import annotations

from datetime import date

# (ondergrens inclusief, bovengrens exclusief, correctie in procentpunten)
SALDOKLASSEN = [
    (0.0, 10_000.0, -0.25),
    (10_000.0, 25_000.0, 0.0),
    (25_000.0, 50_000.0, -0.15),
    (50_000.0, 100_000.0, -0.25),
    (100_000.0, 1_000_000.0, -0.50),
]


def is_schrikkeljaar(jaar: int) -> bool:
    return jaar % 4 == 0 and (jaar % 100 != 0 or jaar % 400 == 0)


def dagen_in_jaar(jaar: int) -> int:
    return 366 if is_schrikkeljaar(jaar) else 365


def klasse_correctie(saldo: float) -> float | None:
    """Geeft de correctie, of None als er geen rente geldt (> 1 miljoen)."""
    if saldo > 1_000_000:
        return None
    if saldo < 0:
        return None
    for onder, boven, correctie in SALDOKLASSEN:
        if onder <= saldo < boven or (boven == 1_000_000 and saldo == 1_000_000):
            return correctie
    return None


def effectief_percentage(saldo: float, basis_spaarder_pct: float) -> float:
    correctie = klasse_correctie(saldo)
    if correctie is None:
        return 0.0
    return basis_spaarder_pct + correctie


def dagelijkse_rente(saldo: float, basis_spaarder_pct: float, dag: date) -> float:
    """Rente over één dag op basis van het eindsaldo."""
    if saldo <= 0:
        return 0.0
    pct = effectief_percentage(saldo, basis_spaarder_pct)
    return saldo * (pct / 100.0) / dagen_in_jaar(dag.year)


def kwartaal_van(dag: date) -> int:
    return (dag.month - 1) // 3 + 1


def kwartaal_grenzen(jaar: int, kwartaal: int) -> tuple[date, date]:
    starts = {1: (1, 1), 2: (4, 1), 3: (7, 1), 4: (10, 1)}
    einden = {1: (3, 31), 2: (6, 30), 3: (9, 30), 4: (12, 31)}
    sm, sd = starts[kwartaal]
    em, ed = einden[kwartaal]
    return date(jaar, sm, sd), date(jaar, em, ed)


def is_kwartaaleinde(dag: date) -> bool:
    return (dag.month, dag.day) in {(3, 31), (6, 30), (9, 30), (12, 31)}
