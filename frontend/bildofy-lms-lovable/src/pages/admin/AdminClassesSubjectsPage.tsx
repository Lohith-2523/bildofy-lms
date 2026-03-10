import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, Plus, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import SearchableSelect from "@/components/form/SearchableSelect";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

type Teacher = { id: number; label: string };
type SubjectRow = { id: string; name: string; type: "core" | "extracurricular"; teacherId: string };

const newRow = (): SubjectRow => ({
  id: crypto.randomUUID(),
  name: "",
  type: "core",
  teacherId: "",
});

const AdminClassesSubjectsPage = () => {
  const [status, setStatus] = useState<string | null>(null);
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [grade, setGrade] = useState("");
  const [section, setSection] = useState("");
  const [codePrefix, setCodePrefix] = useState("");
  const [rows, setRows] = useState<SubjectRow[]>([newRow()]);

  useEffect(() => {
    fetch("http://localhost:8000/api/admin/dashboard/lookup/teachers", {
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
    })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load teachers");
        return r.json();
      })
      .then(setTeachers)
      .catch((err) => setStatus(err.message));
  }, []);

  const teacherOptions = teachers.map((t) => ({ value: String(t.id), label: t.label }));

  const save = async () => {
    const subjects = rows
      .filter((r) => r.name && r.teacherId)
      .map((r) => ({ name: r.name, type: r.type, teacher_id: Number(r.teacherId) }));

    const res = await fetch("http://localhost:8000/api/admin/dashboard/classes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify({
        grade: Number(grade),
        section,
        code_prefix: codePrefix,
        subjects,
      }),
    });
    if (!res.ok) throw new Error("Failed to create class");
    setStatus("Class and subjects created.");
    setRows([newRow()]);
    setGrade("");
    setSection("");
    setCodePrefix("");
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/admin">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <h1 className="text-xl font-bold">Class & Subjects Setup</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-4xl space-y-4">
        {status && <div className="p-3 rounded border bg-secondary/40 text-sm">{status}</div>}
        <div className="grid md:grid-cols-3 gap-3">
          <Input placeholder="Grade (9-12)" value={grade} onChange={(e) => setGrade(e.target.value)} />
          <Input placeholder="Section (A/B/C)" value={section} onChange={(e) => setSection(e.target.value)} />
          <Input placeholder="Code Prefix (e.g. 0901)" value={codePrefix} onChange={(e) => setCodePrefix(e.target.value)} />
        </div>

        {rows.map((row, i) => (
          <div key={row.id} className="border rounded-lg p-3 bg-card grid md:grid-cols-4 gap-3 items-end">
            <Input
              placeholder={`Subject ${i + 1} name`}
              value={row.name}
              onChange={(e) =>
                setRows((prev) => prev.map((x) => (x.id === row.id ? { ...x, name: e.target.value } : x)))
              }
            />
            <Select
              value={row.type}
              onValueChange={(v) =>
                setRows((prev) =>
                  prev.map((x) => (x.id === row.id ? { ...x, type: v as "core" | "extracurricular" } : x))
                )
              }
            >
              <SelectTrigger>
                <SelectValue placeholder="Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="core">Core</SelectItem>
                <SelectItem value="extracurricular">Extra-curricular</SelectItem>
              </SelectContent>
            </Select>
            <SearchableSelect
              value={row.teacherId}
              options={teacherOptions}
              placeholder="Search teacher..."
              onChange={(val) =>
                setRows((prev) => prev.map((x) => (x.id === row.id ? { ...x, teacherId: val } : x)))
              }
            />
            <Button
              variant="destructive"
              onClick={() => setRows((prev) => prev.filter((x) => x.id !== row.id))}
              disabled={rows.length === 1}
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        ))}

        <Button variant="outline" onClick={() => setRows((prev) => [...prev, newRow()])}>
          <Plus className="w-4 h-4 mr-1" />
          Add Subject Row
        </Button>

        <Button onClick={() => save().catch((err) => setStatus(err.message))}>Create Class & Subjects</Button>
      </main>
    </div>
  );
};

export default AdminClassesSubjectsPage;
