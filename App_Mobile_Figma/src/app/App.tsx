import { useState } from "react";
import {
  Bell, Home, MessageCircle, User, Clock,
  UserCircle, ChevronRight, CheckCircle, Plus, Users,
  Edit2, Sliders, Headphones, LogOut, Mail,
  X, ArrowLeft, Phone, MapPin, Save, Calendar, AlertCircle,
} from "lucide-react";
import { ActivityDetailsScreen } from "./components/ActivityDetailsScreen";
import { ChatScreen } from "./components/ChatScreen";

/* MARKER-MAKE-KIT-INVOKED */
/* MARKER-MAKE-KIT-DISCOVERY-READ */

type MainScreen = "home" | "messages" | "profile";

// ─── Data ────────────────────────────────────────────────────────────────────

const enrolledActivity = {
  id: "gym",
  title: "Aula de Ginástica",
  time: "15:00 – 16:00",
  date: "Hoje, 13 de Junho de 2026",
  tutor: "Prof. Ana Souza",
  tutorBio: "Especialista em educação física para terceira idade. Mais de 15 anos de experiência com grupos sênior.",
  location: "Sala Virtual 3",
  description:
    "Aula de ginástica leve focada em mobilidade, equilíbrio e fortalecimento muscular. Exercícios adaptados para o público sênior, sem impacto e com atenção individualizada. Traga roupas confortáveis e uma garrafa de água.",
  participants: 12,
  maxParticipants: 20,
  level: "Iniciante",
  category: "Saúde",
  color: "#1a4fba",
};

const availableActivities = [
  { id: "yoga", title: "Yoga para Idosos", time: "Amanhã, 10:00", tutor: "Prof. Carlos Lima", category: "Saúde" },
  { id: "art", title: "Pintura em Aquarela", time: "Quinta, 14:00", tutor: "Profa. Marta Alves", category: "Arte" },
  { id: "tech", title: "Informática Básica", time: "Sexta, 09:00", tutor: "Prof. Roberto Cruz", category: "Tecnologia" },
];

const conversations = [
  {
    id: 1, name: "Grupo: Ginástica", isGroup: true, avatarColor: "#1a4fba", avatarInitials: "GG",
    lastMessage: "Professora: A aula de hoje está confirmada!", time: "10:32", unread: 3, online: false,
  },
  {
    id: 2, name: "Tutora Maria", isGroup: false, avatarColor: "#0d6e4e", avatarInitials: "TM",
    lastMessage: "Nos vemos na próxima aula, João!", time: "Ontem", unread: 0, online: true,
  },
  {
    id: 3, name: "Amigo Carlos", isGroup: false, avatarColor: "#7c3aed", avatarInitials: "AC",
    lastMessage: "Vai na aula de ginástica hoje?", time: "09:26", unread: 1, online: true,
  },
];

const notificationsData = [
  { id: 1, type: "success", title: "Matrícula confirmada!", body: "Sua inscrição em Yoga para Idosos foi confirmada com sucesso.", time: "Há 5 min", read: false },
  { id: 2, type: "message", title: "Nova mensagem", body: "Tutora Maria: Nos vemos na próxima aula, João!", time: "Há 1 hora", read: false },
  { id: 3, type: "warning", title: "Aula cancelada", body: "A aula de Informática Básica de sexta-feira foi cancelada.", time: "Ontem", read: true },
];

const contactsData = [
  { id: 1, name: "Tutora Maria", initials: "TM", color: "#0d6e4e", role: "Tutora", isGroup: false, online: true },
  { id: 2, name: "Amigo Carlos", initials: "AC", color: "#7c3aed", role: "Amigo", isGroup: false, online: true },
  { id: 3, name: "Prof. Carlos Lima", initials: "CL", color: "#b45309", role: "Tutor", isGroup: false, online: false },
  { id: 4, name: "Grupo: Ginástica", initials: "GG", color: "#1a4fba", role: "Grupo", isGroup: true, online: false },
  { id: 5, name: "Grupo: Aquarela", initials: "GA", color: "#be185d", role: "Grupo", isGroup: true, online: false },
];

