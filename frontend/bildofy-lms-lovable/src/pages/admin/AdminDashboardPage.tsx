import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";

type Overview = {
  teachers: number;
  students: number;
  classes: number;
  subjects: number;
};

const AdminDashboardPage = () => {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/admin/dashboard/overview", {
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
    })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load admin overview");
        return r.json();
      })
      .then(setOverview)
      .catch((err) => setStatus(err.message));
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-xl font-bold">Admin Dashboard</h1>
            <p className="text-sm text-muted-foreground">Control center for school operations</p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 grid gap-6">
        {status && <div className="p-3 rounded border bg-secondary/40 text-sm">{status}</div>}

        <section className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <Stat label="Teachers" value={overview?.teachers ?? 0} />
          <Stat label="Students" value={overview?.students ?? 0} />
          <Stat label="Classes" value={overview?.classes ?? 0} />
          <Stat label="Subjects" value={overview?.subjects ?? 0} />
        </section>

        <section className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          <NavCard
            title="Teacher Management"
            description="Create teacher users and assign class/subjects."
            to="/admin/teachers"
          />
          <NavCard
            title="Class & Subjects"
            description="Create classes and define core/extracurricular subjects."
            to="/admin/classes-subjects"
          />
          <NavCard
            title="Bulk Student Import"
            description="Import student data using Excel/CSV/PDF."
            to="/admin/bulk-import"
          />
          <NavCard
            title="Infrastructure"
            description="Boards, grades, mapping, metadata, licensed content."
            to="/admin/infrastructure"
          />
          <NavCard
            title="System Configuration"
            description="Reassign users/classes and teacher-subject relations."
            to="/admin/system-config"
          />
        </section>
      </main>
    </div>
  );
};

const Stat = ({ label, value }: { label: string; value: number }) => (
  <div className="border rounded-lg p-3 bg-card">
    <p className="text-xs text-muted-foreground">{label}</p>
    <p className="text-2xl font-bold">{value}</p>
  </div>
);

const NavCard = ({
  title,
  description,
  to,
}: {
  title: string;
  description: string;
  to: string;
}) => (
  <Link to={to} className="border rounded-xl p-4 bg-card hover:shadow-md transition">
    <h2 className="font-semibold">{title}</h2>
    <p className="text-sm text-muted-foreground mt-1">{description}</p>
    <p className="text-sm text-primary mt-3">Open</p>
  </Link>
);

export default AdminDashboardPage;
