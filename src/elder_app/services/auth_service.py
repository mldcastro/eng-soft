"""
Serviço de autenticação (Módulo Base, seção 1.3).

No login bem-sucedido, é aqui que nasce a identidade do usuário (``user_id`` e
``user_role``) que a View injeta na sessão (``st.session_state``) para rotear
para a "View" correta. Neste MVP não há verificação de senha: o usuário é
localizado por nome+papel ou criado caso ainda não exista.
"""

from __future__ import annotations

from elder_app.models import Role, User
from elder_app.repositories import UserRepository


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    def login(self, name: str, role: Role) -> User:
        """Localiza (ou cria) o usuário com o nome e papel informados."""
        existing = self._users.find_by_name_and_role(name, role)
        if existing is not None:
            return existing
        return self._users.create(name, role)

    def get_user(self, user_id: int) -> User | None:
        return self._users.get_by_id(user_id)

    def update_name(self, user_id: int, name: str) -> User | None:
        self._users.update_name(user_id, name)
        return self._users.get_by_id(user_id)
