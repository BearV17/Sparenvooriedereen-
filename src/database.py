"""SQLite-laag voor SparenVoorIedereen."""

from __future__ import annotations

import hashlib
import sqlite3
from datetime import date
from pathlib import Path

DB_PAD = Path(__file__).resolve().parent.parent / "data" / "svi.db"

DEMO_GEBRUIKER = "admin"
DEMO_PIN = "1234"


def hash_pin(pincode: str) -> str:
    return hashlib.sha256(pincode.encode("utf-8")).hexdigest()


def connectie() -> sqlite3.Connection:
    DB_PAD.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PAD)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialiseer() -> None:
    conn = connectie()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS klant (
                id INTEGER PRIMARY KEY,
                naam TEXT NOT NULL,
                gebruikersnaam TEXT NOT NULL UNIQUE,
                pincode_hash TEXT NOT NULL,
                aangemaakt_op TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS rekening (
                id INTEGER PRIMARY KEY,
                klant_id INTEGER NOT NULL UNIQUE,
                iban TEXT NOT NULL UNIQUE,
                saldo REAL NOT NULL,
                geopend_op TEXT NOT NULL,
                FOREIGN KEY (klant_id) REFERENCES klant(id)
            );

            CREATE TABLE IF NOT EXISTS transactie (
                id INTEGER PRIMARY KEY,
                rekening_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                bedrag REAL NOT NULL,
                saldo_na REAL NOT NULL,
                omschrijving TEXT NOT NULL,
                datum TEXT NOT NULL,
                FOREIGN KEY (rekening_id) REFERENCES rekening(id)
            );

            CREATE TABLE IF NOT EXISTS rente_dag (
                id INTEGER PRIMARY KEY,
                rekening_id INTEGER NOT NULL,
                datum TEXT NOT NULL,
                saldo REAL NOT NULL,
                percentage REAL NOT NULL,
                bedrag REAL NOT NULL,
                UNIQUE (rekening_id, datum),
                FOREIGN KEY (rekening_id) REFERENCES rekening(id)
            );

            CREATE TABLE IF NOT EXISTS tarief (
                id INTEGER PRIMARY KEY,
                geldig_vanaf TEXT NOT NULL UNIQUE,
                bank_pct REAL NOT NULL,
                spaarder_pct REAL NOT NULL
            );
            """
        )
        if conn.execute("SELECT COUNT(*) AS n FROM klant").fetchone()["n"] == 0:
            _seed(conn)
        conn.commit()
    finally:
        conn.close()


def _seed(conn: sqlite3.Connection) -> None:
    vandaag = "2025-01-01"
    conn.execute(
        """
        INSERT INTO klant (naam, gebruikersnaam, pincode_hash, aangemaakt_op)
        VALUES (?, ?, ?, ?)
        """,
        ("Demo Klant", DEMO_GEBRUIKER, hash_pin(DEMO_PIN), vandaag),
    )
    klant_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute(
        """
        INSERT INTO rekening (klant_id, iban, saldo, geopend_op)
        VALUES (?, ?, ?, ?)
        """,
        (klant_id, "NL00SVI0000000001", 12500.00, vandaag),
    )
    rekening_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute(
        """
        INSERT INTO transactie
            (rekening_id, type, bedrag, saldo_na, omschrijving, datum)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (rekening_id, "storting", 12500.00, 12500.00, "Openingsstorting", vandaag),
    )
    conn.execute(
        """
        INSERT INTO tarief (geldig_vanaf, bank_pct, spaarder_pct)
        VALUES (?, ?, ?)
        """,
        ("2025-01-01", 2.05, 1.80),
    )


def zoek_klant(gebruikersnaam: str, pincode: str) -> sqlite3.Row | None:
    conn = connectie()
    try:
        return conn.execute(
            """
            SELECT k.id AS klant_id, k.naam, k.gebruikersnaam,
                   r.id AS rekening_id, r.iban, r.saldo
            FROM klant k
            JOIN rekening r ON r.klant_id = k.id
            WHERE k.gebruikersnaam = ? AND k.pincode_hash = ?
            """,
            (gebruikersnaam, hash_pin(pincode)),
        ).fetchone()
    finally:
        conn.close()


def haal_rekening(rekening_id: int) -> sqlite3.Row:
    conn = connectie()
    try:
        return conn.execute(
            "SELECT * FROM rekening WHERE id = ?", (rekening_id,)
        ).fetchone()
    finally:
        conn.close()


