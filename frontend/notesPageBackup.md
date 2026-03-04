import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { XPBadge } from "@/components/gamification/XPBadge";
import { useOnlineStatus } from "@/contexts/OnlineContext";
import {
  ArrowLeft,
  FileText,
  Plus,
  Download,
  Search,
  WifiOff,
  CheckCircle,
  CloudOff,
  Eye,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

/* === KaTeX + Markdown support (non-visual) === */
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

const NOTES_CACHE_KEY = "student_notes_cache_v1";

type NoteItem = {
  id: string;
  title: string;
  subject: string;
  chapter: string;
  createdAt: Date;
  xpEarned: number;
  isOfflineAvailable: boolean;
  pages: number;
};

const NotesPage: React.FC = () => {
  const { isOnline } = useOnlineStatus();

  const [searchQuery, setSearchQuery] = useState("");
  const [showGenerateForm, setShowGenerateForm] = useState(false);
  const [notesList, setNotesList] = useState<NoteItem[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeContent, setActiveContent] = useState<string | null>(null);
  const [teacherNotes, setTeacherNotes] = useState<any[]>([]);

  const [subject, setSubject] = useState("");
  const [chapter, setChapter] = useState("");
  const [difficulty, setDifficulty] = useState("medium");

  /* === Load cached notes on boot === */
  useEffect(() => {
    const cached = localStorage.getItem(NOTES_CACHE_KEY);
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        setNotesList(
          parsed.map((n: any) => ({
            ...n,
            createdAt: new Date(n.createdAt),
          }))
        );
      } catch {
        localStorage.removeItem(NOTES_CACHE_KEY);
      }
    }
  }, []);

  /* === Persist cache === */
  useEffect(() => {
    if (notesList.length > 0) {
      localStorage.setItem(NOTES_CACHE_KEY, JSON.stringify(notesList));
    }
  }, [notesList]);

  useEffect(() => {
    fetch("http://localhost:8000/api/student/notes/teacher")
      .then((res) => res.json())
      .then(setTeacherNotes)
      .catch(console.error);
  }, []);

  const filteredNotes = notesList.filter(
    (note) =>
      note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      note.subject.toLowerCase().includes(searchQuery.toLowerCase())
  );

  /* === Backend integration: Generate Notes === */
  const handleGenerateNotes = async () => {
  if (!subject || !chapter) return;

  setIsGenerating(true);

  try {
    const res = await fetch(
      "http://localhost:8000/api/student/notes/generate",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          subject,
          chapter,
          difficulty,
          context: {
            client_type: window.innerWidth < 768 ? "mobile" : "desktop",
            connectivity: navigator.onLine ? "online" : "offline",
            model_capability: navigator.onLine ? "heavy" : "light",
            user_id: 1, // DEV auth placeholder
          },
        }),
      }
    );

    

    if (!res.ok) throw new Error("Failed to generate notes");

    const data = await res.json();

    setActiveContent(data.summary ? data.summary : "");

    setNotesList((prev) => [
      {
        id: data.content_id,
        title: chapter,
        subject,
        chapter,
        createdAt: new Date(),
        xpEarned: 25,
        isOfflineAvailable: true,
        pages: Math.ceil((data.summary?.length || 800) / 800),
      },
      ...prev,
    ]);

    setShowGenerateForm(false);
    setSubject("");
    setChapter("");
    setDifficulty("medium");
  } catch (err) {
    console.error(err);
  } finally {
    setIsGenerating(false);
  }
};


  /* === PDF export (KaTeX-safe, UI-neutral) === */
  const exportNoteAsPDF = () => {
    const win = window.open("", "_blank");
    if (!win) return;

    win.document.write(`
      <html>
        <head>
          <title>Notes</title>
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
          <style>
            body { font-family: serif; padding: 24px; }
          </style>
        </head>
        <body>
          <p>Rendered notes content will appear here.</p>
        </body>
      </html>
    `);

    win.document.close();
    win.print();
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Link to="/student">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <div>
              <h1 className="text-xl font-display font-bold text-foreground">
                Notes
              </h1>
              <p className="text-sm text-muted-foreground">
                AI-generated study notes
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search notes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>

          <Button
            className="flex items-center gap-2"
            onClick={() => setShowGenerateForm(true)}
            disabled={!isOnline}
          >
            {!isOnline ? (
              <WifiOff className="w-4 h-4" />
            ) : (
              <Plus className="w-4 h-4" />
            )}
            Generate Notes
            <XPBadge xp={25} />
          </Button>
        </div>

        {/* Generate Modal */}
        {showGenerateForm && (
          <div className="mb-6 p-6 rounded-xl bg-card border border-border shadow-lg animate-scale-in">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Generate Notes</h2>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setShowGenerateForm(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              <div className="space-y-4">
                <Input
                  placeholder="Subject"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                />
                <Input
                  placeholder="Chapter / Topic"
                  value={chapter}
                  onChange={(e) => setChapter(e.target.value)}
                />
                <Input
                  placeholder="Difficulty (easy / medium / hard)"
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                />

                <Button
                  className="w-full"
                  onClick={handleGenerateNotes}
                  disabled={isGenerating}
                >
                  {isGenerating ? "Generating..." : "Generate (+25 XP)"}
                </Button>
              </div>
            </div>
        )}

        {/* Notes List */}
        <div className="grid gap-4">
          {filteredNotes.map((note) => (
            <div
              key={note.id}
              className="p-4 rounded-xl bg-card border hover:shadow-sm transition"
            >
              <div className="flex justify-between">
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-lg bg-primary/10">
                    <FileText className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">
                      {note.title}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {note.subject} • {note.chapter} • {note.pages} pages
                    </p>
                    <div className="flex items-center gap-3 mt-2">
                      <div className="flex items-center gap-1 text-xs text-success">
                        <CheckCircle className="w-3 h-3" />
                        <span>+{note.xpEarned} XP earned</span>
                      </div>
                      {note.isOfflineAvailable ? (
                        <div className="flex items-center gap-1 text-xs text-muted-foreground">
                          <CheckCircle className="w-3 h-3" />
                          <span>Available offline</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1 text-xs text-muted-foreground">
                          <CloudOff className="w-3 h-3" />
                          <span>Online only</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="icon">
                    <Eye className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={exportNoteAsPDF}
                  >
                    <Download className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
        {activeContent && (
          <div className="mt-8 p-6 border rounded-lg bg-card">
            <ReactMarkdown
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            >
              {activeContent}
            </ReactMarkdown>
          </div>
        )}


        {filteredNotes.length === 0 && (
          <div className="text-center py-12">
            <FileText className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold text-foreground mb-2">
              No notes found
            </h3>
            <p className="text-muted-foreground">
              Try adjusting your search or generate new notes.
            </p>
          </div>
        )}
      </main>
    </div>
  );
};

export default NotesPage;