const initialProfile = {
  name: "João Silva",
  email: "joao.silva@email.com",
  phone: "(11) 98765-4321",
  address: "Rua das Flores, 123",
  city: "São Paulo – SP",
  birthdate: "15/03/1955",
};

// ─── Shared components ────────────────────────────────────────────────────────

function StatusBar() {
  return (
    <div className="px-5 pt-3 pb-2 flex items-center justify-between shrink-0 bg-primary">
      <span className="text-primary-foreground" style={{ fontSize: 14, fontWeight: 600 }}>09:41</span>
      <span className="text-primary-foreground" style={{ fontSize: 13, opacity: 0.8 }}>●●●</span>
    </div>
  );
}

function NotificationBell({ count, onOpen }: { count: number; onOpen: () => void }) {
  return (
    <button
      onClick={onOpen}
      aria-label={`${count} notificações`}
      style={{ minWidth: 52, minHeight: 52 }}
      className="relative flex items-center justify-center rounded-full bg-white/20 active:bg-white/30 transition-colors"
    >
      <Bell size={28} strokeWidth={2} className="text-white" />
      {count > 0 && (
        <span aria-hidden className="absolute top-1 right-1 bg-destructive text-destructive-foreground rounded-full flex items-center justify-center" style={{ width: 20, height: 20, fontSize: 12, fontWeight: 700 }}>
          {count}
        </span>
      )}
    </button>
  );
}

