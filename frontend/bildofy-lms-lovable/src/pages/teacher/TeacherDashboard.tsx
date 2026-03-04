import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { StatCard } from '@/components/cards/StatCard';
import {
  Users,
  ClipboardCheck,
  TrendingUp,
  Plus,
  BarChart3,
  BookOpen,
  Settings,
  LogOut,
  Sparkles,
} from 'lucide-react';

const TeacherDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [analytics, setAnalytics] = useState<any | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');

    fetch('http://localhost:8000/analytics/overview', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then(setAnalytics)
      .catch(console.error);
  }, []);

  const classData = analytics?.scope === 'teacher' ? analytics.class : null;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
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

      <main className="container mx-auto px-4 py-6">
        <div className="mb-8">
          <h1 className="text-2xl md:text-3xl font-display font-bold">
            Teacher Dashboard
          </h1>
          <p className="text-muted-foreground mt-1">
            Manage your classes and track performance.
          </p>
        </div>

        {/* Quick Actions */}
        <section className="mb-8">
          <h2 className="text-lg font-display font-semibold mb-4">
            Quick Actions
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Button
              variant="action"
              className="h-auto py-4 flex-col gap-2"
              onClick={() => navigate('/teacher/create-assignment')}
            >
              <Plus className="w-6 h-6 text-primary" />
              <span>Create Assignment</span>
            </Button>

            <Button
              variant="action"
              className="h-auto py-4 flex-col gap-2"
              onClick={() => navigate('/teacher/create-test')}
            >
              <ClipboardCheck className="w-6 h-6 text-primary" />
              <span>Create Test</span>
            </Button>

            <Button
              variant="action"
              className="h-auto py-4 flex-col gap-2"
              onClick={() => navigate('/teacher/ai-content')}
            >
              <Sparkles className="w-6 h-6 text-primary" />
              <span>AI Content</span>
            </Button>

            <Button
              variant="action"
              className="h-auto py-4 flex-col gap-2"
              onClick={() => navigate('/teacher/analytics')}
            >
              <BarChart3 className="w-6 h-6 text-primary" />
              <span>View Analytics</span>
            </Button>
          </div>
        </section>

        {/* Overview */}
        {classData && (
          <section className="mb-8">
            <h2 className="text-lg font-display font-semibold mb-4">
              Overview
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatCard
                title="Total Students"
                value={classData.students}
                icon={Users}
              />
              <StatCard
                title="Average Score"
                value={classData.average_score}
                icon={ClipboardCheck}
              />
              <StatCard
                title="Class Average"
                value={`${classData.average_percentage}%`}
                icon={TrendingUp}
              />
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default TeacherDashboard;
