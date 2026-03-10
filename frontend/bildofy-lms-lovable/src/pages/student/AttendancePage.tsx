import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { formatDisplayDate } from "@/lib/date";

type Summary = {
  overall: {
    total: number;
    present: number;
    absent: number;
    percentage: number;
  };
  subjects: Array<{
    subject_id: number;
    subject_name: string;
    total: number;
    present: number;
    absent: number;
    percentage: number;
  }>;
};

type RecordRow = {
  attendance_date: string;
  subject_id: number;
  subject_name: string;
  present: boolean;
  remark?: string | null;
};

const AttendancePage: React.FC = () => {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [records, setRecords] = useState<RecordRow[]>([]);
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    const headers = { Authorization: `Bearer ${localStorage.getItem("access_token")}` };

    fetch("http://localhost:8000/api/student/attendance/summary", { headers })
      .then(async (r) => {
        if (!r.ok) throw new Error("Failed to load summary");
        return r.json();
      })
      .then(setSummary)
      .catch((err) => setStatus(err.message));

    fetch("http://localhost:8000/api/student/attendance/", { headers })
      .then(async (r) => {
        if (!r.ok) throw new Error("Failed to load attendance records");
        return r.json();
      })
      .then((data) => setRecords(Array.isArray(data) ? data : []))
      .catch((err) => setStatus(err.message));
  }, []);

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
            <h1 className="text-xl font-bold">My Attendance</h1>
            <p className="text-sm text-muted-foreground">Track daily attendance</p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 space-y-5">
        {status && <div className="p-3 rounded border bg-secondary/40 text-sm">{status}</div>}

        {summary && (
          <section className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Stat title="Total Classes" value={summary.overall.total} />
            <Stat title="Present" value={summary.overall.present} />
            <Stat title="Absent" value={summary.overall.absent} />
            <Stat title="Attendance %" value={summary.overall.percentage} />
          </section>
        )}

        <section className="border rounded-lg bg-card p-4">
          <h2 className="font-semibold mb-3">By Subject</h2>
          <div className="grid md:grid-cols-2 gap-3">
            {(summary?.subjects || []).map((s) => (
              <div key={s.subject_id} className="border rounded p-3">
                <p className="font-medium">{s.subject_name}</p>
                <p className="text-sm text-muted-foreground">
                  {s.present}/{s.total} present ({s.percentage}%)
                </p>
              </div>
            ))}
            {(summary?.subjects || []).length === 0 && (
              <p className="text-sm text-muted-foreground">No subject attendance yet.</p>
            )}
          </div>
        </section>

        <section className="border rounded-lg bg-card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-muted/40">
                <th className="text-left px-3 py-2">Date</th>
                <th className="text-left px-3 py-2">Subject</th>
                <th className="text-left px-3 py-2">Status</th>
                <th className="text-left px-3 py-2">Remark</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r, idx) => (
                <tr key={`${r.subject_id}-${r.attendance_date}-${idx}`} className="border-b last:border-0">
                  <td className="px-3 py-2">{formatDisplayDate(r.attendance_date)}</td>
                  <td className="px-3 py-2">{r.subject_name}</td>
                  <td className="px-3 py-2">{r.present ? "Present" : "Absent"}</td>
                  <td className="px-3 py-2">{r.remark || "-"}</td>
                </tr>
              ))}
              {records.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-3 py-4 text-muted-foreground">
                    No attendance records yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
};

const Stat = ({ title, value }: { title: string; value: number }) => (
  <div className="border rounded-lg p-3 bg-card">
    <p className="text-xs text-muted-foreground">{title}</p>
    <p className="text-2xl font-bold">{value}</p>
  </div>
);

export default AttendancePage;
