import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import SearchableSelect from "@/components/form/SearchableSelect";

type LookupItem = { id: number; label: string };

const AdminTeachersPage = () => {
  const [status, setStatus] = useState<string | null>(null);
  const [classes, setClasses] = useState<LookupItem[]>([]);
  const [subjects, setSubjects] = useState<LookupItem[]>([]);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [classId, setClassId] = useState<string>("");
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [subjectToAdd, setSubjectToAdd] = useState<string>("");

  useEffect(() => {
    const headers = { Authorization: `Bearer ${localStorage.getItem("access_token")}` };
    Promise.all([
      fetch("http://localhost:8000/api/admin/dashboard/lookup/classes", { headers }),
      fetch("http://localhost:8000/api/admin/dashboard/lookup/subjects", { headers }),
    ])
      .then(async ([c, s]) => {
        if (!c.ok || !s.ok) throw new Error("Failed to load lookup data");
        return [await c.json(), await s.json()];
      })
      .then(([cData, sData]) => {
        setClasses(cData);
        setSubjects(sData);
      })
      .catch((err) => setStatus(err.message));
  }, []);

  const addSubject = () => {
    if (!subjectToAdd) return;
    if (!selectedSubjects.includes(subjectToAdd)) {
      setSelectedSubjects((prev) => [...prev, subjectToAdd]);
    }
    setSubjectToAdd("");
  };

  const createTeacher = async () => {
    const res = await fetch("http://localhost:8000/api/admin/dashboard/teachers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify({
        name,
        email,
        password,
        class_id: classId ? Number(classId) : null,
        subject_ids: selectedSubjects.map(Number),
      }),
    });
    if (!res.ok) throw new Error("Failed to create teacher");
    setStatus("Teacher created successfully.");
    setName("");
    setEmail("");
    setPassword("");
    setClassId("");
    setSelectedSubjects([]);
  };

  const classOptions = classes.map((c) => ({ value: String(c.id), label: c.label }));
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
          <h1 className="text-xl font-bold">Teacher Management</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-3xl space-y-4">
        {status && <div className="p-3 rounded border bg-secondary/40 text-sm">{status}</div>}

        <Input placeholder="Teacher Name" value={name} onChange={(e) => setName(e.target.value)} />
        <Input placeholder="Teacher Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <Input placeholder="Temporary Password" value={password} onChange={(e) => setPassword(e.target.value)} />

        <div>
          <p className="text-sm mb-2">Assign Class (optional)</p>
          <SearchableSelect
            value={classId}
            options={classOptions}
            placeholder="Search class..."
            onChange={setClassId}
          />
        </div>

        <div className="space-y-2">
          <p className="text-sm">Assign Subjects</p>
          <div className="flex gap-2">
            <div className="flex-1">
              <SearchableSelect
                value={subjectToAdd}
                options={subjectOptions}
                placeholder="Search subject..."
                onChange={setSubjectToAdd}
              />
            </div>
            <Button variant="outline" onClick={addSubject}>
              Add
            </Button>
          </div>
          <div className="flex flex-wrap gap-2">
            {selectedSubjects.map((sid) => {
              const found = subjects.find((s) => String(s.id) === sid);
              return (
                <button
                  key={sid}
                  className="text-xs px-2 py-1 rounded bg-secondary"
                  onClick={() => setSelectedSubjects((prev) => prev.filter((x) => x !== sid))}
                >
                  {found?.label || sid} ×
                </button>
              );
            })}
          </div>
        </div>

        <Button onClick={() => createTeacher().catch((err) => setStatus(err.message))}>
          Create Teacher
        </Button>
      </main>
    </div>
  );
};

export default AdminTeachersPage;
