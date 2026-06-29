"""
Camada de Lógica de Negócio (Controller / Service).

Contém as regras de negócio puras (matrícula, lista de espera, permissões,
relatórios). Recebe requisições da View, valida e delega a persistência à
camada de Repositório. **Não** contém SQL e **não** importa Streamlit —
mantendo a Separação de Responsabilidades da seção 1.2.
"""

from elder_app.services.activity_manager import ActivityManager
from elder_app.services.auth_service import AuthService
from elder_app.services.communication_manager import CommunicationManager

__all__ = ["ActivityManager", "AuthService", "CommunicationManager"]
