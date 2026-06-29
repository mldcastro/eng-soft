"""Repositório de atividades — CRUD da tabela ``activities``."""

from __future__ import annotations

import sqlite3

from elder_app.models import Activity
from elder_app.repositories.database import Database


class ActivityRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    @staticmethod
    def _to_activity(row: sqlite3.Row) -> Activity:
        return Activity(
            id=row["id"],
            title=row["title"],
            tutor_name=row["tutor_name"],
            time=row["time"],
            location=row["location"],
            type=row["type"],
            total_spots=row["total_spots"],
            remaining_spots=row["remaining_spots"],
            emoji=row["emoji"],
            color=row["color"],
            description=row["description"],
        )

    def list_all(self) -> list[Activity]:
        with self._db.connect() as conn:
            rows = conn.execute("SELECT * FROM activities ORDER BY id DESC").fetchall()
        return [self._to_activity(r) for r in rows]

    def get_by_id(self, activity_id: int) -> Activity | None:
        with self._db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM activities WHERE id = ?", (activity_id,)
            ).fetchone()
        return self._to_activity(row) if row else None

    def insert(self, activity: Activity) -> Activity:
        with self._db.connect() as conn:
            cur = conn.execute(
                """INSERT INTO activities
                   (title, tutor_name, time, location, type,
                    total_spots, remaining_spots, emoji, color, description)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    activity.title, activity.tutor_name, activity.time,
                    activity.location, activity.type, activity.total_spots,
                    activity.remaining_spots, activity.emoji, activity.color,
                    activity.description,
                ),
            )
            activity.id = int(cur.lastrowid or 0)
        return activity

    def update_remaining_spots(self, activity_id: int, remaining_spots: int) -> None:
        with self._db.connect() as conn:
            conn.execute(
                "UPDATE activities SET remaining_spots = ? WHERE id = ?",
                (remaining_spots, activity_id),
            )

    def delete(self, activity_id: int) -> None:
        with self._db.connect() as conn:
            conn.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
