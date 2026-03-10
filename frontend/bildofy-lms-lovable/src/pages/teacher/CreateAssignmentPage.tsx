import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, FileText, Upload } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import SearchableSelect from "@/components/form/SearchableSelect";
import { formatDisplayDate } from "@/lib/date";

type Mode = "LMS" | "PDF";
type TeacherSubject = { id: number; name: string; type: string; class_id: number | null };

const CreateAssignmentPage = () => {
  const [title, setTitle] = useState("");
  const [subjectId, setSubjectId] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [mode, setMode] = useState<Mode>("LMS");
  const [content, setContent] = useState("");
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
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

  const handleCreate = async () => {
    if (!title || !selectedSubject || !dueDate) {
      setStatus("Please fill title, subject, and due date.");
      return;
    }

    const token = localStorage.getItem("access_token");
    setSaving(true);
    setStatus(null);

    try {
      if (mode === "PDF") {
        if (!pdfFile) throw new Error("Please upload a PDF question paper.");

        const formData = new FormData();
        formData.append("title", title);
        formData.append("subject", selectedSubject.name);
        formData.append("due_date", `${dueDate}T00:00:00`);
        formData.append("file", pdfFile);

        const res = await fetch("http://localhost:8000/api/teacher/assignments/upload", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });
        if (!res.ok) throw new Error("Failed to create PDF assignment");
      } else {
        const res = await fetch("http://localhost:8000/api/teacher/assignments/create", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            title,
            subject: selectedSubject.name,
            due_date: `${dueDate}T00:00:00`,
            mode: "LMS",
            content,
          }),
        });
        if (!res.ok) throw new Error("Failed to create LMS assignment");
      }

      setStatus("Assignment created successfully.");
      setTitle("");
      setDueDate("");
      setContent("");
      setPdfFile(null);
    } catch (err: any) {
      setStatus(err.message || "Failed to create assignment");
    } finally {
      setSaving(false);
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
          <h1 className="text-xl font-bold">Create Assignment</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-2xl space-y-4">
        <Input
          placeholder="Assignment Title"
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
        <div className="space-y-1">
          <Input type="date" value={dueDate} onChange={(e) => setDueDate(e.target.value)} />
          {dueDate && (
            <p className="text-xs text-muted-foreground">Due date: {formatDisplayDate(dueDate)}</p>
          )}
        </div>

        <Select value={mode} onValueChange={(v) => setMode(v as Mode)}>
          <SelectTrigger>
            <SelectValue placeholder="Select Mode" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="LMS">Create in LMS</SelectItem>
            <SelectItem value="PDF">Upload Question Paper PDF</SelectItem>
          </SelectContent>
        </Select>

        {mode === "LMS" ? (
          <Textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write assignment questions/instructions here..."
            className="min-h-[180px]"
          />
        ) : (
          <div className="space-y-2">
            <Input
              type="file"
              accept=".pdf"
              onChange={(e) => setPdfFile(e.target.files?.[0] || null)}
            />
            <p className="text-xs text-muted-foreground">
              Upload only PDF question papers.
            </p>
          </div>
        )}

        {status && (
          <div className="text-sm p-3 rounded-md border bg-secondary/30">{status}</div>
        )}

        <Button className="w-full gap-2" onClick={handleCreate} disabled={saving}>
          {mode === "PDF" ? <Upload className="w-4 h-4" /> : <FileText className="w-4 h-4" />}
          {saving ? "Creating..." : "Create Assignment"}
        </Button>
      </main>
    </div>
  );
};

export default CreateAssignmentPage;
