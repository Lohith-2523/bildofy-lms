import { useEffect, useState } from "react";
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { SubjectPerformanceChart } from "@/components/analytics/AnalyticsCharts";
import { StudentTable } from "@/components/analytics/StudentTable";
import { StatCard } from "@/components/cards/StatCard";
import {
  Users,
  ClipboardCheck,
  TrendingUp,
  Settings,
  LogOut,
  CalendarCheck,
} from 'lucide-react';

const AnalyticsPage = () => {
  const [overview, setOverview] = useState<any>(null);
  const [students, setStudents] = useState<any[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    fetch("http://localhost:8000/analytics/overview", {
      headers: { Authorization: `Bearer ${token}` },
    }).then(r => r.json()).then(setOverview);

    fetch("http://localhost:8000/analytics/students", {
      headers: { Authorization: `Bearer ${token}` },
    }).then(r => r.json()).then(setStudents);
  }, []);

  if (!overview) return null;

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link to="/" className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
                  <span className="text-primary-foreground font-bold text-sm">L</span>
                </div>
                <span className="font-display font-bold text-lg text-foreground">
                  LearnSphere
                </span>
              </Link>
              <span className="text-sm text-muted-foreground px-2 py-0.5 bg-secondary rounded-full">
                Teacher
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon">
                <Settings className="w-5 h-5" />
              </Button>
              <Link to="/">
                <Button variant="ghost" size="icon">
                  <LogOut className="w-5 h-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>
      <div className="container mx-auto py-6 space-y-8">
        <h1 className="text-2xl font-bold">Class Analytics</h1>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard title="Students" value={overview.class?.students ?? 0} icon={Users} />
          <StatCard title="Average Score" value={overview.class?.average_score ?? 0} icon={ClipboardCheck} />
          <StatCard title="Class Average" value={`${overview.class?.average_percentage ?? 0}%`} icon={TrendingUp} />
          <StatCard
            title="Attendance"
            value={`${overview.class?.attendance_percentage ?? 0}%`}
            icon={CalendarCheck}
          />
        </div>

        <SubjectPerformanceChart data={overview.subjects} />

        <div>
          <h2 className="text-lg font-semibold mb-2">Students</h2>
          <StudentTable students={students} />
        </div>

        <Button
          onClick={() =>
            window.open("http://localhost:8000/analytics/export/students.csv")
          }
        >
          Export CSV
        </Button>
      </div>
    </div>

  );
};

export default AnalyticsPage;
