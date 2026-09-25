from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


class Store:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.conn() as c:
            c.executescript("""CREATE TABLE IF NOT EXISTS tickets(
                id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, body TEXT, category TEXT, queue TEXT,
                confidence REAL, priority TEXT, priority_score INTEGER, summary TEXT, model_version TEXT, created_at TEXT);
                CREATE TABLE IF NOT EXISTS feedback(
                id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id INTEGER, correct_category TEXT, notes TEXT, created_at TEXT);""")

    @contextmanager
    def conn(self):
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        try:
            yield c
            c.commit()
        finally:
            c.close()

    def save(self, subject, body, result):
        with self.conn() as c:
            cur = c.execute(
                "INSERT INTO tickets(subject,body,category,queue,confidence,priority,priority_score,summary,model_version,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (subject, body, result["category"], result["queue"], result["confidence"], result["priority"],
                 result["priority_score"], result["summary"], result["model_version"], datetime.now(timezone.utc).isoformat()),
            )
            return int(cur.lastrowid)

    def recent(self, limit=50):
        with self.conn() as c:
            rows = c.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

    def feedback(self, ticket_id, correct, notes=""):
        with self.conn() as c:
            c.execute(
                "INSERT INTO feedback(ticket_id,correct_category,notes,created_at) VALUES(?,?,?,?)",
                (ticket_id, correct, notes, datetime.now(timezone.utc).isoformat()),
            )

    def metrics(self):
        with self.conn() as c:
            total = c.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
            high = c.execute("SELECT COUNT(*) FROM tickets WHERE priority IN ('high','critical')").fetchone()[0]
            feedback = c.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
            cats = c.execute("SELECT category,COUNT(*) n FROM tickets GROUP BY category ORDER BY n DESC").fetchall()
        return {"tickets": total, "high_priority": high, "feedback": feedback, "by_category": [dict(x) for x in cats]}
