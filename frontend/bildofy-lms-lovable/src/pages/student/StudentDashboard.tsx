import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { StudentHeader } from '@/components/layout/StudentHeader';
import { ActionCard } from '@/components/cards/ActionCard';
import { StatCard } from '@/components/cards/StatCard';
import { AcademicTimeline } from '@/components/timeline/AcademicTimeline';
import { ProgressRing } from '@/components/progress/ProgressRing';
import { XPBadge } from '@/components/gamification/XPBadge';
import {
  FileText,
  ClipboardCheck,
  BookOpen,
  Layers,
  Play,
  MessageCircleQuestion,
  Target,
  TrendingUp,
  Zap,
  Trophy,
  CalendarCheck,
} from 'lucide-react';
import { addDays } from 'date-fns';

// Mock data - in production, this comes from API
const mockStudent = {
  name: 'Arjun Sharma',
  avatar: '',
  grade: 'Class 11',
  board: 'CBSE',
  level: 12,
  currentXP: 2450,
  maxXP: 3000,
  streak: 7,
};

const mockStats = {
  testsCompleted: 24,
  assignmentsSubmitted: 18,
  accuracy: 78,
  xpThisWeek: 850,
};

const mockEvents = [
  {
    id: '1',
    title: 'Physics Chapter 5 Test',
    type: 'test' as const,
    date: addDays(new Date(), 1),
    subject: 'Physics',
    xpReward: 100,
  },
  {
    id: '2',
    title: 'Math Assignment - Calculus',
    type: 'assignment' as const,
    date: addDays(new Date(), 2),
    subject: 'Mathematics',
    xpReward: 50,
  },
  {
    id: '3',
    title: 'Chemistry Mid-term',
    type: 'exam' as const,
    date: addDays(new Date(), 5),
    subject: 'Chemistry',
    xpReward: 200,
  },
  {
    id: '4',
    title: 'Science Fair Registration',
    type: 'event' as const,
    date: addDays(new Date(), 7),
  },
];

const StudentDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [analytics, setAnalytics] = useState<any | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');

    fetch('http://localhost:8000/analytics/overview', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error('Failed to load analytics');
        return res.json();
      })
      .then(setAnalytics)
      .catch(() => null);
  }, []);

  const studentMetrics = analytics?.scope === 'student' ? analytics.data : null;

  return (
    <div className="min-h-screen bg-background">
      <StudentHeader student={mockStudent} onMenuClick={() => setSidebarOpen(!isSidebarOpen)} />

      <main className="container mx-auto px-4 py-6">
        {/* Welcome Section */}
        <div className="mb-8 animate-fade-up">
          <h1 className="text-2xl md:text-3xl font-display font-bold text-foreground">
            Welcome back, {mockStudent.name.split(' ')[0]}! 👋
          </h1>
          <p className="text-muted-foreground mt-1">
            You're on a {mockStudent.streak}-day streak! Keep it going.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Learning Actions */}
            <section className="animate-fade-up" style={{ animationDelay: '0.1s' }}>
              <h2 className="text-lg font-display font-semibold text-foreground mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-xp" />
                Continue Learning
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <ActionCard
                  title="Generate Notes"
                  description="AI-powered notes for any topic"
                  icon={FileText}
                  xpReward={25}
                  onClick={() => navigate('/student/notes')}
                  variant="featured"
                />
                <ActionCard
                  title="Attempt Test"
                  description="Practice with adaptive quizzes"
                  icon={ClipboardCheck}
                  xpReward={100}
                  progress={35}
                  requiresOnline
                  onClick={() => navigate('/student/tests')}
                />
                <ActionCard
                  title="View Assignments"
                  description="3 pending assignments"
                  icon={BookOpen}
                  xpReward={50}
                  onClick={() => navigate('/student/assignments')}
                />
                <ActionCard
                  title="Attendance"
                  description="Track your daily attendance"
                  icon={CalendarCheck}
                  xpReward={0}
                  onClick={() => navigate('/student/attendance')}
                />
                <ActionCard
                  title="Study Flashcards"
                  description="Review and memorize key concepts"
                  icon={Layers}
                  xpReward={15}
                  progress={60}
                  onClick={() => navigate('/student/flashcards')}
                />
                <ActionCard
                 title="Watch Videos"
                 description="Visual explanations for complex topics"
                 icon={Play}
                 xpReward={20}
                 requiresOnline
                onClick={() => navigate('/student/watch-videos')}
                />

                <ActionCard
                  title="Ask AI Doubt"
                  description="Get instant explanations"
                  icon={MessageCircleQuestion}
                  xpReward={10}
                  onClick={() => navigate('/student/doubt-chat')}
                />
              </div>
            </section>

            {/* Progress & Analytics */}
            <section className="animate-fade-up" style={{ animationDelay: '0.2s' }}>
              <h2 className="text-lg font-display font-semibold text-foreground mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-success" />
                Your Progress
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <StatCard
                  title="Tests Completed"
                  value={mockStats.testsCompleted}
                  icon={Target}
                  trend={{ value: 12, isPositive: true }}
                />
                <StatCard
                  title="Assignments"
                  value={mockStats.assignmentsSubmitted}
                  icon={BookOpen}
                  trend={{ value: 5, isPositive: true }}
                />
                <StatCard
                  title="Accuracy"
                  value={`${studentMetrics?.average_percentage ?? mockStats.accuracy}%`}
                  icon={Trophy}
                  trend={{ value: 3, isPositive: true }}
                />
                <StatCard
                  title="Attendance"
                  value={`${studentMetrics?.attendance_percentage ?? 0}%`}
                  icon={CalendarCheck}
                  description="Overall"
                />
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Weekly XP */}
            <div className="p-5 rounded-xl bg-card border border-border shadow-sm animate-fade-up" style={{ animationDelay: '0.15s' }}>
              <h3 className="font-display font-semibold text-foreground mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-xp" />
                Weekly XP
              </h3>
              <div className="flex items-center justify-between">
                <ProgressRing progress={68} size={90} color="xp" />
                <div className="text-right">
                  <p className="text-2xl font-bold text-foreground">{mockStats.xpThisWeek}</p>
                  <p className="text-sm text-muted-foreground">XP this week</p>
                  <XPBadge xp={150} size="sm" className="mt-2" />
                </div>
              </div>
            </div>

            {/* Academic Timeline */}
            <div className="p-5 rounded-xl bg-card border border-border shadow-sm animate-fade-up" style={{ animationDelay: '0.25s' }}>
              <AcademicTimeline
                events={mockEvents}
                onEventClick={(event) => console.log('Event clicked:', event)}
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default StudentDashboard;
