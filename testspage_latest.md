import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { XPBadge } from '@/components/gamification/XPBadge';
import { ProgressRing } from '@/components/progress/ProgressRing';
import { useOnlineStatus } from '@/contexts/OnlineContext';
import MarkdownKatexRenderer from '@/components/MarkdownKatexRenderer';
import {
  ArrowLeft,
  ClipboardCheck,
  Clock,
  Target,
  Play,
  Trophy,
  Zap,
  WifiOff,
} from 'lucide-react';
import { cn } from '@/lib/utils';
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
import { Loader2 } from "lucide-react";


type Difficulty = 'easy' | 'medium' | 'hard';

type TestSummary = {
  id: number;
  title: string;
  subject: string;
  difficulty: Difficulty;
  total_questions: number;
  duration: number;
  xp_reward: number;
  is_completed: boolean;
  best_score: number | null;
};

type Question = {
  question: string;
  options: string[];
};

type FullTest = {
  id: number;
  title: string;
  questions: Question[];
};

const SUBJECTS = {
  Science: ["Electrostatics", "Magnetism"],
  Mathematics: ["Trigonometry", "Differential Calculus"],
  "Computer Science": ["Basics of Python", "Basics of SQL"],
};
const SUBJECT_ID_MAP: Record<string, number> = {
  Science: 2,
};

const DIFFICULTIES = ["easy", "medium", "hard"] as const;

const difficultyConfig = {
  easy: { label: 'Easy', color: 'bg-success/10 text-success border-success/30' },
  medium: { label: 'Medium', color: 'bg-warning/10 text-warning border-warning/30' },
  hard: { label: 'Hard', color: 'bg-destructive/10 text-destructive border-destructive/30' },
};

