import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import SearchableSelect from "@/components/form/SearchableSelect";

type SubjectLookup = { id: number; label: string; name: string };

const AdminInfrastructurePage = () => {
  const [status, setStatus] = useState<string | null>(null);
  const [boards, setBoards] = useState("CBSE,ICSE,State");
  const [grades, setGrades] = useState("9,10,11,12");
  const [subjectMapping, setSubjectMapping] = useState("{}");
  const [chapterMetadata, setChapterMetadata] = useState("{}");

  const [schoolId, setSchoolId] = useState("school-1");
  const [board, setBoard] = useState("CBSE");
  const [grade, setGrade] = useState("9");
  const [subjectId, setSubjectId] = useState("");
  const [chapter, setChapter] = useState("");
  const [licensedFile, setLicensedFile] = useState<File | null>(null);
  const [subjects, setSubjects] = useState<SubjectLookup[]>([]);

  useEffect(() => {
    const headers = { Authorization: `Bearer ${localStorage.getItem("access_token")}` };
    fetch("http://localhost:8000/api/admin/dashboard/lookup/subjects", { headers })
      .then((r) => r.json())
      .then(setSubjects)
      .catch(() => null);

    fetch("http://localhost:8000/api/admin/dashboard/infrastructure", { headers })
      .then(async (r) => {
        if (!r.ok) return;
        const data = await r.json();
        setBoards((data.boards || []).join(","));
        setGrades((data.grades || []).join(","));
        setSubjectMapping(JSON.stringify(data.subject_mapping || {}, null, 2));
        setChapterMetadata(JSON.stringify(data.chapter_metadata || {}, null, 2));
      })
      .catch(() => null);
  }, []);

  const saveInfra = async () => {
    const res = await fetch("http://localhost:8000/api/admin/dashboard/infrastructure", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify({
        boards: boards.split(",").map((x) => x.trim()).filter(Boolean),
        grades: grades.split(",").map((x) => Number(x.trim())).filter((n) => !Number.isNaN(n)),
        subject_mapping: JSON.parse(subjectMapping || "{}"),
        chapter_metadata: JSON.parse(chapterMetadata || "{}"),
      }),
    });
    if (!res.ok) throw new Error("Failed to save infrastructure");
    setStatus("Infrastructure saved.");
  };

  const uploadLicensed = async () => {
    if (!licensedFile) throw new Error("Choose licensed content PDF");
    const selectedSubject = subjects.find((s) => String(s.id) === subjectId);
    const form = new FormData();
    form.append("school_id", schoolId);
    form.append("board", board);
    form.append("grade", grade);
    form.append("subject", selectedSubject?.name || "");
    form.append("chapter", chapter);
    form.append("file", licensedFile);

    const res = await fetch("http://localhost:8000/api/admin/dashboard/licensed-content", {
      method: "POST",
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
      body: form,
    });
    if (!res.ok) throw new Error("Licensed content upload failed");
    setStatus("Licensed content uploaded and school-locked.");
  };

  const subjectOptions = subjects.map((s) => ({ value: String(s.id), label: s.label }));

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/admin">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <h1 className="text-xl font-bold">Academic Infrastructure</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-4xl space-y-4">
        {status && <div className="p-3 rounded border bg-secondary/40 text-sm">{status}</div>}

        <Input placeholder="Boards (comma separated)" value={boards} onChange={(e) => setBoards(e.target.value)} />
        <Input placeholder="Grades (comma separated)" value={grades} onChange={(e) => setGrades(e.target.value)} />
        <Textarea value={subjectMapping} onChange={(e) => setSubjectMapping(e.target.value)} className="min-h-[140px]" />
        <Textarea value={chapterMetadata} onChange={(e) => setChapterMetadata(e.target.value)} className="min-h-[140px]" />
        <Button onClick={() => saveInfra().catch((err) => setStatus(err.message))}>Save Infrastructure</Button>

        <div className="border-t pt-4 space-y-3">
          <h2 className="font-semibold">Licensed Content Upload (School Locked)</h2>
          <div className="grid md:grid-cols-3 gap-3">
            <Input placeholder="School ID" value={schoolId} onChange={(e) => setSchoolId(e.target.value)} />
            <Input placeholder="Board" value={board} onChange={(e) => setBoard(e.target.value)} />
            <Input placeholder="Grade" value={grade} onChange={(e) => setGrade(e.target.value)} />
            <SearchableSelect
              value={subjectId}
              options={subjectOptions}
              placeholder="Search subject..."
              onChange={setSubjectId}
            />
            <Input placeholder="Chapter" value={chapter} onChange={(e) => setChapter(e.target.value)} />
            <Input type="file" accept=".pdf" onChange={(e) => setLicensedFile(e.target.files?.[0] || null)} />
          </div>
          <Button onClick={() => uploadLicensed().catch((err) => setStatus(err.message))}>
            Upload Licensed Content
          </Button>
        </div>
      </main>
    </div>
  );
};

export default AdminInfrastructurePage;
