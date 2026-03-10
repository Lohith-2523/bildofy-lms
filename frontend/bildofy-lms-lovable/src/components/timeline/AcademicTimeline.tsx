import React from 'react';
import { isPast } from 'date-fns';
import {
  Calendar,
  FileText,
  ClipboardCheck,
  GraduationCap,
  Clock,
} from 'lucide-react';

import { XPBadge } from '@/components/gamification/XPBadge';
import { formatDisplayDate } from '@/lib/date';
import { cn } from '@/lib/utils';

type EventType = 'assignment' | 'test' | 'exam' | 'event';

interface TimelineEvent {
  id: string;
  title: string;
  type: EventType;
  date: Date;
  subject?: string;
  xpReward?: number;
  isCompleted?: boolean;
}

interface AcademicTimelineProps {
  events: TimelineEvent[];
  onEventClick?: (event: TimelineEvent) => void;
  className?: string;
}

const eventConfig: Record<EventType, { icon: typeof Calendar; color: string; label: string }> = {
  assignment: { icon: FileText, color: 'bg-primary/10 text-primary border-primary/30', label: 'Assignment' },
  test: { icon: ClipboardCheck, color: 'bg-accent/10 text-accent border-accent/30', label: 'Test' },
  exam: { icon: GraduationCap, color: 'bg-destructive/10 text-destructive border-destructive/30', label: 'Exam' },
  event: { icon: Calendar, color: 'bg-success/10 text-success border-success/30', label: 'Event' },
};

export const AcademicTimeline: React.FC<AcademicTimelineProps> = ({
  events,
  onEventClick,
  className,
}) => {
  const sortedEvents = [...events].sort((a, b) => a.date.getTime() - b.date.getTime());

  return (
    <div className={cn('space-y-3', className)}>
      <h3 className="font-display font-semibold text-foreground flex items-center gap-2">
        <Clock className="w-5 h-5 text-primary" />
        Upcoming Events
      </h3>
      <div className="relative">
        <div className="absolute left-5 top-0 bottom-0 w-0.5 bg-border" />

        <div className="space-y-3">
          {sortedEvents.map((event) => {
            const config = eventConfig[event.type];
            const Icon = config.icon;
            const isOverdue = isPast(event.date) && !event.isCompleted;

            return (
              <button
                key={event.id}
                onClick={() => onEventClick?.(event)}
                className={cn(
                  'relative w-full text-left pl-12 pr-4 py-3 rounded-xl transition-all duration-200',
                  'bg-card border border-border shadow-sm',
                  'hover:shadow-md hover:border-primary/30 hover:-translate-x-1',
                  'focus:outline-none focus:ring-2 focus:ring-primary/50',
                  event.isCompleted && 'opacity-60',
                  isOverdue && 'border-destructive/30'
                )}
              >
                <div
                  className={cn(
                    'absolute left-2 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full border-2 flex items-center justify-center bg-card',
                    config.color
                  )}
                >
                  <Icon className="w-3.5 h-3.5" />
                </div>

                <div className="flex items-center justify-between gap-2">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <span
                        className={cn(
                          'text-xs font-medium px-2 py-0.5 rounded-full',
                          config.color
                        )}
                      >
                        {config.label}
                      </span>
                      {isOverdue && (
                        <span className="text-xs font-medium text-destructive">Overdue</span>
                      )}
                    </div>
                    <h4 className="font-semibold text-foreground mt-1 truncate">{event.title}</h4>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {event.subject && `${event.subject} / `}
                      {formatDisplayDate(event.date)}
                    </p>
                  </div>
                  {event.xpReward && !event.isCompleted && (
                    <XPBadge xp={event.xpReward} size="sm" />
                  )}
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
