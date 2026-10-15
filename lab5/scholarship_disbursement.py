"""Scholarship disbursement ledger.

Grants awards under different schemes, disburses the funds, archives
records and counts awards per scheme.
"""

import sqlite3

SCHEMA = (
    "CREATE TABLE awards ("
    "id INTEGER PRIMARY KEY, student TEXT, scheme TEXT, "
    "amount INTEGER, disbursed INTEGER)"
)
INSERT_AWARD = (
    "INSERT INTO awards (student, scheme, amount, disbursed) "
    "VALUES (?, ?, ?, 0)"
)
SELECT_AMOUNT = "SELECT amount FROM awards WHERE id = ?"
MARK_DISBURSED = "UPDATE awards SET disbursed = 1 WHERE id = ?"
COUNT_BY_SCHEME = "SELECT COUNT(*) FROM awards WHERE scheme = ?"


class Ledger:
    """In-memory ledger of scholarship awards."""

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute(SCHEMA)
        self.disbursed_total = 0

    def grant(self, student, scheme, amount, audit=None):
        """Record an award for student and return the updated audit list."""
        if audit is None:
            audit = []
        self.conn.execute(INSERT_AWARD, (student, scheme, amount))
        audit.append(student)
        return audit

    def disburse(self, award_id):
        """Mark an award disbursed and return its amount, or None if absent."""
        row = self.conn.execute(SELECT_AMOUNT, (award_id,)).fetchone()
        if row is None:
            return None
        self.conn.execute(MARK_DISBURSED, (award_id,))
        self.disbursed_total += row[0]
        return row[0]

    def by_scheme_count(self, scheme):
        """Return the number of awards for scheme, or 0 when scheme is None."""
        if scheme is None:
            return 0
        row = self.conn.execute(COUNT_BY_SCHEME, (scheme,)).fetchone()
        return row[0]

    @staticmethod
    def archive():
        """Announce that awards are being archived."""
        print("archiving awards")


def main():
    """Run a short demonstration of the ledger."""
    ledger = Ledger()
    ledger.grant("Ishaan", "Merit", 50000)
    ledger.grant("Divya", "Need-based", 75000)
    print(ledger.disburse(1), ledger.disburse(9))
    print(ledger.by_scheme_count("Merit"), ledger.disbursed_total)
    ledger.archive()


if __name__ == "__main__":
    main()
