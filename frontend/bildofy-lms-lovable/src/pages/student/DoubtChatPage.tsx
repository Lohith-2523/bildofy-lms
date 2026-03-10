import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { XPBadge } from "@/components/gamification/XPBadge";
import { useOnlineStatus } from "@/contexts/OnlineContext";
import MarkdownKatexRenderer from "@/components/MarkdownKatexRenderer";
import {
  ArrowLeft,
  MessageCircleQuestion,
  Send,
  Bot,
  User,
  WifiOff,
  Sparkles,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
}

const normalizeAssistantContent = (raw: string) => {
  const source = (raw ?? "").trim();
  if (!source) return source;

  // If model accidentally wraps response in JSON-like shape, unwrap readable text.
  const unwrapped = source
    .replace(/^\s*\{+\s*/, "")
    .replace(/\s*\}+\s*$/, "")
    .replace(/^["'`]+/, "")
    .replace(/["'`]+$/, "")
    .replace(/\\"/g, '"')
    .replace(/\\n/g, "\n");

  return unwrapped.replace(/^\s*(response|answer)\s*:\s*/i, "").trim();
};

const initialMessages: Message[] = [
  {
    id: "1",
    content:
      "Hello! I'm your AI study assistant.\n\nAsk any academic doubt and I will explain step by step. I can format math using KaTeX, for example: $a^2+b^2=c^2$.",
    role: "assistant",
    timestamp: new Date(),
  },
];

const DoubtChatPage: React.FC = () => {
  const { isOnline } = useOnlineStatus();
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      role: "user",
      timestamp: new Date(),
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");
    setError(null);
    setIsTyping(true);

    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch("http://localhost:8000/api/student/ai/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          messages: updatedMessages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
          context: {
            client_type: window.innerWidth < 768 ? "mobile" : "desktop",
            connectivity: navigator.onLine ? "online" : "offline",
            model_capability: navigator.onLine ? "heavy" : "light",
          },
        }),
      });

      if (!res.ok) throw new Error("Failed to get AI response");
      const data = await res.json();
      const content = normalizeAssistantContent(data.response || "");

      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        content,
        role: "assistant",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiResponse]);
    } catch (err: any) {
      setError(err.message || "Could not fetch AI response.");
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 2).toString(),
          role: "assistant",
          content:
            "I could not process that right now. Please try again.\n\nIf your question includes formulas, you can type them like `$x^2+2x+1$`.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link to="/student">
                <Button variant="ghost" size="icon">
                  <ArrowLeft className="w-5 h-5" />
                </Button>
              </Link>
              <div>
                <h1 className="text-xl font-display font-bold text-foreground flex items-center gap-2">
                  <MessageCircleQuestion className="w-5 h-5 text-primary" />
                  AI Doubt Assistant
                </h1>
                <p className="text-sm text-muted-foreground">
                  {isOnline
                    ? "Online - Full capabilities"
                    : "Offline - Limited responses"}
                </p>
              </div>
            </div>
            <XPBadge xp={10} size="sm" />
          </div>
        </div>
      </header>

      {!isOnline && (
        <div className="bg-offline/10 border-b border-offline/30 px-4 py-2 flex items-center justify-center gap-2 text-sm">
          <WifiOff className="w-4 h-4 text-offline" />
          <span className="text-foreground">
            Limited AI responses in offline mode
          </span>
        </div>
      )}

      <main className="flex-1 overflow-y-auto p-4">
        <div className="container mx-auto max-w-2xl space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex gap-3 animate-fade-up",
                message.role === "user" && "flex-row-reverse"
              )}
            >
              <div
                className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0",
                  message.role === "assistant"
                    ? "bg-gradient-primary text-primary-foreground"
                    : "bg-secondary text-secondary-foreground"
                )}
              >
                {message.role === "assistant" ? (
                  <Bot className="w-4 h-4" />
                ) : (
                  <User className="w-4 h-4" />
                )}
              </div>
              <div
                className={cn(
                  "max-w-[80%] p-4 rounded-2xl",
                  message.role === "assistant"
                    ? "bg-card border border-border rounded-tl-sm"
                    : "bg-primary text-primary-foreground rounded-tr-sm"
                )}
              >
                {message.role === "assistant" ? (
                  <div className="[&_ul]:list-disc [&_ol]:list-decimal [&_ul]:ml-6 [&_ol]:ml-6 [&_li]:mb-1 [&_code]:bg-muted [&_code]:px-1 [&_code]:py-0.5 [&_code]:rounded">
                    <MarkdownKatexRenderer content={message.content} />
                  </div>
                ) : (
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                )}
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex gap-3 animate-fade-up">
              <div className="w-8 h-8 rounded-full bg-gradient-primary text-primary-foreground flex items-center justify-center">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-card border border-border p-4 rounded-2xl rounded-tl-sm">
                <div className="flex gap-1">
                  <span
                    className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                    style={{ animationDelay: "0ms" }}
                  />
                  <span
                    className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                    style={{ animationDelay: "150ms" }}
                  />
                  <span
                    className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                    style={{ animationDelay: "300ms" }}
                  />
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="text-sm text-destructive bg-destructive/10 border border-destructive/30 p-3 rounded-lg">
              {error}
            </div>
          )}
        </div>
      </main>

      <footer className="sticky bottom-0 bg-card border-t border-border p-4">
        <div className="container mx-auto max-w-2xl">
          <div className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask your doubt..."
              className="flex-1"
            />
            <Button onClick={handleSend} disabled={!input.trim() || isTyping}>
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <p className="text-xs text-center text-muted-foreground mt-2">
            <Sparkles className="w-3 h-3 inline mr-1" />
            Earn XP for meaningful questions and interactions
          </p>
        </div>
      </footer>
    </div>
  );
};

export default DoubtChatPage;
