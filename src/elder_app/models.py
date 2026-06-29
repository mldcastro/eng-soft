"""
Camada Model — entidades de domínio.

Reúne as classes do domínio descritas no diagrama de classes (Sprint #2):
``User`` (especializado em ``Senior``/``Tutor`` pelo atributo ``role``),
``Activity``, ``ActivityReport`` e as entidades de comunicação social
(``Conversation``/``Message``).

São objetos de dados puros (``dataclass``): não contêm SQL nem regras de
negócio. São produzidos pela camada de Repositório e consumidos pelas camadas
de Serviço e de Apresentação.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# Papéis injetados na sessão pelo Módulo Base (seção 1.3 do documento).
Role = Literal["senior", "tutor", "moderator"]

# Situação de uma matrícula de um Sênior em uma Atividade.
EnrollmentStatus = Literal["enrolled", "waitlist"]


@dataclass
class User:
    """Ator do sistema. O campo ``role`` distingue Sênior, Tutor e Moderador."""

    id: int
    name: str
    role: Role
    age: int | None = None
    email_address: str | None = None
    cellphone_number: str | None = None

    @property
    def is_senior(self) -> bool:
        return self.role == "senior"

    @property
    def is_tutor(self) -> bool:
        return self.role == "tutor"


@dataclass
class Activity:
    """Atividade publicada no mural por um Tutor."""

    id: int
    title: str
    tutor_name: str
    time: str
    location: str
    type: str
    total_spots: int
    remaining_spots: int
    emoji: str
    color: str
    description: str

    @property
    def has_open_spots(self) -> bool:
        return self.remaining_spots > 0

    @property
    def spots_label(self) -> str:
        """Rótulo amigável exibido na View (deriva de ``remaining_spots``)."""
        return "Vagas abertas" if self.has_open_spots else "Lista de Espera"


@dataclass
class ActivityReport:
    """Relatório de engajamento de uma atividade (consumido pelo TutorBoard)."""

    activity: Activity
    enrolled_count: int
    waitlist_count: int


@dataclass
class Conversation:
    """Conversa do módulo de comunicação social (grupo, privada ou suporte)."""

    id: str
    name: str
    type: Literal["group", "private", "support"]
    emoji: str
    last_message: str = ""
    last_time: str = ""
    unread: int = 0


@dataclass
class Message:
    """Mensagem trocada dentro de uma conversa."""

    id: int
    conversation_id: str
    sender: Literal["me", "other"]
    sender_name: str
    text: str
    time: str
