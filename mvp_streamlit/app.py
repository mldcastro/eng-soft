"""
MVP — Plataforma Comunitária para Adultos 65+
Sprint 4 — Implementação em Streamlit
INF01127 — Engenharia de Software | UFRGS 2025/1

Arquitetura (seção 1.3): a integração entre módulos usa o Session State nativo
do Streamlit (st.session_state). No login, o Módulo Base injeta na sessão global
as variáveis `user_id` e `user_role` ('senior' | 'tutor'). Cada view consome
essas variáveis para rotear o usuário para a interface correta — por exemplo,
"Realizar Matrícula" só aparece para 'senior'; "Criar Atividade" só para 'tutor'
(controle de acesso previsto nos UC21/UC23).
"""

import streamlit as st
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ComunidadeAtiva",
    page_icon="🌻",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Helper crítico: o markdown do Streamlit interpreta linhas indentadas (4+
# espaços) como bloco de código. H() remove a indentação de cada linha antes
# de renderizar, garantindo que o HTML seja sempre tratado como HTML.
# ---------------------------------------------------------------------------
def H(html_str: str):
    cleaned = "\n".join(line.lstrip() for line in html_str.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Paleta de cores centralizada
# ---------------------------------------------------------------------------
C = {
    "blue":        "#2563EB",
    "blue_dark":   "#1D4ED8",
    "blue_light":  "#EFF6FF",
    "blue_mid":    "#BFDBFE",
    "teal":        "#0D9488",
    "teal_light":  "#F0FDFA",
    "orange":      "#EA580C",
    "orange_light":"#FFF7ED",
    "green":       "#16A34A",
    "green_light": "#F0FDF4",
    "red":         "#DC2626",
    "text_dark":   "#0F172A",
    "text_mid":    "#334155",
    "text_muted":  "#64748B",
    "border":      "#E2E8F0",
    "bg_card":     "#FFFFFF",
}

# ---------------------------------------------------------------------------
# CSS global
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
  .stApp {{ background-color: #EFF4FB !important; }}
  .block-container {{ padding: 0 0 1rem 0 !important; max-width: 480px !important; }}

  /* Oculta chrome padrão do Streamlit */
  #MainMenu, footer {{ visibility: hidden !important; }}
  [data-testid="stToolbar"] {{ display: none !important; }}
  [data-testid="stDecoration"] {{ display: none !important; }}
  .stDeployButton {{ display: none !important; }}

  /* Botões — azul por padrão */
  div[data-testid="stButton"] > button {{
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    border: none !important;
    padding: 0.7rem 1rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: filter 0.15s !important;
    color: white !important;
    background-color: {C['blue']} !important;
    white-space: pre-line !important;
    line-height: 1.25 !important;
  }}
  div[data-testid="stButton"] > button:hover {{ filter: brightness(0.92) !important; }}

  /* Variações de botão — alvo via atributo help/title */
  div[data-testid="stButton"] > button[title="teal"]   {{ background-color: {C['teal']} !important; }}
  div[data-testid="stButton"] > button[title="orange"] {{ background-color: {C['orange']} !important; }}
  div[data-testid="stButton"] > button[title="red"]    {{ background-color: {C['red']} !important; }}
  div[data-testid="stButton"] > button[title="green"]  {{ background-color: {C['green']} !important; }}
  div[data-testid="stButton"] > button[title="ghost"]  {{
    background-color: #E2E8F0 !important; color: {C['text_dark']} !important;
  }}
  div[data-testid="stButton"] > button[title="nav-on"] {{
    background-color: {C['blue_light']} !important; color: {C['blue']} !important;
    border: 2px solid {C['blue']} !important;
  }}
  div[data-testid="stButton"] > button[title="nav-off"] {{
    background-color: white !important; color: {C['text_muted']} !important;
    border: 2px solid {C['border']} !important;
  }}

  /* Inputs */
  div[data-testid="stTextInput"] input,
  div[data-testid="stTextArea"] textarea {{
    font-size: 1.1rem !important;
    border-radius: 12px !important;
    border: 2px solid #CBD5E1 !important;
    padding: 0.6rem 1rem !important;
    color: #1E293B !important;
    background: white !important;
  }}
  div[data-testid="stTextInput"] label,
  div[data-testid="stTextArea"] label,
  div[data-testid="stSelectbox"] label,
  div[data-testid="stRadio"] label,
  div[data-testid="stSlider"] label {{
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: {C['text_mid']} !important;
  }}

  /* Texto das opções do radio (seletor de papel) — cor escura legível */
  div[data-testid="stRadio"] label p,
  div[data-testid="stRadio"] div[role="radiogroup"] label > div:last-child p {{
    color: {C['text_dark']} !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
  }}

  div[data-testid="stAlert"] {{ border-radius: 14px !important; font-size: 1.05rem !important; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Dados mockados (sementes — simulam o banco de dados)
# ---------------------------------------------------------------------------
SEED_ACTIVITIES = [
    {"id": "1", "title": "Yoga na Cadeira", "tutor": "Prof. Ana Maria",
     "time": "Hoje, 15:00", "location": "Ao vivo (Vídeo)", "type": "Exercício Físico",
     "spots": "Vagas abertas", "emoji": "🧘", "color": "#2563EB",
     "description": ("Uma aula leve e relaxante feita especialmente para você, "
                     "sem precisar levantar da cadeira. Ótimo para circulação e bem-estar.")},
    {"id": "2", "title": "Roda de Conversa: Livros", "tutor": "Mediador Carlos",
     "time": "Amanhã, 10:00", "location": "Sala de Chat", "type": "Social",
     "spots": "Lista de Espera", "emoji": "📚", "color": "#7C3AED",
     "description": ("Vamos conversar sobre nossas leituras favoritas e conhecer novos "
                     "amigos. Traga seu cafezinho!")},
    {"id": "3", "title": "Pintura com Aquarela", "tutor": "Profa. Beatriz",
     "time": "Sexta, 14:00", "location": "Ao vivo (Vídeo)", "type": "Arte",
     "spots": "Vagas abertas", "emoji": "🎨", "color": "#DC2626",
     "description": ("Aprenda técnicas simples de aquarela em um ambiente acolhedor. "
                     "Nenhuma experiência anterior necessária — só boa vontade!")},
]

# Emoji/cor padrão por tipo de atividade (usado ao criar novas atividades)
TYPE_STYLE = {
    "Exercício Físico": ("🧘", "#2563EB"),
    "Social":           ("📚", "#7C3AED"),
    "Arte":             ("🎨", "#DC2626"),
    "Jogos":            ("🎲", "#0891B2"),
    "Conteúdo":         ("📖", "#16A34A"),
}

CHATS = [
    {"id": "g1", "name": "Turma de Yoga",      "type": "group",
     "last": "Ana: Nos vemos às 15h!",   "time": "10:30", "unread": 2, "emoji": "👥"},
    {"id": "u1", "name": "Dona Maria",         "type": "private",
     "last": "Você: Que foto linda!",    "time": "Ontem", "unread": 0, "emoji": "👩"},
    {"id": "m1", "name": "Suporte / Moderador","type": "support",
     "last": "Moderador: Posso ajudar?", "time": "Ontem", "unread": 0, "emoji": "🛡️"},
]

INITIAL_MESSAGES = {
    "g1": [
        {"text": "Olá pessoal!", "sender": "other", "name": "Ana", "time": "10:00"},
        {"text": "Oi! Tudo bem com vocês?", "sender": "me", "name": "Você", "time": "10:05"},
        {"text": "Prontos para a aula de hoje?", "sender": "other", "name": "Ana", "time": "10:30"},
        {"text": "Claro! Já estou animada 😊", "sender": "me", "name": "Você", "time": "10:31"},
        {"text": "Nos encontramos às 15h. 🧘", "sender": "other", "name": "Ana", "time": "10:32"},
    ],
    "u1": [
        {"text": "Oi João, tudo bem?", "sender": "other", "name": "Dona Maria", "time": "Ontem"},
        {"text": "Tudo sim! E você?", "sender": "me", "name": "Você", "time": "Ontem"},
        {"text": "Que foto linda do jardim!", "sender": "other", "name": "Dona Maria", "time": "Ontem"},
        {"text": "Que foto linda!", "sender": "me", "name": "Você", "time": "Ontem"},
    ],
    "m1": [
        {"text": "Bem-vindo ao suporte!", "sender": "other", "name": "Moderador", "time": "Semana passada"},
        {"text": "Posso ajudar com a matrícula?", "sender": "other", "name": "Moderador", "time": "Ontem"},
    ],
}

# Rótulos amigáveis dos papéis (user_role -> texto exibido)
ROLE_LABEL = {"senior": "Sênior", "tutor": "Tutor(a)"}

# ---------------------------------------------------------------------------
# Estado de sessão — incluindo as variáveis de integração (1.3)
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "page": "login",
        # --- Variáveis injetadas pelo Módulo Base no login (seção 1.3) ---
        "user_id": None,        # identificador único do usuário na sessão
        "user_role": None,      # 'senior' | 'tutor' — controla o roteamento de views
        "user_name": "",
        # --- Estado das demais telas ---
        "selected_activity": None,
        "selected_chat": None,
        "activities": [dict(a) for a in SEED_ACTIVITIES],  # cópia editável (tutor cria)
        "messages": {k: list(v) for k, v in INITIAL_MESSAGES.items()},
        "enroll_status": {},    # {activity_id: 'success' | 'waitlist'}
        "font_size": "Normal",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def go(page, **kw):
    st.session_state.page = page
    for k, v in kw.items():
        st.session_state[k] = v

def is_senior() -> bool:
    return st.session_state.user_role == "senior"

def is_tutor() -> bool:
    return st.session_state.user_role == "tutor"

# ---------------------------------------------------------------------------
# Barra de navegação inferior — adaptada ao papel (user_role)
# ---------------------------------------------------------------------------
def nav_items():
    """Itens de navegação variam conforme o papel injetado na sessão."""
    if is_tutor():
        return [("📋\nAtividades", "mural"),
                ("💬\nMensagens",  "chat_list"),
                ("👤\nMeu Perfil", "profile")]
    return [("🏠\nInício",     "mural"),
            ("💬\nMensagens",  "chat_list"),
            ("👤\nMeu Perfil", "profile")]

def render_nav():
    H('<div style="height:1.5rem;"></div>')
    H(f'<div style="border-top:2px solid {C["border"]};margin-bottom:0.6rem;"></div>')
    items = nav_items()
    cols = st.columns(len(items))
    for col, (label, target) in zip(cols, items):
        with col:
            active = (st.session_state.page == target)
            if st.button(label, key=f"nav_{target}", help="nav-on" if active else "nav-off"):
                go(target)
                st.rerun()

# ---------------------------------------------------------------------------
# Tela 1 — Login (Módulo Base injeta user_id e user_role na sessão)
# ---------------------------------------------------------------------------
def page_login():
    H(f"""
    <div style="background:{C['blue']};padding:3rem 2rem 2.5rem;text-align:center;">
      <div style="font-size:5rem;margin-bottom:0.75rem;">🌻</div>
      <h1 style="color:white;font-size:2.2rem;font-weight:800;margin:0;">ComunidadeAtiva</h1>
      <p style="color:{C['blue_mid']};font-size:1.1rem;margin-top:0.4rem;">
        Conectando pessoas. Fortalecendo vínculos.
      </p>
    </div>
    <div style="background:{C['bg_card']};border-radius:28px 28px 0 0;margin-top:-1.2rem;
                padding:2rem 1.5rem 0.5rem;box-shadow:0 -4px 20px rgba(0,0,0,0.1);">
      <h2 style="color:{C['text_dark']};font-size:1.5rem;font-weight:700;margin:0 0 0.3rem 0;">
        Bem-vindo de volta! 👋
      </h2>
      <p style="color:{C['text_muted']};font-size:1rem;margin:0 0 1rem 0;">
        Entre e escolha como deseja acessar a plataforma.
      </p>
    </div>
    """)

    nome = st.text_input("👤  Seu nome", value="João da Silva",
                         placeholder="Como quer ser chamado?")
    st.text_input("🔒  Senha", type="password", placeholder="••••••••")

    # Seleção de papel — define qual View será carregada após o login
    H(f'<p style="color:{C["text_mid"]};font-weight:600;font-size:1rem;'
      f'margin:0.75rem 0 0.25rem;">Como você vai acessar?</p>')
    papel = st.radio(
        "Tipo de acesso", ["Sou Sênior", "Sou Tutor(a)"],
        label_visibility="collapsed", horizontal=True,
    )

    if st.button("Entrar  →"):
        if not nome.strip():
            st.error("Por favor, informe seu nome para entrar.")
        else:
            # --- Injeção das variáveis de sessão (seção 1.3) ---
            role = "senior" if papel == "Sou Sênior" else "tutor"
            st.session_state.user_role = role
            st.session_state.user_id = f"{role}_{datetime.now().strftime('%H%M%S')}"
            st.session_state.user_name = nome.strip()
            go("mural")
            st.rerun()

    H(f"""
    <p style="text-align:center;color:{C['text_muted']};font-size:0.95rem;margin-top:1.2rem;">
      Precisa de ajuda? Chame um mediador. 📞
    </p>
    """)

# ---------------------------------------------------------------------------
# Componente reutilizável: cartão de atividade
# ---------------------------------------------------------------------------
def activity_card(act):
    waitlist = act["spots"] == "Lista de Espera"
    s_color = C["orange"] if waitlist else C["green"]
    s_bg    = C["orange_light"] if waitlist else C["green_light"]
    s_icon  = "⏳" if waitlist else "✅"

    H(f"""
    <div style="background:white;border-radius:22px;overflow:hidden;
                box-shadow:0 3px 12px rgba(0,0,0,0.09);border:1px solid {C['border']};
                margin:0 0 0.85rem;">
      <div style="background:linear-gradient(135deg,{act['color']},{act['color']}CC);
                  height:130px;display:flex;align-items:center;justify-content:center;
                  position:relative;">
        <span style="font-size:5rem;filter:drop-shadow(0 2px 6px rgba(0,0,0,0.2));">
          {act['emoji']}
        </span>
        <div style="position:absolute;top:12px;left:14px;background:rgba(255,255,255,0.92);
                    border-radius:99px;padding:0.2rem 0.75rem;font-size:0.85rem;
                    font-weight:700;color:{act['color']};">
          {act['type']}
        </div>
      </div>
      <div style="padding:1.1rem 1.25rem 1.25rem;">
        <h4 style="color:{C['text_dark']};font-size:1.3rem;font-weight:700;margin:0 0 0.75rem 0;">
          {act['title']}
        </h4>
        <div style="display:flex;align-items:center;gap:0.5rem;color:{C['text_mid']};
                    font-size:1rem;margin-bottom:0.4rem;">
          <span style="color:{C['blue']};">🕐</span>
          <span style="color:{C['text_mid']};">{act['time']}</span>
        </div>
        <div style="display:flex;align-items:center;gap:0.5rem;color:{C['text_mid']};
                    font-size:1rem;margin-bottom:0.75rem;">
          <span style="color:{C['blue']};">👤</span>
          <span style="color:{C['text_mid']};">{act['tutor']}</span>
        </div>
        <div style="background:{s_bg};border-radius:10px;padding:0.35rem 0.75rem;
                    display:inline-block;font-size:0.9rem;font-weight:600;color:{s_color};">
          {s_icon} {act['spots']}
        </div>
      </div>
    </div>
    """)

# ---------------------------------------------------------------------------
# Tela 2 — Mural (roteia para a View correta conforme user_role)
# ---------------------------------------------------------------------------
def page_mural():
    if is_tutor():
        _mural_tutor()
    else:
        _mural_senior()

def _mural_senior():
    """View do Sênior: navega e se matricula nas atividades."""
    nome = st.session_state.user_name.split()[0]
    H(f"""
    <div style="background:{C['blue']};padding:1.5rem 1.5rem 1.75rem;
                border-radius:0 0 28px 28px;margin-bottom:1.25rem;">
      <h2 style="color:white;font-size:1.9rem;font-weight:800;margin:0 0 0.2rem 0;">
        Olá, {nome}! 👋
      </h2>
      <p style="color:{C['blue_mid']};font-size:1.1rem;margin:0;">
        O que você gostaria de fazer hoje?
      </p>
    </div>
    <h3 style="color:{C['text_dark']};font-size:1.35rem;font-weight:700;
               padding:0 0.5rem;margin:0 0 0.75rem 0;">
      📅 Atividades Disponíveis
    </h3>
    """)

    for act in st.session_state.activities:
        activity_card(act)
        if st.button("📋  Ver Detalhes", key=f"det_{act['id']}"):
            go("activity_detail", selected_activity=act["id"])
            st.rerun()
        H('<div style="height:0.4rem;"></div>')

    render_nav()

def _mural_tutor():
    """View do Tutor: gerencia e cria atividades (UC21/UC23)."""
    nome = st.session_state.user_name.split()[0]
    H(f"""
    <div style="background:{C['teal']};padding:1.5rem 1.5rem 1.75rem;
                border-radius:0 0 28px 28px;margin-bottom:1.25rem;">
      <div style="display:inline-block;background:rgba(255,255,255,0.2);border-radius:99px;
                  padding:0.15rem 0.75rem;font-size:0.85rem;font-weight:700;color:white;
                  margin-bottom:0.5rem;">👨‍🏫 Painel do Tutor</div>
      <h2 style="color:white;font-size:1.9rem;font-weight:800;margin:0 0 0.2rem 0;">
        Olá, {nome}!
      </h2>
      <p style="color:#CCFBF1;font-size:1.1rem;margin:0;">
        Gerencie as atividades da comunidade.
      </p>
    </div>
    """)

    # Ação exclusiva do tutor (controle de acesso 1.3): Criar Atividade
    if st.button("➕  Criar Nova Atividade", help="teal"):
        go("create_activity")
        st.rerun()

    H(f"""
    <h3 style="color:{C['text_dark']};font-size:1.35rem;font-weight:700;
               padding:0 0.5rem;margin:1rem 0 0.75rem 0;">
      📋 Minhas Atividades
    </h3>
    """)

    for act in st.session_state.activities:
        activity_card(act)
        if st.button("⚙️  Gerenciar", key=f"mng_{act['id']}", help="ghost"):
            go("activity_detail", selected_activity=act["id"])
            st.rerun()
        H('<div style="height:0.4rem;"></div>')

    render_nav()

# ---------------------------------------------------------------------------
# Tela 2b — Criar Atividade (acessível somente ao Tutor)
# ---------------------------------------------------------------------------
def page_create_activity():
    # Guarda de acesso — reforça o controle do 1.3 mesmo se a rota for forçada
    if not is_tutor():
        st.error("Acesso restrito a tutores.")
        if st.button("← Voltar"):
            go("mural"); st.rerun()
        return

    if st.button("← Voltar", key="back_create", help="ghost"):
        go("mural"); st.rerun()

    H(f"""
    <div style="background:{C['teal']};padding:1.75rem 1.5rem;border-radius:0 0 24px 24px;
                margin-top:-0.5rem;margin-bottom:1.25rem;">
      <h2 style="color:white;font-size:1.6rem;font-weight:800;margin:0;">➕ Criar Atividade</h2>
      <p style="color:#CCFBF1;font-size:1rem;margin:0.25rem 0 0;">
        Preencha os dados para publicar no mural.
      </p>
    </div>
    """)

    with st.form("create_activity_form", clear_on_submit=False):
        titulo = st.text_input("Título da atividade", placeholder="Ex: Alongamento Matinal")
        tipo   = st.selectbox("Tipo", list(TYPE_STYLE.keys()))
        horario= st.text_input("Quando acontece?", placeholder="Ex: Segunda, 09:00")
        local  = st.text_input("Onde / Como", placeholder="Ex: Ao vivo (Vídeo)")
        vagas  = st.selectbox("Disponibilidade", ["Vagas abertas", "Lista de Espera"])
        desc   = st.text_area("Descrição", placeholder="Conte do que se trata a atividade...")
        publicar = st.form_submit_button("✅  Publicar Atividade")

        if publicar:
            if not titulo.strip():
                st.error("Informe ao menos o título da atividade.")
            else:
                emoji, color = TYPE_STYLE.get(tipo, ("📌", C["blue"]))
                new_act = {
                    "id": f"new_{datetime.now().strftime('%H%M%S')}",
                    "title": titulo.strip(),
                    "tutor": st.session_state.user_name,  # autor = tutor logado
                    "time": horario.strip() or "A definir",
                    "location": local.strip() or "A definir",
                    "type": tipo,
                    "spots": vagas,
                    "emoji": emoji,
                    "color": color,
                    "description": desc.strip() or "Sem descrição.",
                }
                st.session_state.activities.insert(0, new_act)
                st.success(f"Atividade “{new_act['title']}” publicada no mural!")

    H('<div style="height:0.4rem;"></div>')
    if st.button("📋  Voltar ao Painel", help="ghost"):
        go("mural"); st.rerun()

# ---------------------------------------------------------------------------
# Tela 3 — Detalhe da Atividade (botão de ação depende do user_role)
# ---------------------------------------------------------------------------
def page_activity_detail():
    act = next((a for a in st.session_state.activities
                if a["id"] == st.session_state.selected_activity), None)
    if not act:
        st.error("Atividade não encontrada.")
        if st.button("← Voltar"):
            go("mural"); st.rerun()
        return

    if st.button("← Voltar", key="back_detail", help="ghost"):
        go("mural"); st.rerun()

    H(f"""
    <div style="background:linear-gradient(135deg,{act['color']},{act['color']}BB);
                height:200px;display:flex;align-items:center;justify-content:center;">
      <span style="font-size:6rem;">{act['emoji']}</span>
    </div>
    <div style="background:white;border-radius:28px 28px 0 0;margin-top:-1.5rem;
                padding:1.75rem 1.5rem 0.5rem;position:relative;z-index:2;">
      <h2 style="color:{C['text_dark']};font-size:1.6rem;font-weight:800;margin:0 0 1rem 0;">
        {act['title']}
      </h2>
    </div>
    <div style="background:{C['blue_light']};border-radius:16px;padding:1rem 1.25rem;
                margin:0 0 1.25rem 0;">
      <div style="font-size:1.05rem;color:{C['text_mid']};margin:0.35rem 0;">
        🕐 <b style="color:{C['text_dark']};">{act['time']}</b></div>
      <div style="font-size:1.05rem;color:{C['text_mid']};margin:0.35rem 0;">
        📍 <b style="color:{C['text_dark']};">{act['location']}</b></div>
      <div style="font-size:1.05rem;color:{C['text_mid']};margin:0.35rem 0;">
        👤 <b style="color:{C['text_dark']};">Professor: {act['tutor']}</b></div>
      <div style="font-size:1.05rem;color:{C['text_mid']};margin:0.35rem 0;">
        🎟️ <b style="color:{C['text_dark']};">{act['spots']}</b></div>
    </div>
    <h3 style="color:{C['text_dark']};font-size:1.2rem;font-weight:700;margin:0 0 0.4rem 0;">
      Sobre a atividade
    </h3>
    <p style="color:{C['text_mid']};font-size:1.05rem;line-height:1.65;margin:0 0 1.25rem 0;">
      {act['description']}
    </p>
    """)

    # === Roteamento de ação por papel (núcleo da seção 1.3) ===
    if is_tutor():
        _detail_actions_tutor(act)
    else:
        _detail_actions_senior(act)

def _detail_actions_senior(act):
    """Sênior: pode realizar matrícula / entrar na lista de espera."""
    status   = st.session_state.enroll_status.get(act["id"], "idle")
    waitlist = act["spots"] == "Lista de Espera"

    if status == "success":
        H(f"""
        <div style="background:{C['green_light']};border:2px solid {C['green']};
                    border-radius:16px;padding:1rem 1.25rem;margin-bottom:1rem;">
          <b style="color:{C['green']};font-size:1.15rem;">✅ Matrícula Confirmada!</b><br>
          <span style="color:#166534;font-size:1rem;">
            Sua vaga está garantida. Adicionamos na sua agenda.</span>
        </div>
        """)
        # Permite desfazer a matrícula
        if st.button("❌  Cancelar Matrícula", help="red"):
            st.session_state.enroll_status.pop(act["id"], None)
            st.rerun()
        H('<div style="height:0.3rem;"></div>')
        if st.button("🏠  Voltar para o Início", help="ghost"):
            go("mural"); st.rerun()

    elif status == "waitlist":
        H(f"""
        <div style="background:{C['orange_light']};border:2px solid {C['orange']};
                    border-radius:16px;padding:1rem 1.25rem;margin-bottom:1rem;">
          <b style="color:{C['orange']};font-size:1.15rem;">⏳ Na lista de espera!</b><br>
          <span style="color:#7c2d12;font-size:1rem;">
            Avisaremos se abrir uma vaga para você.</span>
        </div>
        """)
        # Permite sair da lista de espera
        if st.button("❌  Sair da Lista de Espera", help="red"):
            st.session_state.enroll_status.pop(act["id"], None)
            st.rerun()
        H('<div style="height:0.3rem;"></div>')
        if st.button("🏠  Voltar para o Início", help="ghost"):
            go("mural"); st.rerun()

    else:
        if waitlist:
            if st.button("⏳  Entrar na Lista de Espera", help="orange"):
                st.session_state.enroll_status[act["id"]] = "waitlist"; st.rerun()
        else:
            if st.button("✅  Realizar Matrícula"):
                st.session_state.enroll_status[act["id"]] = "success"; st.rerun()
        # Permite voltar ao mural sem se matricular
        H('<div style="height:0.3rem;"></div>')
        if st.button("🏠  Voltar para o Início", help="ghost"):
            go("mural"); st.rerun()

def _detail_actions_tutor(act):
    """Tutor: não se matricula; vê painel de gestão da atividade."""
    H(f"""
    <div style="background:{C['teal_light']};border:2px solid {C['teal']};
                border-radius:16px;padding:1rem 1.25rem;margin-bottom:1rem;">
      <b style="color:{C['teal']};font-size:1.1rem;">👨‍🏫 Você está gerenciando esta atividade</b><br>
      <span style="color:#115E59;font-size:1rem;">
        Participantes inscritos: 0 · Status: {act['spots']}</span>
    </div>
    """)
    if st.button("🗑️  Remover Atividade", help="red"):
        st.session_state.activities = [
            a for a in st.session_state.activities if a["id"] != act["id"]
        ]
        go("mural"); st.rerun()
    H('<div style="height:0.3rem;"></div>')
    if st.button("📋  Voltar ao Painel", help="ghost"):
        go("mural"); st.rerun()

# ---------------------------------------------------------------------------
# Tela 4 — Lista de Conversas
# ---------------------------------------------------------------------------
def page_chat_list():
    H(f"""
    <div style="background:{C['blue']};padding:1.4rem 1.5rem 1.7rem;
                border-radius:0 0 28px 28px;margin-bottom:1.25rem;">
      <h2 style="color:white;font-size:1.8rem;font-weight:800;margin:0;">💬 Minhas Conversas</h2>
    </div>
    """)

    for chat in CHATS:
        unread_html = ""
        if chat["unread"] > 0:
            unread_html = (f'<span style="background:{C["blue"]};color:white;border-radius:99px;'
                           f'padding:0.1rem 0.55rem;font-size:0.85rem;font-weight:700;'
                           f'margin-left:0.4rem;">{chat["unread"]}</span>')
        last_weight = "700" if chat["unread"] > 0 else "400"
        av_bg = "#FEF2F2" if chat["type"] == "support" else C["blue_light"]

        H(f"""
        <div style="background:white;border-radius:18px;padding:1rem 1.25rem;
                    margin:0 0 0.65rem;box-shadow:0 2px 8px rgba(0,0,0,0.07);
                    border:1px solid {C['border']};display:flex;align-items:center;gap:1rem;">
          <div style="width:60px;height:60px;border-radius:50%;background:{av_bg};
                      display:flex;align-items:center;justify-content:center;
                      font-size:1.9rem;flex-shrink:0;">{chat['emoji']}</div>
          <div style="flex:1;min-width:0;">
            <div style="display:flex;justify-content:space-between;align-items:center;
                        margin-bottom:0.2rem;">
              <span style="color:{C['text_dark']};font-size:1.1rem;font-weight:700;">
                {chat['name']}</span>
              <span style="color:{C['text_muted']};font-size:0.85rem;">
                {chat['time']}{unread_html}</span>
            </div>
            <span style="color:{C['text_muted']};font-size:0.95rem;font-weight:{last_weight};
                         white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block;">
              {chat['last']}</span>
          </div>
        </div>
        """)

        if st.button("Abrir conversa →", key=f"open_{chat['id']}"):
            go("chat_room", selected_chat=chat["id"])
            st.rerun()
        H('<div style="height:0.3rem;"></div>')

    render_nav()

# ---------------------------------------------------------------------------
# Tela 5 — Sala de Chat
# ---------------------------------------------------------------------------
def page_chat_room():
    chat = next((c for c in CHATS if c["id"] == st.session_state.selected_chat), None)
    if not chat:
        if st.button("← Voltar"):
            go("chat_list"); st.rerun()
        return

    H(f"""
    <div style="background:{C['blue']};padding:1.1rem 1.5rem;border-radius:0 0 20px 20px;
                margin-bottom:0.75rem;display:flex;align-items:center;gap:0.75rem;">
      <span style="font-size:2rem;">{chat['emoji']}</span>
      <span style="color:white;font-size:1.4rem;font-weight:700;">{chat['name']}</span>
    </div>
    """)

    if st.button("← Voltar", key="back_chat", help="ghost"):
        go("chat_list"); st.rerun()

    H('<div style="background:#E8EEF5;border-radius:16px;padding:0.75rem;margin:0.5rem 0;">')

    is_group = chat["type"] == "group"
    for msg in st.session_state.messages.get(chat["id"], []):
        if msg["sender"] == "me":
            H(f"""
            <div style="background:#D1FAE5;border-radius:18px 18px 4px 18px;
                        padding:0.7rem 1rem;margin:0.4rem 0 0.4rem 3rem;
                        box-shadow:0 1px 4px rgba(0,0,0,0.08);">
              <span style="color:{C['text_dark']};font-size:1.05rem;">{msg['text']}</span>
              <div style="color:{C['text_muted']};font-size:0.75rem;text-align:right;
                          margin-top:0.2rem;">{msg['time']}</div>
            </div>
            """)
        else:
            sender = (f'<div style="color:{C["blue"]};font-size:0.85rem;font-weight:700;'
                      f'margin-bottom:0.15rem;">{msg["name"]}</div>' if is_group else "")
            H(f"""
            <div style="background:white;border-radius:18px 18px 18px 4px;
                        padding:0.7rem 1rem;margin:0.4rem 3rem 0.4rem 0;
                        box-shadow:0 1px 4px rgba(0,0,0,0.08);">
              {sender}
              <span style="color:{C['text_dark']};font-size:1.05rem;">{msg['text']}</span>
              <div style="color:{C['text_muted']};font-size:0.75rem;text-align:right;
                          margin-top:0.2rem;">{msg['time']}</div>
            </div>
            """)

    H('</div>')

    with st.form(key=f"form_{chat['id']}", clear_on_submit=True):
        col_in, col_btn = st.columns([5, 1])
        with col_in:
            text = st.text_input("msg", placeholder="Digite aqui...",
                                 label_visibility="collapsed")
        with col_btn:
            send = st.form_submit_button("📤")
        if send and text.strip():
            now = datetime.now().strftime("%H:%M")
            st.session_state.messages[chat["id"]].append(
                {"text": text.strip(), "sender": "me", "name": "Você", "time": now})
            st.rerun()

# ---------------------------------------------------------------------------
# Tela 6 — Perfil (mostra o papel ativo na sessão)
# ---------------------------------------------------------------------------
def page_profile():
    nome = st.session_state.user_name
    role_txt = ROLE_LABEL.get(st.session_state.user_role, "Membro")

    H(f"""
    <div style="background:{C['blue']};padding:2rem 1.5rem 2.25rem;
                border-radius:0 0 28px 28px;text-align:center;margin-bottom:1.25rem;">
      <div style="width:90px;height:90px;background:rgba(255,255,255,0.2);border-radius:50%;
                  margin:0 auto 0.75rem;display:flex;align-items:center;justify-content:center;
                  font-size:3rem;">👤</div>
      <h2 style="color:white;font-size:1.6rem;font-weight:800;margin:0 0 0.3rem 0;">{nome}</h2>
      <span style="display:inline-block;background:rgba(255,255,255,0.2);color:white;
                   border-radius:99px;padding:0.15rem 0.85rem;font-size:0.9rem;font-weight:700;">
        {role_txt}
      </span>
    </div>
    <div style="background:white;border-radius:18px;padding:1.25rem 1.4rem;margin:0 0 0.85rem;
                box-shadow:0 2px 8px rgba(0,0,0,0.06);border:1px solid {C['border']};">
      <h3 style="color:{C['text_dark']};font-size:1.15rem;font-weight:700;margin:0 0 0.2rem;">
        ⚙️ Acessibilidade</h3>
      <p style="color:{C['text_muted']};font-size:0.95rem;margin:0;">Ajuste o tamanho da letra</p>
    </div>
    """)

    font = st.select_slider("Tamanho da letra",
                            options=["Pequeno", "Normal", "Grande", "Muito grande"],
                            value=st.session_state.get("font_size", "Normal"))
    st.session_state.font_size = font
    sizes = {"Pequeno": "15px", "Normal": "18px", "Grande": "22px", "Muito grande": "26px"}
    st.markdown(f"<style>html,body{{font-size:{sizes[font]}!important;}}</style>",
                unsafe_allow_html=True)

    H(f"""
    <div style="background:white;border-radius:18px;padding:1.25rem 1.4rem;margin:0.85rem 0;
                box-shadow:0 2px 8px rgba(0,0,0,0.06);border:1px solid {C['border']};">
      <h3 style="color:{C['text_dark']};font-size:1.15rem;font-weight:700;margin:0 0 0.2rem;">
        🛡️ Meus Dados</h3>
      <p style="color:{C['text_muted']};font-size:0.95rem;margin:0;">Atualize seu nome ou senha</p>
    </div>
    """)

    new_name = st.text_input("Seu nome", value=nome)
    st.text_input("Nova senha (opcional)", type="password", placeholder="••••••••")

    if st.button("💾  Salvar Alterações"):
        st.session_state.user_name = new_name.strip() or nome
        st.success("✅ Dados atualizados com sucesso!")

    H('<div style="height:0.5rem;"></div>')

    # Logout — limpa toda a sessão (incluindo user_role/user_id) e volta ao login
    if st.button("🚪  Sair do Aplicativo", help="red"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_state()
        st.rerun()

    render_nav()

# ---------------------------------------------------------------------------
# Roteador principal — protege rotas internas exigindo sessão autenticada
# ---------------------------------------------------------------------------
PAGES = {
    "login":            page_login,
    "mural":            page_mural,
    "create_activity":  page_create_activity,
    "activity_detail":  page_activity_detail,
    "chat_list":        page_chat_list,
    "chat_room":        page_chat_room,
    "profile":          page_profile,
}

# Guarda global: sem user_role na sessão, só a tela de login é acessível
if st.session_state.user_role is None and st.session_state.page != "login":
    st.session_state.page = "login"

PAGES.get(st.session_state.page, page_login)()
