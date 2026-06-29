"""Repositório de usuários — CRUD da tabela ``users``."""

from __future__ import annotations

import sqlite3

from elder_app.models import Role, User
from elder_app.repositories.database import Database


class UserRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    @staticmethod
    def _to_user(row: sqlite3.Row) -> User:
        return User(
            id=row["id"],
            name=row["name"],
            role=row["role"],
            age=row["age"],
            email_address=row["email"],
            cellphone_number=row["cellphone"],
        )

    def get_by_id(self, user_id: int) -> User | None:
        with self._db.connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return self._to_user(row) if row else None

    def find_by_name_and_role(self, name: str, role: Role) -> User | None:
        with self._db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE name = ? AND role = ?", (name, role)
            ).fetchone()
        return self._to_user(row) if row else None

    def create(self, name: str, role: Role) -> User:
        with self._db.connect() as conn:
            cur = conn.execute(
                "INSERT INTO users (name, role) VALUES (?, ?)", (name, role)
            )
            user_id = int(cur.lastrowid or 0)
        return User(id=user_id, name=name, role=role)

    def update_name(self, user_id: int, name: str) -> None:
        with self._db.connect() as conn:
            conn.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
