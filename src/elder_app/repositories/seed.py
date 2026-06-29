"""
Dados-semente (sementes) usados para popular o banco na primeira execução.

Antes da existência do backend, esses dados moravam diretamente na View
(``mvp_streamlit/app.py``). Movê-los para a camada de dados respeita a
Separação de Responsabilidades: a View deixa de conhecer dados iniciais.
"""

# Atividades iniciais do mural. ``total_spots``/``remaining_spots`` substituem
# o antigo rótulo textual de vagas — o rótulo passa a ser derivado (ver
# ``Activity.spots_label``). "Roda de Conversa" começa sem vagas (lista de espera).
SEED_ACTIVITIES = [
    {
        "title": "Yoga na Cadeira",
        "tutor_name": "Prof. Ana Maria",
        "time": "Hoje, 15:00",
        "location": "Ao vivo (Vídeo)",
        "type": "Exercício Físico",
        "total_spots": 12,
        "remaining_spots": 12,
        "emoji": "🧘",
        "color": "#2563EB",
        "description": (
            "Uma aula leve e relaxante feita especialmente para você, "
            "sem precisar levantar da cadeira. Ótimo para circulação e bem-estar."
        ),
    },
    {
        "title": "Roda de Conversa: Livros",
        "tutor_name": "Mediador Carlos",
        "time": "Amanhã, 10:00",
        "location": "Sala de Chat",
        "type": "Social",
        "total_spots": 8,
        "remaining_spots": 0,
        "emoji": "📚",
        "color": "#7C3AED",
        "description": (
            "Vamos conversar sobre nossas leituras favoritas e conhecer novos "
            "amigos. Traga seu cafezinho!"
        ),
    },
    {
        "title": "Pintura com Aquarela",
        "tutor_name": "Profa. Beatriz",
        "time": "Sexta, 14:00",
        "location": "Ao vivo (Vídeo)",
        "type": "Arte",
        "total_spots": 10,
        "remaining_spots": 10,
        "emoji": "🎨",
        "color": "#DC2626",
        "description": (
            "Aprenda técnicas simples de aquarela em um ambiente acolhedor. "
            "Nenhuma experiência anterior necessária — só boa vontade!"
        ),
    },
]

# Conversas-semente do módulo de comunicação social.
SEED_CONVERSATIONS = [
    {"id": "g1", "name": "Turma de Yoga", "type": "group",
     "emoji": "👥", "last_message": "Ana: Nos vemos às 15h!", "last_time": "10:30", "unread": 2},
    {"id": "u1", "name": "Dona Maria", "type": "private",
     "emoji": "👩", "last_message": "Você: Que foto linda!", "last_time": "Ontem", "unread": 0},
    {"id": "m1", "name": "Suporte / Moderador", "type": "support",
     "emoji": "🛡️", "last_message": "Moderador: Posso ajudar?", "last_time": "Ontem", "unread": 0},
]

# Mensagens-semente por conversa (``sender`` = 'me' | 'other').
SEED_MESSAGES = {
    "g1": [
        {"sender": "other", "sender_name": "Ana", "text": "Olá pessoal!", "time": "10:00"},
        {"sender": "me", "sender_name": "Você", "text": "Oi! Tudo bem com vocês?", "time": "10:05"},
        {"sender": "other", "sender_name": "Ana", "text": "Prontos para a aula de hoje?", "time": "10:30"},
        {"sender": "me", "sender_name": "Você", "text": "Claro! Já estou animada 😊", "time": "10:31"},
        {"sender": "other", "sender_name": "Ana", "text": "Nos encontramos às 15h. 🧘", "time": "10:32"},
    ],
    "u1": [
        {"sender": "other", "sender_name": "Dona Maria", "text": "Oi João, tudo bem?", "time": "Ontem"},
        {"sender": "me", "sender_name": "Você", "text": "Tudo sim! E você?", "time": "Ontem"},
        {"sender": "other", "sender_name": "Dona Maria", "text": "Que foto linda do jardim!", "time": "Ontem"},
        {"sender": "me", "sender_name": "Você", "text": "Que foto linda!", "time": "Ontem"},
    ],
    "m1": [
        {"sender": "other", "sender_name": "Moderador", "text": "Bem-vindo ao suporte!", "time": "Semana passada"},
        {"sender": "other", "sender_name": "Moderador", "text": "Posso ajudar com a matrícula?", "time": "Ontem"},
    ],
}
