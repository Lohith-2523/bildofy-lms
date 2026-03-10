import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import SearchableSelect from "@/components/form/SearchableSelect";

type Lookup = { id: number; label: string };

const AdminSystemConfigPage = () => {
  const [status, setStatus] = useState<string | null>(null);
  const [users, setUsers] = useState<Lookup[]>([]);
  const [classes, setClasses] = useState<Lookup[]>([]);
  const [subjects, setSubjects] = useState<Lookup[]>([]);
  const [teachers, setTeachers] = useState<Lookup[]>([]);

  const [selectedUser, setSelectedUser] = useState("");
  const [selectedClass, setSelectedClass] = useState("");
  const [selectedSubject, setSelectedSubject] = useState("");
  const [selectedTeacher, setSelectedTeacher] = useState("");

  useEffect(() => {
    const headers = { Authorization: `Bearer ${localStorage.getItem("access_token")}` };
    Promise.all([
      fetch("http://localhost:8000/api/admin/dashboard/lookup/users", { headers }),
      fetch("http://localhost:8000/api/admin/dashboard/lookup/classes", { headers }),
      fetch("http://localhost:8000/api/admin/dashboard/lookup/subjects", { headers }),
      fetch("http://localhost:8000/api/admin/dashboard/lookup/teachers", { headers }),
    ])
      .then(async ([u, c, s, t]) => {
        if (!u.ok || !c.ok || !s.ok || !t.ok) throw new Error("Failed to load lookup data");
        return [await u.json(), await c.json(), await s.json(), await t.json()];
      })
      .then(([u, c, s, t]) => {
        setUsers(u);
        setClasses(c);
        setSubjects(s);
        setTeachers(t);
      })
      .catch((err) => setStatus(err.message));
  }, []);

  const reassignClass = async () => {
    const res = await fetch("http://localhost:8000/api/admin/dashboard/system/reassign-class", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify({
        user_id: Number(selectedUser),
        class_id: selectedClass ? Number(selectedClass) : null,
      }),
    });
    if (!res.ok) throw new Error("Failed to reassign class");
    setStatus("User class reassigned.");
  };

  const assignTeacher = async () => {
    const res = await fetch("http://localhost:8000/api/admin/dashboard/system/assign-teacher-subject", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify({
        subject_id: Number(selectedSubject),
        teacher_id: Number(selectedTeacher),
      }),
    });
    if (!res.ok) throw new Error("Failed to assign teacher");
    setStatus("Teacher assigned to subject.");
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
          <h1 className="text-xl font-bold">System Configuration</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-3xl space-y-5">
        {status && <div className="p-3 rounded border bg-secondary/40 text-sm">{status}</div>}

        <section className="border rounded-xl p-4 bg-card space-y-3">
          <h2 className="font-semibold">Change User Class</h2>
          <SearchableSelect
            value={selectedUser}
            options={users.map((x) => ({ value: String(x.id), label: x.label }))}
            placeholder="Search user..."
            onChange={setSelectedUser}
          />
          <SearchableSelect
            value={selectedClass}
            options={classes.map((x) => ({ value: String(x.id), label: x.label }))}
            placeholder="Search class..."
            onChange={setSelectedClass}
          />
          <Button onClick={() => reassignClass().catch((err) => setStatus(err.message))}>
            Update User Class
          </Button>
        </section>

        <section className="border rounded-xl p-4 bg-card space-y-3">
          <h2 className="font-semibold">Assign/Change Teacher for Subject</h2>
          <SearchableSelect
            value={selectedSubject}
            options={subjects.map((x) => ({ value: String(x.id), label: x.label }))}
            placeholder="Search subject..."
            onChange={setSelectedSubject}
          />
          <SearchableSelect
            value={selectedTeacher}
            options={teachers.map((x) => ({ value: String(x.id), label: x.label }))}
            placeholder="Search teacher..."
            onChange={setSelectedTeacher}
          />
          <Button onClick={() => assignTeacher().catch((err) => setStatus(err.message))}>
            Update Subject Teacher
          </Button>
        </section>
      </main>
    </div>
  );
};

export default AdminSystemConfigPage;
