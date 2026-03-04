import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useOnlineStatus } from "@/contexts/OnlineContext";
import { api } from "@/lib/api";
import {
  ArrowLeft,
  FileText,
  Plus,
  Download,
  Search,
  CloudOff,
  Eye,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

/* === Markdown + KaTeX === */
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

const NOTES_CACHE_KEY = "student_notes_cache_v1";

const SUBJECTS = {
  Science: ["Electrostatics", "Magnetism"],
  Mathematics: ["Trigonometry", "Differential Calculus"],
  "Computer Science": ["Basics of Python", "Basics of SQL"],
};

const DIFFICULTIES = ["easy", "medium", "hard"] as const;

const difficultyConfig = {
  easy: { label: 'Easy', color: 'bg-success/10 text-success border-success/30' },
  medium: { label: 'Medium', color: 'bg-warning/10 text-warning border-warning/30' },
  hard: { label: 'Hard', color: 'bg-destructive/10 text-destructive border-destructive/30' },
};

type NoteItem = {
  id: string;
  title: string;
  subject: string;
  chapter: string;
  createdAt: Date;
  isOfflineAvailable: boolean;
};

const NotesPage: React.FC = () => {
  const { isOnline } = useOnlineStatus();

  const [searchQuery, setSearchQuery] = useState("");
  const [showGenerateForm, setShowGenerateForm] = useState(false);
  const [notesList, setNotesList] = useState<NoteItem[]>([]);
  const [teacherNotes, setTeacherNotes] = useState<any[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const [subject, setSubject] = useState<string | null>(null);
  const [chapter, setChapter] = useState<string | null>(null);
  const [difficulty, setDifficulty] = useState<string | null>(null);
  const token = localStorage.getItem("access_token");
  const [activeNoteId, setActiveNoteId] = useState<string | null>(null);
  const [activeContent, setActiveContent] = useState<string | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  const GENERATION_COOLDOWN_MS = 60 * 1000; // 1 minute (UI only)
  const [lastGeneratedAt, setLastGeneratedAt] = useState<number | null>(null);

  const isOnCooldown =
    lastGeneratedAt !== null &&
    Date.now() - lastGeneratedAt < GENERATION_COOLDOWN_MS;

  const cooldownRemaining = lastGeneratedAt
    ? Math.max(
        0,
        Math.ceil(
          (GENERATION_COOLDOWN_MS - (Date.now() - lastGeneratedAt)) / 1000
        )
      )
    : 0;
  const getAuthHeaders = () => {
    const token = localStorage.getItem("access_token");
    return {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };
  };
  const handleViewNote = async (noteId: string) => {
    try {
      const res = await fetch(
        `http://localhost:8000/api/student/notes/storage/${noteId}`,
        {
          method: "GET",
          headers: getAuthHeaders(),
        }
      );

      if (!res.ok) {
        throw new Error("Failed to fetch note");
      }

      const data = await res.json();
      setActiveNoteId(noteId);
      setActiveContent(data.content);
    } catch (err) {
      console.error("View note error:", err);
    }
  };

  const handleDownloadNote = async (noteId: string) => {
    try {
      const res = await fetch(
        `http://localhost:8000/api/student/notes/storage/${noteId}/pdf`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );

      if (!res.ok) {
        throw new Error("Download failed");
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `notes_${noteId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download error:", err);
    }
  };

const handleViewPdf = async (noteId: string) => {
  try {
    const token = localStorage.getItem("access_token");

    const res = await fetch(
      `http://localhost:8000/api/student/notes/storage/${noteId}/pdf`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!res.ok) {
      throw new Error("Failed to generate PDF");
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    setPdfUrl(url);

  } catch (err) {
    console.error(err);
  }
};


    

  /* === Load cached notes === */
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
    localStorage.setItem(NOTES_CACHE_KEY, JSON.stringify(notesList));
  }, [notesList]);

  /* === Fetch teacher-provided notes === */
  useEffect(() => {
  const token = localStorage.getItem("access_token");

  fetch("http://localhost:8000/api/student/notes/teacher/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Failed to fetch teacher notes");
      }
      return res.json();
    })
    .then((data) => {
      // Defensive: ensure we always set an array
      if (Array.isArray(data)) {
        setTeacherNotes(data);
      } else {
        setTeacherNotes([]);
        console.error("Unexpected response:", data);
      }
    })
    .catch(console.error);
}, []);


  const filteredNotes = notesList.filter(
    (note) =>
      note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      note.subject.toLowerCase().includes(searchQuery.toLowerCase())
  );

  /* === Generate student notes === */
  const handleGenerateNotes = async () => {
    if (!subject || !chapter) return;

    setIsGenerating(true);

    try {
      const res = await fetch(
        "http://localhost:8000/api/student/notes/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            subject,
            chapter,
            difficulty,
            context: {
              client_type: window.innerWidth < 768 ? "mobile" : "desktop",
              connectivity: navigator.onLine ? "online" : "offline",
              model_capability: navigator.onLine ? "heavy" : "light",
              user_id: 1, // DEV auth
            },
          }),
        }
      );

      if (!res.ok) throw new Error("Failed to generate notes");

      const data = await res.json();

      const noteRes = await fetch(
        `http://localhost:8000/api/student/notes/storage/${data.content_id}`
      );
      const noteData = await noteRes.json();

      setActiveNoteId(data.content_id);
      setActiveContent(noteData.content);

      setNotesList((prev) => [
        {
          id: data.content_id,
          title: chapter,
          subject,
          chapter,
          createdAt: new Date(),
          isOfflineAvailable: true,
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

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/student">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-xl font-bold">Notes</h1>
            <p className="text-sm text-muted-foreground">
              AI-generated & teacher-shared notes
            </p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search notes"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
            <div className="relative">
              <Button
                onClick={() => setShowGenerateForm(true)}
                disabled={isOnCooldown}
              >
                <Plus className="w-4 h-4 mr-1" />Generate Notes
              </Button>
              {/* XP Overlay */}
              <div className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs px-2 py-0.5 rounded-full flex items-center gap-1 shadow">
                <Zap className="w-3 h-3" />
                {isOnCooldown ? `${cooldownRemaining}s` : "+40 XP"}
              </div>
            </div>
        </div>
        {/* Generate Form */}
        {showGenerateForm && (
          <div className="border rounded-xl p-6 bg-card mb-8 space-y-4">
            <h2 className="text-lg font-semibold">Generate Notes</h2>

            <div className="space-y-3">
              <Select
                value={subject ?? ""}
                onValueChange={(val) => {
                  setSubject(val);
                  setChapter(null);
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Subject" />
                </SelectTrigger>
                <SelectContent>
                  {Object.keys(SUBJECTS).map((subj) => (
                    <SelectItem key={subj} value={subj}>
                      {subj}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Select
                value={chapter ?? ""}
                onValueChange={setChapter}
                disabled={!subject}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Chapter" />
                </SelectTrigger>
                <SelectContent>
                  {subject &&
                    SUBJECTS[subject].map((chap) => (
                      <SelectItem key={chap} value={chap}>
                        {chap}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>

              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="w-full border rounded-md px-3 py-2 bg-background"
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>

            <div className="flex gap-3">
              <Button
                onClick={handleGenerateNotes}
                disabled={isGenerating || isOnCooldown}
              >
                {isGenerating ? "Generating..." : "Generate"}
              </Button>

              <Button
                variant="outline"
                onClick={() => setShowGenerateForm(false)}
              >
                Cancel
              </Button>
            </div>
          </div>
        )}


        {/* Student Notes */}
        <div className="space-y-3">
          {filteredNotes.map((note) => (
            <div
              key={note.id}
              className="border rounded-lg p-4 flex justify-between"
            >
              <div>
                <p className="font-medium">{note.title}</p>
                <p className="text-sm text-muted-foreground">
                  {note.subject}
                </p>
              </div>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  onClick={() => handleViewPdf(note.id)}
                >
                  <Eye className="w-4 h-4" />
                </Button>
                <Button
                  size="sm"
                  onClick={() => handleDownloadNote(note.id)}
                >

                  <Download className="w-4 h-4" />
                </Button>
              </div>
            </div>
          ))}
        </div>

        {/* Teacher Notes */}
        <div className="mt-10">
          <h2 className="text-lg font-semibold mb-4">
            Notes Shared by Teacher
          </h2>

          <div className="space-y-3">
            {teacherNotes.map((note) => (
              <div
                key={note.id}
                className="border rounded-lg p-4 flex justify-between"
              >
                <div>
                  <p className="font-medium">
                    {note.subject} — {note.chapter}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {note.mode === "upload" ? "PDF" : "AI / Manual"}
                  </p>
                </div>
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    onClick={async () => {
                      const res = await fetch(
                        `http://localhost:8000/api/student/notes/teacher/${note.id}`
                      );
                      const data = await res.json();
                      if (data.type === "markdown") {
                        setActiveContent(data.content);
                      } else {
                        window.open(data.url, "_blank");
                      }
                    }}
                  >
                    View
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() =>
                      window.open(
                        `http://localhost:8000/api/student/notes/teacher/${note.id}/download`,
                        "_blank"
                      )
                    }
                  >
                    Download
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Notes Viewer */}
        {pdfUrl && (
          <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
            <div className="bg-white w-[90%] h-[90%] rounded-lg relative">
              
              <button
                onClick={() => {
                  URL.revokeObjectURL(pdfUrl);
                  setPdfUrl(null);
                }}
                className="absolute top-3 right-3 bg-red-500 text-white px-3 py-1 rounded"
              >
                Close
              </button>

              <iframe
                src={pdfUrl}
                className="w-full h-full rounded-lg"
                title="PDF Viewer"
              />
            </div>
          </div>
        )}

      </main>
    </div>
  );
};

export default NotesPage;
