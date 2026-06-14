import { useState } from "react";
import { ArrowLeft, Clock, Calendar, UserCircle, MapPin, CheckCircle, AlertTriangle, Users, Star } from "lucide-react";

interface Activity {
  id: string;
  title: string;
  time: string;
  date: string;
  tutor: string;
  tutorBio: string;
  location: string;
  description: string;
  participants: number;
  maxParticipants: number;
  level: string;
  category: string;
  color: string;
}

interface ActivityDetailsScreenProps {
  activity: Activity;
  onBack: () => void;
}

export function ActivityDetailsScreen({ activity, onBack }: ActivityDetailsScreenProps) {
  const [showCancelConfirm, setShowCancelConfirm] = useState(false);
  const [cancelled, setCancelled] = useState(false);
  const [entered, setEntered] = useState(false);

  function handleCancel() {
    setCancelled(true);
    setShowCancelConfirm(false);
    setTimeout(() => onBack(), 1200);
  }

  return (
    <div className="flex flex-col flex-1 overflow-hidden relative">
      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto">
        {/* Hero image area */}
        <div
          className="relative shrink-0 flex flex-col justify-end"
          style={{ height: 240, background: `linear-gradient(160deg, ${activity.color} 0%, #0d3a8f 100%)` }}
        >
          {/* Back button — overlaid on hero */}
          <button
            onClick={onBack}
            aria-label="Voltar para a tela anterior"
            style={{ minWidth: 52, minHeight: 52, top: 16, left: 16 }}
            className="absolute flex items-center gap-2 bg-white/20 backdrop-blur-sm rounded-2xl px-4 py-3 active:bg-white/30 transition-colors"
          >
            <ArrowLeft size={26} strokeWidth={2.5} className="text-white" />
            <span className="text-white" style={{ fontSize: 17, fontWeight: 700 }}>
              Voltar
            </span>
          </button>

          {/* Category badge */}
          <div className="absolute top-16 right-4">
            <span
              className="bg-white/25 text-white rounded-full px-4 py-1.5"
              style={{ fontSize: 14, fontWeight: 600 }}
            >
              {activity.category}
            </span>
          </div>

          {/* Decorative circles */}
          <div
            aria-hidden="true"
            className="absolute rounded-full"
            style={{
              width: 180,
              height: 180,
              background: "rgba(255,255,255,0.06)",
              top: -40,
              right: -30,
            }}
          />
          <div
            aria-hidden="true"
            className="absolute rounded-full"
            style={{
              width: 100,
              height: 100,
              background: "rgba(255,255,255,0.06)",
              top: 60,
              right: 80,
            }}
          />

          {/* Activity icon area */}
          <div className="flex flex-col items-center pb-6">
            <div
              className="bg-white/20 rounded-3xl flex items-center justify-center mb-2"
              style={{ width: 72, height: 72, fontSize: 36 }}
              aria-hidden="true"
            >
              {activity.id === "gym" ? "🏃" : activity.id === "yoga" ? "🧘" : activity.id === "art" ? "🎨" : "💻"}
            </div>
          </div>
        </div>

        {/* Content card */}
        <div className="bg-background px-5 pt-6 pb-32">
          {/* Title */}
          <h1 className="text-foreground mb-5" style={{ fontSize: 28, fontWeight: 800, lineHeight: 1.25 }}>
            {activity.title}
          </h1>

          {/* Info grid */}
          <div className="flex flex-col gap-4 mb-6">
            <InfoRow icon={<Clock size={22} className="text-primary" />} label="Horário" value={activity.time} />
            <InfoRow icon={<Calendar size={22} className="text-primary" />} label="Data" value={activity.date} />
            <InfoRow
              icon={<UserCircle size={22} className="text-primary" />}
              label="Instrutor(a)"
              value={activity.tutor}
            />
            <InfoRow icon={<MapPin size={22} className="text-primary" />} label="Local" value={activity.location} />
          </div>

          {/* Divider */}
          <div className="border-t border-border mb-6" />

          {/* Participants bar */}
          <div className="bg-card rounded-2xl p-4 border border-border mb-6">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Users size={20} className="text-primary" />
                <span className="text-foreground" style={{ fontSize: 16, fontWeight: 700 }}>
                  Vagas
                </span>
              </div>
              <span className="text-foreground" style={{ fontSize: 16, fontWeight: 700 }}>
                {activity.participants}/{activity.maxParticipants}
              </span>
            </div>
            <div className="bg-muted rounded-full overflow-hidden" style={{ height: 10 }}>
              <div
                className="bg-primary rounded-full h-full transition-all"
                style={{ width: `${(activity.participants / activity.maxParticipants) * 100}%` }}
              />
            </div>
            <div className="flex items-center justify-between mt-2">
              <span className="text-muted-foreground" style={{ fontSize: 14 }}>
                {activity.maxParticipants - activity.participants} vagas disponíveis
              </span>
              <span
                className="rounded-full px-3 py-0.5"
                style={{
                  fontSize: 13,
                  fontWeight: 600,
                  background: activity.level === "Iniciante" ? "#d1fae5" : activity.level === "Intermediário" ? "#fef3c7" : "#fee2e2",
                  color: activity.level === "Iniciante" ? "#065f46" : activity.level === "Intermediário" ? "#92400e" : "#991b1b",
                }}
              >
                {activity.level}
              </span>
            </div>
          </div>

          {/* Description */}
          <div className="mb-6">
            <h2 className="text-foreground mb-3" style={{ fontSize: 20, fontWeight: 700 }}>
              Sobre a Atividade
            </h2>
            <p className="text-foreground" style={{ fontSize: 17, lineHeight: 1.75 }}>
              {activity.description}
            </p>
          </div>

          {/* Tutor card */}
          <div className="bg-card rounded-2xl p-4 border border-border">
            <h2 className="text-foreground mb-3" style={{ fontSize: 18, fontWeight: 700 }}>
              Sobre o(a) Instrutor(a)
            </h2>
            <div className="flex items-start gap-4">
              <div
                className="bg-secondary rounded-full flex items-center justify-center shrink-0"
                style={{ width: 56, height: 56 }}
              >
                <UserCircle size={32} className="text-primary" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-foreground" style={{ fontSize: 17, fontWeight: 700 }}>
                    {activity.tutor}
                  </span>
                  <Star size={16} className="text-amber-500" fill="currentColor" />
                  <span style={{ fontSize: 15, fontWeight: 600, color: "#92400e" }}>4.9</span>
                </div>
                <p className="text-muted-foreground" style={{ fontSize: 15, lineHeight: 1.6 }}>
                  {activity.tutorBio}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Fixed action area — anchored to bottom */}
      <div
        className="absolute bottom-0 left-0 right-0 bg-card border-t border-border px-5 pt-4 pb-6 flex flex-col gap-3"
        style={{ boxShadow: "0 -4px 24px rgba(0,0,0,0.10)" }}
      >
        {cancelled ? (
          <div
            className="w-full rounded-2xl flex items-center justify-center gap-3 bg-muted"
            style={{ minHeight: 60 }}
          >
            <CheckCircle size={22} className="text-muted-foreground" />
            <span className="text-muted-foreground" style={{ fontSize: 17, fontWeight: 700 }}>
              Inscrição cancelada
            </span>
          </div>
        ) : (
          <>
            {/* Primary CTA */}
            <button
              onClick={() => setEntered(true)}
              style={{ minHeight: 60, fontSize: 19, fontWeight: 800 }}
              className={`w-full rounded-2xl flex items-center justify-center gap-2 transition-all shadow-md ${
                entered ? "bg-green-600 text-white" : "bg-primary text-primary-foreground active:opacity-85"
              }`}
            >
              {entered ? (
                <>
                  <CheckCircle size={24} /> Sala Aberta!
                </>
              ) : (
                "Entrar na Sala"
              )}
            </button>

            {/* Spacer + visual warning separator */}
            <div className="flex items-center gap-3 px-1">
              <div className="flex-1 border-t border-border" />
              <span className="text-muted-foreground" style={{ fontSize: 13 }}>
                ou
              </span>
              <div className="flex-1 border-t border-border" />
            </div>

            {/* Danger CTA */}
            {!showCancelConfirm ? (
              <button
                onClick={() => setShowCancelConfirm(true)}
                style={{ minHeight: 56, fontSize: 17, fontWeight: 700 }}
                className="w-full rounded-2xl flex items-center justify-center gap-2 border-2 border-destructive text-destructive bg-transparent active:bg-red-50 transition-colors"
              >
                <AlertTriangle size={20} strokeWidth={2.5} />
                Cancelar Inscrição
              </button>
            ) : (
              <div className="bg-red-50 border-2 border-destructive rounded-2xl p-4">
                <p className="text-destructive mb-3" style={{ fontSize: 16, fontWeight: 700, textAlign: "center" }}>
                  Tem certeza que deseja cancelar?
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={() => setShowCancelConfirm(false)}
                    style={{ minHeight: 52, fontSize: 16, fontWeight: 700 }}
                    className="flex-1 bg-muted text-foreground rounded-xl active:opacity-70 transition-opacity"
                  >
                    Não
                  </button>
                  <button
                    onClick={handleCancel}
                    style={{ minHeight: 52, fontSize: 16, fontWeight: 700 }}
                    className="flex-1 bg-destructive text-destructive-foreground rounded-xl active:opacity-80 transition-opacity"
                  >
                    Sim, cancelar
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Cancel confirm overlay — extra spacing guard */}
      {showCancelConfirm && (
        <div
          aria-hidden="true"
          className="absolute inset-0 bg-foreground/10 pointer-events-none"
        />
      )}
    </div>
  );
}

function InfoRow({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-start gap-4">
      <div
        className="bg-secondary rounded-xl flex items-center justify-center shrink-0"
        style={{ width: 48, height: 48 }}
      >
        {icon}
      </div>
      <div className="flex-1 flex flex-col justify-center" style={{ minHeight: 48 }}>
        <span className="text-muted-foreground" style={{ fontSize: 14, fontWeight: 500, lineHeight: 1.3 }}>
          {label}
        </span>
        <span className="text-foreground" style={{ fontSize: 18, fontWeight: 600, lineHeight: 1.4 }}>
          {value}
        </span>
      </div>
    </div>
  );
}
