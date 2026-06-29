"""Repositório de comunicação — CRUD das tabelas ``conversations`` e ``messages``."""

from __future__ import annotations

import sqlite3

from elder_app.models import Conversation, Message
from elder_app.repositories.database import Database


class ChatRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    @staticmethod
    def _to_conversation(row: sqlite3.Row) -> Conversation:
        return Conversation(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            emoji=row["emoji"],
            last_message=row["last_message"],
            last_time=row["last_time"],
            unread=row["unread"],
        )

    @staticmethod
    def _to_message(row: sqlite3.Row) -> Message:
        return Message(
            id=row["id"],
            conversation_id=row["conversation_id"],
            sender=row["sender"],
            sender_name=row["sender_name"],
            text=row["text"],
            time=row["time"],
        )

    def list_conversations(self) -> list[Conversation]:
        with self._db.connect() as conn:
            rows = conn.execute("SELECT * FROM conversations ORDER BY rowid").fetchall()
        return [self._to_conversation(r) for r in rows]

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        with self._db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
            ).fetchone()
        return self._to_conversation(row) if row else None

    def list_messages(self, conversation_id: str) -> list[Message]:
        with self._db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY id",
                (conversation_id,),
            ).fetchall()
        return [self._to_message(r) for r in rows]

    def add_message(
        self, conversation_id: str, sender: str, sender_name: str, text: str, time: str
    ) -> Message:
        with self._db.connect() as conn:
            cur = conn.execute(
                """INSERT INTO messages (conversation_id, sender, sender_name, text, time)
                   VALUES (?, ?, ?, ?, ?)""",
                (conversation_id, sender, sender_name, text, time),
            )
            message_id = int(cur.lastrowid or 0)
        return Message(message_id, conversation_id, "me", sender_name, text, time)  # type: ignore[arg-type]
