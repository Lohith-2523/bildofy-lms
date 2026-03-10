import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, ClipboardCheck, Sparkles, Plus, Trash2 } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import SearchableSelect from "@/components/form/SearchableSelect";

type QuestionType = "MCQ" | "SUBJECTIVE";

type BuilderQuestion = {
  id: string;
  question: string;
  options: string[];
  correctAnswer: string;
};

type SuggestedQuestion = {
  question: string;
  question_type: QuestionType;
  options: string[];
  correct_answer: string;
};

const newQuestion = (): BuilderQuestion => ({
  id: crypto.randomUUID(),
  question: "",
  options: ["", "", "", ""],
  correctAnswer: "",
});

type TeacherSubject = {
  id: number;
  name: string;
  type: string;
  class_id: number | null;
};

const CreateTestPage = () => {
  const [title, setTitle] = useState("");
  const [subjectId, setSubjectId] = useState("");
  const [chapter, setChapter] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [questionType, setQuestionType] = useState<QuestionType>("MCQ");
  const [questions, setQuestions] = useState<BuilderQuestion[]>([newQuestion()]);
  const [suggestions, setSuggestions] = useState<Record<string, SuggestedQuestion>>(
    {}
  );
  const [loadingByQuestion, setLoadingByQuestion] = useState<Record<string, boolean>>(
    {}
  );
  const [status, setStatus] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [teacherSubjects, setTeacherSubjects] = useState<TeacherSubject[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/teacher/subjects/", {
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
    })
      .then(async (r) => {
        if (!r.ok) throw new Error("Failed to load your subjects");
        return r.json();
      })
      .then((data) => {
        const subjects = Array.isArray(data) ? data : [];
        setTeacherSubjects(subjects);
        if (subjects.length === 1) {
          setSubjectId(String(subjects[0].id));
        }
      })
      .catch((err) => setStatus(err.message));
  }, []);

  const selectedSubject = useMemo(
    () => teacherSubjects.find((s) => String(s.id) === subjectId) || null,
    [teacherSubjects, subjectId]
  );

  const updateQuestion = (
    id: string,
    patch: Partial<BuilderQuestion>
  ) => {
    setQuestions((prev) => prev.map((q) => (q.id === id ? { ...q, ...patch } : q)));
  };

  const updateOption = (id: string, optionIndex: number, value: string) => {
    setQuestions((prev) =>
      prev.map((q) => {
        if (q.id !== id) return q;
        const nextOptions = [...q.options];
        nextOptions[optionIndex] = value;
        return { ...q, options: nextOptions };
      })
    );
  };

  const handleSuggest = async (q: BuilderQuestion) => {
    if (!selectedSubject || !chapter) {
      setStatus("Please select subject and chapter before AI assist.");
      return;
    }

    setStatus(null);
    setLoadingByQuestion((prev) => ({ ...prev, [q.id]: true }));

    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(
        "http://localhost:8000/api/teacher/tests/ai-suggest-question",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            subject: selectedSubject.name,
            chapter,
            difficulty,
            question_type: questionType,
            context: {
              client_type: window.innerWidth < 768 ? "mobile" : "desktop",
              connectivity: navigator.onLine ? "online" : "offline",
              model_capability: navigator.onLine ? "heavy" : "light",
            },
          }),
        }
      );
      if (!res.ok) throw new Error("AI suggestion failed");
      const data = await res.json();
      setSuggestions((prev) => ({ ...prev, [q.id]: data }));
    } catch (err: any) {
      setStatus(err.message || "Failed to fetch AI suggestion");
    } finally {
      setLoadingByQuestion((prev) => ({ ...prev, [q.id]: false }));
    }
  };

  const applySuggestion = (id: string) => {
    const suggestion = suggestions[id];
    if (!suggestion) return;

    updateQuestion(id, {
      question: suggestion.question,
      correctAnswer: suggestion.correct_answer,
      options:
        questionType === "MCQ"
          ? [...(suggestion.options || []), "", "", "", ""].slice(0, 4)
          : ["", "", "", ""],
    });
    setSuggestions((prev) => {
      const next = { ...prev };
      delete next[id];
      return next;
    });
  };

  const rejectSuggestion = (id: string) => {
    setSuggestions((prev) => {
      const next = { ...prev };
      delete next[id];
      return next;
    });
  };

  const handleSaveTest = async () => {
    if (!title || !subjectId || questions.length === 0) {
      setStatus("Please fill title, subject id, and at least one question.");
      return;
    }

    const token = localStorage.getItem("access_token");
    setIsSaving(true);
    setStatus(null);

    try {
      const payload = {
        title,
        subject_id: Number(subjectId),
        difficulty,
        questions: questions.map((q) => ({
          question: q.question,
          question_type: questionType,
          options: questionType === "MCQ" ? q.options.filter(Boolean) : [],
          correct_answer: q.correctAnswer,
        })),
      };

      const res = await fetch("http://localhost:8000/api/teacher/tests/create-manual", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to create test");
      setStatus("Test created successfully.");
      setQuestions([newQuestion()]);
      setTitle("");
      setChapter("");
    } catch (err: any) {
      setStatus(err.message || "Failed to create test");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card border-b">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/teacher">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <h1 className="text-xl font-bold">Create Test</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-4xl space-y-6">
        <div className="grid md:grid-cols-2 gap-4">
          <Input
            placeholder="Test Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <SearchableSelect
            value={subjectId}
            options={teacherSubjects.map((s) => ({
              value: String(s.id),
              label: `${s.name} (#${s.id})`,
            }))}
            placeholder="Select your subject"
            onChange={setSubjectId}
            disabled={teacherSubjects.length === 1}
          />
          <Input
            placeholder="Chapter (for AI assist)"
            value={chapter}
            onChange={(e) => setChapter(e.target.value)}
          />
          <Select value={difficulty} onValueChange={setDifficulty}>
            <SelectTrigger>
              <SelectValue placeholder="Difficulty" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="easy">Easy</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="hard">Hard</SelectItem>
            </SelectContent>
          </Select>
          <Select
            value={questionType}
            onValueChange={(v) => setQuestionType(v as QuestionType)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Question Type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="MCQ">MCQ</SelectItem>
              <SelectItem value="SUBJECTIVE">Subjective</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {questions.map((q, idx) => (
          <div key={q.id} className="border rounded-lg p-4 space-y-3 bg-card">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold">Question {idx + 1}</h3>
              <div className="flex items-center gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleSuggest(q)}
                  disabled={loadingByQuestion[q.id]}
                >
                  <Sparkles className="w-4 h-4 mr-1" />
                  {loadingByQuestion[q.id] ? "Suggesting..." : "AI Assist"}
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() =>
                    setQuestions((prev) => prev.filter((x) => x.id !== q.id))
                  }
                  disabled={questions.length === 1}
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            </div>

            {suggestions[q.id] && (
              <div className="p-3 rounded-md border bg-secondary/30 space-y-2">
                <p className="text-sm font-medium">AI Suggestion</p>
                <p className="text-sm">{suggestions[q.id].question}</p>
                {questionType === "MCQ" && (
                  <ul className="text-sm list-disc ml-5">
                    {suggestions[q.id].options.map((o, i) => (
                      <li key={i}>{o}</li>
                    ))}
                  </ul>
                )}
                <p className="text-sm">
                  <span className="font-medium">Answer: </span>
                  {suggestions[q.id].correct_answer}
                </p>
                <div className="flex gap-2">
                  <Button size="sm" onClick={() => applySuggestion(q.id)}>
                    Use Suggestion
                  </Button>
                  <Button size="sm" variant="outline" onClick={() => rejectSuggestion(q.id)}>
                    Reject
                  </Button>
                </div>
              </div>
            )}

            <Textarea
              placeholder="Question text"
              value={q.question}
              onChange={(e) => updateQuestion(q.id, { question: e.target.value })}
            />

            {questionType === "MCQ" && (
              <div className="grid md:grid-cols-2 gap-2">
                {q.options.map((opt, oIdx) => (
                  <Input
                    key={oIdx}
                    placeholder={`Option ${oIdx + 1}`}
                    value={opt}
                    onChange={(e) => updateOption(q.id, oIdx, e.target.value)}
                  />
                ))}
              </div>
            )}

            <Input
              placeholder={questionType === "MCQ" ? "Correct option text" : "Reference answer"}
              value={q.correctAnswer}
              onChange={(e) =>
                updateQuestion(q.id, { correctAnswer: e.target.value })
              }
            />
          </div>
        ))}

        <Button
          variant="outline"
          className="w-full"
          onClick={() => setQuestions((prev) => [...prev, newQuestion()])}
        >
          <Plus className="w-4 h-4 mr-1" />
          Add Question
        </Button>

        {status && (
          <div className="text-sm p-3 rounded-md border bg-secondary/30">{status}</div>
        )}

        <Button className="w-full gap-2" onClick={handleSaveTest} disabled={isSaving}>
          <ClipboardCheck className="w-4 h-4" />
          {isSaving ? "Creating Test..." : "Create Test"}
        </Button>
      </main>
    </div>
  );
};

export default CreateTestPage;
