"""
Gerenciamento da conexão e do esquema do banco SQLite.

``Database`` centraliza a abertura de conexões e a criação/semeadura do
esquema. Cada operação de repositório abre e fecha sua própria conexão
(via ``connect()``), o que é seguro para o modelo de re-execução do Streamlit
e para múltiplas sessões simultâneas.
"""

from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from elder_app.repositories import seed

# Caminho padrão do arquivo de banco. Pode ser sobrescrito pela variável de
# ambiente COMUNIDADE_DB (útil para testes com um banco temporário).
_DEFAULT_DB_PATH = Path("data") / "comunidade.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL,
    role      TEXT NOT NULL CHECK (role IN ('senior', 'tutor', 'moderator')),
    age       INTEGER,
    email     TEXT,
    cellphone TEXT
);

CREATE TABLE IF NOT EXISTS activities (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT NOT NULL,
    tutor_name      TEXT NOT NULL,
    time            TEXT NOT NULL,
    location        TEXT NOT NULL,
    type            TEXT NOT NULL,
    total_spots     INTEGER NOT NULL,
    remaining_spots INTEGER NOT NULL,
    emoji           TEXT NOT NULL,
    color           TEXT NOT NULL,
    description     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS enrollments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    senior_id   INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    activity_id INTEGER NOT NULL REFERENCES activities (id) ON DELETE CASCADE,
    status      TEXT NOT NULL CHECK (status IN ('enrolled', 'waitlist')),
    created_at  TEXT NOT NULL,
    UNIQUE (senior_id, activity_id)
);

CREATE TABLE IF NOT EXISTS conversations (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    type         TEXT NOT NULL,
    emoji        TEXT NOT NULL,
    last_message TEXT NOT NULL DEFAULT '',
    last_time    TEXT NOT NULL DEFAULT '',
    unread       INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL REFERENCES conversations (id) ON DELETE CASCADE,
    sender          TEXT NOT NULL CHECK (sender IN ('me', 'other')),
    sender_name     TEXT NOT NULL,
    text            TEXT NOT NULL,
    time            TEXT NOT NULL
);
"""


class Database:
    """Fábrica de conexões + inicialização do esquema SQLite."""

    def __init__(self, path: str | Path | None = None) -> None:
        env_path = os.environ.get("COMUNIDADE_DB")
        self.path = Path(path or env_path or _DEFAULT_DB_PATH)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """Abre uma conexão, faz commit ao final e sempre fecha."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_schema(self) -> None:
        """Cria as tabelas (se necessário) e popula os dados-semente uma vez."""
        with self.connect() as conn:
            conn.executescript(_SCHEMA)
            self._seed_if_empty(conn)

    @staticmethod
    def _seed_if_empty(conn: sqlite3.Connection) -> None:
        if conn.execute("SELECT COUNT(*) FROM activities").fetchone()[0] == 0:
            conn.executemany(
                """INSERT INTO activities
                   (title, tutor_name, time, location, type,
                    total_spots, remaining_spots, emoji, color, description)
                   VALUES (:title, :tutor_name, :time, :location, :type,
                           :total_spots, :remaining_spots, :emoji, :color, :description)""",
                seed.SEED_ACTIVITIES,
            )

        if conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0] == 0:
            conn.executemany(
                """INSERT INTO conversations
                   (id, name, type, emoji, last_message, last_time, unread)
                   VALUES (:id, :name, :type, :emoji, :last_message, :last_time, :unread)""",
                seed.SEED_CONVERSATIONS,
            )
            rows = [
                (conv_id, m["sender"], m["sender_name"], m["text"], m["time"])
                for conv_id, msgs in seed.SEED_MESSAGES.items()
                for m in msgs
            ]
            conn.executemany(
                """INSERT INTO messages
                   (conversation_id, sender, sender_name, text, time)
                   VALUES (?, ?, ?, ?, ?)""",
                rows,
            )
