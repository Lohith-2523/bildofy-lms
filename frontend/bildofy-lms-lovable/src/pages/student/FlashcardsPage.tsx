import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { XPBadge } from "@/components/gamification/XPBadge";
import { ProgressRing } from "@/components/progress/ProgressRing";
import {
  ArrowLeft,
  Play,
  ChevronLeft,
  ChevronRight,
  Check,
  X,
  CheckCircle,
  Plus,
  Zap,
  Loader2,
  Trash2,
} from "lucide-react";
import { cn } from "@/lib/utils";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

type ViewState = "list" | "study" | "complete";

type Flashcard = {
  front: string;
  back: string;
};

type FlashcardSetSummary = {
  id: number;
  subject: string;
  chapter: string;
  cards_count: number;
  created_at: string;
};

const SUBJECTS: Record<string, string[]> = {
  Science: ["Electrostatics", "Magnetism"],
  Mathematics: ["Trigonometry", "Differential Calculus"],
  "Computer Science": ["Basics of Python", "Basics of SQL"],
};

const MASTERED_CACHE_KEY = "student_flashcards_mastered_v1";
const GENERATION_COOLDOWN_MS = 60 * 1000;

type CardLine = { kind: "paragraph" | "bullet"; text: string };

const parseDocumentLines = (raw: string): CardLine[] => {
  const normalized = (raw ?? "")
    .replace(/\\r\\n/g, "\n")
    .replace(/\\n/g, "\n")
    .replace(/\/n/g, "\n")
    .replace(/\r\n/g, "\n")
    .replace(/\t/g, "  ")
    .trim();

  const lines = normalized.split("\n");
  const parsed: CardLine[] = [];

  for (const originalLine of lines) {
    let line = originalLine.trim();
    if (!line) continue;

    line = line
      .replace(/^[\{\[\],]+/, "")
      .replace(/[\}\[\],]+$/, "")
      .replace(/^["'`]+/, "")
      .replace(/["'`]+$/, "")
      .replace(/,$/, "")
      .trim();

    line = line.replace(/^(front|back|question|answer|q|a)\s*:\s*/i, "");

    if (!line) continue;

    const isBullet =
      /^[-*�]\s+/.test(line) || /^\d+[\.\)]\s+/.test(line);

    if (isBullet) {
      line = line.replace(/^[-*�]\s+/, "").replace(/^\d+[\.\)]\s+/, "").trim();
      if (line) parsed.push({ kind: "bullet", text: line });
      continue;
    }

    parsed.push({ kind: "paragraph", text: line });
  }

  if (!parsed.length && normalized) {
    return [{ kind: "paragraph", text: normalized }];
  }

  return parsed;
};

const renderCardDocument = (raw: string) => {
  const lines = parseDocumentLines(raw);

  return (
    <div className="w-full max-h-[240px] overflow-y-auto pr-1 space-y-2">
      {lines.map((line, idx) =>
        line.kind === "bullet" ? (
          <p
            key={`b-${idx}`}
            className="text-sm sm:text-base leading-relaxed text-left max-w-[95%] mx-auto"
          >
            <span className="mr-2">�</span>
            {line.text}
          </p>
        ) : (
          <p
            key={`p-${idx}`}
            className="text-sm sm:text-base leading-relaxed text-center"
          >
            {line.text}
          </p>
        )
      )}
    </div>
  );
};

const FlashcardsPage: React.FC = () => {
  const [view, setView] = useState<ViewState>("list");
  const [flashcardSets, setFlashcardSets] = useState<FlashcardSetSummary[]>([]);
  const [cardsBySetId, setCardsBySetId] = useState<Record<number, Flashcard[]>>(
    {}
  );
  const [masteredBySetId, setMasteredBySetId] = useState<Record<number, number>>(
    {}
  );
  const [selectedSetId, setSelectedSetId] = useState<number | null>(null);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [knownInSession, setKnownInSession] = useState<Record<number, boolean>>(
    {}
  );
  const [status, setStatus] = useState<string | null>(null);

  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [showLoadingModal, setShowLoadingModal] = useState(false);
  const [subject, setSubject] = useState<string | null>(null);
  const [chapter, setChapter] = useState<string | null>(null);
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

  const currentCards = useMemo(() => {
    if (selectedSetId === null) return [];
    return cardsBySetId[selectedSetId] ?? [];
  }, [cardsBySetId, selectedSetId]);

  const currentCard = currentCards[currentCardIndex];

  const fetchFlashcardSets = async () => {
    const token = localStorage.getItem("access_token");
    const res = await fetch("http://localhost:8000/api/student/flashcards/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch flashcards");
    const data = await res.json();
    setFlashcardSets(Array.isArray(data) ? data : []);
  };

  const fetchFlashcardSetById = async (setId: number) => {
    if (cardsBySetId[setId]) return cardsBySetId[setId];

    const token = localStorage.getItem("access_token");
    const res = await fetch(
      `http://localhost:8000/api/student/flashcards/${setId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    if (!res.ok) throw new Error("Failed to load flashcard set");
    const data = await res.json();
    const cards = Array.isArray(data.cards) ? data.cards : [];
    setCardsBySetId((prev) => ({ ...prev, [setId]: cards }));
    return cards;
  };

  useEffect(() => {
    const cached = localStorage.getItem(MASTERED_CACHE_KEY);
    if (cached) {
      try {
        setMasteredBySetId(JSON.parse(cached));
      } catch {
        localStorage.removeItem(MASTERED_CACHE_KEY);
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(MASTERED_CACHE_KEY, JSON.stringify(masteredBySetId));
  }, [masteredBySetId]);

  useEffect(() => {
    fetchFlashcardSets().catch((err) =>
      setStatus(err.message || "Failed to fetch flashcards")
    );
  }, []);

  const resetStudy = () => {
    setCurrentCardIndex(0);
    setIsFlipped(false);
    setSelectedSetId(null);
    setKnownInSession({});
    setView("list");
  };

  const markCardAndAdvance = (didKnow: boolean) => {
    if (didKnow) {
      setKnownInSession((prev) => ({ ...prev, [currentCardIndex]: true }));
    }

    setIsFlipped(false);
    if (currentCardIndex === currentCards.length - 1) {
      if (selectedSetId !== null) {
        const sessionMastered = Object.keys({
          ...knownInSession,
          ...(didKnow ? { [currentCardIndex]: true } : {}),
        }).length;
        setMasteredBySetId((prev) => ({
          ...prev,
          [selectedSetId]: Math.max(prev[selectedSetId] ?? 0, sessionMastered),
        }));
      }
      setView("complete");
      return;
    }
    setCurrentCardIndex((i) => i + 1);
  };

  const handleStartReview = async (setId: number) => {
    try {
      setStatus(null);
      const cards = await fetchFlashcardSetById(setId);
      if (!cards.length) {
        setStatus("This flashcard set has no cards.");
        return;
      }
      setSelectedSetId(setId);
      setCurrentCardIndex(0);
      setIsFlipped(false);
      setKnownInSession({});
      setView("study");
    } catch (err: any) {
      setStatus(err.message || "Failed to open flashcard set");
    }
  };

  const handleGenerateFlashcards = async () => {
    if (!subject || !chapter || isOnCooldown) return;

    const token = localStorage.getItem("access_token");
    setShowGenerateModal(false);
    setShowLoadingModal(true);
    setStatus(null);

    try {
      const res = await fetch(
        "http://localhost:8000/api/student/flashcards/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            subject,
            chapter,
            context: {
              client_type: window.innerWidth < 768 ? "mobile" : "desktop",
              connectivity: navigator.onLine ? "online" : "offline",
              model_capability: navigator.onLine ? "heavy" : "light",
            },
          }),
        }
      );

      if (!res.ok) throw new Error("Failed to generate flashcards");
      const generated = await res.json();

      const setId = Number(generated.set_id);
      const cards = Array.isArray(generated.cards) ? generated.cards : [];
      if (setId && cards.length) {
        setCardsBySetId((prev) => ({ ...prev, [setId]: cards }));
      }

      setLastGeneratedAt(Date.now());
      setSubject(null);
      setChapter(null);
      await fetchFlashcardSets();
    } catch (err: any) {
      setStatus(err.message || "Failed to generate flashcards");
    } finally {
      setShowLoadingModal(false);
    }
  };

  const handleDeleteSet = async (setId: number) => {
    const confirmed = window.confirm(
      "Delete this flashcard set? This action cannot be undone."
    );
    if (!confirmed) return;

    const token = localStorage.getItem("access_token");
    setStatus(null);

    try {
      const res = await fetch(
        `http://localhost:8000/api/student/flashcards/${setId}`,
        {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (!res.ok) throw new Error("Failed to delete flashcard set");

      setFlashcardSets((prev) => prev.filter((s) => s.id !== setId));
      setCardsBySetId((prev) => {
        const next = { ...prev };
        delete next[setId];
        return next;
      });
      setMasteredBySetId((prev) => {
        const next = { ...prev };
        delete next[setId];
        return next;
      });
    } catch (err: any) {
      setStatus(err.message || "Failed to delete flashcard set");
    }
  };

  if (view === "study" && selectedSetId !== null && currentCard) {
    return (
      <div className="min-h-screen bg-background">
        <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
          <div className="container mx-auto px-4 py-4 flex justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={resetStudy}>
                <ArrowLeft className="w-5 h-5" />
              </Button>
              <div>
                <h1 className="text-xl font-bold">Review Mode</h1>
                <p className="text-sm text-muted-foreground">
                  Card {currentCardIndex + 1} of {currentCards.length}
                </p>
              </div>
            </div>
            <XPBadge xp={15} size="sm" />
          </div>
        </header>

        <main className="container mx-auto px-4 py-8">
          <div className="flex justify-center mb-6 gap-1">
            {currentCards.map((_, index) => (
              <div
                key={index}
                className={cn(
                  "w-8 h-2 rounded-full",
                  index < currentCardIndex
                    ? "bg-success"
                    : index === currentCardIndex
                    ? "bg-primary"
                    : "bg-secondary"
                )}
              />
            ))}
          </div>

          <div
            className="max-w-lg mx-auto cursor-pointer"
            onClick={() => setIsFlipped(!isFlipped)}
          >
            <div
              className="relative w-full aspect-[3/2] transition-all duration-500"
              style={{
                transformStyle: "preserve-3d",
                transform: isFlipped ? "rotateY(180deg)" : "rotateY(0deg)",
              }}
            >
              <div
                className="absolute inset-0 p-8 rounded-2xl bg-gradient-primary text-primary-foreground shadow-lg flex flex-col items-center justify-center text-center"
                style={{ backfaceVisibility: "hidden" }}
              >
                <p className="text-xs uppercase opacity-70 mb-4">Question</p>
                <div className="w-full max-h-[240px] overflow-y-auto pr-1 text-left text-lg leading-relaxed whitespace-pre-wrap break-words">
                  {renderCardDocument(currentCard.front)}
                </div>
                <p className="text-sm opacity-70 mt-4">Tap to reveal</p>
              </div>

              <div
                className="absolute inset-0 p-8 rounded-2xl bg-card border shadow-lg flex flex-col items-center justify-center text-center"
                style={{
                  backfaceVisibility: "hidden",
                  transform: "rotateY(180deg)",
                }}
              >
                <p className="text-xs uppercase text-muted-foreground mb-4">
                  Answer
                </p>
                <div className="w-full max-h-[240px] overflow-y-auto pr-1 text-left text-base leading-relaxed whitespace-pre-wrap break-words">
                  {renderCardDocument(currentCard.back)}
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-center gap-4 mt-8">
            <Button
              variant="outline"
              size="lg"
              disabled={currentCardIndex === 0}
              onClick={() => {
                setIsFlipped(false);
                setCurrentCardIndex((i) => i - 1);
              }}
            >
              <ChevronLeft />
            </Button>

            <Button
              variant="destructive"
              size="lg"
              onClick={() => markCardAndAdvance(false)}
            >
              <X className="mr-1" /> Didn't Know
            </Button>

            <Button variant="success" size="lg" onClick={() => markCardAndAdvance(true)}>
              <Check className="mr-1" /> Got It
            </Button>

            <Button
              variant="outline"
              size="lg"
              disabled={currentCardIndex === currentCards.length - 1}
              onClick={() => {
                setIsFlipped(false);
                setCurrentCardIndex((i) => i + 1);
              }}
            >
              <ChevronRight />
            </Button>
          </div>
        </main>
      </div>
    );
  }

  if (view === "complete") {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-4">
          <CheckCircle className="w-12 h-12 mx-auto text-success" />
          <h2 className="text-2xl font-bold">Session Complete</h2>
          <p className="text-muted-foreground">You earned XP for studying!</p>
          <Button onClick={resetStudy}>Back to Flashcards</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/student">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-xl font-bold">Flashcards</h1>
            <p className="text-sm text-muted-foreground">
              Review and memorize concepts
            </p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 grid gap-4">
        <div className="flex justify-end">
          <div className="relative">
            <Button onClick={() => setShowGenerateModal(true)} disabled={isOnCooldown}>
              <Plus className="w-4 h-4 mr-1" />
              Generate Flashcards
            </Button>
            <div className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs px-2 py-0.5 rounded-full flex items-center gap-1 shadow">
              <Zap className="w-3 h-3" />
              {isOnCooldown ? `${cooldownRemaining}s` : "+30 XP"}
            </div>
          </div>
        </div>

        {status && (
          <div className="p-3 rounded-md border border-destructive/30 bg-destructive/10 text-sm text-destructive">
            {status}
          </div>
        )}

        {flashcardSets.length === 0 && !status && (
          <div className="p-6 rounded-xl border bg-card text-center text-muted-foreground">
            No flashcards generated yet. Create your first set.
          </div>
        )}

        {flashcardSets.map((set) => {
          const mastered = Math.min(
            masteredBySetId[set.id] ?? 0,
            set.cards_count || 0
          );
          const progress =
            set.cards_count > 0
              ? Math.round((mastered / set.cards_count) * 100)
              : 0;

          return (
            <div
              key={set.id}
              className="p-5 rounded-xl bg-card border hover:shadow-md transition"
            >
              <div className="flex justify-between">
                <div className="flex gap-4">
                  <ProgressRing progress={progress} size={80} />
                  <div>
                    <h3 className="font-semibold">{set.chapter}</h3>
                    <p className="text-sm text-muted-foreground">
                      {set.subject} - {mastered}/{set.cards_count} mastered
                    </p>
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <XPBadge xp={15} size="sm" />
                  <div className="flex items-center gap-2">
                    <Button size="sm" onClick={() => handleStartReview(set.id)}>
                      <Play className="w-4 h-4 mr-1" />
                      Review
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => handleDeleteSet(set.id)}
                    >
                      <Trash2 className="w-4 h-4 mr-1" />
                      Delete
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </main>

      <Dialog open={showGenerateModal} onOpenChange={setShowGenerateModal}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Generate Flashcards</DialogTitle>
          </DialogHeader>

          <div className="space-y-4">
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

            <Button
              className="w-full"
              disabled={!subject || !chapter || isOnCooldown}
              onClick={handleGenerateFlashcards}
            >
              Generate Flashcards
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      <Dialog open={showLoadingModal}>
        <DialogContent className="sm:max-w-sm text-center">
          <div className="flex flex-col items-center gap-4 py-6">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
            <p className="text-sm text-muted-foreground">
              Generating your flashcards...
            </p>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default FlashcardsPage;

