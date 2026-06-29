"""
elder_app — backend da Plataforma Comunitária para Adultos 65+.

Organizado em camadas (MVC simplificado, seção 1.2 do documento):

* ``elder_app.models``        — Model: entidades de domínio (dataclasses).
* ``elder_app.repositories``  — Acesso a Dados: única camada com SQL/SQLite.
* ``elder_app.services``      — Lógica de Negócio: regras, validações, permissões.
* ``elder_app.backend``       — composição das camadas (fachada para a View).

A camada de Apresentação (``mvp_streamlit/app.py``) consome apenas
``build_backend()`` / ``Backend``.
"""

from elder_app.backend import Backend, build_backend

__all__ = ["Backend", "build_backend"]
