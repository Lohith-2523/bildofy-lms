import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  ArrowLeft,
  BookOpen,
  Calendar,
  CheckCircle,
  Upload,
  Download,
} from "lucide-react";
import { formatDisplayDate } from "@/lib/date";

type ViewState = "list" | "detail" | "submit" | "complete";

type AssignmentItem = {
  id: number;
  title: string;
  subject: string;
  due_date: string;
  mode: "LMS" | "PDF";
};

type AssignmentDetail = AssignmentItem & {
  content: string;
};

const AssignmentsPage: React.FC = () => {
  const [view, setView] = useState<ViewState>("list");
  const [assignments, setAssignments] = useState<AssignmentItem[]>([]);
  const [selectedAssignment, setSelectedAssignment] = useState<AssignmentDetail | null>(
    null
  );
  const [submissionFile, setSubmissionFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchAssignments = async () => {
    const token = localStorage.getItem("access_token");
    const res = await fetch("http://localhost:8000/api/student/assignments/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch assignments");
    const data = await res.json();
    setAssignments(Array.isArray(data) ? data : []);
  };

  useEffect(() => {
    fetchAssignments().catch((err) => setStatus(err.message));
  }, []);

  const openAssignment = async (id: number) => {
    const token = localStorage.getItem("access_token");
    const res = await fetch(`http://localhost:8000/api/student/assignments/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
      setStatus("Failed to open assignment");
      return;
    }
    const data = await res.json();
    setSelectedAssignment(data);
    setView("detail");
  };

  const downloadPaper = async (assignmentId: number) => {
    const token = localStorage.getItem("access_token");
    const res = await fetch(
      `http://localhost:8000/api/student/assignments/${assignmentId}/paper/pdf`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    if (!res.ok) {
      setStatus("Failed to download question paper");
      return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `assignment_${assignmentId}_paper.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  const submitAssignment = async () => {
    if (!selectedAssignment || !submissionFile) {
      setStatus("Please upload a written PDF before submitting.");
      return;
    }

    setLoading(true);
    setStatus(null);
    try {
      const token = localStorage.getItem("access_token");
      const form = new FormData();
      form.append("file", submissionFile);

      const res = await fetch(
        `http://localhost:8000/api/student/assignments/${selectedAssignment.id}/submit`,
        {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
          body: form,
        }
      );
      if (!res.ok) throw new Error("Submission failed");

      setView("complete");
      setSubmissionFile(null);
    } catch (err: any) {
      setStatus(err.message || "Submission failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Link to="/student">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <div>
              <h1 className="text-xl font-bold">Assignments</h1>
              <p className="text-sm text-muted-foreground">
                Complete and upload your written PDF solutions
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {status && (
          <div className="mb-4 p-3 rounded-md border bg-secondary/30 text-sm">{status}</div>
        )}

        {view === "list" && (
          <div className="grid gap-4">
            {assignments.map((assignment) => (
              <div
                key={assignment.id}
                className="p-5 rounded-xl bg-card border border-border shadow-sm"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-primary/10">
                      <BookOpen className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-semibold">{assignment.title}</h3>
                      <p className="text-sm text-muted-foreground">{assignment.subject}</p>
                      <div className="flex items-center gap-2 mt-2 text-sm text-muted-foreground">
                        <Calendar className="w-4 h-4" />
                        Due {formatDisplayDate(assignment.due_date)}
                      </div>
                      <p className="text-xs mt-1 text-muted-foreground">
                        Mode: {assignment.mode === "LMS" ? "Created in LMS" : "Teacher PDF paper"}
                      </p>
                    </div>
                  </div>

                  <div className="flex flex-col gap-2">
                    <Button size="sm" variant="outline" onClick={() => downloadPaper(assignment.id)}>
                      <Download className="w-4 h-4 mr-1" />
                      Export PDF
                    </Button>
                    <Button size="sm" onClick={() => openAssignment(assignment.id)}>
                      <Upload className="w-4 h-4 mr-1" />
                      Submit
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {view === "detail" && selectedAssignment && (
          <div className="max-w-3xl mx-auto space-y-4">
            <h2 className="text-2xl font-bold">{selectedAssignment.title}</h2>
            <p className="text-muted-foreground">Subject: {selectedAssignment.subject}</p>
            <p className="text-sm text-muted-foreground">
              Due {formatDisplayDate(selectedAssignment.due_date)}
            </p>

            {selectedAssignment.mode === "LMS" ? (
              <div className="border rounded-lg p-4 whitespace-pre-wrap bg-card">
                {selectedAssignment.content || "No assignment content provided."}
              </div>
            ) : (
              <div className="border rounded-lg p-4 bg-card text-sm text-muted-foreground">
                Teacher uploaded a PDF question paper. Use "Export PDF" to download.
              </div>
            )}

            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setView("list")}>
                Back
              </Button>
              <Button
                variant="outline"
                onClick={() => selectedAssignment && downloadPaper(selectedAssignment.id)}
              >
                <Download className="w-4 h-4 mr-1" />
                Export Question Paper PDF
              </Button>
              <Button onClick={() => setView("submit")}>Proceed to Submit</Button>
            </div>
          </div>
        )}

        {view === "submit" && selectedAssignment && (
          <div className="max-w-xl mx-auto space-y-4">
            <h2 className="text-xl font-semibold">Upload Written PDF</h2>
            <InputFile onFileChange={setSubmissionFile} />
            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setView("detail")}>
                Back
              </Button>
              <Button onClick={submitAssignment} disabled={loading}>
                {loading ? "Submitting..." : "Submit Assignment"}
              </Button>
            </div>
          </div>
        )}

        {view === "complete" && selectedAssignment && (
          <div className="text-center space-y-4 py-12">
            <CheckCircle className="w-12 h-12 mx-auto text-success" />
            <h2 className="text-2xl font-bold">Assignment Submitted</h2>
            <p className="text-muted-foreground">{selectedAssignment.title}</p>
            <Button
              onClick={() => {
                setView("list");
                setSelectedAssignment(null);
              }}
            >
              Back to Assignments
            </Button>
          </div>
        )}
      </main>
    </div>
  );
};

const InputFile = ({ onFileChange }: { onFileChange: (file: File | null) => void }) => (
  <input type="file" accept=".pdf" onChange={(e) => onFileChange(e.target.files?.[0] || null)} />
);

export default AssignmentsPage;
