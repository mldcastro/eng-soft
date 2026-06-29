"""
Camada de Acesso a Dados (Model / Repository).

É a **única** camada autorizada a conter comandos SQL e a tocar o arquivo
SQLite (``.db``), conforme a restrição arquitetural da seção 1.2 do documento.
As camadas de Serviço e de Apresentação só enxergam objetos de domínio
(``elder_app.models``), nunca linhas de banco ou conexões.
"""

from elder_app.repositories.activity_repository import ActivityRepository
from elder_app.repositories.chat_repository import ChatRepository
from elder_app.repositories.database import Database
from elder_app.repositories.enrollment_repository import EnrollmentRepository
from elder_app.repositories.user_repository import UserRepository

__all__ = [
    "ActivityRepository",
    "ChatRepository",
    "Database",
    "EnrollmentRepository",
    "UserRepository",
]
