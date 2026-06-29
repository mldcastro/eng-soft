"""
Gerenciador de Comunicação (classe ``CommunicationManager`` do diagrama).

Regras de negócio do módulo de comunicação social: listar conversas, abrir uma
conversa e enviar mensagens. Delega a persistência ao ``ChatRepository``.
"""

from __future__ import annotations

from datetime import datetime

from elder_app.models import Conversation, Message
from elder_app.repositories import ChatRepository


class CommunicationManager:
    def __init__(self, chat: ChatRepository) -> None:
        self._chat = chat

    def get_conversations(self) -> list[Conversation]:
        return self._chat.list_conversations()

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return self._chat.get_conversation(conversation_id)

    def get_messages(self, conversation_id: str) -> list[Message]:
        return self._chat.list_messages(conversation_id)

    def send_message(
        self, conversation_id: str, text: str, sender_name: str = "Você"
    ) -> Message | None:
        """Envia uma mensagem do usuário atual ('me') para a conversa."""
        text = text.strip()
        if not text:
            return None
        now = datetime.now().strftime("%H:%M")
        return self._chat.add_message(conversation_id, "me", sender_name, text, now)
