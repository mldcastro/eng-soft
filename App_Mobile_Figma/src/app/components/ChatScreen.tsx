import { useState, useRef, useEffect } from "react";
import { ArrowLeft, Send, Users, UserCircle } from "lucide-react";

interface Conversation {
  id: number;
  name: string;
  isGroup: boolean;
  avatarColor: string;
  avatarInitials: string;
}

interface Message {
  id: number;
  text: string;
  fromMe: boolean;
  time: string;
}

const seedMessages: Record<number, Message[]> = {
  1: [
    { id: 1, text: "Bom dia a todos! A aula de hoje está confirmada às 15h.", fromMe: false, time: "08:02" },
    { id: 2, text: "Ótimo! Estarei lá, professora.", fromMe: true, time: "08:15" },
    { id: 3, text: "João, lembre-se de trazer uma garrafa de água.", fromMe: false, time: "08:18" },
    { id: 4, text: "Obrigado pela lembrança! Até logo.", fromMe: true, time: "08:20" },
  ],
  2: [
    { id: 1, text: "Olá João! Tudo bem com você?", fromMe: false, time: "Ontem" },
    { id: 2, text: "Tudo ótimo, professora! E a senhora?", fromMe: true, time: "Ontem" },
    { id: 3, text: "Muito bem! Nos vemos na próxima aula.", fromMe: false, time: "Ontem" },
  ],
  3: [
    { id: 1, text: "João! Vai na aula de ginástica hoje?", fromMe: false, time: "09:10" },
    { id: 2, text: "Vou sim! A gente se encontra lá.", fromMe: true, time: "09:25" },
    { id: 3, text: "Perfeito! Até mais.", fromMe: false, time: "09:26" },
  ],
};

export function ChatScreen({ conversation, onBack }: { conversation: Conversation; onBack: () => void }) {
  const [messages, setMessages] = useState<Message[]>(seedMessages[conversation.id] ?? []);
  const [draft, setDraft] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function send() {
    const text = draft.trim();
    if (!text) return;
    const now = new Date();
    const time = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;
    setMessages((prev) => [...prev, { id: Date.now(), text, fromMe: true, time }]);
    setDraft("");
  }

  return (
    <div className="flex flex-col flex-1 overflow-hidden bg-background">
      {/* Chat header */}
      <div className="bg-primary px-4 py-3 flex items-center gap-3 shrink-0" style={{ minHeight: 68 }}>
        <button
          onClick={onBack}
          aria-label="Voltar"
          style={{ minWidth: 52, minHeight: 52 }}
          className="flex items-center justify-center rounded-full bg-white/20 active:bg-white/30 transition-colors shrink-0"
        >
          <ArrowLeft size={26} strokeWidth={2.5} className="text-white" />
        </button>

        <div
          className="rounded-full flex items-center justify-center shrink-0"
          style={{ width: 48, height: 48, background: conversation.avatarColor }}
        >
          {conversation.isGroup ? (
            <Users size={24} className="text-white" />
          ) : (
            <span className="text-white" style={{ fontSize: 18, fontWeight: 700 }}>
              {conversation.avatarInitials}
            </span>
          )}
        </div>

        <div className="flex-1 min-w-0">
          <span className="text-white block truncate" style={{ fontSize: 19, fontWeight: 700 }}>
            {conversation.name}
          </span>
          <span className="text-white block" style={{ fontSize: 14, opacity: 0.8 }}>
            {conversation.isGroup ? "Grupo" : "Online agora"}
          </span>
        </div>
      </div>

      {/* Message list */}
      <div className="flex-1 overflow-y-auto px-4 py-5 flex flex-col gap-3">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.fromMe ? "justify-end" : "justify-start"}`}>
            {!msg.fromMe && (
              <div
                className="rounded-full flex items-center justify-center shrink-0 mr-2 self-end mb-1"
                style={{ width: 36, height: 36, background: conversation.avatarColor }}
              >
                {conversation.isGroup ? (
                  <Users size={18} className="text-white" />
                ) : (
                  <span className="text-white" style={{ fontSize: 13, fontWeight: 700 }}>
                    {conversation.avatarInitials}
                  </span>
                )}
              </div>
            )}
            <div
              className="rounded-2xl px-4 py-3 shadow-sm"
              style={{
                maxWidth: "72%",
                background: msg.fromMe ? "#1a4fba" : "#ffffff",
                borderBottomRightRadius: msg.fromMe ? 4 : undefined,
                borderBottomLeftRadius: !msg.fromMe ? 4 : undefined,
                border: msg.fromMe ? "none" : "1.5px solid #c9d3e8",
              }}
            >
              <p
                style={{ fontSize: 17, lineHeight: 1.55, color: msg.fromMe ? "#ffffff" : "#0f1c2e" }}
              >
                {msg.text}
              </p>
              <span
                className="block text-right mt-1"
                style={{ fontSize: 12, opacity: 0.65, color: msg.fromMe ? "#ffffff" : "#4a5568" }}
              >
                {msg.time}
              </span>
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="bg-card border-t border-border px-4 py-3 flex items-end gap-3 shrink-0">
        <textarea
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
          placeholder="Escreva uma mensagem..."
          rows={1}
          aria-label="Escreva uma mensagem"
          className="flex-1 bg-secondary rounded-2xl px-4 py-3 resize-none outline-none border border-border text-foreground placeholder:text-muted-foreground"
          style={{ fontSize: 17, lineHeight: 1.5, maxHeight: 120 }}
        />
        <button
          onClick={send}
          aria-label="Enviar mensagem"
          style={{ minWidth: 52, minHeight: 52 }}
          className={`rounded-full flex items-center justify-center transition-colors ${
            draft.trim() ? "bg-primary active:opacity-80" : "bg-muted"
          }`}
        >
          <Send size={22} strokeWidth={2} className={draft.trim() ? "text-white" : "text-muted-foreground"} />
        </button>
      </div>
    </div>
  );
}
