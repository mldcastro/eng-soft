"""
Composição do backend (montagem das camadas).

Ponto único de entrada que a camada de Apresentação (Streamlit) consome.
Monta os repositórios sobre o ``Database`` e injeta-os nos serviços, expondo
apenas os serviços de negócio. A View nunca instancia repositórios nem toca o
banco diretamente.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from elder_app.repositories import (
    ActivityRepository,
    ChatRepository,
    Database,
    EnrollmentRepository,
    UserRepository,
)
from elder_app.services import ActivityManager, AuthService, CommunicationManager


@dataclass(frozen=True)
class Backend:
    """Fachada com os três serviços de negócio expostos à View."""

    auth: AuthService
    activities: ActivityManager
    chat: CommunicationManager


def build_backend(db_path: str | Path | None = None) -> Backend:
    """Cria o banco (se necessário), monta as camadas e devolve a fachada."""
    db = Database(db_path)
    db.init_schema()

    user_repo = UserRepository(db)
    activity_repo = ActivityRepository(db)
    enrollment_repo = EnrollmentRepository(db)
    chat_repo = ChatRepository(db)

    return Backend(
        auth=AuthService(user_repo),
        activities=ActivityManager(activity_repo, enrollment_repo),
        chat=CommunicationManager(chat_repo),
    )
