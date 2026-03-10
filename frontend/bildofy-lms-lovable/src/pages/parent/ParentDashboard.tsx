import React from 'react';
import { addDays } from 'date-fns';
import { Link } from 'react-router-dom';
import {
  Clock,
  Trophy,
  Calendar,
  Settings,
  LogOut,
  Target,
  Flame,
  Star,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { StatCard } from '@/components/cards/StatCard';
import { XPBar } from '@/components/gamification/XPBar';
import { formatDisplayDate } from '@/lib/date';

const mockChildData = {
  name: 'Arjun Sharma',
  grade: 'Class 11',
  board: 'CBSE',
  level: 12,
  currentXP: 2450,
  maxXP: 3000,
  streak: 7,
  weeklyStudyTime: '12h 30m',
  testsThisWeek: 4,
  avgScore: 78,
  attendance: 92,
};

const weeklyInsights = [
  { id: '1', insight: 'Arjun spent 3 hours more on Physics this week compared to last week.', type: 'positive' },
  { id: '2', insight: 'Math practice test score improved by 12% from previous attempt.', type: 'positive' },
  { id: '3', insight: 'Chemistry chapter review is pending. Due in 2 days.', type: 'warning' },
];

const ParentDashboard: React.FC = () => {
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
                <span className="font-display font-bold text-lg text-foreground">LearnSphere</span>
              </Link>
              <span className="text-sm text-muted-foreground px-2 py-0.5 bg-secondary rounded-full">
                Parent
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
        <div className="mb-8 animate-fade-up">
          <h1 className="text-2xl md:text-3xl font-display font-bold text-foreground">
            Parent Dashboard
          </h1>
          <p className="text-muted-foreground mt-1">
            Monitor {mockChildData.name}&apos;s learning progress and achievements.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <section className="p-6 rounded-xl bg-card border border-border shadow-sm animate-fade-up" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-16 h-16 rounded-full bg-gradient-primary flex items-center justify-center text-2xl font-bold text-primary-foreground">
                  {mockChildData.name.charAt(0)}
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-display font-bold text-foreground">{mockChildData.name}</h2>
                  <p className="text-muted-foreground">{mockChildData.grade} / {mockChildData.board}</p>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-1 text-streak font-bold">
                    <Flame className="w-5 h-5" />
                    <span>{mockChildData.streak} day streak</span>
                  </div>
                </div>
              </div>
              <XPBar
                currentXP={mockChildData.currentXP}
                maxXP={mockChildData.maxXP}
                level={mockChildData.level}
              />
            </section>

            <section className="animate-fade-up" style={{ animationDelay: '0.2s' }}>
              <h2 className="text-lg font-display font-semibold text-foreground mb-4">This Week&apos;s Performance</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <StatCard title="Study Time" value={mockChildData.weeklyStudyTime} icon={Clock} />
                <StatCard title="Tests Taken" value={mockChildData.testsThisWeek} icon={Target} />
                <StatCard
                  title="Average Score"
                  value={`${mockChildData.avgScore}%`}
                  icon={Trophy}
                  trend={{ value: 8, isPositive: true }}
                />
                <StatCard title="Attendance" value={`${mockChildData.attendance}%`} icon={Calendar} />
              </div>
            </section>

            <section className="animate-fade-up" style={{ animationDelay: '0.3s' }}>
              <h2 className="text-lg font-display font-semibold text-foreground mb-4 flex items-center gap-2">
                <Star className="w-5 h-5 text-xp" />
                AI-Generated Insights
              </h2>
              <div className="space-y-3">
                {weeklyInsights.map((item) => (
                  <div
                    key={item.id}
                    className={`p-4 rounded-xl border ${
                      item.type === 'positive'
                        ? 'bg-success/5 border-success/20'
                        : 'bg-warning/5 border-warning/20'
                    }`}
                  >
                    <p className="text-sm text-foreground">{item.insight}</p>
                  </div>
                ))}
              </div>
            </section>
          </div>

          <div className="space-y-6">
            <div className="p-5 rounded-xl bg-card border border-border shadow-sm animate-fade-up" style={{ animationDelay: '0.15s' }}>
              <h3 className="font-display font-semibold text-foreground mb-4">Subject Progress</h3>
              <div className="space-y-4">
                {[
                  { subject: 'Physics', progress: 75 },
                  { subject: 'Chemistry', progress: 62 },
                  { subject: 'Mathematics', progress: 88 },
                  { subject: 'Biology', progress: 70 },
                ].map((item) => (
                  <div key={item.subject} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-foreground">{item.subject}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-secondary rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-primary rounded-full"
                          style={{ width: `${item.progress}%` }}
                        />
                      </div>
                      <span className="text-xs text-muted-foreground w-8">{item.progress}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="p-5 rounded-xl bg-card border border-border shadow-sm animate-fade-up" style={{ animationDelay: '0.25s' }}>
              <h3 className="font-display font-semibold text-foreground mb-4 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-primary" />
                Upcoming
              </h3>
              <div className="space-y-3">
                <div className="p-3 rounded-lg bg-secondary/50">
                  <p className="font-medium text-foreground text-sm">Physics Test</p>
                  <p className="text-xs text-muted-foreground">
                    {formatDisplayDate(addDays(new Date(), 1))} / Chapter 5
                  </p>
                </div>
                <div className="p-3 rounded-lg bg-secondary/50">
                  <p className="font-medium text-foreground text-sm">Math Assignment</p>
                  <p className="text-xs text-muted-foreground">
                    {formatDisplayDate(addDays(new Date(), 2))} / Calculus
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ParentDashboard;