function BottomNav({ active, onChange }: { active: MainScreen; onChange: (s: MainScreen) => void }) {
  const items: { id: MainScreen; label: string; icon: React.ReactNode; badge?: number }[] = [
    { id: "home", label: "Início", icon: <Home size={28} strokeWidth={2} /> },
    { id: "messages", label: "Mensagens", icon: <MessageCircle size={28} strokeWidth={2} />, badge: 4 },
    { id: "profile", label: "Perfil", icon: <User size={28} strokeWidth={2} /> },
  ];
  return (
    <nav className="bg-card border-t-2 border-border px-2 pt-2 pb-4 shrink-0">
      <div className="flex">
        {items.map(({ id, label, icon, badge }) => {
          const isActive = active === id;
          return (
            <button
              key={id}
              onClick={() => onChange(id)}
              aria-label={label}
              aria-current={isActive ? "page" : undefined}
              style={{ minHeight: 64 }}
              className={`flex-1 relative flex flex-col items-center justify-center gap-1 rounded-xl transition-colors ${isActive ? "bg-secondary" : "active:bg-secondary"}`}
            >
              <span className={`relative ${isActive ? "text-primary" : "text-muted-foreground"}`}>
                {icon}
                {badge && !isActive && (
                  <span className="absolute -top-1 -right-1 bg-destructive text-destructive-foreground rounded-full flex items-center justify-center" style={{ width: 18, height: 18, fontSize: 11, fontWeight: 700 }}>
                    {badge}
                  </span>
                )}
              </span>
              <span style={{ fontSize: 13, fontWeight: isActive ? 700 : 500 }} className={isActive ? "text-primary" : "text-muted-foreground"}>
                {label}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}

// ─── Notifications Panel ──────────────────────────────────────────────────────

function NotificationsPanel({ onClose }: { onClose: () => void }) {
  const [items, setItems] = useState(notificationsData);

  function markAllRead() {
    setItems((prev) => prev.map((n) => ({ ...n, read: true })));
  }

  const unreadCount = items.filter((n) => !n.read).length;

  const iconForType: Record<string, React.ReactNode> = {
    success: <CheckCircle size={22} className="text-green-600" />,
    message: <MessageCircle size={22} className="text-primary" />,
    warning: <AlertCircle size={22} className="text-amber-500" />,
  };

  return (
    <div className="absolute inset-0 z-50 flex flex-col bg-background">
      <div className="bg-primary px-5 py-5 shrink-0 flex items-center justify-between">
        <h1 className="text-primary-foreground" style={{ fontSize: 24, fontWeight: 800 }}>Notificações</h1>
        <button
          onClick={onClose}
          aria-label="Fechar notificações"
          style={{ minWidth: 48, minHeight: 48 }}
          className="bg-white/20 rounded-full flex items-center justify-center active:bg-white/30 transition-colors"
        >
          <X size={26} className="text-white" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 pt-4 pb-6">
        {unreadCount > 0 && (
          <div className="flex items-center justify-between mb-4">
            <span className="text-muted-foreground" style={{ fontSize: 15 }}>
              {unreadCount} não lida{unreadCount > 1 ? "s" : ""}
            </span>
            <button
              onClick={markAllRead}
              className="text-primary active:opacity-70 transition-opacity"
              style={{ fontSize: 15, fontWeight: 700 }}
            >
              Marcar todas como lidas
            </button>
          </div>
        )}

        <div className="flex flex-col gap-3">
          {items.map((notif) => (
            <div
              key={notif.id}
              className={`bg-card rounded-2xl p-4 border-2 flex gap-4 ${notif.read ? "border-border" : "border-primary/30 bg-blue-50/50"}`}
            >
              <div className="shrink-0 mt-0.5">{iconForType[notif.type]}</div>
              <div className="flex-1 min-w-0">
                <p className="text-foreground" style={{ fontSize: 17, fontWeight: notif.read ? 500 : 700, lineHeight: 1.3 }}>
                  {notif.title}
                </p>
                <p className="text-muted-foreground mt-1" style={{ fontSize: 15, lineHeight: 1.4 }}>
                  {notif.body}
                </p>
                <p className="text-muted-foreground mt-2" style={{ fontSize: 13 }}>
                  {notif.time}
                </p>
              </div>
              {!notif.read && (
                <div className="w-2.5 h-2.5 rounded-full bg-primary shrink-0 mt-1.5" />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Home Screen ─────────────────────────────────────────────────────────────

function EnrolledActivityCard({ onViewDetails }: { onViewDetails: () => void }) {
  return (
    <div className="bg-primary rounded-2xl p-6 shadow-md">
      <div className="flex items-center gap-2 mb-2">
        <CheckCircle size={20} className="text-primary-foreground" style={{ opacity: 0.85 }} />
        <span className="text-primary-foreground" style={{ fontSize: 14, fontWeight: 600, opacity: 0.85 }}>INSCRITO</span>
      </div>
      <h3 className="text-primary-foreground" style={{ fontSize: 22, fontWeight: 700, lineHeight: 1.3 }}>
        {enrolledActivity.title}
      </h3>
      <div className="flex items-center gap-2 mt-2 mb-1">
        <Clock size={18} className="text-primary-foreground" style={{ opacity: 0.8 }} />
        <span className="text-primary-foreground" style={{ fontSize: 17, opacity: 0.9 }}>Hoje, 15:00</span>
      </div>
      <div className="flex items-center gap-2 mb-5">
        <UserCircle size={18} className="text-primary-foreground" style={{ opacity: 0.8 }} />
        <span className="text-primary-foreground" style={{ fontSize: 17, opacity: 0.9 }}>{enrolledActivity.tutor}</span>
      </div>
      <button
        onClick={onViewDetails}
        style={{ minHeight: 56, fontSize: 18, fontWeight: 700 }}
        className="w-full bg-white text-primary rounded-xl flex items-center justify-center gap-2 active:opacity-80 transition-opacity shadow"
      >
        Entrar na Sala <ChevronRight size={22} />
      </button>
    </div>
  );
}

function AvailableActivityCard({ activity }: { activity: typeof availableActivities[0] }) {
  const [enrolled, setEnrolled] = useState(false);
  const [confirming, setConfirming] = useState(false);

  if (confirming) {
    return (
      <div className="bg-card rounded-2xl p-5 shadow-sm border-2 border-destructive/40">
        <h3 className="text-foreground mb-2" style={{ fontSize: 20, fontWeight: 700 }}>{activity.title}</h3>
        <p className="text-muted-foreground mb-5" style={{ fontSize: 16, lineHeight: 1.4 }}>
          Tem certeza que deseja cancelar sua matrícula nesta atividade?
        </p>
        <div className="flex gap-3">
          <button
            onClick={() => setConfirming(false)}
            style={{ minHeight: 56, fontSize: 17, fontWeight: 700 }}
            className="flex-1 rounded-xl bg-secondary text-foreground active:opacity-80 transition-opacity"
          >
            Manter
          </button>
          <button
            onClick={() => { setEnrolled(false); setConfirming(false); }}
            style={{ minHeight: 56, fontSize: 17, fontWeight: 700 }}
            className="flex-1 rounded-xl bg-destructive text-destructive-foreground active:opacity-80 transition-opacity"
          >
            Cancelar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card rounded-2xl p-5 shadow-sm border border-border">
      <div className="flex items-start justify-between gap-3 mb-3">
        <h3 className="text-foreground" style={{ fontSize: 20, fontWeight: 700, lineHeight: 1.3 }}>{activity.title}</h3>
        <span className="bg-secondary text-secondary-foreground rounded-full px-3 py-1 shrink-0" style={{ fontSize: 13, fontWeight: 600 }}>
          {activity.category}
        </span>
      </div>
      <div className="flex items-center gap-2 mb-1">
        <Clock size={18} className="text-muted-foreground shrink-0" />
        <span className="text-foreground" style={{ fontSize: 17 }}>{activity.time}</span>
      </div>
      <div className="flex items-center gap-2 mb-5">
        <UserCircle size={18} className="text-muted-foreground shrink-0" />
        <span className="text-muted-foreground" style={{ fontSize: 16 }}>{activity.tutor}</span>
      </div>

      {enrolled ? (
        <div className="flex flex-col gap-3">
          <div
            className="w-full rounded-xl flex items-center justify-center gap-2 bg-green-50 border-2 border-green-500"
            style={{ minHeight: 52, fontSize: 17, fontWeight: 700, color: "#16a34a" }}
          >
            <CheckCircle size={22} className="text-green-600" /> Matriculado!
          </div>
          <button
            onClick={() => setConfirming(true)}
            style={{ minHeight: 52, fontSize: 16, fontWeight: 600 }}
            className="w-full rounded-xl border-2 border-destructive/50 text-destructive active:bg-destructive/10 transition-colors"
          >
            Cancelar Matrícula
          </button>
        </div>
      ) : (
        <button
          onClick={() => setEnrolled(true)}
          style={{ minHeight: 56, fontSize: 18, fontWeight: 700 }}
          className="w-full rounded-xl flex items-center justify-center gap-2 bg-primary text-primary-foreground active:opacity-80 transition-opacity"
        >
          Realizar Matrícula
        </button>
      )}
    </div>
  );
}

function HomeScreen({ onViewDetails }: { onViewDetails: () => void }) {
  return (
    <div className="flex-1 overflow-y-auto px-4 pb-6 pt-2">
      <section className="mb-6">
        <h2 className="text-foreground mb-4" style={{ fontSize: 21, fontWeight: 700 }}>Minhas Atividades</h2>
        <EnrolledActivityCard onViewDetails={onViewDetails} />
      </section>
      <section>
        <h2 className="text-foreground mb-4" style={{ fontSize: 21, fontWeight: 700 }}>Atividades Disponíveis</h2>
        <div className="flex flex-col gap-4">
          {availableActivities.map((a) => <AvailableActivityCard key={a.id} activity={a} />)}
        </div>
      </section>
    </div>
  );
}

// ─── Messages Screen ──────────────────────────────────────────────────────────

function ConvAvatar({ conv }: { conv: typeof conversations[0] }) {
  return (
    <div className="relative shrink-0">
      <div className="rounded-full flex items-center justify-center" style={{ width: 60, height: 60, background: conv.avatarColor }}>
        {conv.isGroup
          ? <Users size={28} className="text-white" />
          : <span className="text-white" style={{ fontSize: 20, fontWeight: 700 }}>{conv.avatarInitials}</span>
        }
      </div>
      {conv.online && !conv.isGroup && (
        <span aria-label="Online" className="absolute bottom-0.5 right-0.5 bg-green-500 rounded-full border-2 border-card" style={{ width: 14, height: 14 }} />
      )}
    </div>
  );
}

function ContactListPanel({ onClose, onSelect }: {
  onClose: () => void;
  onSelect: (c: typeof contactsData[0]) => void;
}) {
  return (
    <div className="absolute inset-0 z-40 flex flex-col bg-background">
      <div className="bg-primary px-5 py-5 shrink-0 flex items-center gap-4">
        <button
          onClick={onClose}
          aria-label="Voltar"
          style={{ minWidth: 48, minHeight: 48 }}
          className="bg-white/20 rounded-full flex items-center justify-center active:bg-white/30 transition-colors shrink-0"
        >
          <ArrowLeft size={26} className="text-white" />
        </button>
        <h1 className="text-primary-foreground flex-1" style={{ fontSize: 22, fontWeight: 800 }}>Nova Mensagem</h1>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="px-5 pt-4 pb-2">
          <span className="text-muted-foreground" style={{ fontSize: 14, fontWeight: 600, letterSpacing: "0.06em" }}>
            SELECIONE UM CONTATO
          </span>
        </div>
        <div className="px-4 pb-6">
          <div className="bg-card rounded-3xl border-2 border-border overflow-hidden shadow-sm">
            {contactsData.map((contact, i, arr) => (
              <button
                key={contact.id}
                onClick={() => onSelect(contact)}
                style={{ minHeight: 76 }}
                className={`w-full flex items-center gap-4 px-5 py-4 text-left active:bg-secondary transition-colors ${i < arr.length - 1 ? "border-b-2 border-border" : ""}`}
              >
                <div className="relative shrink-0">
                  <div className="rounded-full flex items-center justify-center" style={{ width: 56, height: 56, background: contact.color }}>
                    {contact.isGroup
                      ? <Users size={26} className="text-white" />
                      : <span className="text-white" style={{ fontSize: 18, fontWeight: 700 }}>{contact.initials}</span>
                    }
                  </div>
                  {contact.online && (
                    <span className="absolute bottom-0 right-0 bg-green-500 rounded-full border-2 border-card" style={{ width: 14, height: 14 }} />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-foreground" style={{ fontSize: 18, fontWeight: 700 }}>{contact.name}</p>
                  <p className="text-muted-foreground mt-0.5" style={{ fontSize: 15 }}>{contact.role}</p>
                </div>
                <ChevronRight size={20} className="text-muted-foreground shrink-0" style={{ opacity: 0.5 }} />
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function MessagesScreen({ onOpenChat }: { onOpenChat: (conv: typeof conversations[0]) => void }) {
  const [localConvs, setLocalConvs] = useState(conversations);
  const [showContacts, setShowContacts] = useState(false);

  function markRead(id: number) {
    setLocalConvs((prev) => prev.map((c) => c.id === id ? { ...c, unread: 0 } : c));
    const conv = localConvs.find((c) => c.id === id)!;
    onOpenChat(conv);
  }

  function handleSelectContact(contact: typeof contactsData[0]) {
    setShowContacts(false);
    onOpenChat({
      id: contact.id + 100,
      name: contact.name,
      isGroup: contact.isGroup,
      avatarColor: contact.color,
      avatarInitials: contact.initials,
      lastMessage: "",
      time: "",
      unread: 0,
      online: contact.online,
    });
  }

  const totalUnread = localConvs.reduce((sum, c) => sum + c.unread, 0);

  return (
    <div className="flex-1 flex flex-col overflow-hidden relative">
      {showContacts && (
        <ContactListPanel onClose={() => setShowContacts(false)} onSelect={handleSelectContact} />
      )}

      <div className="flex-1 overflow-y-auto flex flex-col">
        <div className="px-5 pt-5 pb-3 shrink-0">
          <h1 className="text-foreground" style={{ fontSize: 28, fontWeight: 800 }}>Mensagens</h1>
          {totalUnread > 0 && (
            <p className="text-muted-foreground mt-1" style={{ fontSize: 16 }}>
              {totalUnread} mensagem{totalUnread > 1 ? "s" : ""} não lida{totalUnread > 1 ? "s" : ""}
            </p>
          )}
        </div>

        <div className="px-4 pb-4 shrink-0">
          <button
            onClick={() => setShowContacts(true)}
            style={{ minHeight: 56, fontSize: 18, fontWeight: 700 }}
            className="w-full bg-primary text-primary-foreground rounded-2xl flex items-center justify-center gap-3 active:opacity-85 transition-opacity shadow-md"
          >
            <span className="bg-white/20 rounded-full flex items-center justify-center" style={{ width: 32, height: 32 }}>
              <Plus size={20} strokeWidth={2.5} className="text-white" />
            </span>
            Nova Mensagem
          </button>
        </div>

        <div className="px-5 pb-2 shrink-0">
          <span className="text-muted-foreground" style={{ fontSize: 14, fontWeight: 600, letterSpacing: "0.06em" }}>
            CONVERSAS RECENTES
          </span>
        </div>

        <div className="flex-1 px-4 pb-6">
          <div className="bg-card rounded-3xl border-2 border-border overflow-hidden shadow-sm">
            {localConvs.map((conv, i) => (
              <button
                key={conv.id}
                onClick={() => markRead(conv.id)}
                style={{ minHeight: 88 }}
                className={`w-full flex items-center gap-4 px-5 py-4 text-left active:bg-secondary transition-colors ${i < localConvs.length - 1 ? "border-b-2 border-border" : ""} ${conv.unread > 0 ? "bg-blue-50/60" : "bg-card"}`}
              >
                <ConvAvatar conv={conv} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-foreground truncate" style={{ fontSize: 18, fontWeight: conv.unread > 0 ? 800 : 600, maxWidth: "65%" }}>
                      {conv.name}
                    </span>
                    <span className="shrink-0 ml-2" style={{ fontSize: 14, fontWeight: conv.unread > 0 ? 700 : 400, color: conv.unread > 0 ? "#1a4fba" : "#4a5568" }}>
                      {conv.time}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground truncate flex-1" style={{ fontSize: 16, fontWeight: conv.unread > 0 ? 500 : 400, lineHeight: 1.4 }}>
                      {conv.lastMessage}
                    </span>
                    {conv.unread > 0 && (
                      <span aria-label={`${conv.unread} mensagens não lidas`} className="bg-primary text-primary-foreground rounded-full flex items-center justify-center shrink-0" style={{ minWidth: 28, height: 28, fontSize: 14, fontWeight: 800, padding: "0 6px" }}>
                        {conv.unread}
                      </span>
                    )}
                  </div>
                </div>
                <ChevronRight size={20} className="text-muted-foreground shrink-0 ml-1" style={{ opacity: 0.5 }} />
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Profile Screen ───────────────────────────────────────────────────────────

function EditProfilePanel({ profile, onClose, onSave }: {
  profile: typeof initialProfile;
  onClose: () => void;
  onSave: (p: typeof initialProfile) => void;
}) {
  const [form, setForm] = useState(profile);

  function update(field: keyof typeof initialProfile, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  const fields: { key: keyof typeof initialProfile; label: string; icon: React.ReactNode; type?: string }[] = [
    { key: "name",      label: "Nome Completo",       icon: <User size={20} className="text-primary" /> },
    { key: "email",     label: "E-mail",              icon: <Mail size={20} className="text-primary" />,    type: "email" },
    { key: "phone",     label: "Telefone / WhatsApp", icon: <Phone size={20} className="text-primary" />,   type: "tel" },
    { key: "address",   label: "Endereço",            icon: <MapPin size={20} className="text-primary" /> },
    { key: "city",      label: "Cidade – Estado",     icon: <MapPin size={20} className="text-primary" /> },
    { key: "birthdate", label: "Data de Nascimento",  icon: <Calendar size={20} className="text-primary" /> },
  ];

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <div className="bg-primary px-5 py-5 shrink-0 flex items-center gap-3">
        <button
          onClick={onClose}
          aria-label="Voltar"
          style={{ minWidth: 48, minHeight: 48 }}
          className="bg-white/20 rounded-full flex items-center justify-center active:bg-white/30 transition-colors shrink-0"
        >
          <ArrowLeft size={26} className="text-white" />
        </button>
        <h1 className="text-primary-foreground flex-1" style={{ fontSize: 22, fontWeight: 800 }}>Editar Meus Dados</h1>
        <button
          onClick={() => onSave(form)}
          aria-label="Salvar"
          style={{ minWidth: 48, minHeight: 48 }}
          className="bg-white/20 rounded-full flex items-center justify-center active:bg-white/30 transition-colors shrink-0"
        >
          <Save size={22} className="text-white" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 pt-5 pb-6">
        <div className="flex flex-col gap-4">
          {fields.map(({ key, label, icon, type }) => (
            <div key={key} className="bg-card rounded-2xl border-2 border-border px-4 pt-3 pb-4">
              <div className="flex items-center gap-2 mb-2">
                {icon}
                <label className="text-muted-foreground" style={{ fontSize: 14, fontWeight: 600 }}>{label}</label>
              </div>
              <input
                type={type ?? "text"}
                value={form[key]}
                onChange={(e) => update(key, e.target.value)}
                style={{ fontSize: 18, fontWeight: 600, minHeight: 44 }}
                className="w-full bg-transparent text-foreground outline-none border-b-2 border-border focus:border-primary pb-1 transition-colors"
              />
            </div>
          ))}
        </div>

        <div style={{ height: 24 }} />

        <button
          onClick={() => onSave(form)}
          style={{ minHeight: 64, fontSize: 20, fontWeight: 700 }}
          className="w-full bg-primary text-primary-foreground rounded-2xl flex items-center justify-center gap-3 active:opacity-80 transition-opacity shadow-md"
        >
          <Save size={24} strokeWidth={2.5} />
          Salvar Alterações
        </button>
      </div>
    </div>
  );
}

function ProfileScreen() {
  const [editingProfile, setEditingProfile] = useState(false);
  const [profile, setProfile] = useState(initialProfile);

  function handleSave(updated: typeof initialProfile) {
    setProfile(updated);
    setEditingProfile(false);
  }

  if (editingProfile) {
    return <EditProfilePanel profile={profile} onClose={() => setEditingProfile(false)} onSave={handleSave} />;
  }

  const menuItems = [
    { icon: <Edit2 size={26} className="text-primary" />,    label: "Editar Meus Dados",              onPress: () => setEditingProfile(true) },
    { icon: <Sliders size={26} className="text-primary" />,  label: "Configurações de Texto e Zoom",  onPress: () => {} },
    { icon: <Headphones size={26} className="text-primary" />, label: "Falar com o Suporte / Moderador", onPress: () => {} },
  ];

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <div className="bg-primary px-5 py-5 shrink-0">
        <h1 className="text-primary-foreground text-center" style={{ fontSize: 26, fontWeight: 800 }}>
          Meu Perfil
        </h1>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="flex flex-col items-center px-4 pt-8 pb-2">
          <div
            className="rounded-full flex items-center justify-center border-4 border-background shadow-xl"
            style={{ width: 120, height: 120, background: "#1a4fba" }}
          >
            <span className="text-white" style={{ fontSize: 44, fontWeight: 800 }}>JS</span>
          </div>
          <h2 className="text-foreground mt-4 text-center" style={{ fontSize: 30, fontWeight: 800 }}>
            {profile.name}
          </h2>
          <div className="flex items-center gap-2 mt-2">
            <Mail size={18} className="text-muted-foreground" />
            <span className="text-muted-foreground" style={{ fontSize: 17 }}>{profile.email}</span>
          </div>
        </div>

        <div className="px-4 pt-6 pb-6">
          <div className="bg-card rounded-3xl border-2 border-border overflow-hidden shadow-sm">
            {menuItems.map((item, i, arr) => (
              <button
                key={item.label}
                onClick={item.onPress}
                style={{ minHeight: 76 }}
                className={`w-full flex items-center gap-4 px-5 py-4 text-left active:bg-secondary transition-colors ${i < arr.length - 1 ? "border-b-2 border-border" : ""}`}
              >
                <div className="bg-secondary rounded-2xl flex items-center justify-center shrink-0" style={{ width: 52, height: 52 }}>
                  {item.icon}
                </div>
                <span className="text-foreground flex-1" style={{ fontSize: 18, fontWeight: 600, lineHeight: 1.3 }}>
                  {item.label}
                </span>
                <ChevronRight size={22} className="text-muted-foreground shrink-0" style={{ opacity: 0.5 }} />
              </button>
            ))}
          </div>

          <div style={{ height: 48 }} />

          <button
            style={{ minHeight: 64, fontSize: 20, fontWeight: 700 }}
            className="w-full bg-destructive text-destructive-foreground rounded-2xl flex items-center justify-center gap-3 active:opacity-80 transition-opacity shadow-md"
          >
            <LogOut size={26} strokeWidth={2.5} />
            Sair do Aplicativo
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Root ─────────────────────────────────────────────────────────────────────

export default function App() {
  const [activeScreen, setActiveScreen] = useState<MainScreen>("home");
  const [showActivityDetails, setShowActivityDetails] = useState(false);
  const [openChat, setOpenChat] = useState<typeof conversations[0] | null>(null);
  const [showNotifications, setShowNotifications] = useState(false);

  const isOverlay = showActivityDetails || openChat !== null;

  return (
    <div className="size-full flex items-center justify-center bg-muted" style={{ fontFamily: "'Inter', sans-serif" }}>
      <div
        className="relative flex flex-col bg-background overflow-hidden shadow-2xl"
        style={{ width: "100%", maxWidth: 420, height: "100%", maxHeight: 900 }}
      >
        {/* ── Notifications overlay ── */}
        {showNotifications && (
          <>
            <StatusBar />
            <NotificationsPanel onClose={() => setShowNotifications(false)} />
          </>
        )}

        {/* ── Activity Details overlay ── */}
        {!showNotifications && showActivityDetails && (
          <>
            <StatusBar />
            <ActivityDetailsScreen
              activity={enrolledActivity}
              onBack={() => setShowActivityDetails(false)}
            />
          </>
        )}

        {/* ── Chat overlay ── */}
        {!showNotifications && !showActivityDetails && openChat && (
          <>
            <StatusBar />
            <ChatScreen
              conversation={openChat}
              onBack={() => setOpenChat(null)}
            />
          </>
        )}

        {/* ── Main app ── */}
        {!showNotifications && !isOverlay && (
          <>
            <StatusBar />

            {activeScreen === "home" && (
              <header className="bg-primary px-5 pb-5 shrink-0">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-primary-foreground" style={{ fontSize: 16, opacity: 0.85 }}>Bem-vindo de volta,</p>
                    <h1 className="text-primary-foreground" style={{ fontSize: 30, fontWeight: 800, lineHeight: 1.2 }}>Olá, João! 👋</h1>
                  </div>
                  <NotificationBell count={2} onOpen={() => setShowNotifications(true)} />
                </div>
              </header>
            )}

            {activeScreen === "home" && <HomeScreen onViewDetails={() => setShowActivityDetails(true)} />}
            {activeScreen === "messages" && <MessagesScreen onOpenChat={setOpenChat} />}
            {activeScreen === "profile" && <ProfileScreen />}

            <BottomNav active={activeScreen} onChange={setActiveScreen} />
          </>
        )}
      </div>
    </div>
  );
}