def mutatie(
    rekening_id: int,
    type_: str,
    bedrag: float,
    omschrijving: str,
    dag: date,
) -> float:
    """Stort of neemt op. Geeft nieuw saldo terug. Verwacht bedrag > 0."""
    conn = connectie()
    try:
        rij = conn.execute(
            "SELECT saldo FROM rekening WHERE id = ?", (rekening_id,)
        ).fetchone()
        saldo = float(rij["saldo"])
        if type_ == "opname":
            if bedrag > saldo:
                raise ValueError("Onvoldoende saldo.")
            nieuw = saldo - bedrag
        else:
            nieuw = saldo + bedrag
        conn.execute(
            "UPDATE rekening SET saldo = ? WHERE id = ?", (nieuw, rekening_id)
        )
        conn.execute(
            """
            INSERT INTO transactie
                (rekening_id, type, bedrag, saldo_na, omschrijving, datum)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (rekening_id, type_, bedrag, nieuw, omschrijving, dag.isoformat()),
        )
        conn.commit()
        return nieuw
    finally:
        conn.close()


def tarief_op(dag: date) -> sqlite3.Row:
    conn = connectie()
    try:
        rij = conn.execute(
            """
            SELECT * FROM tarief
            WHERE geldig_vanaf <= ?
            ORDER BY geldig_vanaf DESC
            LIMIT 1
            """,
            (dag.isoformat(),),
        ).fetchone()
        if rij is None:
            raise ValueError("Geen tarief gevonden voor deze datum.")
        return rij
    finally:
        conn.close()


def sla_rente_dag_op(
    rekening_id: int,
    dag: date,
    saldo: float,
    percentage: float,
    bedrag: float,
) -> None:
    conn = connectie()
    try:
        conn.execute(
            """
            INSERT OR REPLACE INTO rente_dag
                (rekening_id, datum, saldo, percentage, bedrag)
            VALUES (?, ?, ?, ?, ?)
            """,
            (rekening_id, dag.isoformat(), saldo, percentage, bedrag),
        )
        conn.commit()
    finally:
        conn.close()


def som_rente(rekening_id: int, start: date, einde: date) -> float:
    conn = connectie()
    try:
        rij = conn.execute(
            """
            SELECT COALESCE(SUM(bedrag), 0) AS totaal
            FROM rente_dag
            WHERE rekening_id = ? AND datum >= ? AND datum <= ?
            """,
            (rekening_id, start.isoformat(), einde.isoformat()),
        ).fetchone()
        return float(rij["totaal"])
    finally:
        conn.close()


def rente_per_maand(rekening_id: int, start: date, einde: date) -> list[sqlite3.Row]:
    conn = connectie()
    try:
        return conn.execute(
            """
            SELECT substr(datum, 1, 7) AS maand,
                   ROUND(SUM(bedrag), 2) AS totaal
            FROM rente_dag
            WHERE rekening_id = ? AND datum >= ? AND datum <= ?
            GROUP BY maand
            ORDER BY maand
            """,
            (rekening_id, start.isoformat(), einde.isoformat()),
        ).fetchall()
    finally:
        conn.close()


def transacties(
    rekening_id: int, start: date | None = None, einde: date | None = None
) -> list[sqlite3.Row]:
    conn = connectie()
    try:
        sql = "SELECT * FROM transactie WHERE rekening_id = ?"
        params: list = [rekening_id]
        if start:
            sql += " AND datum >= ?"
            params.append(start.isoformat())
        if einde:
            sql += " AND datum <= ?"
            params.append(einde.isoformat())
        sql += " ORDER BY datum, id"
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def som_rente_transacties(rekening_id: int, start: date, einde: date) -> float:
    conn = connectie()
    try:
        rij = conn.execute(
            """
            SELECT COALESCE(SUM(bedrag), 0) AS totaal
            FROM transactie
            WHERE rekening_id = ? AND type = 'rente'
              AND datum >= ? AND datum <= ?
            """,
            (rekening_id, start.isoformat(), einde.isoformat()),
        ).fetchone()
        return float(rij["totaal"])
    finally:
        conn.close()


def schrijf_rente_bij(rekening_id: int, bedrag: float, dag: date, omschrijving: str) -> float:
    if bedrag <= 0:
        return float(haal_rekening(rekening_id)["saldo"])
    return mutatie(rekening_id, "rente", bedrag, omschrijving, dag)
