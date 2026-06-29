"""Repositório de matrículas — CRUD da tabela ``enrollments``."""

from __future__ import annotations

from datetime import datetime

from elder_app.models import EnrollmentStatus
from elder_app.repositories.database import Database


class EnrollmentRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    def get_status(self, senior_id: int, activity_id: int) -> EnrollmentStatus | None:
        with self._db.connect() as conn:
            row = conn.execute(
                "SELECT status FROM enrollments WHERE senior_id = ? AND activity_id = ?",
                (senior_id, activity_id),
            ).fetchone()
        return row["status"] if row else None

    def create(self, senior_id: int, activity_id: int, status: EnrollmentStatus) -> None:
        with self._db.connect() as conn:
            conn.execute(
                """INSERT INTO enrollments (senior_id, activity_id, status, created_at)
                   VALUES (?, ?, ?, ?)""",
                (senior_id, activity_id, status, datetime.now().isoformat()),
            )

    def delete(self, senior_id: int, activity_id: int) -> None:
        with self._db.connect() as conn:
            conn.execute(
                "DELETE FROM enrollments WHERE senior_id = ? AND activity_id = ?",
                (senior_id, activity_id),
            )

    def count_by_status(self, activity_id: int, status: EnrollmentStatus) -> int:
        with self._db.connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS n FROM enrollments WHERE activity_id = ? AND status = ?",
                (activity_id, status),
            ).fetchone()
        return int(row["n"])
