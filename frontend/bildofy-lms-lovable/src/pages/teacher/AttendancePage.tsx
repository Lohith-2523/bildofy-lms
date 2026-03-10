import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import SearchableSelect from "@/components/form/SearchableSelect";
import { toast } from "@/components/ui/use-toast";
import { formatDisplayDate } from "@/lib/date";

type TeacherSubject = {
  id: number;
  name: string;
  type: string;
  class_id: number | null;
};

type RosterRow = {
  student_id: number;
  name: string;
  present: boolean | null;
  remark: string | null;
};

const today = new Date().toISOString().slice(0, 10);

const AttendancePage = () => {
  const [status, setStatus] = useState<string | null>(null);
  const [subjects, setSubjects] = useState<TeacherSubject[]>([]);
  const [subjectId, setSubjectId] = useState("");
  const [attendanceDate, setAttendanceDate] = useState(today);
  const [rows, setRows] = useState<RosterRow[]>([]);
  const [loadingRoster, setLoadingRoster] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/api/teacher/subjects/", {
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
    })
      .then(async (r) => {
        if (!r.ok) throw new Error("Failed to load teacher subjects");
        return r.json();
      })
      .then((data) => {
        const list = Array.isArray(data) ? data : [];
        setSubjects(list);
        if (list.length === 1) setSubjectId(String(list[0].id));
      })
      .catch((err) => setStatus(err.message));
  }, []);

  const loadRoster = async () => {
    if (!subjectId || !attendanceDate) return;
    setLoadingRoster(true);
    setStatus(null);
    try {
      const res = await fetch(
        `http://localhost:8000/api/teacher/attendance/roster?subject_id=${subjectId}&attendance_date=${attendanceDate}`,
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        }
      );
      if (!res.ok) throw new Error("Failed to load attendance roster");
      const data = await res.json();
      const students = Array.isArray(data.students) ? data.students : [];
      setRows(
        students.map((s: RosterRow) => ({
          ...s,
          present: s.present === null ? true : s.present,
          remark: s.remark ?? "",
        }))
      );
    } catch (err: any) {
      setStatus(err.message || "Failed to load roster");
    } finally {
      setLoadingRoster(false);
    }
  };

  useEffect(() => {
    if (subjectId) loadRoster().catch(() => null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [subjectId, attendanceDate]);

  const saveAttendance = async () => {
    if (!subjectId || !attendanceDate) return;
    setSaving(true);
    setStatus(null);
    try {
      const res = await fetch("http://localhost:8000/api/teacher/attendance/mark", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({
          subject_id: Number(subjectId),
          attendance_date: attendanceDate,
          records: rows.map((r) => ({
            student_id: r.student_id,
            present: Boolean(r.present),
            remark: r.remark || null,
          })),
        }),
      });
      if (!res.ok) throw new Error("Failed to save attendance");
      const formattedDate = formatDisplayDate(attendanceDate);
      setStatus(`Attendance saved for ${formattedDate}.`);
      toast({
        title: "Attendance saved",
        description: `Attendance for ${formattedDate} has been recorded.`,
      });
      await loadRoster();
    } catch (err: any) {
      setStatus(err.message || "Failed to save attendance");
    } finally {
      setSaving(false);
    }
  };

  const subjectOptions = useMemo(
    () => subjects.map((s) => ({ value: String(s.id), label: `${s.name} (#${s.id})` })),
    [subjects]
  );

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/teacher">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-xl font-bold">Take Attendance</h1>
            <p className="text-sm text-muted-foreground">Mark attendance for today</p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 space-y-4">
        {status && <div className="p-3 rounded border bg-secondary/40 text-sm">{status}</div>}

        <div className="grid md:grid-cols-2 gap-3">
          <SearchableSelect
            value={subjectId}
            options={subjectOptions}
            placeholder="Select subject"
            onChange={setSubjectId}
            disabled={subjects.length === 1}
          />
          <div className="space-y-1">
            <Input type="date" value={attendanceDate} onChange={(e) => setAttendanceDate(e.target.value)} />
            <p className="text-xs text-muted-foreground">
              Selected date: {formatDisplayDate(attendanceDate)}
            </p>
          </div>
        </div>

        {loadingRoster ? (
          <div className="text-sm text-muted-foreground">Loading roster...</div>
        ) : (
          <div className="border rounded-lg bg-card overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-muted/40">
                  <th className="text-left px-3 py-2">Student</th>
                  <th className="text-left px-3 py-2">Present</th>
                  <th className="text-left px-3 py-2">Remark</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.student_id} className="border-b last:border-0">
                    <td className="px-3 py-2">{row.name}</td>
                    <td className="px-3 py-2">
                      <input
                        type="checkbox"
                        checked={Boolean(row.present)}
                        onChange={(e) =>
                          setRows((prev) =>
                            prev.map((r) =>
                              r.student_id === row.student_id
                                ? { ...r, present: e.target.checked }
                                : r
                            )
                          )
                        }
                      />
                    </td>
                    <td className="px-3 py-2">
                      <Input
                        value={row.remark || ""}
                        onChange={(e) =>
                          setRows((prev) =>
                            prev.map((r) =>
                              r.student_id === row.student_id
                                ? { ...r, remark: e.target.value }
                                : r
                            )
                          )
                        }
                        placeholder="Optional"
                      />
                    </td>
                  </tr>
                ))}
                {rows.length === 0 && (
                  <tr>
                    <td className="px-3 py-4 text-muted-foreground" colSpan={3}>
                      No students found for this subject.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}

        <Button onClick={saveAttendance} disabled={!subjectId || saving || rows.length === 0}>
          {saving ? "Saving..." : "Save Attendance"}
        </Button>
      </main>
    </div>
  );
};

export default AttendancePage;