const TestsPage: React.FC = () => {
  const { isOnline } = useOnlineStatus();
  const navigate = useNavigate();
  const { testId } = useParams();
  const token = localStorage.getItem('access_token');

  const [tests, setTests] = useState<TestSummary[]>([]);
  const [test, setTest] = useState<FullTest | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [score, setScore] = useState<number | null>(null);
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [showLoadingModal, setShowLoadingModal] = useState(false);

  const [subject, setSubject] = useState<string | null>(null);
  const [chapter, setChapter] = useState<string | null>(null);
  const [difficulty, setDifficulty] = useState<string | null>(null);

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
  
  const handleGenerateTest = async () => {
    if (!subject || !chapter || !difficulty || isOnCooldown) return;

    setShowGenerateModal(false);
    setShowLoadingModal(true);

    try {
      const res = await fetch(
        "http://localhost:8000/student/tests/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
             title: `${subject} – ${chapter} (${difficulty})`,
              subject_id: SUBJECT_ID_MAP[subject], // always 2
              subject: subject,
              chapter: chapter,
              difficulty: difficulty,
          }),
        }
      );

      if (!res.ok) {
        throw new Error("Failed to generate test");
      }

      // mark cooldown
      setLastGeneratedAt(Date.now());

      // refresh test list
      await fetchTests();
    } catch (err) {
      console.error(err);
    } finally {
      setShowLoadingModal(false);
    }
  };

  /* ================= LIST TESTS ================= */
  const fetchTests = async () => {
  const res = await fetch("http://localhost:8000/student/tests", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();
    setTests(data);
  };

  useEffect(() => {
    if (!token || testId) return;
    fetchTests();
  }, [token, testId]);


  /* ================= LOAD TEST BY ID ================= */
  useEffect(() => {
    if (!token || !testId) return;

    fetch(`http://localhost:8000/student/tests/${test.id}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => {
        setTest(data);
        setAnswers({});
        setCurrentIndex(0);
        setScore(null);
      });
  }, [token, testId]);

  /* ================= SUBMIT ================= */
  const submitTest = async () => {
    if (!test) return;

    const orderedAnswers = test.questions.map((_, i) => answers[i] ?? '');

    const res = await fetch(
      `http://localhost:8000/student/tests/${test.id}/submit`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ answers: orderedAnswers }),
      }
    );

    const data = await res.json();
    setScore(data.score);
  };

  /* ================= OFFLINE ================= */
  if (!isOnline) {
    return (
      <div className="p-6 text-center text-sm text-muted-foreground">
        <WifiOff className="mx-auto mb-2" />
        Tests require an internet connection.
      </div>
    );
  }

  /* ================= TEST INTERFACE ================= */
  if (testId && test) {
    const q = test.questions[currentIndex];

    return (
      <div className="min-h-screen bg-background p-6 space-y-6">
        <Button variant="ghost" onClick={() => navigate('/student/tests/${test.id}')}>
          <ArrowLeft className="w-4 h-4 mr-1" />
          Back
        </Button>

        {score === null ? (
          <>
            <MarkdownKatexRenderer content={q.question} />

            <div className="space-y-2">
              {q.options.map((opt, idx) => (
                <Button
                  key={idx}
                  variant={answers[currentIndex] === opt ? 'default' : 'outline'}
                  className="w-full justify-start"
                  onClick={() =>
                    setAnswers((a) => ({ ...a, [currentIndex]: opt }))
                  }
                >
                  <MarkdownKatexRenderer content={opt} />
                </Button>
              ))}
            </div>

            <div className="flex justify-between">
              <Button
                variant="outline"
                disabled={currentIndex === 0}
                onClick={() => setCurrentIndex((i) => i - 1)}
              >
                Previous
              </Button>

              {currentIndex === test.questions.length - 1 ? (
                <Button onClick={submitTest}>Submit</Button>
              ) : (
                <Button onClick={() => setCurrentIndex((i) => i + 1)}>
                  Next
                </Button>
              )}
            </div>
          </>
        ) : (
          <div className="text-center">
            <h2 className="text-2xl font-bold">Result</h2>
            <p className="text-lg">
              Score: {score} / {test.questions.length}
            </p>
          </div>
        )}
      </div>
    );
  }

  /* ================= TEST LIST ================= */
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
            <h1 className="text-xl font-display font-bold text-foreground">Tests</h1>
            <p className="text-sm text-muted-foreground">Practice and earn XP</p>
          </div>
        </div>
      </header>
      

      <main className="container mx-auto px-4 py-6">
       <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-display font-semibold text-foreground">
          Available Tests
        </h2>

        <div className="relative">
          <Button
            onClick={() => setShowGenerateModal(true)}
            disabled={isOnCooldown}
          >
            Generate Test
          </Button>


            {/* XP Overlay */}
            <div className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs px-2 py-0.5 rounded-full flex items-center gap-1 shadow">
              <Zap className="w-3 h-3" />
              {isOnCooldown ? `${cooldownRemaining}s` : "+250 XP"}
            </div>
          </div>
        </div>
        <Dialog open={showGenerateModal} onOpenChange={setShowGenerateModal}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Generate Test</DialogTitle>
            </DialogHeader>

            <div className="space-y-4">
              {/* Subject */}
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

              {/* Chapter */}
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

              {/* Difficulty */}
              <Select
                value={difficulty ?? ""}
                onValueChange={setDifficulty}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Difficulty" />
                </SelectTrigger>
                <SelectContent>
                  {DIFFICULTIES.map((diff) => (
                    <SelectItem key={diff} value={diff}>
                      {diff.charAt(0).toUpperCase() + diff.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Button
                className="w-full"
                disabled={!subject || !chapter || !difficulty}
                onClick={handleGenerateTest}
              >
                Generate Test
              </Button>
            </div>
          </DialogContent>
        </Dialog>
        
        <Dialog open={showLoadingModal}>
          <DialogContent className="sm:max-w-sm text-center">
            <div className="flex flex-col items-center gap-4 py-6">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
              <p className="text-sm text-muted-foreground">
                Generating your test…
              </p>
            </div>
          </DialogContent>
        </Dialog>


        <div className="grid gap-4">
          {tests.map((test, index) => {
            const difficulty =
              difficultyConfig[test.difficulty as keyof typeof difficultyConfig] ??
              difficultyConfig.medium;

            return (
              <div
                key={test.id}
                className={cn(
                  'p-5 rounded-xl bg-card border border-border shadow-sm transition-all duration-200',
                  'hover:shadow-md hover:border-primary/30',
                  test.is_completed && 'bg-success/5 border-success/20'
                )}
              >

                <div className="flex items-start justify-between gap-4">
                  <div>
                    <span className={cn('text-xs px-2 py-0.5 rounded-full border', difficulty.color)}>
                      {difficulty.label}
                    </span>
                    <h3 className="font-semibold mt-1">{test.title}</h3>
                    <div className="text-sm text-muted-foreground flex gap-4">
                      <span>{test.total_questions} questions</span>
                      <span>{test.duration} min</span>
                    </div>
                  </div>

                  <div className="flex flex-col items-end gap-2">
                    {test.is_completed ? (
                      <>
                        <ProgressRing
                          progress={test.best_score ?? 0}
                          size={50}
                          color="success"
                        />
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => navigate(`/student/tests/${test.id}`)}
                        >
                          Retry
                        </Button>
                      </>
                    ) : (
                      <>
                        <XPBadge xp={test.xp_reward} />
                        <Button
                          size="sm"
                          onClick={() => navigate(`/student/tests/${test.id}`)}
                        >
                          Start Test
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
};

export default TestsPage;
