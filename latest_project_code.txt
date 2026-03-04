# Combined Project Code


---

### `frontend\bildofy-lms-lovable\src\App.css`

```css
#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.react:hover {
  filter: drop-shadow(0 0 2em #61dafbaa);
}

@keyframes logo-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: no-preference) {
  a:nth-of-type(2) .logo {
    animation: logo-spin infinite 20s linear;
  }
}

.card {
  padding: 2em;
}

.read-the-docs {
  color: #888;
}

```

---

### `frontend\bildofy-lms-lovable\src\App.tsx`

```tsx
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";
import { OnlineProvider } from "@/contexts/OnlineContext";
import { OfflineBanner } from "@/components/layout/OfflineBanner";

// 🔹 Auth
import { AuthProvider, useAuth } from "@/contexts/AuthContext";

// 🔹 Pages (EXISTING – verified from combined_code_latest.md)
import LoginPage from "./pages/auth/LoginPage";
import SignupPage from "./pages/auth/SignupPage";

import StudentDashboard from "./pages/student/StudentDashboard";
import NotesPage from "./pages/student/NotesPage";
import TestsPage from "./pages/student/TestsPage";
import AssignmentsPage from "./pages/student/AssignmentsPage";
import FlashcardsPage from "./pages/student/FlashcardsPage";
import DoubtChatPage from "./pages/student/DoubtChatPage";

import TeacherDashboard from "./pages/teacher/TeacherDashboard";
import ParentDashboard from "./pages/parent/ParentDashboard";

import NotFound from "./pages/NotFound";

// 🔹 Role-based guard (ALREADY PROVIDED EARLIER)
import ProtectedRoute from "@/components/auth/ProtectedRoute";

const queryClient = new QueryClient();

/**
 * Redirects user based on auth state.
 * - Not logged in → /login
 * - Logged in → role dashboard
 */
const RootRedirect = () => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return null;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.role === "student") {
    return <Navigate to="/student" replace />;
  }

  if (user.role === "teacher") {
    return <Navigate to="/teacher" replace />;
  }

  if (user.role === "parent") {
    return <Navigate to="/parent" replace />;
  }

  return <Navigate to="/login" replace />;
};


const AppRoutes = () => (
  <Routes>
    {/* Root */}
    <Route path="/" element={<LoginPage />} />


    {/* Auth */}
    <Route path="/login" element={<LoginPage />} />
    <Route path="/signup" element={<SignupPage />} />

    {/* Student Routes */}
    <Route
      path="/student"
      element={
      <ProtectedRoute role="student">
        <Outlet />
      </ProtectedRoute>
        }
    >
      <Route index element={<StudentDashboard />} />
      <Route path="notes" element={<NotesPage />} />
        {/* ✅ Tests */}
      <Route path="tests" element={<TestsPage />} />
      <Route path="tests/:testId" element={<TestsPage />} />
      <Route path="assignments" element={<AssignmentsPage />} />
      <Route path="flashcards" element={<FlashcardsPage />} />
      <Route path="doubt-chat" element={<DoubtChatPage />} />
    </Route>


    {/* Teacher Routes */}
    <Route
      path="/teacher"
      element={
        <ProtectedRoute role="teacher">
          <TeacherDashboard />
        </ProtectedRoute>
      }
    />

    {/* Parent Routes */}
    <Route
      path="/parent"
      element={
        <ProtectedRoute role="parent">
          <ParentDashboard />
        </ProtectedRoute>
      }
    />

    {/* Catch-all */}
    <Route path="*" element={<NotFound />} />
  </Routes>
);

const App = () => (
  <QueryClientProvider client={queryClient}>
    <AuthProvider>
      <OnlineProvider>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <OfflineBanner />
          <BrowserRouter>
            <AppRoutes />
          </BrowserRouter>
        </TooltipProvider>
      </OnlineProvider>
    </AuthProvider>
  </QueryClientProvider>
);

export default App;

```

---

### `frontend\bildofy-lms-lovable\src\index.css`

```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Core palette - Deep indigo learning theme */
    --background: 220 20% 97%;
    --foreground: 222 47% 11%;
    
    --card: 0 0% 100%;
    --card-foreground: 222 47% 11%;
    
    --popover: 0 0% 100%;
    --popover-foreground: 222 47% 11%;
    
    /* Primary - Deep indigo blue */
    --primary: 234 89% 58%;
    --primary-foreground: 0 0% 100%;
    --primary-glow: 234 89% 68%;
    
    /* Secondary - Soft lavender */
    --secondary: 240 20% 96%;
    --secondary-foreground: 222 47% 11%;
    
    /* Muted */
    --muted: 220 14% 93%;
    --muted-foreground: 220 9% 46%;
    
    /* Accent - Golden orange for XP/rewards */
    --accent: 38 92% 50%;
    --accent-foreground: 0 0% 100%;
    --accent-glow: 38 100% 60%;
    
    /* XP/Gamification colors */
    --xp: 38 92% 50%;
    --xp-glow: 45 100% 60%;
    --level: 280 85% 55%;
    --streak: 15 95% 55%;
    --badge: 170 80% 45%;
    
    /* Success - Emerald */
    --success: 160 84% 39%;
    --success-foreground: 0 0% 100%;
    
    /* Warning */
    --warning: 38 92% 50%;
    --warning-foreground: 0 0% 100%;
    
    /* Destructive */
    --destructive: 0 84% 60%;
    --destructive-foreground: 0 0% 100%;
    
    /* Offline mode */
    --offline: 220 9% 46%;
    --offline-foreground: 0 0% 100%;
    
    --border: 220 13% 91%;
    --input: 220 13% 91%;
    --ring: 234 89% 58%;
    
    --radius: 0.75rem;
    
    /* Gradients */
    --gradient-primary: linear-gradient(135deg, hsl(234 89% 58%) 0%, hsl(280 85% 55%) 100%);
    --gradient-xp: linear-gradient(135deg, hsl(38 92% 50%) 0%, hsl(45 100% 60%) 100%);
    --gradient-success: linear-gradient(135deg, hsl(160 84% 39%) 0%, hsl(170 80% 45%) 100%);
    --gradient-streak: linear-gradient(135deg, hsl(15 95% 55%) 0%, hsl(38 92% 50%) 100%);
    --gradient-card: linear-gradient(180deg, hsl(0 0% 100%) 0%, hsl(220 20% 98%) 100%);
    --gradient-hero: linear-gradient(135deg, hsl(234 89% 58%) 0%, hsl(234 89% 48%) 50%, hsl(280 85% 45%) 100%);
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 hsl(220 20% 10% / 0.05);
    --shadow-md: 0 4px 6px -1px hsl(220 20% 10% / 0.1), 0 2px 4px -2px hsl(220 20% 10% / 0.1);
    --shadow-lg: 0 10px 15px -3px hsl(220 20% 10% / 0.1), 0 4px 6px -4px hsl(220 20% 10% / 0.1);
    --shadow-xl: 0 20px 25px -5px hsl(220 20% 10% / 0.1), 0 8px 10px -6px hsl(220 20% 10% / 0.1);
    --shadow-glow: 0 0 20px hsl(234 89% 58% / 0.3);
    --shadow-xp: 0 0 20px hsl(38 92% 50% / 0.4);
    
    /* Sidebar */
    --sidebar-background: 0 0% 100%;
    --sidebar-foreground: 222 47% 11%;
    --sidebar-primary: 234 89% 58%;
    --sidebar-primary-foreground: 0 0% 100%;
    --sidebar-accent: 220 20% 96%;
    --sidebar-accent-foreground: 222 47% 11%;
    --sidebar-border: 220 13% 91%;
    --sidebar-ring: 234 89% 58%;
  }

  .dark {
    --background: 222 47% 8%;
    --foreground: 210 40% 98%;
    
    --card: 222 47% 11%;
    --card-foreground: 210 40% 98%;
    
    --popover: 222 47% 11%;
    --popover-foreground: 210 40% 98%;
    
    --primary: 234 89% 65%;
    --primary-foreground: 0 0% 100%;
    --primary-glow: 234 89% 75%;
    
    --secondary: 217 33% 17%;
    --secondary-foreground: 210 40% 98%;
    
    --muted: 217 33% 17%;
    --muted-foreground: 215 20% 65%;
    
    --accent: 38 92% 55%;
    --accent-foreground: 0 0% 100%;
    
    --destructive: 0 63% 50%;
    --destructive-foreground: 210 40% 98%;
    
    --border: 217 33% 17%;
    --input: 217 33% 17%;
    --ring: 234 89% 65%;
    
    --sidebar-background: 222 47% 10%;
    --sidebar-foreground: 210 40% 98%;
    --sidebar-primary: 234 89% 65%;
    --sidebar-primary-foreground: 0 0% 100%;
    --sidebar-accent: 217 33% 17%;
    --sidebar-accent-foreground: 210 40% 98%;
    --sidebar-border: 217 33% 17%;
    --sidebar-ring: 234 89% 65%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  
  body {
    @apply bg-background text-foreground antialiased;
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  }
  
  h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', system-ui, sans-serif;
  }
}

@layer components {
  /* XP Animation */
  .xp-pulse {
    animation: xp-pulse 0.6s ease-out;
  }
  
  .xp-float {
    animation: xp-float 1s ease-out forwards;
  }
  
  .level-up {
    animation: level-up 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  
  .streak-flame {
    animation: flame-flicker 0.5s ease-in-out infinite alternate;
  }
  
  .badge-unlock {
    animation: badge-unlock 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  
  .card-hover {
    @apply transition-all duration-300 ease-out;
  }
  
  .card-hover:hover {
    @apply -translate-y-1;
    box-shadow: var(--shadow-xl);
  }
  
  .glow-primary {
    box-shadow: var(--shadow-glow);
  }
  
  .glow-xp {
    box-shadow: var(--shadow-xp);
  }
  
  /* Progress bar shimmer */
  .progress-shimmer {
    background: linear-gradient(
      90deg,
      transparent 0%,
      hsl(0 0% 100% / 0.3) 50%,
      transparent 100%
    );
    animation: shimmer 2s infinite;
  }
  
  /* Offline indicator pulse */
  .offline-pulse {
    animation: offline-pulse 2s ease-in-out infinite;
  }
}

@layer utilities {
  .text-gradient-primary {
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .text-gradient-xp {
    background: var(--gradient-xp);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .bg-gradient-primary {
    background: var(--gradient-primary);
  }
  
  .bg-gradient-xp {
    background: var(--gradient-xp);
  }
  
  .bg-gradient-success {
    background: var(--gradient-success);
  }
  
  .bg-gradient-streak {
    background: var(--gradient-streak);
  }
  
  .bg-gradient-hero {
    background: var(--gradient-hero);
  }
  
  .bg-gradient-card {
    background: var(--gradient-card);
  }
}

@keyframes xp-pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

@keyframes xp-float {
  0% { 
    opacity: 1; 
    transform: translateY(0) scale(1); 
  }
  100% { 
    opacity: 0; 
    transform: translateY(-40px) scale(1.2); 
  }
}

@keyframes level-up {
  0% { 
    transform: scale(0.5) rotate(-10deg); 
    opacity: 0; 
  }
  50% { 
    transform: scale(1.2) rotate(5deg); 
  }
  100% { 
    transform: scale(1) rotate(0deg); 
    opacity: 1; 
  }
}

@keyframes flame-flicker {
  0% { transform: scale(1) rotate(-3deg); }
  100% { transform: scale(1.05) rotate(3deg); }
}

@keyframes badge-unlock {
  0% { 
    transform: scale(0) rotate(-180deg); 
    opacity: 0; 
  }
  100% { 
    transform: scale(1) rotate(0deg); 
    opacity: 1; 
  }
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes offline-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

```

---

### `frontend\bildofy-lms-lovable\src\main.tsx`

```tsx
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import 'katex/dist/katex.min.css';

createRoot(document.getElementById("root")!).render(<App />);

```

---

### `frontend\bildofy-lms-lovable\src\vite-env.d.ts`

```ts
/// <reference types="vite/client" />

```

---

### `frontend\bildofy-lms-lovable\src\components\MarkdownKatexRenderer.tsx`

```tsx
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

type Props = {
  content: string;
};

const MarkdownKatexRenderer: React.FC<Props> = ({ content }) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkMath]}
      rehypePlugins={[rehypeKatex]}
      components={{
        h1: ({ node, ...props }) => (
          <h1 className="text-2xl font-bold mt-6 mb-4" {...props} />
        ),
        h2: ({ node, ...props }) => (
          <h2 className="text-xl font-semibold mt-5 mb-3" {...props} />
        ),
        p: ({ node, ...props }) => (
          <p className="leading-7 mb-3" {...props} />
        ),
        li: ({ node, ...props }) => (
          <li className="ml-6 list-disc mb-1" {...props} />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
};

export default MarkdownKatexRenderer;

```

---

### `frontend\bildofy-lms-lovable\src\components\NavLink.tsx`

```tsx
import { NavLink as RouterNavLink, NavLinkProps } from "react-router-dom";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";

interface NavLinkCompatProps extends Omit<NavLinkProps, "className"> {
  className?: string;
  activeClassName?: string;
  pendingClassName?: string;
}

const NavLink = forwardRef<HTMLAnchorElement, NavLinkCompatProps>(
  ({ className, activeClassName, pendingClassName, to, ...props }, ref) => {
    return (
      <RouterNavLink
        ref={ref}
        to={to}
        className={({ isActive, isPending }) =>
          cn(className, isActive && activeClassName, isPending && pendingClassName)
        }
        {...props}
      />
    );
  },
);

NavLink.displayName = "NavLink";

export { NavLink };

```

---

### `frontend\bildofy-lms-lovable\src\components\auth\ProtectedRoute.tsx`

```tsx
import { Navigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";

type Props = {
  children: JSX.Element;
  role: "student" | "teacher" | "parent" | "admin" | "super-user";
};

const normalizeRole = (role: string) =>
  role.replace("_", "-").toLowerCase();

const ProtectedRoute = ({ children, role }: Props) => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return null;
  }

  console.log("AUTH USER", user);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  const userRole = normalizeRole(user.role);
  const requiredRole = normalizeRole(role);

  if (userRole !== requiredRole) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;

```

---

### `frontend\bildofy-lms-lovable\src\components\cards\ActionCard.tsx`

```tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { XPBadge } from '@/components/gamification/XPBadge';
import { useOnlineStatus } from '@/contexts/OnlineContext';
import { LucideIcon, WifiOff, ChevronRight, Check } from 'lucide-react';

interface ActionCardProps {
  title: string;
  description: string;
  icon: LucideIcon;
  xpReward: number;
  progress?: number; // 0-100
  completed?: boolean;
  requiresOnline?: boolean;
  onClick?: () => void;
  className?: string;
  variant?: 'default' | 'featured';
}

export const ActionCard: React.FC<ActionCardProps> = ({
  title,
  description,
  icon: Icon,
  xpReward,
  progress,
  completed = false,
  requiresOnline = false,
  onClick,
  className,
  variant = 'default',
}) => {
  const { isOnline } = useOnlineStatus();
  const isDisabled = requiresOnline && !isOnline;

  return (
    <button
      onClick={onClick}
      disabled={isDisabled}
      className={cn(
        'relative w-full text-left p-4 rounded-xl transition-all duration-300',
        'bg-card border border-border shadow-sm',
        'hover:shadow-lg hover:-translate-y-1 hover:border-primary/30',
        'focus:outline-none focus:ring-2 focus:ring-primary/50',
        'disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-sm',
        variant === 'featured' && 'border-primary/30 bg-gradient-card',
        completed && 'bg-success/5 border-success/30',
        className
      )}
    >
      {/* Progress bar at top */}
      {progress !== undefined && progress > 0 && !completed && (
        <div className="absolute top-0 left-0 right-0 h-1 bg-secondary rounded-t-xl overflow-hidden">
          <div
            className="h-full bg-gradient-primary transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      <div className="flex items-start gap-4">
        {/* Icon */}
        <div
          className={cn(
            'flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center',
            completed
              ? 'bg-success/10 text-success'
              : variant === 'featured'
              ? 'bg-gradient-primary text-primary-foreground'
              : 'bg-primary/10 text-primary'
          )}
        >
          {completed ? <Check className="w-6 h-6" /> : <Icon className="w-6 h-6" />}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="font-semibold text-foreground">{title}</h3>
              <p className="text-sm text-muted-foreground mt-0.5 line-clamp-2">
                {description}
              </p>
            </div>
            <ChevronRight className="w-5 h-5 text-muted-foreground flex-shrink-0" />
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between mt-3">
            <XPBadge xp={xpReward} size="sm" />
            {isDisabled && (
              <div className="flex items-center gap-1 text-xs text-offline">
                <WifiOff className="w-3 h-3" />
                <span>Requires internet</span>
              </div>
            )}
            {progress !== undefined && !completed && (
              <span className="text-xs text-muted-foreground">{progress}% complete</span>
            )}
          </div>
        </div>
      </div>
    </button>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\cards\RoleCard.tsx`

```tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { LucideIcon, ArrowRight } from 'lucide-react';

interface RoleCardProps {
  title: string;
  description: string;
  icon: LucideIcon;
  gradient: 'primary' | 'accent' | 'success';
  onClick?: () => void;
  className?: string;
}

export const RoleCard: React.FC<RoleCardProps> = ({
  title,
  description,
  icon: Icon,
  gradient,
  onClick,
  className,
}) => {
  const gradientClasses = {
    primary: 'from-primary to-primary/80 hover:shadow-glow',
    accent: 'from-accent to-accent/80 hover:shadow-xp',
    success: 'from-success to-success/80',
  };

  return (
    <button
      onClick={onClick}
      className={cn(
        'group relative w-full p-6 rounded-2xl transition-all duration-500',
        'bg-gradient-to-br text-primary-foreground',
        'hover:-translate-y-2 hover:scale-[1.02]',
        'focus:outline-none focus:ring-4 focus:ring-primary/30',
        'shadow-lg',
        gradientClasses[gradient],
        className
      )}
    >
      {/* Background pattern */}
      <div className="absolute inset-0 rounded-2xl overflow-hidden opacity-10">
        <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/20 rounded-full blur-2xl" />
        <div className="absolute -bottom-10 -left-10 w-32 h-32 bg-white/10 rounded-full blur-xl" />
      </div>

      <div className="relative z-10">
        {/* Icon */}
        <div className="w-16 h-16 mb-4 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
          <Icon className="w-8 h-8" />
        </div>

        {/* Content */}
        <h3 className="text-xl font-display font-bold mb-2">{title}</h3>
        <p className="text-sm opacity-90 mb-4 line-clamp-2">{description}</p>

        {/* CTA */}
        <div className="flex items-center gap-2 text-sm font-semibold group-hover:gap-3 transition-all duration-300">
          <span>Get Started</span>
          <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </div>
      </div>
    </button>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\cards\StatCard.tsx`

```tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  description?: string;
  className?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon: Icon,
  trend,
  description,
  className,
}) => {
  return (
    <div
      className={cn(
        'p-4 rounded-xl bg-card border border-border shadow-sm',
        'hover:shadow-md transition-shadow duration-200',
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm text-muted-foreground font-medium">{title}</p>
          <p className="text-2xl font-bold text-foreground mt-1">{value}</p>
          {description && (
            <p className="text-xs text-muted-foreground mt-1">{description}</p>
          )}
          {trend && (
            <div
              className={cn(
                'flex items-center gap-1 text-xs font-medium mt-2',
                trend.isPositive ? 'text-success' : 'text-destructive'
              )}
            >
              {trend.isPositive ? (
                <TrendingUp className="w-3 h-3" />
              ) : (
                <TrendingDown className="w-3 h-3" />
              )}
              <span>{trend.isPositive ? '+' : ''}{trend.value}%</span>
              <span className="text-muted-foreground">vs last week</span>
            </div>
          )}
        </div>
        <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
          <Icon className="w-5 h-5 text-primary" />
        </div>
      </div>
    </div>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\gamification\LevelBadge.tsx`

```tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { Star } from 'lucide-react';

interface LevelBadgeProps {
  level: number;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const LevelBadge: React.FC<LevelBadgeProps> = ({
  level,
  size = 'md',
  className,
}) => {
  const sizeClasses = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-14 h-14 text-lg',
  };

  const iconSizes = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  };

  return (
    <div
      className={cn(
        'relative inline-flex items-center justify-center rounded-full bg-gradient-primary text-primary-foreground font-bold shadow-glow',
        sizeClasses[size],
        className
      )}
    >
      <Star className={cn(iconSizes[size], 'absolute -top-1 -right-1 fill-xp text-xp')} />
      <span>{level}</span>
    </div>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\gamification\StreakIndicator.tsx`

```tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { Flame } from 'lucide-react';

interface StreakIndicatorProps {
  streak: number;
  isActive?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const StreakIndicator: React.FC<StreakIndicatorProps> = ({
  streak,
  isActive = true,
  size = 'md',
  className,
}) => {
  const sizeClasses = {
    sm: 'text-sm gap-1',
    md: 'text-base gap-1.5',
    lg: 'text-lg gap-2',
  };

  const iconSizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  return (
    <div
      className={cn(
        'flex items-center font-bold',
        sizeClasses[size],
        isActive ? 'text-streak' : 'text-muted-foreground',
        className
      )}
    >
      <Flame
        className={cn(
          iconSizes[size],
          isActive && 'streak-flame fill-streak/20'
        )}
      />
      <span>{streak}</span>
      <span className="text-xs font-medium opacity-70">day{streak !== 1 ? 's' : ''}</span>
    </div>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\gamification\XPBadge.tsx`

```tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { Zap } from 'lucide-react';

interface XPBadgeProps {
  xp: number;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  showIcon?: boolean;
}

export const XPBadge: React.FC<XPBadgeProps> = ({
  xp,
  size = 'md',
  className,
  showIcon = true,
}) => {
  const sizeClasses = {
    sm: 'text-xs px-1.5 py-0.5 gap-0.5',
    md: 'text-sm px-2 py-1 gap-1',
    lg: 'text-base px-3 py-1.5 gap-1.5',
  };

  const iconSizes = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  };

  return (
    <div
      className={cn(
        'inline-flex items-center font-bold rounded-full bg-gradient-xp text-accent-foreground shadow-sm',
        sizeClasses[size],
        className
      )}
    >
      {showIcon && <Zap className={cn(iconSizes[size], 'fill-current')} />}
      <span>+{xp} XP</span>
    </div>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\gamification\XPBar.tsx`

```tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { Sparkles } from 'lucide-react';

interface XPBarProps {
  currentXP: number;
  maxXP: number;
  level: number;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  animated?: boolean;
}

export const XPBar: React.FC<XPBarProps> = ({
  currentXP,
  maxXP,
  level,
  showLabel = true,
  size = 'md',
  className,
  animated = true,
}) => {
  const progress = Math.min((currentXP / maxXP) * 100, 100);

  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
  };

  return (
    <div className={cn('w-full', className)}>
      {showLabel && (
        <div className="flex items-center justify-between mb-1.5">
          <div className="flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-xp" />
            <span className="text-sm font-semibold text-foreground">
              Level {level}
            </span>
          </div>
          <span className="text-xs font-medium text-muted-foreground">
            {currentXP.toLocaleString()} / {maxXP.toLocaleString()} XP
          </span>
        </div>
      )}
      <div
        className={cn(
          'w-full bg-secondary rounded-full overflow-hidden relative',
          sizeClasses[size]
        )}
      >
        <div
          className={cn(
            'h-full bg-gradient-xp rounded-full relative transition-all duration-500 ease-out',
            animated && 'glow-xp'
          )}
          style={{ width: `${progress}%` }}
        >
          {animated && progress > 10 && (
            <div className="absolute inset-0 progress-shimmer" />
          )}
        </div>
      </div>
    </div>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\gamification\XPGainAnimation.tsx`

```tsx
import React, { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { Zap } from 'lucide-react';

interface XPGainAnimationProps {
  xp: number;
  onComplete?: () => void;
  className?: string;
}

export const XPGainAnimation: React.FC<XPGainAnimationProps> = ({
  xp,
  onComplete,
  className,
}) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      onComplete?.();
    }, 1000);

    return () => clearTimeout(timer);
  }, [onComplete]);

  if (!isVisible) return null;

  return (
    <div
      className={cn(
        'fixed inset-0 pointer-events-none flex items-center justify-center z-50',
        className
      )}
    >
      <div className="xp-float flex items-center gap-2 text-2xl font-bold text-xp bg-card/95 backdrop-blur-sm px-6 py-3 rounded-full shadow-xp border border-xp/20">
        <Zap className="w-6 h-6 fill-xp" />
        <span>+{xp} XP</span>
      </div>
    </div>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\layout\OfflineBanner.tsx`

```tsx
import React from 'react';
import { useOnlineStatus } from '@/contexts/OnlineContext';
import { WifiOff, CloudOff } from 'lucide-react';
import { cn } from '@/lib/utils';

interface OfflineBannerProps {
  className?: string;
}

export const OfflineBanner: React.FC<OfflineBannerProps> = ({ className }) => {
  const { isOnline } = useOnlineStatus();

  if (isOnline) return null;

  return (
    <div
      className={cn(
        'fixed top-0 left-0 right-0 z-50 bg-offline text-offline-foreground py-2 px-4 flex items-center justify-center gap-2 text-sm font-medium offline-pulse',
        className
      )}
    >
      <WifiOff className="w-4 h-4" />
      <span>You're offline. Some features may be limited.</span>
      <CloudOff className="w-4 h-4" />
    </div>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\layout\StudentHeader.tsx`

```tsx
import React from 'react';
import { XPBar } from '@/components/gamification/XPBar';
import { StreakIndicator } from '@/components/gamification/StreakIndicator';
import { LevelBadge } from '@/components/gamification/LevelBadge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Bell, Settings, Menu } from 'lucide-react';
import { Link } from 'react-router-dom';

interface StudentHeaderProps {
  student: {
    name: string;
    avatar?: string;
    grade: string;
    board: string;
    level: number;
    currentXP: number;
    maxXP: number;
    streak: number;
  };
  onMenuClick?: () => void;
}

export const StudentHeader: React.FC<StudentHeaderProps> = ({ student, onMenuClick }) => {
  const initials = student.name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  return (
    <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between gap-4">
          {/* Left: Menu + Logo */}
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="icon" className="md:hidden" onClick={onMenuClick}>
              <Menu className="w-5 h-5" />
            </Button>
            <Link to="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-sm">L</span>
              </div>
              <span className="hidden sm:block font-display font-bold text-lg text-foreground">
                LearnSphere
              </span>
            </Link>
          </div>

          {/* Center: XP Progress (hidden on mobile) */}
          <div className="hidden md:flex flex-1 max-w-md">
            <XPBar
              currentXP={student.currentXP}
              maxXP={student.maxXP}
              level={student.level}
              size="sm"
            />
          </div>

          {/* Right: Streak + Avatar + Actions */}
          <div className="flex items-center gap-3">
            <StreakIndicator streak={student.streak} size="sm" />
            
            <div className="hidden sm:flex items-center gap-2">
              <Button variant="ghost" size="icon">
                <Bell className="w-5 h-5" />
              </Button>
              <Button variant="ghost" size="icon">
                <Settings className="w-5 h-5" />
              </Button>
            </div>

            <div className="flex items-center gap-2">
              <LevelBadge level={student.level} size="sm" />
              <div className="hidden sm:block text-right">
                <p className="text-sm font-semibold text-foreground">{student.name}</p>
                <p className="text-xs text-muted-foreground">
                  {student.grade} • {student.board}
                </p>
              </div>
              <Avatar className="w-9 h-9 border-2 border-primary/20">
                <AvatarImage src={student.avatar} alt={student.name} />
                <AvatarFallback className="bg-primary/10 text-primary font-semibold text-sm">
                  {initials}
                </AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>

        {/* Mobile XP Bar */}
        <div className="md:hidden mt-3">
          <XPBar
            currentXP={student.currentXP}
            maxXP={student.maxXP}
            level={student.level}
            size="sm"
          />
        </div>
      </div>
    </header>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\progress\ProgressRing.tsx`

```tsx
import React from 'react';
import { cn } from '@/lib/utils';

interface ProgressRingProps {
  progress: number; // 0-100
  size?: number;
  strokeWidth?: number;
  color?: 'primary' | 'accent' | 'success' | 'xp';
  showLabel?: boolean;
  label?: string;
  className?: string;
}

export const ProgressRing: React.FC<ProgressRingProps> = ({
  progress,
  size = 80,
  strokeWidth = 8,
  color = 'primary',
  showLabel = true,
  label,
  className,
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;

  const colorClasses = {
    primary: 'stroke-primary',
    accent: 'stroke-accent',
    success: 'stroke-success',
    xp: 'stroke-xp',
  };

  return (
    <div className={cn('relative inline-flex items-center justify-center', className)}>
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="none"
          className="text-secondary"
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          className={cn('transition-all duration-500 ease-out', colorClasses[color])}
          style={{
            strokeDasharray: circumference,
            strokeDashoffset: offset,
          }}
        />
      </svg>
      {showLabel && (
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-lg font-bold text-foreground">{Math.round(progress)}%</span>
          {label && <span className="text-xs text-muted-foreground">{label}</span>}
        </div>
      )}
    </div>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\components\timeline\AcademicTimeline.tsx`

```tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { XPBadge } from '@/components/gamification/XPBadge';
import { 
  Calendar, 
  FileText, 
  ClipboardCheck, 
  GraduationCap,
  Clock
} from 'lucide-react';
import { format, isToday, isTomorrow, isPast } from 'date-fns';

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

const formatEventDate = (date: Date): string => {
  if (isToday(date)) return 'Today';
  if (isTomorrow(date)) return 'Tomorrow';
  return format(date, 'EEE, MMM d');
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
        {/* Timeline line */}
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
                {/* Icon */}
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
                      {event.subject && `${event.subject} • `}
                      {formatEventDate(event.date)}
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

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\accordion.tsx`

```tsx
import * as React from "react";
import * as AccordionPrimitive from "@radix-ui/react-accordion";
import { ChevronDown } from "lucide-react";

import { cn } from "@/lib/utils";

const Accordion = AccordionPrimitive.Root;

const AccordionItem = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item>
>(({ className, ...props }, ref) => (
  <AccordionPrimitive.Item ref={ref} className={cn("border-b", className)} {...props} />
));
AccordionItem.displayName = "AccordionItem";

const AccordionTrigger = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Header className="flex">
    <AccordionPrimitive.Trigger
      ref={ref}
      className={cn(
        "flex flex-1 items-center justify-between py-4 font-medium transition-all hover:underline [&[data-state=open]>svg]:rotate-180",
        className,
      )}
      {...props}
    >
      {children}
      <ChevronDown className="h-4 w-4 shrink-0 transition-transform duration-200" />
    </AccordionPrimitive.Trigger>
  </AccordionPrimitive.Header>
));
AccordionTrigger.displayName = AccordionPrimitive.Trigger.displayName;

const AccordionContent = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Content
    ref={ref}
    className="overflow-hidden text-sm transition-all data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down"
    {...props}
  >
    <div className={cn("pb-4 pt-0", className)}>{children}</div>
  </AccordionPrimitive.Content>
));

AccordionContent.displayName = AccordionPrimitive.Content.displayName;

export { Accordion, AccordionItem, AccordionTrigger, AccordionContent };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\alert-dialog.tsx`

```tsx
import * as React from "react";
import * as AlertDialogPrimitive from "@radix-ui/react-alert-dialog";

import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";

const AlertDialog = AlertDialogPrimitive.Root;

const AlertDialogTrigger = AlertDialogPrimitive.Trigger;

const AlertDialogPortal = AlertDialogPrimitive.Portal;

const AlertDialogOverlay = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Overlay
    className={cn(
      "fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className,
    )}
    {...props}
    ref={ref}
  />
));
AlertDialogOverlay.displayName = AlertDialogPrimitive.Overlay.displayName;

const AlertDialogContent = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Content>
>(({ className, ...props }, ref) => (
  <AlertDialogPortal>
    <AlertDialogOverlay />
    <AlertDialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
        className,
      )}
      {...props}
    />
  </AlertDialogPortal>
));
AlertDialogContent.displayName = AlertDialogPrimitive.Content.displayName;

const AlertDialogHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col space-y-2 text-center sm:text-left", className)} {...props} />
);
AlertDialogHeader.displayName = "AlertDialogHeader";

const AlertDialogFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2", className)} {...props} />
);
AlertDialogFooter.displayName = "AlertDialogFooter";

const AlertDialogTitle = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Title ref={ref} className={cn("text-lg font-semibold", className)} {...props} />
));
AlertDialogTitle.displayName = AlertDialogPrimitive.Title.displayName;

const AlertDialogDescription = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Description ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
));
AlertDialogDescription.displayName = AlertDialogPrimitive.Description.displayName;

const AlertDialogAction = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Action>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Action>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Action ref={ref} className={cn(buttonVariants(), className)} {...props} />
));
AlertDialogAction.displayName = AlertDialogPrimitive.Action.displayName;

const AlertDialogCancel = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Cancel>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Cancel>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Cancel
    ref={ref}
    className={cn(buttonVariants({ variant: "outline" }), "mt-2 sm:mt-0", className)}
    {...props}
  />
));
AlertDialogCancel.displayName = AlertDialogPrimitive.Cancel.displayName;

export {
  AlertDialog,
  AlertDialogPortal,
  AlertDialogOverlay,
  AlertDialogTrigger,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogAction,
  AlertDialogCancel,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\alert.tsx`

```tsx
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const alertVariants = cva(
  "relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground",
        destructive: "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

const Alert = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof alertVariants>
>(({ className, variant, ...props }, ref) => (
  <div ref={ref} role="alert" className={cn(alertVariants({ variant }), className)} {...props} />
));
Alert.displayName = "Alert";

const AlertTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h5 ref={ref} className={cn("mb-1 font-medium leading-none tracking-tight", className)} {...props} />
  ),
);
AlertTitle.displayName = "AlertTitle";

const AlertDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("text-sm [&_p]:leading-relaxed", className)} {...props} />
  ),
);
AlertDescription.displayName = "AlertDescription";

export { Alert, AlertTitle, AlertDescription };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\aspect-ratio.tsx`

```tsx
import * as AspectRatioPrimitive from "@radix-ui/react-aspect-ratio";

const AspectRatio = AspectRatioPrimitive.Root;

export { AspectRatio };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\avatar.tsx`

```tsx
import * as React from "react";
import * as AvatarPrimitive from "@radix-ui/react-avatar";

import { cn } from "@/lib/utils";

const Avatar = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn("relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full", className)}
    {...props}
  />
));
Avatar.displayName = AvatarPrimitive.Root.displayName;

const AvatarImage = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Image>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Image ref={ref} className={cn("aspect-square h-full w-full", className)} {...props} />
));
AvatarImage.displayName = AvatarPrimitive.Image.displayName;

const AvatarFallback = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Fallback>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn("flex h-full w-full items-center justify-center rounded-full bg-muted", className)}
    {...props}
  />
));
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName;

export { Avatar, AvatarImage, AvatarFallback };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\badge.tsx`

```tsx
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
        secondary: "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive: "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
        outline: "text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}

export { Badge, badgeVariants };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\breadcrumb.tsx`

```tsx
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { ChevronRight, MoreHorizontal } from "lucide-react";

import { cn } from "@/lib/utils";

const Breadcrumb = React.forwardRef<
  HTMLElement,
  React.ComponentPropsWithoutRef<"nav"> & {
    separator?: React.ReactNode;
  }
>(({ ...props }, ref) => <nav ref={ref} aria-label="breadcrumb" {...props} />);
Breadcrumb.displayName = "Breadcrumb";

const BreadcrumbList = React.forwardRef<HTMLOListElement, React.ComponentPropsWithoutRef<"ol">>(
  ({ className, ...props }, ref) => (
    <ol
      ref={ref}
      className={cn(
        "flex flex-wrap items-center gap-1.5 break-words text-sm text-muted-foreground sm:gap-2.5",
        className,
      )}
      {...props}
    />
  ),
);
BreadcrumbList.displayName = "BreadcrumbList";

const BreadcrumbItem = React.forwardRef<HTMLLIElement, React.ComponentPropsWithoutRef<"li">>(
  ({ className, ...props }, ref) => (
    <li ref={ref} className={cn("inline-flex items-center gap-1.5", className)} {...props} />
  ),
);
BreadcrumbItem.displayName = "BreadcrumbItem";

const BreadcrumbLink = React.forwardRef<
  HTMLAnchorElement,
  React.ComponentPropsWithoutRef<"a"> & {
    asChild?: boolean;
  }
>(({ asChild, className, ...props }, ref) => {
  const Comp = asChild ? Slot : "a";

  return <Comp ref={ref} className={cn("transition-colors hover:text-foreground", className)} {...props} />;
});
BreadcrumbLink.displayName = "BreadcrumbLink";

const BreadcrumbPage = React.forwardRef<HTMLSpanElement, React.ComponentPropsWithoutRef<"span">>(
  ({ className, ...props }, ref) => (
    <span
      ref={ref}
      role="link"
      aria-disabled="true"
      aria-current="page"
      className={cn("font-normal text-foreground", className)}
      {...props}
    />
  ),
);
BreadcrumbPage.displayName = "BreadcrumbPage";

const BreadcrumbSeparator = ({ children, className, ...props }: React.ComponentProps<"li">) => (
  <li role="presentation" aria-hidden="true" className={cn("[&>svg]:size-3.5", className)} {...props}>
    {children ?? <ChevronRight />}
  </li>
);
BreadcrumbSeparator.displayName = "BreadcrumbSeparator";

const BreadcrumbEllipsis = ({ className, ...props }: React.ComponentProps<"span">) => (
  <span
    role="presentation"
    aria-hidden="true"
    className={cn("flex h-9 w-9 items-center justify-center", className)}
    {...props}
  >
    <MoreHorizontal className="h-4 w-4" />
    <span className="sr-only">More</span>
  </span>
);
BreadcrumbEllipsis.displayName = "BreadcrumbElipssis";

export {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbPage,
  BreadcrumbSeparator,
  BreadcrumbEllipsis,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\button.tsx`

```tsx
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow-md hover:bg-primary/90 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0",
        destructive: "bg-destructive text-destructive-foreground shadow-md hover:bg-destructive/90 hover:shadow-lg",
        outline: "border-2 border-input bg-background hover:bg-accent hover:text-accent-foreground hover:border-accent",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80 hover:shadow-md",
        ghost: "hover:bg-accent/10 hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        success: "bg-success text-success-foreground shadow-md hover:bg-success/90 hover:shadow-lg hover:-translate-y-0.5",
        action: "bg-card text-card-foreground border border-border shadow-sm hover:shadow-md hover:border-primary/30 hover:-translate-y-0.5",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3 text-xs",
        lg: "h-12 rounded-xl px-8 text-base",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />;
  },
);
Button.displayName = "Button";

export { Button, buttonVariants };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\calendar.tsx`

```tsx
import * as React from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { DayPicker } from "react-day-picker";

import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";

export type CalendarProps = React.ComponentProps<typeof DayPicker>;

function Calendar({ className, classNames, showOutsideDays = true, ...props }: CalendarProps) {
  return (
    <DayPicker
      showOutsideDays={showOutsideDays}
      className={cn("p-3", className)}
      classNames={{
        months: "flex flex-col sm:flex-row space-y-4 sm:space-x-4 sm:space-y-0",
        month: "space-y-4",
        caption: "flex justify-center pt-1 relative items-center",
        caption_label: "text-sm font-medium",
        nav: "space-x-1 flex items-center",
        nav_button: cn(
          buttonVariants({ variant: "outline" }),
          "h-7 w-7 bg-transparent p-0 opacity-50 hover:opacity-100",
        ),
        nav_button_previous: "absolute left-1",
        nav_button_next: "absolute right-1",
        table: "w-full border-collapse space-y-1",
        head_row: "flex",
        head_cell: "text-muted-foreground rounded-md w-9 font-normal text-[0.8rem]",
        row: "flex w-full mt-2",
        cell: "h-9 w-9 text-center text-sm p-0 relative [&:has([aria-selected].day-range-end)]:rounded-r-md [&:has([aria-selected].day-outside)]:bg-accent/50 [&:has([aria-selected])]:bg-accent first:[&:has([aria-selected])]:rounded-l-md last:[&:has([aria-selected])]:rounded-r-md focus-within:relative focus-within:z-20",
        day: cn(buttonVariants({ variant: "ghost" }), "h-9 w-9 p-0 font-normal aria-selected:opacity-100"),
        day_range_end: "day-range-end",
        day_selected:
          "bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground focus:bg-primary focus:text-primary-foreground",
        day_today: "bg-accent text-accent-foreground",
        day_outside:
          "day-outside text-muted-foreground opacity-50 aria-selected:bg-accent/50 aria-selected:text-muted-foreground aria-selected:opacity-30",
        day_disabled: "text-muted-foreground opacity-50",
        day_range_middle: "aria-selected:bg-accent aria-selected:text-accent-foreground",
        day_hidden: "invisible",
        ...classNames,
      }}
      components={{
        IconLeft: ({ ..._props }) => <ChevronLeft className="h-4 w-4" />,
        IconRight: ({ ..._props }) => <ChevronRight className="h-4 w-4" />,
      }}
      {...props}
    />
  );
}
Calendar.displayName = "Calendar";

export { Calendar };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\card.tsx`

```tsx
import * as React from "react";

import { cn } from "@/lib/utils";

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)} {...props} />
));
Card.displayName = "Card";

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  ),
);
CardHeader.displayName = "CardHeader";

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...props} />
  ),
);
CardTitle.displayName = "CardTitle";

const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
  ),
);
CardDescription.displayName = "CardDescription";

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />,
);
CardContent.displayName = "CardContent";

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
  ),
);
CardFooter.displayName = "CardFooter";

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\carousel.tsx`

```tsx
import * as React from "react";
import useEmblaCarousel, { type UseEmblaCarouselType } from "embla-carousel-react";
import { ArrowLeft, ArrowRight } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

type CarouselApi = UseEmblaCarouselType[1];
type UseCarouselParameters = Parameters<typeof useEmblaCarousel>;
type CarouselOptions = UseCarouselParameters[0];
type CarouselPlugin = UseCarouselParameters[1];

type CarouselProps = {
  opts?: CarouselOptions;
  plugins?: CarouselPlugin;
  orientation?: "horizontal" | "vertical";
  setApi?: (api: CarouselApi) => void;
};

type CarouselContextProps = {
  carouselRef: ReturnType<typeof useEmblaCarousel>[0];
  api: ReturnType<typeof useEmblaCarousel>[1];
  scrollPrev: () => void;
  scrollNext: () => void;
  canScrollPrev: boolean;
  canScrollNext: boolean;
} & CarouselProps;

const CarouselContext = React.createContext<CarouselContextProps | null>(null);

function useCarousel() {
  const context = React.useContext(CarouselContext);

  if (!context) {
    throw new Error("useCarousel must be used within a <Carousel />");
  }

  return context;
}

const Carousel = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & CarouselProps>(
  ({ orientation = "horizontal", opts, setApi, plugins, className, children, ...props }, ref) => {
    const [carouselRef, api] = useEmblaCarousel(
      {
        ...opts,
        axis: orientation === "horizontal" ? "x" : "y",
      },
      plugins,
    );
    const [canScrollPrev, setCanScrollPrev] = React.useState(false);
    const [canScrollNext, setCanScrollNext] = React.useState(false);

    const onSelect = React.useCallback((api: CarouselApi) => {
      if (!api) {
        return;
      }

      setCanScrollPrev(api.canScrollPrev());
      setCanScrollNext(api.canScrollNext());
    }, []);

    const scrollPrev = React.useCallback(() => {
      api?.scrollPrev();
    }, [api]);

    const scrollNext = React.useCallback(() => {
      api?.scrollNext();
    }, [api]);

    const handleKeyDown = React.useCallback(
      (event: React.KeyboardEvent<HTMLDivElement>) => {
        if (event.key === "ArrowLeft") {
          event.preventDefault();
          scrollPrev();
        } else if (event.key === "ArrowRight") {
          event.preventDefault();
          scrollNext();
        }
      },
      [scrollPrev, scrollNext],
    );

    React.useEffect(() => {
      if (!api || !setApi) {
        return;
      }

      setApi(api);
    }, [api, setApi]);

    React.useEffect(() => {
      if (!api) {
        return;
      }

      onSelect(api);
      api.on("reInit", onSelect);
      api.on("select", onSelect);

      return () => {
        api?.off("select", onSelect);
      };
    }, [api, onSelect]);

    return (
      <CarouselContext.Provider
        value={{
          carouselRef,
          api: api,
          opts,
          orientation: orientation || (opts?.axis === "y" ? "vertical" : "horizontal"),
          scrollPrev,
          scrollNext,
          canScrollPrev,
          canScrollNext,
        }}
      >
        <div
          ref={ref}
          onKeyDownCapture={handleKeyDown}
          className={cn("relative", className)}
          role="region"
          aria-roledescription="carousel"
          {...props}
        >
          {children}
        </div>
      </CarouselContext.Provider>
    );
  },
);
Carousel.displayName = "Carousel";

const CarouselContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => {
    const { carouselRef, orientation } = useCarousel();

    return (
      <div ref={carouselRef} className="overflow-hidden">
        <div
          ref={ref}
          className={cn("flex", orientation === "horizontal" ? "-ml-4" : "-mt-4 flex-col", className)}
          {...props}
        />
      </div>
    );
  },
);
CarouselContent.displayName = "CarouselContent";

const CarouselItem = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => {
    const { orientation } = useCarousel();

    return (
      <div
        ref={ref}
        role="group"
        aria-roledescription="slide"
        className={cn("min-w-0 shrink-0 grow-0 basis-full", orientation === "horizontal" ? "pl-4" : "pt-4", className)}
        {...props}
      />
    );
  },
);
CarouselItem.displayName = "CarouselItem";

const CarouselPrevious = React.forwardRef<HTMLButtonElement, React.ComponentProps<typeof Button>>(
  ({ className, variant = "outline", size = "icon", ...props }, ref) => {
    const { orientation, scrollPrev, canScrollPrev } = useCarousel();

    return (
      <Button
        ref={ref}
        variant={variant}
        size={size}
        className={cn(
          "absolute h-8 w-8 rounded-full",
          orientation === "horizontal"
            ? "-left-12 top-1/2 -translate-y-1/2"
            : "-top-12 left-1/2 -translate-x-1/2 rotate-90",
          className,
        )}
        disabled={!canScrollPrev}
        onClick={scrollPrev}
        {...props}
      >
        <ArrowLeft className="h-4 w-4" />
        <span className="sr-only">Previous slide</span>
      </Button>
    );
  },
);
CarouselPrevious.displayName = "CarouselPrevious";

const CarouselNext = React.forwardRef<HTMLButtonElement, React.ComponentProps<typeof Button>>(
  ({ className, variant = "outline", size = "icon", ...props }, ref) => {
    const { orientation, scrollNext, canScrollNext } = useCarousel();

    return (
      <Button
        ref={ref}
        variant={variant}
        size={size}
        className={cn(
          "absolute h-8 w-8 rounded-full",
          orientation === "horizontal"
            ? "-right-12 top-1/2 -translate-y-1/2"
            : "-bottom-12 left-1/2 -translate-x-1/2 rotate-90",
          className,
        )}
        disabled={!canScrollNext}
        onClick={scrollNext}
        {...props}
      >
        <ArrowRight className="h-4 w-4" />
        <span className="sr-only">Next slide</span>
      </Button>
    );
  },
);
CarouselNext.displayName = "CarouselNext";

export { type CarouselApi, Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\chart.tsx`

```tsx
import * as React from "react";
import * as RechartsPrimitive from "recharts";

import { cn } from "@/lib/utils";

// Format: { THEME_NAME: CSS_SELECTOR }
const THEMES = { light: "", dark: ".dark" } as const;

export type ChartConfig = {
  [k in string]: {
    label?: React.ReactNode;
    icon?: React.ComponentType;
  } & ({ color?: string; theme?: never } | { color?: never; theme: Record<keyof typeof THEMES, string> });
};

type ChartContextProps = {
  config: ChartConfig;
};

const ChartContext = React.createContext<ChartContextProps | null>(null);

function useChart() {
  const context = React.useContext(ChartContext);

  if (!context) {
    throw new Error("useChart must be used within a <ChartContainer />");
  }

  return context;
}

const ChartContainer = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div"> & {
    config: ChartConfig;
    children: React.ComponentProps<typeof RechartsPrimitive.ResponsiveContainer>["children"];
  }
>(({ id, className, children, config, ...props }, ref) => {
  const uniqueId = React.useId();
  const chartId = `chart-${id || uniqueId.replace(/:/g, "")}`;

  return (
    <ChartContext.Provider value={{ config }}>
      <div
        data-chart={chartId}
        ref={ref}
        className={cn(
          "flex aspect-video justify-center text-xs [&_.recharts-cartesian-axis-tick_text]:fill-muted-foreground [&_.recharts-cartesian-grid_line[stroke='#ccc']]:stroke-border/50 [&_.recharts-curve.recharts-tooltip-cursor]:stroke-border [&_.recharts-dot[stroke='#fff']]:stroke-transparent [&_.recharts-layer]:outline-none [&_.recharts-polar-grid_[stroke='#ccc']]:stroke-border [&_.recharts-radial-bar-background-sector]:fill-muted [&_.recharts-rectangle.recharts-tooltip-cursor]:fill-muted [&_.recharts-reference-line_[stroke='#ccc']]:stroke-border [&_.recharts-sector[stroke='#fff']]:stroke-transparent [&_.recharts-sector]:outline-none [&_.recharts-surface]:outline-none",
          className,
        )}
        {...props}
      >
        <ChartStyle id={chartId} config={config} />
        <RechartsPrimitive.ResponsiveContainer>{children}</RechartsPrimitive.ResponsiveContainer>
      </div>
    </ChartContext.Provider>
  );
});
ChartContainer.displayName = "Chart";

const ChartStyle = ({ id, config }: { id: string; config: ChartConfig }) => {
  const colorConfig = Object.entries(config).filter(([_, config]) => config.theme || config.color);

  if (!colorConfig.length) {
    return null;
  }

  return (
    <style
      dangerouslySetInnerHTML={{
        __html: Object.entries(THEMES)
          .map(
            ([theme, prefix]) => `
${prefix} [data-chart=${id}] {
${colorConfig
  .map(([key, itemConfig]) => {
    const color = itemConfig.theme?.[theme as keyof typeof itemConfig.theme] || itemConfig.color;
    return color ? `  --color-${key}: ${color};` : null;
  })
  .join("\n")}
}
`,
          )
          .join("\n"),
      }}
    />
  );
};

const ChartTooltip = RechartsPrimitive.Tooltip;

const ChartTooltipContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<typeof RechartsPrimitive.Tooltip> &
    React.ComponentProps<"div"> & {
      hideLabel?: boolean;
      hideIndicator?: boolean;
      indicator?: "line" | "dot" | "dashed";
      nameKey?: string;
      labelKey?: string;
    }
>(
  (
    {
      active,
      payload,
      className,
      indicator = "dot",
      hideLabel = false,
      hideIndicator = false,
      label,
      labelFormatter,
      labelClassName,
      formatter,
      color,
      nameKey,
      labelKey,
    },
    ref,
  ) => {
    const { config } = useChart();

    const tooltipLabel = React.useMemo(() => {
      if (hideLabel || !payload?.length) {
        return null;
      }

      const [item] = payload;
      const key = `${labelKey || item.dataKey || item.name || "value"}`;
      const itemConfig = getPayloadConfigFromPayload(config, item, key);
      const value =
        !labelKey && typeof label === "string"
          ? config[label as keyof typeof config]?.label || label
          : itemConfig?.label;

      if (labelFormatter) {
        return <div className={cn("font-medium", labelClassName)}>{labelFormatter(value, payload)}</div>;
      }

      if (!value) {
        return null;
      }

      return <div className={cn("font-medium", labelClassName)}>{value}</div>;
    }, [label, labelFormatter, payload, hideLabel, labelClassName, config, labelKey]);

    if (!active || !payload?.length) {
      return null;
    }

    const nestLabel = payload.length === 1 && indicator !== "dot";

    return (
      <div
        ref={ref}
        className={cn(
          "grid min-w-[8rem] items-start gap-1.5 rounded-lg border border-border/50 bg-background px-2.5 py-1.5 text-xs shadow-xl",
          className,
        )}
      >
        {!nestLabel ? tooltipLabel : null}
        <div className="grid gap-1.5">
          {payload.map((item, index) => {
            const key = `${nameKey || item.name || item.dataKey || "value"}`;
            const itemConfig = getPayloadConfigFromPayload(config, item, key);
            const indicatorColor = color || item.payload.fill || item.color;

            return (
              <div
                key={item.dataKey}
                className={cn(
                  "flex w-full flex-wrap items-stretch gap-2 [&>svg]:h-2.5 [&>svg]:w-2.5 [&>svg]:text-muted-foreground",
                  indicator === "dot" && "items-center",
                )}
              >
                {formatter && item?.value !== undefined && item.name ? (
                  formatter(item.value, item.name, item, index, item.payload)
                ) : (
                  <>
                    {itemConfig?.icon ? (
                      <itemConfig.icon />
                    ) : (
                      !hideIndicator && (
                        <div
                          className={cn("shrink-0 rounded-[2px] border-[--color-border] bg-[--color-bg]", {
                            "h-2.5 w-2.5": indicator === "dot",
                            "w-1": indicator === "line",
                            "w-0 border-[1.5px] border-dashed bg-transparent": indicator === "dashed",
                            "my-0.5": nestLabel && indicator === "dashed",
                          })}
                          style={
                            {
                              "--color-bg": indicatorColor,
                              "--color-border": indicatorColor,
                            } as React.CSSProperties
                          }
                        />
                      )
                    )}
                    <div
                      className={cn(
                        "flex flex-1 justify-between leading-none",
                        nestLabel ? "items-end" : "items-center",
                      )}
                    >
                      <div className="grid gap-1.5">
                        {nestLabel ? tooltipLabel : null}
                        <span className="text-muted-foreground">{itemConfig?.label || item.name}</span>
                      </div>
                      {item.value && (
                        <span className="font-mono font-medium tabular-nums text-foreground">
                          {item.value.toLocaleString()}
                        </span>
                      )}
                    </div>
                  </>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  },
);
ChartTooltipContent.displayName = "ChartTooltip";

const ChartLegend = RechartsPrimitive.Legend;

const ChartLegendContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div"> &
    Pick<RechartsPrimitive.LegendProps, "payload" | "verticalAlign"> & {
      hideIcon?: boolean;
      nameKey?: string;
    }
>(({ className, hideIcon = false, payload, verticalAlign = "bottom", nameKey }, ref) => {
  const { config } = useChart();

  if (!payload?.length) {
    return null;
  }

  return (
    <div
      ref={ref}
      className={cn("flex items-center justify-center gap-4", verticalAlign === "top" ? "pb-3" : "pt-3", className)}
    >
      {payload.map((item) => {
        const key = `${nameKey || item.dataKey || "value"}`;
        const itemConfig = getPayloadConfigFromPayload(config, item, key);

        return (
          <div
            key={item.value}
            className={cn("flex items-center gap-1.5 [&>svg]:h-3 [&>svg]:w-3 [&>svg]:text-muted-foreground")}
          >
            {itemConfig?.icon && !hideIcon ? (
              <itemConfig.icon />
            ) : (
              <div
                className="h-2 w-2 shrink-0 rounded-[2px]"
                style={{
                  backgroundColor: item.color,
                }}
              />
            )}
            {itemConfig?.label}
          </div>
        );
      })}
    </div>
  );
});
ChartLegendContent.displayName = "ChartLegend";

// Helper to extract item config from a payload.
function getPayloadConfigFromPayload(config: ChartConfig, payload: unknown, key: string) {
  if (typeof payload !== "object" || payload === null) {
    return undefined;
  }

  const payloadPayload =
    "payload" in payload && typeof payload.payload === "object" && payload.payload !== null
      ? payload.payload
      : undefined;

  let configLabelKey: string = key;

  if (key in payload && typeof payload[key as keyof typeof payload] === "string") {
    configLabelKey = payload[key as keyof typeof payload] as string;
  } else if (
    payloadPayload &&
    key in payloadPayload &&
    typeof payloadPayload[key as keyof typeof payloadPayload] === "string"
  ) {
    configLabelKey = payloadPayload[key as keyof typeof payloadPayload] as string;
  }

  return configLabelKey in config ? config[configLabelKey] : config[key as keyof typeof config];
}

export { ChartContainer, ChartTooltip, ChartTooltipContent, ChartLegend, ChartLegendContent, ChartStyle };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\checkbox.tsx`

```tsx
import * as React from "react";
import * as CheckboxPrimitive from "@radix-ui/react-checkbox";
import { Check } from "lucide-react";

import { cn } from "@/lib/utils";

const Checkbox = React.forwardRef<
  React.ElementRef<typeof CheckboxPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof CheckboxPrimitive.Root>
>(({ className, ...props }, ref) => (
  <CheckboxPrimitive.Root
    ref={ref}
    className={cn(
      "peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
      className,
    )}
    {...props}
  >
    <CheckboxPrimitive.Indicator className={cn("flex items-center justify-center text-current")}>
      <Check className="h-4 w-4" />
    </CheckboxPrimitive.Indicator>
  </CheckboxPrimitive.Root>
));
Checkbox.displayName = CheckboxPrimitive.Root.displayName;

export { Checkbox };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\collapsible.tsx`

```tsx
import * as CollapsiblePrimitive from "@radix-ui/react-collapsible";

const Collapsible = CollapsiblePrimitive.Root;

const CollapsibleTrigger = CollapsiblePrimitive.CollapsibleTrigger;

const CollapsibleContent = CollapsiblePrimitive.CollapsibleContent;

export { Collapsible, CollapsibleTrigger, CollapsibleContent };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\command.tsx`

```tsx
import * as React from "react";
import { type DialogProps } from "@radix-ui/react-dialog";
import { Command as CommandPrimitive } from "cmdk";
import { Search } from "lucide-react";

import { cn } from "@/lib/utils";
import { Dialog, DialogContent } from "@/components/ui/dialog";

const Command = React.forwardRef<
  React.ElementRef<typeof CommandPrimitive>,
  React.ComponentPropsWithoutRef<typeof CommandPrimitive>
>(({ className, ...props }, ref) => (
  <CommandPrimitive
    ref={ref}
    className={cn(
      "flex h-full w-full flex-col overflow-hidden rounded-md bg-popover text-popover-foreground",
      className,
    )}
    {...props}
  />
));
Command.displayName = CommandPrimitive.displayName;

interface CommandDialogProps extends DialogProps {}

const CommandDialog = ({ children, ...props }: CommandDialogProps) => {
  return (
    <Dialog {...props}>
      <DialogContent className="overflow-hidden p-0 shadow-lg">
        <Command className="[&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:font-medium [&_[cmdk-group-heading]]:text-muted-foreground [&_[cmdk-group]:not([hidden])_~[cmdk-group]]:pt-0 [&_[cmdk-group]]:px-2 [&_[cmdk-input-wrapper]_svg]:h-5 [&_[cmdk-input-wrapper]_svg]:w-5 [&_[cmdk-input]]:h-12 [&_[cmdk-item]]:px-2 [&_[cmdk-item]]:py-3 [&_[cmdk-item]_svg]:h-5 [&_[cmdk-item]_svg]:w-5">
          {children}
        </Command>
      </DialogContent>
    </Dialog>
  );
};

const CommandInput = React.forwardRef<
  React.ElementRef<typeof CommandPrimitive.Input>,
  React.ComponentPropsWithoutRef<typeof CommandPrimitive.Input>
>(({ className, ...props }, ref) => (
  <div className="flex items-center border-b px-3" cmdk-input-wrapper="">
    <Search className="mr-2 h-4 w-4 shrink-0 opacity-50" />
    <CommandPrimitive.Input
      ref={ref}
      className={cn(
        "flex h-11 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    />
  </div>
));

CommandInput.displayName = CommandPrimitive.Input.displayName;

const CommandList = React.forwardRef<
  React.ElementRef<typeof CommandPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof CommandPrimitive.List>
>(({ className, ...props }, ref) => (
  <CommandPrimitive.List
    ref={ref}
    className={cn("max-h-[300px] overflow-y-auto overflow-x-hidden", className)}
    {...props}
  />
));

CommandList.displayName = CommandPrimitive.List.displayName;

const CommandEmpty = React.forwardRef<
  React.ElementRef<typeof CommandPrimitive.Empty>,
  React.ComponentPropsWithoutRef<typeof CommandPrimitive.Empty>
>((props, ref) => <CommandPrimitive.Empty ref={ref} className="py-6 text-center text-sm" {...props} />);

CommandEmpty.displayName = CommandPrimitive.Empty.displayName;

const CommandGroup = React.forwardRef<
  React.ElementRef<typeof CommandPrimitive.Group>,
  React.ComponentPropsWithoutRef<typeof CommandPrimitive.Group>
>(({ className, ...props }, ref) => (
  <CommandPrimitive.Group
    ref={ref}
    className={cn(
      "overflow-hidden p-1 text-foreground [&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:py-1.5 [&_[cmdk-group-heading]]:text-xs [&_[cmdk-group-heading]]:font-medium [&_[cmdk-group-heading]]:text-muted-foreground",
      className,
    )}
    {...props}
  />
));

CommandGroup.displayName = CommandPrimitive.Group.displayName;

const CommandSeparator = React.forwardRef<
  React.ElementRef<typeof CommandPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof CommandPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <CommandPrimitive.Separator ref={ref} className={cn("-mx-1 h-px bg-border", className)} {...props} />
));
CommandSeparator.displayName = CommandPrimitive.Separator.displayName;

const CommandItem = React.forwardRef<
  React.ElementRef<typeof CommandPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof CommandPrimitive.Item>
>(({ className, ...props }, ref) => (
  <CommandPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none data-[disabled=true]:pointer-events-none data-[selected='true']:bg-accent data-[selected=true]:text-accent-foreground data-[disabled=true]:opacity-50",
      className,
    )}
    {...props}
  />
));

CommandItem.displayName = CommandPrimitive.Item.displayName;

const CommandShortcut = ({ className, ...props }: React.HTMLAttributes<HTMLSpanElement>) => {
  return <span className={cn("ml-auto text-xs tracking-widest text-muted-foreground", className)} {...props} />;
};
CommandShortcut.displayName = "CommandShortcut";

export {
  Command,
  CommandDialog,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandShortcut,
  CommandSeparator,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\context-menu.tsx`

```tsx
import * as React from "react";
import * as ContextMenuPrimitive from "@radix-ui/react-context-menu";
import { Check, ChevronRight, Circle } from "lucide-react";

import { cn } from "@/lib/utils";

const ContextMenu = ContextMenuPrimitive.Root;

const ContextMenuTrigger = ContextMenuPrimitive.Trigger;

const ContextMenuGroup = ContextMenuPrimitive.Group;

const ContextMenuPortal = ContextMenuPrimitive.Portal;

const ContextMenuSub = ContextMenuPrimitive.Sub;

const ContextMenuRadioGroup = ContextMenuPrimitive.RadioGroup;

const ContextMenuSubTrigger = React.forwardRef<
  React.ElementRef<typeof ContextMenuPrimitive.SubTrigger>,
  React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.SubTrigger> & {
    inset?: boolean;
  }
>(({ className, inset, children, ...props }, ref) => (
  <ContextMenuPrimitive.SubTrigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none data-[state=open]:bg-accent data-[state=open]:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
      inset && "pl-8",
      className,
    )}
    {...props}
  >
    {children}
    <ChevronRight className="ml-auto h-4 w-4" />
  </ContextMenuPrimitive.SubTrigger>
));
ContextMenuSubTrigger.displayName = ContextMenuPrimitive.SubTrigger.displayName;

const ContextMenuSubContent = React.forwardRef<
  React.ElementRef<typeof ContextMenuPrimitive.SubContent>,
  React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.SubContent>
>(({ className, ...props }, ref) => (
  <ContextMenuPrimitive.SubContent
    ref={ref}
    className={cn(
      "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
      className,
    )}
    {...props}
  />
));
ContextMenuSubContent.displayName = ContextMenuPrimitive.SubContent.displayName;

const ContextMenuContent = React.forwardRef<
  React.ElementRef<typeof ContextMenuPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.Content>
>(({ className, ...props }, ref) => (
  <ContextMenuPrimitive.Portal>
    <ContextMenuPrimitive.Content
      ref={ref}
      className={cn(
        "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md animate-in fade-in-80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
        className,
      )}
      {...props}
    />
  </ContextMenuPrimitive.Portal>
));
ContextMenuContent.displayName = ContextMenuPrimitive.Content.displayName;

const ContextMenuItem = React.forwardRef<
  React.ElementRef<typeof ContextMenuPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.Item> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <ContextMenuPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      inset && "pl-8",
      className,
    )}
    {...props}
  />
));
ContextMenuItem.displayName = ContextMenuPrimitive.Item.displayName;

const ContextMenuCheckboxItem = React.forwardRef<
  React.ElementRef<typeof ContextMenuPrimitive.CheckboxItem>,
  React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.CheckboxItem>
>(({ className, children, checked, ...props }, ref) => (
  <ContextMenuPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      className,
    )}
    checked={checked}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <ContextMenuPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </ContextMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </ContextMenuPrimitive.CheckboxItem>
));
ContextMenuCheckboxItem.displayName = ContextMenuPrimitive.CheckboxItem.displayName;

const ContextMenuRadioItem = React.forwardRef<
  React.ElementRef<typeof ContextMenuPrimitive.RadioItem>,
  React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.RadioItem>
>(({ className, children, ...props }, ref) => (
  <ContextMenuPrimitive.RadioItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      className,
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <ContextMenuPrimitive.ItemIndicator>
        <Circle className="h-2 w-2 fill-current" />
      </ContextMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </ContextMenuPrimitive.RadioItem>
));
ContextMenuRadioItem.displayName = ContextMenuPrimitive.RadioItem.displayName;

const ContextMenuLabel = React.forwardRef<
  React.ElementRef<typeof ContextMenuPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.Label> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <ContextMenuPrimitive.Label
    ref={ref}
    className={cn("px-2 py-1.5 text-sm font-semibold text-foreground", inset && "pl-8", className)}
    {...props}
  />
));
ContextMenuLabel.displayName = ContextMenuPrimitive.Label.displayName;

const ContextMenuSeparator = React.forwardRef<
  React.ElementRef<typeof ContextMenuPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <ContextMenuPrimitive.Separator ref={ref} className={cn("-mx-1 my-1 h-px bg-border", className)} {...props} />
));
ContextMenuSeparator.displayName = ContextMenuPrimitive.Separator.displayName;

const ContextMenuShortcut = ({ className, ...props }: React.HTMLAttributes<HTMLSpanElement>) => {
  return <span className={cn("ml-auto text-xs tracking-widest text-muted-foreground", className)} {...props} />;
};
ContextMenuShortcut.displayName = "ContextMenuShortcut";

export {
  ContextMenu,
  ContextMenuTrigger,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuCheckboxItem,
  ContextMenuRadioItem,
  ContextMenuLabel,
  ContextMenuSeparator,
  ContextMenuShortcut,
  ContextMenuGroup,
  ContextMenuPortal,
  ContextMenuSub,
  ContextMenuSubContent,
  ContextMenuSubTrigger,
  ContextMenuRadioGroup,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\dialog.tsx`

```tsx
import * as React from "react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { X } from "lucide-react";

import { cn } from "@/lib/utils";

const Dialog = DialogPrimitive.Root;

const DialogTrigger = DialogPrimitive.Trigger;

const DialogPortal = DialogPrimitive.Portal;

const DialogClose = DialogPrimitive.Close;

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className,
    )}
    {...props}
  />
));
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName;

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
        className,
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity data-[state=open]:bg-accent data-[state=open]:text-muted-foreground hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
));
DialogContent.displayName = DialogPrimitive.Content.displayName;

const DialogHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col space-y-1.5 text-center sm:text-left", className)} {...props} />
);
DialogHeader.displayName = "DialogHeader";

const DialogFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2", className)} {...props} />
);
DialogFooter.displayName = "DialogFooter";

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold leading-none tracking-tight", className)}
    {...props}
  />
));
DialogTitle.displayName = DialogPrimitive.Title.displayName;

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
));
DialogDescription.displayName = DialogPrimitive.Description.displayName;

export {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogClose,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\drawer.tsx`

```tsx
import * as React from "react";
import { Drawer as DrawerPrimitive } from "vaul";

import { cn } from "@/lib/utils";

const Drawer = ({ shouldScaleBackground = true, ...props }: React.ComponentProps<typeof DrawerPrimitive.Root>) => (
  <DrawerPrimitive.Root shouldScaleBackground={shouldScaleBackground} {...props} />
);
Drawer.displayName = "Drawer";

const DrawerTrigger = DrawerPrimitive.Trigger;

const DrawerPortal = DrawerPrimitive.Portal;

const DrawerClose = DrawerPrimitive.Close;

const DrawerOverlay = React.forwardRef<
  React.ElementRef<typeof DrawerPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DrawerPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DrawerPrimitive.Overlay ref={ref} className={cn("fixed inset-0 z-50 bg-black/80", className)} {...props} />
));
DrawerOverlay.displayName = DrawerPrimitive.Overlay.displayName;

const DrawerContent = React.forwardRef<
  React.ElementRef<typeof DrawerPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DrawerPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DrawerPortal>
    <DrawerOverlay />
    <DrawerPrimitive.Content
      ref={ref}
      className={cn(
        "fixed inset-x-0 bottom-0 z-50 mt-24 flex h-auto flex-col rounded-t-[10px] border bg-background",
        className,
      )}
      {...props}
    >
      <div className="mx-auto mt-4 h-2 w-[100px] rounded-full bg-muted" />
      {children}
    </DrawerPrimitive.Content>
  </DrawerPortal>
));
DrawerContent.displayName = "DrawerContent";

const DrawerHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("grid gap-1.5 p-4 text-center sm:text-left", className)} {...props} />
);
DrawerHeader.displayName = "DrawerHeader";

const DrawerFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("mt-auto flex flex-col gap-2 p-4", className)} {...props} />
);
DrawerFooter.displayName = "DrawerFooter";

const DrawerTitle = React.forwardRef<
  React.ElementRef<typeof DrawerPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DrawerPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DrawerPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold leading-none tracking-tight", className)}
    {...props}
  />
));
DrawerTitle.displayName = DrawerPrimitive.Title.displayName;

const DrawerDescription = React.forwardRef<
  React.ElementRef<typeof DrawerPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DrawerPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DrawerPrimitive.Description ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
));
DrawerDescription.displayName = DrawerPrimitive.Description.displayName;

export {
  Drawer,
  DrawerPortal,
  DrawerOverlay,
  DrawerTrigger,
  DrawerClose,
  DrawerContent,
  DrawerHeader,
  DrawerFooter,
  DrawerTitle,
  DrawerDescription,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\dropdown-menu.tsx`

```tsx
import * as React from "react";
import * as DropdownMenuPrimitive from "@radix-ui/react-dropdown-menu";
import { Check, ChevronRight, Circle } from "lucide-react";

import { cn } from "@/lib/utils";

const DropdownMenu = DropdownMenuPrimitive.Root;

const DropdownMenuTrigger = DropdownMenuPrimitive.Trigger;

const DropdownMenuGroup = DropdownMenuPrimitive.Group;

const DropdownMenuPortal = DropdownMenuPrimitive.Portal;

const DropdownMenuSub = DropdownMenuPrimitive.Sub;

const DropdownMenuRadioGroup = DropdownMenuPrimitive.RadioGroup;

const DropdownMenuSubTrigger = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.SubTrigger>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.SubTrigger> & {
    inset?: boolean;
  }
>(({ className, inset, children, ...props }, ref) => (
  <DropdownMenuPrimitive.SubTrigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none data-[state=open]:bg-accent focus:bg-accent",
      inset && "pl-8",
      className,
    )}
    {...props}
  >
    {children}
    <ChevronRight className="ml-auto h-4 w-4" />
  </DropdownMenuPrimitive.SubTrigger>
));
DropdownMenuSubTrigger.displayName = DropdownMenuPrimitive.SubTrigger.displayName;

const DropdownMenuSubContent = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.SubContent>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.SubContent>
>(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.SubContent
    ref={ref}
    className={cn(
      "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
      className,
    )}
    {...props}
  />
));
DropdownMenuSubContent.displayName = DropdownMenuPrimitive.SubContent.displayName;

const DropdownMenuContent = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <DropdownMenuPrimitive.Portal>
    <DropdownMenuPrimitive.Content
      ref={ref}
      sideOffset={sideOffset}
      className={cn(
        "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
        className,
      )}
      {...props}
    />
  </DropdownMenuPrimitive.Portal>
));
DropdownMenuContent.displayName = DropdownMenuPrimitive.Content.displayName;

const DropdownMenuItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Item> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <DropdownMenuPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      inset && "pl-8",
      className,
    )}
    {...props}
  />
));
DropdownMenuItem.displayName = DropdownMenuPrimitive.Item.displayName;

const DropdownMenuCheckboxItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.CheckboxItem>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.CheckboxItem>
>(({ className, children, checked, ...props }, ref) => (
  <DropdownMenuPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      className,
    )}
    checked={checked}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <DropdownMenuPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </DropdownMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </DropdownMenuPrimitive.CheckboxItem>
));
DropdownMenuCheckboxItem.displayName = DropdownMenuPrimitive.CheckboxItem.displayName;

const DropdownMenuRadioItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.RadioItem>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.RadioItem>
>(({ className, children, ...props }, ref) => (
  <DropdownMenuPrimitive.RadioItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      className,
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <DropdownMenuPrimitive.ItemIndicator>
        <Circle className="h-2 w-2 fill-current" />
      </DropdownMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </DropdownMenuPrimitive.RadioItem>
));
DropdownMenuRadioItem.displayName = DropdownMenuPrimitive.RadioItem.displayName;

const DropdownMenuLabel = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Label> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <DropdownMenuPrimitive.Label
    ref={ref}
    className={cn("px-2 py-1.5 text-sm font-semibold", inset && "pl-8", className)}
    {...props}
  />
));
DropdownMenuLabel.displayName = DropdownMenuPrimitive.Label.displayName;

const DropdownMenuSeparator = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.Separator ref={ref} className={cn("-mx-1 my-1 h-px bg-muted", className)} {...props} />
));
DropdownMenuSeparator.displayName = DropdownMenuPrimitive.Separator.displayName;

const DropdownMenuShortcut = ({ className, ...props }: React.HTMLAttributes<HTMLSpanElement>) => {
  return <span className={cn("ml-auto text-xs tracking-widest opacity-60", className)} {...props} />;
};
DropdownMenuShortcut.displayName = "DropdownMenuShortcut";

export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuCheckboxItem,
  DropdownMenuRadioItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuGroup,
  DropdownMenuPortal,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuRadioGroup,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\form.tsx`

```tsx
import * as React from "react";
import * as LabelPrimitive from "@radix-ui/react-label";
import { Slot } from "@radix-ui/react-slot";
import { Controller, ControllerProps, FieldPath, FieldValues, FormProvider, useFormContext } from "react-hook-form";

import { cn } from "@/lib/utils";
import { Label } from "@/components/ui/label";

const Form = FormProvider;

type FormFieldContextValue<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
> = {
  name: TName;
};

const FormFieldContext = React.createContext<FormFieldContextValue>({} as FormFieldContextValue);

const FormField = <
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
>({
  ...props
}: ControllerProps<TFieldValues, TName>) => {
  return (
    <FormFieldContext.Provider value={{ name: props.name }}>
      <Controller {...props} />
    </FormFieldContext.Provider>
  );
};

const useFormField = () => {
  const fieldContext = React.useContext(FormFieldContext);
  const itemContext = React.useContext(FormItemContext);
  const { getFieldState, formState } = useFormContext();

  const fieldState = getFieldState(fieldContext.name, formState);

  if (!fieldContext) {
    throw new Error("useFormField should be used within <FormField>");
  }

  const { id } = itemContext;

  return {
    id,
    name: fieldContext.name,
    formItemId: `${id}-form-item`,
    formDescriptionId: `${id}-form-item-description`,
    formMessageId: `${id}-form-item-message`,
    ...fieldState,
  };
};

type FormItemContextValue = {
  id: string;
};

const FormItemContext = React.createContext<FormItemContextValue>({} as FormItemContextValue);

const FormItem = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => {
    const id = React.useId();

    return (
      <FormItemContext.Provider value={{ id }}>
        <div ref={ref} className={cn("space-y-2", className)} {...props} />
      </FormItemContext.Provider>
    );
  },
);
FormItem.displayName = "FormItem";

const FormLabel = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root>
>(({ className, ...props }, ref) => {
  const { error, formItemId } = useFormField();

  return <Label ref={ref} className={cn(error && "text-destructive", className)} htmlFor={formItemId} {...props} />;
});
FormLabel.displayName = "FormLabel";

const FormControl = React.forwardRef<React.ElementRef<typeof Slot>, React.ComponentPropsWithoutRef<typeof Slot>>(
  ({ ...props }, ref) => {
    const { error, formItemId, formDescriptionId, formMessageId } = useFormField();

    return (
      <Slot
        ref={ref}
        id={formItemId}
        aria-describedby={!error ? `${formDescriptionId}` : `${formDescriptionId} ${formMessageId}`}
        aria-invalid={!!error}
        {...props}
      />
    );
  },
);
FormControl.displayName = "FormControl";

const FormDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => {
    const { formDescriptionId } = useFormField();

    return <p ref={ref} id={formDescriptionId} className={cn("text-sm text-muted-foreground", className)} {...props} />;
  },
);
FormDescription.displayName = "FormDescription";

const FormMessage = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, children, ...props }, ref) => {
    const { error, formMessageId } = useFormField();
    const body = error ? String(error?.message) : children;

    if (!body) {
      return null;
    }

    return (
      <p ref={ref} id={formMessageId} className={cn("text-sm font-medium text-destructive", className)} {...props}>
        {body}
      </p>
    );
  },
);
FormMessage.displayName = "FormMessage";

export { useFormField, Form, FormItem, FormLabel, FormControl, FormDescription, FormMessage, FormField };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\hover-card.tsx`

```tsx
import * as React from "react";
import * as HoverCardPrimitive from "@radix-ui/react-hover-card";

import { cn } from "@/lib/utils";

const HoverCard = HoverCardPrimitive.Root;

const HoverCardTrigger = HoverCardPrimitive.Trigger;

const HoverCardContent = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Content>
>(({ className, align = "center", sideOffset = 4, ...props }, ref) => (
  <HoverCardPrimitive.Content
    ref={ref}
    align={align}
    sideOffset={sideOffset}
    className={cn(
      "z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
      className,
    )}
    {...props}
  />
));
HoverCardContent.displayName = HoverCardPrimitive.Content.displayName;

export { HoverCard, HoverCardTrigger, HoverCardContent };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\input-otp.tsx`

```tsx
import * as React from "react";
import { OTPInput, OTPInputContext } from "input-otp";
import { Dot } from "lucide-react";

import { cn } from "@/lib/utils";

const InputOTP = React.forwardRef<React.ElementRef<typeof OTPInput>, React.ComponentPropsWithoutRef<typeof OTPInput>>(
  ({ className, containerClassName, ...props }, ref) => (
    <OTPInput
      ref={ref}
      containerClassName={cn("flex items-center gap-2 has-[:disabled]:opacity-50", containerClassName)}
      className={cn("disabled:cursor-not-allowed", className)}
      {...props}
    />
  ),
);
InputOTP.displayName = "InputOTP";

const InputOTPGroup = React.forwardRef<React.ElementRef<"div">, React.ComponentPropsWithoutRef<"div">>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("flex items-center", className)} {...props} />,
);
InputOTPGroup.displayName = "InputOTPGroup";

const InputOTPSlot = React.forwardRef<
  React.ElementRef<"div">,
  React.ComponentPropsWithoutRef<"div"> & { index: number }
>(({ index, className, ...props }, ref) => {
  const inputOTPContext = React.useContext(OTPInputContext);
  const { char, hasFakeCaret, isActive } = inputOTPContext.slots[index];

  return (
    <div
      ref={ref}
      className={cn(
        "relative flex h-10 w-10 items-center justify-center border-y border-r border-input text-sm transition-all first:rounded-l-md first:border-l last:rounded-r-md",
        isActive && "z-10 ring-2 ring-ring ring-offset-background",
        className,
      )}
      {...props}
    >
      {char}
      {hasFakeCaret && (
        <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
          <div className="animate-caret-blink h-4 w-px bg-foreground duration-1000" />
        </div>
      )}
    </div>
  );
});
InputOTPSlot.displayName = "InputOTPSlot";

const InputOTPSeparator = React.forwardRef<React.ElementRef<"div">, React.ComponentPropsWithoutRef<"div">>(
  ({ ...props }, ref) => (
    <div ref={ref} role="separator" {...props}>
      <Dot />
    </div>
  ),
);
InputOTPSeparator.displayName = "InputOTPSeparator";

export { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\input.tsx`

```tsx
import * as React from "react";

import { cn } from "@/lib/utils";

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Input.displayName = "Input";

export { Input };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\label.tsx`

```tsx
import * as React from "react";
import * as LabelPrimitive from "@radix-ui/react-label";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const labelVariants = cva("text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70");

const Label = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root> & VariantProps<typeof labelVariants>
>(({ className, ...props }, ref) => (
  <LabelPrimitive.Root ref={ref} className={cn(labelVariants(), className)} {...props} />
));
Label.displayName = LabelPrimitive.Root.displayName;

export { Label };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\menubar.tsx`

```tsx
import * as React from "react";
import * as MenubarPrimitive from "@radix-ui/react-menubar";
import { Check, ChevronRight, Circle } from "lucide-react";

import { cn } from "@/lib/utils";

const MenubarMenu = MenubarPrimitive.Menu;

const MenubarGroup = MenubarPrimitive.Group;

const MenubarPortal = MenubarPrimitive.Portal;

const MenubarSub = MenubarPrimitive.Sub;

const MenubarRadioGroup = MenubarPrimitive.RadioGroup;

const Menubar = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.Root
    ref={ref}
    className={cn("flex h-10 items-center space-x-1 rounded-md border bg-background p-1", className)}
    {...props}
  />
));
Menubar.displayName = MenubarPrimitive.Root.displayName;

const MenubarTrigger = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-3 py-1.5 text-sm font-medium outline-none data-[state=open]:bg-accent data-[state=open]:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
      className,
    )}
    {...props}
  />
));
MenubarTrigger.displayName = MenubarPrimitive.Trigger.displayName;

const MenubarSubTrigger = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.SubTrigger>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.SubTrigger> & {
    inset?: boolean;
  }
>(({ className, inset, children, ...props }, ref) => (
  <MenubarPrimitive.SubTrigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none data-[state=open]:bg-accent data-[state=open]:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
      inset && "pl-8",
      className,
    )}
    {...props}
  >
    {children}
    <ChevronRight className="ml-auto h-4 w-4" />
  </MenubarPrimitive.SubTrigger>
));
MenubarSubTrigger.displayName = MenubarPrimitive.SubTrigger.displayName;

const MenubarSubContent = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.SubContent>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.SubContent>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.SubContent
    ref={ref}
    className={cn(
      "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
      className,
    )}
    {...props}
  />
));
MenubarSubContent.displayName = MenubarPrimitive.SubContent.displayName;

const MenubarContent = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Content>
>(({ className, align = "start", alignOffset = -4, sideOffset = 8, ...props }, ref) => (
  <MenubarPrimitive.Portal>
    <MenubarPrimitive.Content
      ref={ref}
      align={align}
      alignOffset={alignOffset}
      sideOffset={sideOffset}
      className={cn(
        "z-50 min-w-[12rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
        className,
      )}
      {...props}
    />
  </MenubarPrimitive.Portal>
));
MenubarContent.displayName = MenubarPrimitive.Content.displayName;

const MenubarItem = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Item> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <MenubarPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      inset && "pl-8",
      className,
    )}
    {...props}
  />
));
MenubarItem.displayName = MenubarPrimitive.Item.displayName;

const MenubarCheckboxItem = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.CheckboxItem>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.CheckboxItem>
>(({ className, children, checked, ...props }, ref) => (
  <MenubarPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      className,
    )}
    checked={checked}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <MenubarPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </MenubarPrimitive.ItemIndicator>
    </span>
    {children}
  </MenubarPrimitive.CheckboxItem>
));
MenubarCheckboxItem.displayName = MenubarPrimitive.CheckboxItem.displayName;

const MenubarRadioItem = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.RadioItem>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.RadioItem>
>(({ className, children, ...props }, ref) => (
  <MenubarPrimitive.RadioItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      className,
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <MenubarPrimitive.ItemIndicator>
        <Circle className="h-2 w-2 fill-current" />
      </MenubarPrimitive.ItemIndicator>
    </span>
    {children}
  </MenubarPrimitive.RadioItem>
));
MenubarRadioItem.displayName = MenubarPrimitive.RadioItem.displayName;

const MenubarLabel = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Label> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <MenubarPrimitive.Label
    ref={ref}
    className={cn("px-2 py-1.5 text-sm font-semibold", inset && "pl-8", className)}
    {...props}
  />
));
MenubarLabel.displayName = MenubarPrimitive.Label.displayName;

const MenubarSeparator = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.Separator ref={ref} className={cn("-mx-1 my-1 h-px bg-muted", className)} {...props} />
));
MenubarSeparator.displayName = MenubarPrimitive.Separator.displayName;

const MenubarShortcut = ({ className, ...props }: React.HTMLAttributes<HTMLSpanElement>) => {
  return <span className={cn("ml-auto text-xs tracking-widest text-muted-foreground", className)} {...props} />;
};
MenubarShortcut.displayname = "MenubarShortcut";

export {
  Menubar,
  MenubarMenu,
  MenubarTrigger,
  MenubarContent,
  MenubarItem,
  MenubarSeparator,
  MenubarLabel,
  MenubarCheckboxItem,
  MenubarRadioGroup,
  MenubarRadioItem,
  MenubarPortal,
  MenubarSubContent,
  MenubarSubTrigger,
  MenubarGroup,
  MenubarSub,
  MenubarShortcut,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\navigation-menu.tsx`

```tsx
import * as React from "react";
import * as NavigationMenuPrimitive from "@radix-ui/react-navigation-menu";
import { cva } from "class-variance-authority";
import { ChevronDown } from "lucide-react";

import { cn } from "@/lib/utils";

const NavigationMenu = React.forwardRef<
  React.ElementRef<typeof NavigationMenuPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof NavigationMenuPrimitive.Root>
>(({ className, children, ...props }, ref) => (
  <NavigationMenuPrimitive.Root
    ref={ref}
    className={cn("relative z-10 flex max-w-max flex-1 items-center justify-center", className)}
    {...props}
  >
    {children}
    <NavigationMenuViewport />
  </NavigationMenuPrimitive.Root>
));
NavigationMenu.displayName = NavigationMenuPrimitive.Root.displayName;

const NavigationMenuList = React.forwardRef<
  React.ElementRef<typeof NavigationMenuPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof NavigationMenuPrimitive.List>
>(({ className, ...props }, ref) => (
  <NavigationMenuPrimitive.List
    ref={ref}
    className={cn("group flex flex-1 list-none items-center justify-center space-x-1", className)}
    {...props}
  />
));
NavigationMenuList.displayName = NavigationMenuPrimitive.List.displayName;

const NavigationMenuItem = NavigationMenuPrimitive.Item;

const navigationMenuTriggerStyle = cva(
  "group inline-flex h-10 w-max items-center justify-center rounded-md bg-background px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none disabled:pointer-events-none disabled:opacity-50 data-[active]:bg-accent/50 data-[state=open]:bg-accent/50",
);

const NavigationMenuTrigger = React.forwardRef<
  React.ElementRef<typeof NavigationMenuPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof NavigationMenuPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <NavigationMenuPrimitive.Trigger
    ref={ref}
    className={cn(navigationMenuTriggerStyle(), "group", className)}
    {...props}
  >
    {children}{" "}
    <ChevronDown
      className="relative top-[1px] ml-1 h-3 w-3 transition duration-200 group-data-[state=open]:rotate-180"
      aria-hidden="true"
    />
  </NavigationMenuPrimitive.Trigger>
));
NavigationMenuTrigger.displayName = NavigationMenuPrimitive.Trigger.displayName;

const NavigationMenuContent = React.forwardRef<
  React.ElementRef<typeof NavigationMenuPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof NavigationMenuPrimitive.Content>
>(({ className, ...props }, ref) => (
  <NavigationMenuPrimitive.Content
    ref={ref}
    className={cn(
      "left-0 top-0 w-full data-[motion^=from-]:animate-in data-[motion^=to-]:animate-out data-[motion^=from-]:fade-in data-[motion^=to-]:fade-out data-[motion=from-end]:slide-in-from-right-52 data-[motion=from-start]:slide-in-from-left-52 data-[motion=to-end]:slide-out-to-right-52 data-[motion=to-start]:slide-out-to-left-52 md:absolute md:w-auto",
      className,
    )}
    {...props}
  />
));
NavigationMenuContent.displayName = NavigationMenuPrimitive.Content.displayName;

const NavigationMenuLink = NavigationMenuPrimitive.Link;

const NavigationMenuViewport = React.forwardRef<
  React.ElementRef<typeof NavigationMenuPrimitive.Viewport>,
  React.ComponentPropsWithoutRef<typeof NavigationMenuPrimitive.Viewport>
>(({ className, ...props }, ref) => (
  <div className={cn("absolute left-0 top-full flex justify-center")}>
    <NavigationMenuPrimitive.Viewport
      className={cn(
        "origin-top-center relative mt-1.5 h-[var(--radix-navigation-menu-viewport-height)] w-full overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-90 md:w-[var(--radix-navigation-menu-viewport-width)]",
        className,
      )}
      ref={ref}
      {...props}
    />
  </div>
));
NavigationMenuViewport.displayName = NavigationMenuPrimitive.Viewport.displayName;

const NavigationMenuIndicator = React.forwardRef<
  React.ElementRef<typeof NavigationMenuPrimitive.Indicator>,
  React.ComponentPropsWithoutRef<typeof NavigationMenuPrimitive.Indicator>
>(({ className, ...props }, ref) => (
  <NavigationMenuPrimitive.Indicator
    ref={ref}
    className={cn(
      "top-full z-[1] flex h-1.5 items-end justify-center overflow-hidden data-[state=visible]:animate-in data-[state=hidden]:animate-out data-[state=hidden]:fade-out data-[state=visible]:fade-in",
      className,
    )}
    {...props}
  >
    <div className="relative top-[60%] h-2 w-2 rotate-45 rounded-tl-sm bg-border shadow-md" />
  </NavigationMenuPrimitive.Indicator>
));
NavigationMenuIndicator.displayName = NavigationMenuPrimitive.Indicator.displayName;

export {
  navigationMenuTriggerStyle,
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuContent,
  NavigationMenuTrigger,
  NavigationMenuLink,
  NavigationMenuIndicator,
  NavigationMenuViewport,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\pagination.tsx`

```tsx
import * as React from "react";
import { ChevronLeft, ChevronRight, MoreHorizontal } from "lucide-react";

import { cn } from "@/lib/utils";
import { ButtonProps, buttonVariants } from "@/components/ui/button";

const Pagination = ({ className, ...props }: React.ComponentProps<"nav">) => (
  <nav
    role="navigation"
    aria-label="pagination"
    className={cn("mx-auto flex w-full justify-center", className)}
    {...props}
  />
);
Pagination.displayName = "Pagination";

const PaginationContent = React.forwardRef<HTMLUListElement, React.ComponentProps<"ul">>(
  ({ className, ...props }, ref) => (
    <ul ref={ref} className={cn("flex flex-row items-center gap-1", className)} {...props} />
  ),
);
PaginationContent.displayName = "PaginationContent";

const PaginationItem = React.forwardRef<HTMLLIElement, React.ComponentProps<"li">>(({ className, ...props }, ref) => (
  <li ref={ref} className={cn("", className)} {...props} />
));
PaginationItem.displayName = "PaginationItem";

type PaginationLinkProps = {
  isActive?: boolean;
} & Pick<ButtonProps, "size"> &
  React.ComponentProps<"a">;

const PaginationLink = ({ className, isActive, size = "icon", ...props }: PaginationLinkProps) => (
  <a
    aria-current={isActive ? "page" : undefined}
    className={cn(
      buttonVariants({
        variant: isActive ? "outline" : "ghost",
        size,
      }),
      className,
    )}
    {...props}
  />
);
PaginationLink.displayName = "PaginationLink";

const PaginationPrevious = ({ className, ...props }: React.ComponentProps<typeof PaginationLink>) => (
  <PaginationLink aria-label="Go to previous page" size="default" className={cn("gap-1 pl-2.5", className)} {...props}>
    <ChevronLeft className="h-4 w-4" />
    <span>Previous</span>
  </PaginationLink>
);
PaginationPrevious.displayName = "PaginationPrevious";

const PaginationNext = ({ className, ...props }: React.ComponentProps<typeof PaginationLink>) => (
  <PaginationLink aria-label="Go to next page" size="default" className={cn("gap-1 pr-2.5", className)} {...props}>
    <span>Next</span>
    <ChevronRight className="h-4 w-4" />
  </PaginationLink>
);
PaginationNext.displayName = "PaginationNext";

const PaginationEllipsis = ({ className, ...props }: React.ComponentProps<"span">) => (
  <span aria-hidden className={cn("flex h-9 w-9 items-center justify-center", className)} {...props}>
    <MoreHorizontal className="h-4 w-4" />
    <span className="sr-only">More pages</span>
  </span>
);
PaginationEllipsis.displayName = "PaginationEllipsis";

export {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\popover.tsx`

```tsx
import * as React from "react";
import * as PopoverPrimitive from "@radix-ui/react-popover";

import { cn } from "@/lib/utils";

const Popover = PopoverPrimitive.Root;

const PopoverTrigger = PopoverPrimitive.Trigger;

const PopoverContent = React.forwardRef<
  React.ElementRef<typeof PopoverPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof PopoverPrimitive.Content>
>(({ className, align = "center", sideOffset = 4, ...props }, ref) => (
  <PopoverPrimitive.Portal>
    <PopoverPrimitive.Content
      ref={ref}
      align={align}
      sideOffset={sideOffset}
      className={cn(
        "z-50 w-72 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
        className,
      )}
      {...props}
    />
  </PopoverPrimitive.Portal>
));
PopoverContent.displayName = PopoverPrimitive.Content.displayName;

export { Popover, PopoverTrigger, PopoverContent };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\progress.tsx`

```tsx
import * as React from "react";
import * as ProgressPrimitive from "@radix-ui/react-progress";

import { cn } from "@/lib/utils";

const Progress = React.forwardRef<
  React.ElementRef<typeof ProgressPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root>
>(({ className, value, ...props }, ref) => (
  <ProgressPrimitive.Root
    ref={ref}
    className={cn("relative h-4 w-full overflow-hidden rounded-full bg-secondary", className)}
    {...props}
  >
    <ProgressPrimitive.Indicator
      className="h-full w-full flex-1 bg-primary transition-all"
      style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
    />
  </ProgressPrimitive.Root>
));
Progress.displayName = ProgressPrimitive.Root.displayName;

export { Progress };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\radio-group.tsx`

```tsx
import * as React from "react";
import * as RadioGroupPrimitive from "@radix-ui/react-radio-group";
import { Circle } from "lucide-react";

import { cn } from "@/lib/utils";

const RadioGroup = React.forwardRef<
  React.ElementRef<typeof RadioGroupPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof RadioGroupPrimitive.Root>
>(({ className, ...props }, ref) => {
  return <RadioGroupPrimitive.Root className={cn("grid gap-2", className)} {...props} ref={ref} />;
});
RadioGroup.displayName = RadioGroupPrimitive.Root.displayName;

const RadioGroupItem = React.forwardRef<
  React.ElementRef<typeof RadioGroupPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof RadioGroupPrimitive.Item>
>(({ className, ...props }, ref) => {
  return (
    <RadioGroupPrimitive.Item
      ref={ref}
      className={cn(
        "aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    >
      <RadioGroupPrimitive.Indicator className="flex items-center justify-center">
        <Circle className="h-2.5 w-2.5 fill-current text-current" />
      </RadioGroupPrimitive.Indicator>
    </RadioGroupPrimitive.Item>
  );
});
RadioGroupItem.displayName = RadioGroupPrimitive.Item.displayName;

export { RadioGroup, RadioGroupItem };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\resizable.tsx`

```tsx
import { GripVertical } from "lucide-react";
import * as ResizablePrimitive from "react-resizable-panels";

import { cn } from "@/lib/utils";

const ResizablePanelGroup = ({ className, ...props }: React.ComponentProps<typeof ResizablePrimitive.PanelGroup>) => (
  <ResizablePrimitive.PanelGroup
    className={cn("flex h-full w-full data-[panel-group-direction=vertical]:flex-col", className)}
    {...props}
  />
);

const ResizablePanel = ResizablePrimitive.Panel;

const ResizableHandle = ({
  withHandle,
  className,
  ...props
}: React.ComponentProps<typeof ResizablePrimitive.PanelResizeHandle> & {
  withHandle?: boolean;
}) => (
  <ResizablePrimitive.PanelResizeHandle
    className={cn(
      "relative flex w-px items-center justify-center bg-border after:absolute after:inset-y-0 after:left-1/2 after:w-1 after:-translate-x-1/2 data-[panel-group-direction=vertical]:h-px data-[panel-group-direction=vertical]:w-full data-[panel-group-direction=vertical]:after:left-0 data-[panel-group-direction=vertical]:after:h-1 data-[panel-group-direction=vertical]:after:w-full data-[panel-group-direction=vertical]:after:-translate-y-1/2 data-[panel-group-direction=vertical]:after:translate-x-0 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:ring-offset-1 [&[data-panel-group-direction=vertical]>div]:rotate-90",
      className,
    )}
    {...props}
  >
    {withHandle && (
      <div className="z-10 flex h-4 w-3 items-center justify-center rounded-sm border bg-border">
        <GripVertical className="h-2.5 w-2.5" />
      </div>
    )}
  </ResizablePrimitive.PanelResizeHandle>
);

export { ResizablePanelGroup, ResizablePanel, ResizableHandle };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\scroll-area.tsx`

```tsx
import * as React from "react";
import * as ScrollAreaPrimitive from "@radix-ui/react-scroll-area";

import { cn } from "@/lib/utils";

const ScrollArea = React.forwardRef<
  React.ElementRef<typeof ScrollAreaPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof ScrollAreaPrimitive.Root>
>(({ className, children, ...props }, ref) => (
  <ScrollAreaPrimitive.Root ref={ref} className={cn("relative overflow-hidden", className)} {...props}>
    <ScrollAreaPrimitive.Viewport className="h-full w-full rounded-[inherit]">{children}</ScrollAreaPrimitive.Viewport>
    <ScrollBar />
    <ScrollAreaPrimitive.Corner />
  </ScrollAreaPrimitive.Root>
));
ScrollArea.displayName = ScrollAreaPrimitive.Root.displayName;

const ScrollBar = React.forwardRef<
  React.ElementRef<typeof ScrollAreaPrimitive.ScrollAreaScrollbar>,
  React.ComponentPropsWithoutRef<typeof ScrollAreaPrimitive.ScrollAreaScrollbar>
>(({ className, orientation = "vertical", ...props }, ref) => (
  <ScrollAreaPrimitive.ScrollAreaScrollbar
    ref={ref}
    orientation={orientation}
    className={cn(
      "flex touch-none select-none transition-colors",
      orientation === "vertical" && "h-full w-2.5 border-l border-l-transparent p-[1px]",
      orientation === "horizontal" && "h-2.5 flex-col border-t border-t-transparent p-[1px]",
      className,
    )}
    {...props}
  >
    <ScrollAreaPrimitive.ScrollAreaThumb className="relative flex-1 rounded-full bg-border" />
  </ScrollAreaPrimitive.ScrollAreaScrollbar>
));
ScrollBar.displayName = ScrollAreaPrimitive.ScrollAreaScrollbar.displayName;

export { ScrollArea, ScrollBar };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\select.tsx`

```tsx
import * as React from "react";
import * as SelectPrimitive from "@radix-ui/react-select";
import { Check, ChevronDown, ChevronUp } from "lucide-react";

import { cn } from "@/lib/utils";

const Select = SelectPrimitive.Root;

const SelectGroup = SelectPrimitive.Group;

const SelectValue = SelectPrimitive.Value;

const SelectTrigger = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
      className,
    )}
    {...props}
  >
    {children}
    <SelectPrimitive.Icon asChild>
      <ChevronDown className="h-4 w-4 opacity-50" />
    </SelectPrimitive.Icon>
  </SelectPrimitive.Trigger>
));
SelectTrigger.displayName = SelectPrimitive.Trigger.displayName;

const SelectScrollUpButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollUpButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollUpButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollUpButton
    ref={ref}
    className={cn("flex cursor-default items-center justify-center py-1", className)}
    {...props}
  >
    <ChevronUp className="h-4 w-4" />
  </SelectPrimitive.ScrollUpButton>
));
SelectScrollUpButton.displayName = SelectPrimitive.ScrollUpButton.displayName;

const SelectScrollDownButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollDownButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollDownButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollDownButton
    ref={ref}
    className={cn("flex cursor-default items-center justify-center py-1", className)}
    {...props}
  >
    <ChevronDown className="h-4 w-4" />
  </SelectPrimitive.ScrollDownButton>
));
SelectScrollDownButton.displayName = SelectPrimitive.ScrollDownButton.displayName;

const SelectContent = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Content>
>(({ className, children, position = "popper", ...props }, ref) => (
  <SelectPrimitive.Portal>
    <SelectPrimitive.Content
      ref={ref}
      className={cn(
        "relative z-50 max-h-96 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
        position === "popper" &&
          "data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1",
        className,
      )}
      position={position}
      {...props}
    >
      <SelectScrollUpButton />
      <SelectPrimitive.Viewport
        className={cn(
          "p-1",
          position === "popper" &&
            "h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]",
        )}
      >
        {children}
      </SelectPrimitive.Viewport>
      <SelectScrollDownButton />
    </SelectPrimitive.Content>
  </SelectPrimitive.Portal>
));
SelectContent.displayName = SelectPrimitive.Content.displayName;

const SelectLabel = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Label>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Label ref={ref} className={cn("py-1.5 pl-8 pr-2 text-sm font-semibold", className)} {...props} />
));
SelectLabel.displayName = SelectPrimitive.Label.displayName;

const SelectItem = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Item>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 focus:bg-accent focus:text-accent-foreground",
      className,
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <SelectPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </SelectPrimitive.ItemIndicator>
    </span>

    <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
  </SelectPrimitive.Item>
));
SelectItem.displayName = SelectPrimitive.Item.displayName;

const SelectSeparator = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Separator ref={ref} className={cn("-mx-1 my-1 h-px bg-muted", className)} {...props} />
));
SelectSeparator.displayName = SelectPrimitive.Separator.displayName;

export {
  Select,
  SelectGroup,
  SelectValue,
  SelectTrigger,
  SelectContent,
  SelectLabel,
  SelectItem,
  SelectSeparator,
  SelectScrollUpButton,
  SelectScrollDownButton,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\separator.tsx`

```tsx
import * as React from "react";
import * as SeparatorPrimitive from "@radix-ui/react-separator";

import { cn } from "@/lib/utils";

const Separator = React.forwardRef<
  React.ElementRef<typeof SeparatorPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof SeparatorPrimitive.Root>
>(({ className, orientation = "horizontal", decorative = true, ...props }, ref) => (
  <SeparatorPrimitive.Root
    ref={ref}
    decorative={decorative}
    orientation={orientation}
    className={cn("shrink-0 bg-border", orientation === "horizontal" ? "h-[1px] w-full" : "h-full w-[1px]", className)}
    {...props}
  />
));
Separator.displayName = SeparatorPrimitive.Root.displayName;

export { Separator };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\sheet.tsx`

```tsx
import * as SheetPrimitive from "@radix-ui/react-dialog";
import { cva, type VariantProps } from "class-variance-authority";
import { X } from "lucide-react";
import * as React from "react";

import { cn } from "@/lib/utils";

const Sheet = SheetPrimitive.Root;

const SheetTrigger = SheetPrimitive.Trigger;

const SheetClose = SheetPrimitive.Close;

const SheetPortal = SheetPrimitive.Portal;

const SheetOverlay = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Overlay
    className={cn(
      "fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className,
    )}
    {...props}
    ref={ref}
  />
));
SheetOverlay.displayName = SheetPrimitive.Overlay.displayName;

const sheetVariants = cva(
  "fixed z-50 gap-4 bg-background p-6 shadow-lg transition ease-in-out data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:duration-300 data-[state=open]:duration-500",
  {
    variants: {
      side: {
        top: "inset-x-0 top-0 border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top",
        bottom:
          "inset-x-0 bottom-0 border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom",
        left: "inset-y-0 left-0 h-full w-3/4 border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left sm:max-w-sm",
        right:
          "inset-y-0 right-0 h-full w-3/4  border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right sm:max-w-sm",
      },
    },
    defaultVariants: {
      side: "right",
    },
  },
);

interface SheetContentProps
  extends React.ComponentPropsWithoutRef<typeof SheetPrimitive.Content>,
    VariantProps<typeof sheetVariants> {}

const SheetContent = React.forwardRef<React.ElementRef<typeof SheetPrimitive.Content>, SheetContentProps>(
  ({ side = "right", className, children, ...props }, ref) => (
    <SheetPortal>
      <SheetOverlay />
      <SheetPrimitive.Content ref={ref} className={cn(sheetVariants({ side }), className)} {...props}>
        {children}
        <SheetPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity data-[state=open]:bg-secondary hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none">
          <X className="h-4 w-4" />
          <span className="sr-only">Close</span>
        </SheetPrimitive.Close>
      </SheetPrimitive.Content>
    </SheetPortal>
  ),
);
SheetContent.displayName = SheetPrimitive.Content.displayName;

const SheetHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col space-y-2 text-center sm:text-left", className)} {...props} />
);
SheetHeader.displayName = "SheetHeader";

const SheetFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2", className)} {...props} />
);
SheetFooter.displayName = "SheetFooter";

const SheetTitle = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Title>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Title ref={ref} className={cn("text-lg font-semibold text-foreground", className)} {...props} />
));
SheetTitle.displayName = SheetPrimitive.Title.displayName;

const SheetDescription = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Description>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Description ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
));
SheetDescription.displayName = SheetPrimitive.Description.displayName;

export {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetOverlay,
  SheetPortal,
  SheetTitle,
  SheetTrigger,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\sidebar.tsx`

```tsx
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { VariantProps, cva } from "class-variance-authority";
import { PanelLeft } from "lucide-react";

import { useIsMobile } from "@/hooks/use-mobile";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { Skeleton } from "@/components/ui/skeleton";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

const SIDEBAR_COOKIE_NAME = "sidebar:state";
const SIDEBAR_COOKIE_MAX_AGE = 60 * 60 * 24 * 7;
const SIDEBAR_WIDTH = "16rem";
const SIDEBAR_WIDTH_MOBILE = "18rem";
const SIDEBAR_WIDTH_ICON = "3rem";
const SIDEBAR_KEYBOARD_SHORTCUT = "b";

type SidebarContext = {
  state: "expanded" | "collapsed";
  open: boolean;
  setOpen: (open: boolean) => void;
  openMobile: boolean;
  setOpenMobile: (open: boolean) => void;
  isMobile: boolean;
  toggleSidebar: () => void;
};

const SidebarContext = React.createContext<SidebarContext | null>(null);

function useSidebar() {
  const context = React.useContext(SidebarContext);
  if (!context) {
    throw new Error("useSidebar must be used within a SidebarProvider.");
  }

  return context;
}

const SidebarProvider = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div"> & {
    defaultOpen?: boolean;
    open?: boolean;
    onOpenChange?: (open: boolean) => void;
  }
>(({ defaultOpen = true, open: openProp, onOpenChange: setOpenProp, className, style, children, ...props }, ref) => {
  const isMobile = useIsMobile();
  const [openMobile, setOpenMobile] = React.useState(false);

  // This is the internal state of the sidebar.
  // We use openProp and setOpenProp for control from outside the component.
  const [_open, _setOpen] = React.useState(defaultOpen);
  const open = openProp ?? _open;
  const setOpen = React.useCallback(
    (value: boolean | ((value: boolean) => boolean)) => {
      const openState = typeof value === "function" ? value(open) : value;
      if (setOpenProp) {
        setOpenProp(openState);
      } else {
        _setOpen(openState);
      }

      // This sets the cookie to keep the sidebar state.
      document.cookie = `${SIDEBAR_COOKIE_NAME}=${openState}; path=/; max-age=${SIDEBAR_COOKIE_MAX_AGE}`;
    },
    [setOpenProp, open],
  );

  // Helper to toggle the sidebar.
  const toggleSidebar = React.useCallback(() => {
    return isMobile ? setOpenMobile((open) => !open) : setOpen((open) => !open);
  }, [isMobile, setOpen, setOpenMobile]);

  // Adds a keyboard shortcut to toggle the sidebar.
  React.useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === SIDEBAR_KEYBOARD_SHORTCUT && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        toggleSidebar();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [toggleSidebar]);

  // We add a state so that we can do data-state="expanded" or "collapsed".
  // This makes it easier to style the sidebar with Tailwind classes.
  const state = open ? "expanded" : "collapsed";

  const contextValue = React.useMemo<SidebarContext>(
    () => ({
      state,
      open,
      setOpen,
      isMobile,
      openMobile,
      setOpenMobile,
      toggleSidebar,
    }),
    [state, open, setOpen, isMobile, openMobile, setOpenMobile, toggleSidebar],
  );

  return (
    <SidebarContext.Provider value={contextValue}>
      <TooltipProvider delayDuration={0}>
        <div
          style={
            {
              "--sidebar-width": SIDEBAR_WIDTH,
              "--sidebar-width-icon": SIDEBAR_WIDTH_ICON,
              ...style,
            } as React.CSSProperties
          }
          className={cn("group/sidebar-wrapper flex min-h-svh w-full has-[[data-variant=inset]]:bg-sidebar", className)}
          ref={ref}
          {...props}
        >
          {children}
        </div>
      </TooltipProvider>
    </SidebarContext.Provider>
  );
});
SidebarProvider.displayName = "SidebarProvider";

const Sidebar = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div"> & {
    side?: "left" | "right";
    variant?: "sidebar" | "floating" | "inset";
    collapsible?: "offcanvas" | "icon" | "none";
  }
>(({ side = "left", variant = "sidebar", collapsible = "offcanvas", className, children, ...props }, ref) => {
  const { isMobile, state, openMobile, setOpenMobile } = useSidebar();

  if (collapsible === "none") {
    return (
      <div
        className={cn("flex h-full w-[--sidebar-width] flex-col bg-sidebar text-sidebar-foreground", className)}
        ref={ref}
        {...props}
      >
        {children}
      </div>
    );
  }

  if (isMobile) {
    return (
      <Sheet open={openMobile} onOpenChange={setOpenMobile} {...props}>
        <SheetContent
          data-sidebar="sidebar"
          data-mobile="true"
          className="w-[--sidebar-width] bg-sidebar p-0 text-sidebar-foreground [&>button]:hidden"
          style={
            {
              "--sidebar-width": SIDEBAR_WIDTH_MOBILE,
            } as React.CSSProperties
          }
          side={side}
        >
          <div className="flex h-full w-full flex-col">{children}</div>
        </SheetContent>
      </Sheet>
    );
  }

  return (
    <div
      ref={ref}
      className="group peer hidden text-sidebar-foreground md:block"
      data-state={state}
      data-collapsible={state === "collapsed" ? collapsible : ""}
      data-variant={variant}
      data-side={side}
    >
      {/* This is what handles the sidebar gap on desktop */}
      <div
        className={cn(
          "relative h-svh w-[--sidebar-width] bg-transparent transition-[width] duration-200 ease-linear",
          "group-data-[collapsible=offcanvas]:w-0",
          "group-data-[side=right]:rotate-180",
          variant === "floating" || variant === "inset"
            ? "group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4))]"
            : "group-data-[collapsible=icon]:w-[--sidebar-width-icon]",
        )}
      />
      <div
        className={cn(
          "fixed inset-y-0 z-10 hidden h-svh w-[--sidebar-width] transition-[left,right,width] duration-200 ease-linear md:flex",
          side === "left"
            ? "left-0 group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)]"
            : "right-0 group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)]",
          // Adjust the padding for floating and inset variants.
          variant === "floating" || variant === "inset"
            ? "p-2 group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4)_+2px)]"
            : "group-data-[collapsible=icon]:w-[--sidebar-width-icon] group-data-[side=left]:border-r group-data-[side=right]:border-l",
          className,
        )}
        {...props}
      >
        <div
          data-sidebar="sidebar"
          className="flex h-full w-full flex-col bg-sidebar group-data-[variant=floating]:rounded-lg group-data-[variant=floating]:border group-data-[variant=floating]:border-sidebar-border group-data-[variant=floating]:shadow"
        >
          {children}
        </div>
      </div>
    </div>
  );
});
Sidebar.displayName = "Sidebar";

const SidebarTrigger = React.forwardRef<React.ElementRef<typeof Button>, React.ComponentProps<typeof Button>>(
  ({ className, onClick, ...props }, ref) => {
    const { toggleSidebar } = useSidebar();

    return (
      <Button
        ref={ref}
        data-sidebar="trigger"
        variant="ghost"
        size="icon"
        className={cn("h-7 w-7", className)}
        onClick={(event) => {
          onClick?.(event);
          toggleSidebar();
        }}
        {...props}
      >
        <PanelLeft />
        <span className="sr-only">Toggle Sidebar</span>
      </Button>
    );
  },
);
SidebarTrigger.displayName = "SidebarTrigger";

const SidebarRail = React.forwardRef<HTMLButtonElement, React.ComponentProps<"button">>(
  ({ className, ...props }, ref) => {
    const { toggleSidebar } = useSidebar();

    return (
      <button
        ref={ref}
        data-sidebar="rail"
        aria-label="Toggle Sidebar"
        tabIndex={-1}
        onClick={toggleSidebar}
        title="Toggle Sidebar"
        className={cn(
          "absolute inset-y-0 z-20 hidden w-4 -translate-x-1/2 transition-all ease-linear after:absolute after:inset-y-0 after:left-1/2 after:w-[2px] group-data-[side=left]:-right-4 group-data-[side=right]:left-0 hover:after:bg-sidebar-border sm:flex",
          "[[data-side=left]_&]:cursor-w-resize [[data-side=right]_&]:cursor-e-resize",
          "[[data-side=left][data-state=collapsed]_&]:cursor-e-resize [[data-side=right][data-state=collapsed]_&]:cursor-w-resize",
          "group-data-[collapsible=offcanvas]:translate-x-0 group-data-[collapsible=offcanvas]:after:left-full group-data-[collapsible=offcanvas]:hover:bg-sidebar",
          "[[data-side=left][data-collapsible=offcanvas]_&]:-right-2",
          "[[data-side=right][data-collapsible=offcanvas]_&]:-left-2",
          className,
        )}
        {...props}
      />
    );
  },
);
SidebarRail.displayName = "SidebarRail";

const SidebarInset = React.forwardRef<HTMLDivElement, React.ComponentProps<"main">>(({ className, ...props }, ref) => {
  return (
    <main
      ref={ref}
      className={cn(
        "relative flex min-h-svh flex-1 flex-col bg-background",
        "peer-data-[variant=inset]:min-h-[calc(100svh-theme(spacing.4))] md:peer-data-[variant=inset]:m-2 md:peer-data-[state=collapsed]:peer-data-[variant=inset]:ml-2 md:peer-data-[variant=inset]:ml-0 md:peer-data-[variant=inset]:rounded-xl md:peer-data-[variant=inset]:shadow",
        className,
      )}
      {...props}
    />
  );
});
SidebarInset.displayName = "SidebarInset";

const SidebarInput = React.forwardRef<React.ElementRef<typeof Input>, React.ComponentProps<typeof Input>>(
  ({ className, ...props }, ref) => {
    return (
      <Input
        ref={ref}
        data-sidebar="input"
        className={cn(
          "h-8 w-full bg-background shadow-none focus-visible:ring-2 focus-visible:ring-sidebar-ring",
          className,
        )}
        {...props}
      />
    );
  },
);
SidebarInput.displayName = "SidebarInput";

const SidebarHeader = React.forwardRef<HTMLDivElement, React.ComponentProps<"div">>(({ className, ...props }, ref) => {
  return <div ref={ref} data-sidebar="header" className={cn("flex flex-col gap-2 p-2", className)} {...props} />;
});
SidebarHeader.displayName = "SidebarHeader";

const SidebarFooter = React.forwardRef<HTMLDivElement, React.ComponentProps<"div">>(({ className, ...props }, ref) => {
  return <div ref={ref} data-sidebar="footer" className={cn("flex flex-col gap-2 p-2", className)} {...props} />;
});
SidebarFooter.displayName = "SidebarFooter";

const SidebarSeparator = React.forwardRef<React.ElementRef<typeof Separator>, React.ComponentProps<typeof Separator>>(
  ({ className, ...props }, ref) => {
    return (
      <Separator
        ref={ref}
        data-sidebar="separator"
        className={cn("mx-2 w-auto bg-sidebar-border", className)}
        {...props}
      />
    );
  },
);
SidebarSeparator.displayName = "SidebarSeparator";

const SidebarContent = React.forwardRef<HTMLDivElement, React.ComponentProps<"div">>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      data-sidebar="content"
      className={cn(
        "flex min-h-0 flex-1 flex-col gap-2 overflow-auto group-data-[collapsible=icon]:overflow-hidden",
        className,
      )}
      {...props}
    />
  );
});
SidebarContent.displayName = "SidebarContent";

const SidebarGroup = React.forwardRef<HTMLDivElement, React.ComponentProps<"div">>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      data-sidebar="group"
      className={cn("relative flex w-full min-w-0 flex-col p-2", className)}
      {...props}
    />
  );
});
SidebarGroup.displayName = "SidebarGroup";

const SidebarGroupLabel = React.forwardRef<HTMLDivElement, React.ComponentProps<"div"> & { asChild?: boolean }>(
  ({ className, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "div";

    return (
      <Comp
        ref={ref}
        data-sidebar="group-label"
        className={cn(
          "flex h-8 shrink-0 items-center rounded-md px-2 text-xs font-medium text-sidebar-foreground/70 outline-none ring-sidebar-ring transition-[margin,opa] duration-200 ease-linear focus-visible:ring-2 [&>svg]:size-4 [&>svg]:shrink-0",
          "group-data-[collapsible=icon]:-mt-8 group-data-[collapsible=icon]:opacity-0",
          className,
        )}
        {...props}
      />
    );
  },
);
SidebarGroupLabel.displayName = "SidebarGroupLabel";

const SidebarGroupAction = React.forwardRef<HTMLButtonElement, React.ComponentProps<"button"> & { asChild?: boolean }>(
  ({ className, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";

    return (
      <Comp
        ref={ref}
        data-sidebar="group-action"
        className={cn(
          "absolute right-3 top-3.5 flex aspect-square w-5 items-center justify-center rounded-md p-0 text-sidebar-foreground outline-none ring-sidebar-ring transition-transform hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 [&>svg]:size-4 [&>svg]:shrink-0",
          // Increases the hit area of the button on mobile.
          "after:absolute after:-inset-2 after:md:hidden",
          "group-data-[collapsible=icon]:hidden",
          className,
        )}
        {...props}
      />
    );
  },
);
SidebarGroupAction.displayName = "SidebarGroupAction";

const SidebarGroupContent = React.forwardRef<HTMLDivElement, React.ComponentProps<"div">>(
  ({ className, ...props }, ref) => (
    <div ref={ref} data-sidebar="group-content" className={cn("w-full text-sm", className)} {...props} />
  ),
);
SidebarGroupContent.displayName = "SidebarGroupContent";

const SidebarMenu = React.forwardRef<HTMLUListElement, React.ComponentProps<"ul">>(({ className, ...props }, ref) => (
  <ul ref={ref} data-sidebar="menu" className={cn("flex w-full min-w-0 flex-col gap-1", className)} {...props} />
));
SidebarMenu.displayName = "SidebarMenu";

const SidebarMenuItem = React.forwardRef<HTMLLIElement, React.ComponentProps<"li">>(({ className, ...props }, ref) => (
  <li ref={ref} data-sidebar="menu-item" className={cn("group/menu-item relative", className)} {...props} />
));
SidebarMenuItem.displayName = "SidebarMenuItem";

const sidebarMenuButtonVariants = cva(
  "peer/menu-button flex w-full items-center gap-2 overflow-hidden rounded-md p-2 text-left text-sm outline-none ring-sidebar-ring transition-[width,height,padding] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 group-has-[[data-sidebar=menu-action]]/menu-item:pr-8 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active=true]:bg-sidebar-accent data-[active=true]:font-medium data-[active=true]:text-sidebar-accent-foreground data-[state=open]:hover:bg-sidebar-accent data-[state=open]:hover:text-sidebar-accent-foreground group-data-[collapsible=icon]:!size-8 group-data-[collapsible=icon]:!p-2 [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
        outline:
          "bg-background shadow-[0_0_0_1px_hsl(var(--sidebar-border))] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:shadow-[0_0_0_1px_hsl(var(--sidebar-accent))]",
      },
      size: {
        default: "h-8 text-sm",
        sm: "h-7 text-xs",
        lg: "h-12 text-sm group-data-[collapsible=icon]:!p-0",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

const SidebarMenuButton = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<"button"> & {
    asChild?: boolean;
    isActive?: boolean;
    tooltip?: string | React.ComponentProps<typeof TooltipContent>;
  } & VariantProps<typeof sidebarMenuButtonVariants>
>(({ asChild = false, isActive = false, variant = "default", size = "default", tooltip, className, ...props }, ref) => {
  const Comp = asChild ? Slot : "button";
  const { isMobile, state } = useSidebar();

  const button = (
    <Comp
      ref={ref}
      data-sidebar="menu-button"
      data-size={size}
      data-active={isActive}
      className={cn(sidebarMenuButtonVariants({ variant, size }), className)}
      {...props}
    />
  );

  if (!tooltip) {
    return button;
  }

  if (typeof tooltip === "string") {
    tooltip = {
      children: tooltip,
    };
  }

  return (
    <Tooltip>
      <TooltipTrigger asChild>{button}</TooltipTrigger>
      <TooltipContent side="right" align="center" hidden={state !== "collapsed" || isMobile} {...tooltip} />
    </Tooltip>
  );
});
SidebarMenuButton.displayName = "SidebarMenuButton";

const SidebarMenuAction = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<"button"> & {
    asChild?: boolean;
    showOnHover?: boolean;
  }
>(({ className, asChild = false, showOnHover = false, ...props }, ref) => {
  const Comp = asChild ? Slot : "button";

  return (
    <Comp
      ref={ref}
      data-sidebar="menu-action"
      className={cn(
        "absolute right-1 top-1.5 flex aspect-square w-5 items-center justify-center rounded-md p-0 text-sidebar-foreground outline-none ring-sidebar-ring transition-transform peer-hover/menu-button:text-sidebar-accent-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 [&>svg]:size-4 [&>svg]:shrink-0",
        // Increases the hit area of the button on mobile.
        "after:absolute after:-inset-2 after:md:hidden",
        "peer-data-[size=sm]/menu-button:top-1",
        "peer-data-[size=default]/menu-button:top-1.5",
        "peer-data-[size=lg]/menu-button:top-2.5",
        "group-data-[collapsible=icon]:hidden",
        showOnHover &&
          "group-focus-within/menu-item:opacity-100 group-hover/menu-item:opacity-100 data-[state=open]:opacity-100 peer-data-[active=true]/menu-button:text-sidebar-accent-foreground md:opacity-0",
        className,
      )}
      {...props}
    />
  );
});
SidebarMenuAction.displayName = "SidebarMenuAction";

const SidebarMenuBadge = React.forwardRef<HTMLDivElement, React.ComponentProps<"div">>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      data-sidebar="menu-badge"
      className={cn(
        "pointer-events-none absolute right-1 flex h-5 min-w-5 select-none items-center justify-center rounded-md px-1 text-xs font-medium tabular-nums text-sidebar-foreground",
        "peer-hover/menu-button:text-sidebar-accent-foreground peer-data-[active=true]/menu-button:text-sidebar-accent-foreground",
        "peer-data-[size=sm]/menu-button:top-1",
        "peer-data-[size=default]/menu-button:top-1.5",
        "peer-data-[size=lg]/menu-button:top-2.5",
        "group-data-[collapsible=icon]:hidden",
        className,
      )}
      {...props}
    />
  ),
);
SidebarMenuBadge.displayName = "SidebarMenuBadge";

const SidebarMenuSkeleton = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div"> & {
    showIcon?: boolean;
  }
>(({ className, showIcon = false, ...props }, ref) => {
  // Random width between 50 to 90%.
  const width = React.useMemo(() => {
    return `${Math.floor(Math.random() * 40) + 50}%`;
  }, []);

  return (
    <div
      ref={ref}
      data-sidebar="menu-skeleton"
      className={cn("flex h-8 items-center gap-2 rounded-md px-2", className)}
      {...props}
    >
      {showIcon && <Skeleton className="size-4 rounded-md" data-sidebar="menu-skeleton-icon" />}
      <Skeleton
        className="h-4 max-w-[--skeleton-width] flex-1"
        data-sidebar="menu-skeleton-text"
        style={
          {
            "--skeleton-width": width,
          } as React.CSSProperties
        }
      />
    </div>
  );
});
SidebarMenuSkeleton.displayName = "SidebarMenuSkeleton";

const SidebarMenuSub = React.forwardRef<HTMLUListElement, React.ComponentProps<"ul">>(
  ({ className, ...props }, ref) => (
    <ul
      ref={ref}
      data-sidebar="menu-sub"
      className={cn(
        "mx-3.5 flex min-w-0 translate-x-px flex-col gap-1 border-l border-sidebar-border px-2.5 py-0.5",
        "group-data-[collapsible=icon]:hidden",
        className,
      )}
      {...props}
    />
  ),
);
SidebarMenuSub.displayName = "SidebarMenuSub";

const SidebarMenuSubItem = React.forwardRef<HTMLLIElement, React.ComponentProps<"li">>(({ ...props }, ref) => (
  <li ref={ref} {...props} />
));
SidebarMenuSubItem.displayName = "SidebarMenuSubItem";

const SidebarMenuSubButton = React.forwardRef<
  HTMLAnchorElement,
  React.ComponentProps<"a"> & {
    asChild?: boolean;
    size?: "sm" | "md";
    isActive?: boolean;
  }
>(({ asChild = false, size = "md", isActive, className, ...props }, ref) => {
  const Comp = asChild ? Slot : "a";

  return (
    <Comp
      ref={ref}
      data-sidebar="menu-sub-button"
      data-size={size}
      data-active={isActive}
      className={cn(
        "flex h-7 min-w-0 -translate-x-px items-center gap-2 overflow-hidden rounded-md px-2 text-sidebar-foreground outline-none ring-sidebar-ring aria-disabled:pointer-events-none aria-disabled:opacity-50 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0 [&>svg]:text-sidebar-accent-foreground",
        "data-[active=true]:bg-sidebar-accent data-[active=true]:text-sidebar-accent-foreground",
        size === "sm" && "text-xs",
        size === "md" && "text-sm",
        "group-data-[collapsible=icon]:hidden",
        className,
      )}
      {...props}
    />
  );
});
SidebarMenuSubButton.displayName = "SidebarMenuSubButton";

export {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupAction,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInput,
  SidebarInset,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuBadge,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSkeleton,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarProvider,
  SidebarRail,
  SidebarSeparator,
  SidebarTrigger,
  useSidebar,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\skeleton.tsx`

```tsx
import { cn } from "@/lib/utils";

function Skeleton({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("animate-pulse rounded-md bg-muted", className)} {...props} />;
}

export { Skeleton };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\slider.tsx`

```tsx
import * as React from "react";
import * as SliderPrimitive from "@radix-ui/react-slider";

import { cn } from "@/lib/utils";

const Slider = React.forwardRef<
  React.ElementRef<typeof SliderPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof SliderPrimitive.Root>
>(({ className, ...props }, ref) => (
  <SliderPrimitive.Root
    ref={ref}
    className={cn("relative flex w-full touch-none select-none items-center", className)}
    {...props}
  >
    <SliderPrimitive.Track className="relative h-2 w-full grow overflow-hidden rounded-full bg-secondary">
      <SliderPrimitive.Range className="absolute h-full bg-primary" />
    </SliderPrimitive.Track>
    <SliderPrimitive.Thumb className="block h-5 w-5 rounded-full border-2 border-primary bg-background ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50" />
  </SliderPrimitive.Root>
));
Slider.displayName = SliderPrimitive.Root.displayName;

export { Slider };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\sonner.tsx`

```tsx
import { useTheme } from "next-themes";
import { Toaster as Sonner, toast } from "sonner";

type ToasterProps = React.ComponentProps<typeof Sonner>;

const Toaster = ({ ...props }: ToasterProps) => {
  const { theme = "system" } = useTheme();

  return (
    <Sonner
      theme={theme as ToasterProps["theme"]}
      className="toaster group"
      toastOptions={{
        classNames: {
          toast:
            "group toast group-[.toaster]:bg-background group-[.toaster]:text-foreground group-[.toaster]:border-border group-[.toaster]:shadow-lg",
          description: "group-[.toast]:text-muted-foreground",
          actionButton: "group-[.toast]:bg-primary group-[.toast]:text-primary-foreground",
          cancelButton: "group-[.toast]:bg-muted group-[.toast]:text-muted-foreground",
        },
      }}
      {...props}
    />
  );
};

export { Toaster, toast };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\switch.tsx`

```tsx
import * as React from "react";
import * as SwitchPrimitives from "@radix-ui/react-switch";

import { cn } from "@/lib/utils";

const Switch = React.forwardRef<
  React.ElementRef<typeof SwitchPrimitives.Root>,
  React.ComponentPropsWithoutRef<typeof SwitchPrimitives.Root>
>(({ className, ...props }, ref) => (
  <SwitchPrimitives.Root
    className={cn(
      "peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors data-[state=checked]:bg-primary data-[state=unchecked]:bg-input focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50",
      className,
    )}
    {...props}
    ref={ref}
  >
    <SwitchPrimitives.Thumb
      className={cn(
        "pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0",
      )}
    />
  </SwitchPrimitives.Root>
));
Switch.displayName = SwitchPrimitives.Root.displayName;

export { Switch };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\table.tsx`

```tsx
import * as React from "react";

import { cn } from "@/lib/utils";

const Table = React.forwardRef<HTMLTableElement, React.HTMLAttributes<HTMLTableElement>>(
  ({ className, ...props }, ref) => (
    <div className="relative w-full overflow-auto">
      <table ref={ref} className={cn("w-full caption-bottom text-sm", className)} {...props} />
    </div>
  ),
);
Table.displayName = "Table";

const TableHeader = React.forwardRef<HTMLTableSectionElement, React.HTMLAttributes<HTMLTableSectionElement>>(
  ({ className, ...props }, ref) => <thead ref={ref} className={cn("[&_tr]:border-b", className)} {...props} />,
);
TableHeader.displayName = "TableHeader";

const TableBody = React.forwardRef<HTMLTableSectionElement, React.HTMLAttributes<HTMLTableSectionElement>>(
  ({ className, ...props }, ref) => (
    <tbody ref={ref} className={cn("[&_tr:last-child]:border-0", className)} {...props} />
  ),
);
TableBody.displayName = "TableBody";

const TableFooter = React.forwardRef<HTMLTableSectionElement, React.HTMLAttributes<HTMLTableSectionElement>>(
  ({ className, ...props }, ref) => (
    <tfoot ref={ref} className={cn("border-t bg-muted/50 font-medium [&>tr]:last:border-b-0", className)} {...props} />
  ),
);
TableFooter.displayName = "TableFooter";

const TableRow = React.forwardRef<HTMLTableRowElement, React.HTMLAttributes<HTMLTableRowElement>>(
  ({ className, ...props }, ref) => (
    <tr
      ref={ref}
      className={cn("border-b transition-colors data-[state=selected]:bg-muted hover:bg-muted/50", className)}
      {...props}
    />
  ),
);
TableRow.displayName = "TableRow";

const TableHead = React.forwardRef<HTMLTableCellElement, React.ThHTMLAttributes<HTMLTableCellElement>>(
  ({ className, ...props }, ref) => (
    <th
      ref={ref}
      className={cn(
        "h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0",
        className,
      )}
      {...props}
    />
  ),
);
TableHead.displayName = "TableHead";

const TableCell = React.forwardRef<HTMLTableCellElement, React.TdHTMLAttributes<HTMLTableCellElement>>(
  ({ className, ...props }, ref) => (
    <td ref={ref} className={cn("p-4 align-middle [&:has([role=checkbox])]:pr-0", className)} {...props} />
  ),
);
TableCell.displayName = "TableCell";

const TableCaption = React.forwardRef<HTMLTableCaptionElement, React.HTMLAttributes<HTMLTableCaptionElement>>(
  ({ className, ...props }, ref) => (
    <caption ref={ref} className={cn("mt-4 text-sm text-muted-foreground", className)} {...props} />
  ),
);
TableCaption.displayName = "TableCaption";

export { Table, TableHeader, TableBody, TableFooter, TableHead, TableRow, TableCell, TableCaption };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\tabs.tsx`

```tsx
import * as React from "react";
import * as TabsPrimitive from "@radix-ui/react-tabs";

import { cn } from "@/lib/utils";

const Tabs = TabsPrimitive.Root;

const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground",
      className,
    )}
    {...props}
  />
));
TabsList.displayName = TabsPrimitive.List.displayName;

const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
      className,
    )}
    {...props}
  />
));
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName;

const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
      className,
    )}
    {...props}
  />
));
TabsContent.displayName = TabsPrimitive.Content.displayName;

export { Tabs, TabsList, TabsTrigger, TabsContent };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\textarea.tsx`

```tsx
import * as React from "react";

import { cn } from "@/lib/utils";

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(({ className, ...props }, ref) => {
  return (
    <textarea
      className={cn(
        "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      ref={ref}
      {...props}
    />
  );
});
Textarea.displayName = "Textarea";

export { Textarea };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\toast.tsx`

```tsx
import * as React from "react";
import * as ToastPrimitives from "@radix-ui/react-toast";
import { cva, type VariantProps } from "class-variance-authority";
import { X } from "lucide-react";

import { cn } from "@/lib/utils";

const ToastProvider = ToastPrimitives.Provider;

const ToastViewport = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Viewport>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Viewport>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Viewport
    ref={ref}
    className={cn(
      "fixed top-0 z-[100] flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-0 sm:right-0 sm:top-auto sm:flex-col md:max-w-[420px]",
      className,
    )}
    {...props}
  />
));
ToastViewport.displayName = ToastPrimitives.Viewport.displayName;

const toastVariants = cva(
  "group pointer-events-auto relative flex w-full items-center justify-between space-x-4 overflow-hidden rounded-md border p-6 pr-8 shadow-lg transition-all data-[swipe=cancel]:translate-x-0 data-[swipe=end]:translate-x-[var(--radix-toast-swipe-end-x)] data-[swipe=move]:translate-x-[var(--radix-toast-swipe-move-x)] data-[swipe=move]:transition-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[swipe=end]:animate-out data-[state=closed]:fade-out-80 data-[state=closed]:slide-out-to-right-full data-[state=open]:slide-in-from-top-full data-[state=open]:sm:slide-in-from-bottom-full",
  {
    variants: {
      variant: {
        default: "border bg-background text-foreground",
        destructive: "destructive group border-destructive bg-destructive text-destructive-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

const Toast = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Root>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Root> & VariantProps<typeof toastVariants>
>(({ className, variant, ...props }, ref) => {
  return <ToastPrimitives.Root ref={ref} className={cn(toastVariants({ variant }), className)} {...props} />;
});
Toast.displayName = ToastPrimitives.Root.displayName;

const ToastAction = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Action>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Action>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Action
    ref={ref}
    className={cn(
      "inline-flex h-8 shrink-0 items-center justify-center rounded-md border bg-transparent px-3 text-sm font-medium ring-offset-background transition-colors group-[.destructive]:border-muted/40 hover:bg-secondary group-[.destructive]:hover:border-destructive/30 group-[.destructive]:hover:bg-destructive group-[.destructive]:hover:text-destructive-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 group-[.destructive]:focus:ring-destructive disabled:pointer-events-none disabled:opacity-50",
      className,
    )}
    {...props}
  />
));
ToastAction.displayName = ToastPrimitives.Action.displayName;

const ToastClose = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Close>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Close>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Close
    ref={ref}
    className={cn(
      "absolute right-2 top-2 rounded-md p-1 text-foreground/50 opacity-0 transition-opacity group-hover:opacity-100 group-[.destructive]:text-red-300 hover:text-foreground group-[.destructive]:hover:text-red-50 focus:opacity-100 focus:outline-none focus:ring-2 group-[.destructive]:focus:ring-red-400 group-[.destructive]:focus:ring-offset-red-600",
      className,
    )}
    toast-close=""
    {...props}
  >
    <X className="h-4 w-4" />
  </ToastPrimitives.Close>
));
ToastClose.displayName = ToastPrimitives.Close.displayName;

const ToastTitle = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Title>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Title>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Title ref={ref} className={cn("text-sm font-semibold", className)} {...props} />
));
ToastTitle.displayName = ToastPrimitives.Title.displayName;

const ToastDescription = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Description>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Description>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Description ref={ref} className={cn("text-sm opacity-90", className)} {...props} />
));
ToastDescription.displayName = ToastPrimitives.Description.displayName;

type ToastProps = React.ComponentPropsWithoutRef<typeof Toast>;

type ToastActionElement = React.ReactElement<typeof ToastAction>;

export {
  type ToastProps,
  type ToastActionElement,
  ToastProvider,
  ToastViewport,
  Toast,
  ToastTitle,
  ToastDescription,
  ToastClose,
  ToastAction,
};

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\toaster.tsx`

```tsx
import { useToast } from "@/hooks/use-toast";
import { Toast, ToastClose, ToastDescription, ToastProvider, ToastTitle, ToastViewport } from "@/components/ui/toast";

export function Toaster() {
  const { toasts } = useToast();

  return (
    <ToastProvider>
      {toasts.map(function ({ id, title, description, action, ...props }) {
        return (
          <Toast key={id} {...props}>
            <div className="grid gap-1">
              {title && <ToastTitle>{title}</ToastTitle>}
              {description && <ToastDescription>{description}</ToastDescription>}
            </div>
            {action}
            <ToastClose />
          </Toast>
        );
      })}
      <ToastViewport />
    </ToastProvider>
  );
}

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\toggle-group.tsx`

```tsx
import * as React from "react";
import * as ToggleGroupPrimitive from "@radix-ui/react-toggle-group";
import { type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";
import { toggleVariants } from "@/components/ui/toggle";

const ToggleGroupContext = React.createContext<VariantProps<typeof toggleVariants>>({
  size: "default",
  variant: "default",
});

const ToggleGroup = React.forwardRef<
  React.ElementRef<typeof ToggleGroupPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof ToggleGroupPrimitive.Root> & VariantProps<typeof toggleVariants>
>(({ className, variant, size, children, ...props }, ref) => (
  <ToggleGroupPrimitive.Root ref={ref} className={cn("flex items-center justify-center gap-1", className)} {...props}>
    <ToggleGroupContext.Provider value={{ variant, size }}>{children}</ToggleGroupContext.Provider>
  </ToggleGroupPrimitive.Root>
));

ToggleGroup.displayName = ToggleGroupPrimitive.Root.displayName;

const ToggleGroupItem = React.forwardRef<
  React.ElementRef<typeof ToggleGroupPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof ToggleGroupPrimitive.Item> & VariantProps<typeof toggleVariants>
>(({ className, children, variant, size, ...props }, ref) => {
  const context = React.useContext(ToggleGroupContext);

  return (
    <ToggleGroupPrimitive.Item
      ref={ref}
      className={cn(
        toggleVariants({
          variant: context.variant || variant,
          size: context.size || size,
        }),
        className,
      )}
      {...props}
    >
      {children}
    </ToggleGroupPrimitive.Item>
  );
});

ToggleGroupItem.displayName = ToggleGroupPrimitive.Item.displayName;

export { ToggleGroup, ToggleGroupItem };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\toggle.tsx`

```tsx
import * as React from "react";
import * as TogglePrimitive from "@radix-ui/react-toggle";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const toggleVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors hover:bg-muted hover:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=on]:bg-accent data-[state=on]:text-accent-foreground",
  {
    variants: {
      variant: {
        default: "bg-transparent",
        outline: "border border-input bg-transparent hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-3",
        sm: "h-9 px-2.5",
        lg: "h-11 px-5",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

const Toggle = React.forwardRef<
  React.ElementRef<typeof TogglePrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof TogglePrimitive.Root> & VariantProps<typeof toggleVariants>
>(({ className, variant, size, ...props }, ref) => (
  <TogglePrimitive.Root ref={ref} className={cn(toggleVariants({ variant, size, className }))} {...props} />
));

Toggle.displayName = TogglePrimitive.Root.displayName;

export { Toggle, toggleVariants };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\tooltip.tsx`

```tsx
import * as React from "react";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";

import { cn } from "@/lib/utils";

const TooltipProvider = TooltipPrimitive.Provider;

const Tooltip = TooltipPrimitive.Root;

const TooltipTrigger = TooltipPrimitive.Trigger;

const TooltipContent = React.forwardRef<
  React.ElementRef<typeof TooltipPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <TooltipPrimitive.Content
    ref={ref}
    sideOffset={sideOffset}
    className={cn(
      "z-50 overflow-hidden rounded-md border bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
      className,
    )}
    {...props}
  />
));
TooltipContent.displayName = TooltipPrimitive.Content.displayName;

export { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider };

```

---

### `frontend\bildofy-lms-lovable\src\components\ui\use-toast.ts`

```ts
import { useToast, toast } from "@/hooks/use-toast";

export { useToast, toast };

```

---

### `frontend\bildofy-lms-lovable\src\hooks\use-toast.ts`

```ts
import * as React from "react";

import type { ToastActionElement, ToastProps } from "@/components/ui/toast";

const TOAST_LIMIT = 1;
const TOAST_REMOVE_DELAY = 1000000;

type ToasterToast = ToastProps & {
  id: string;
  title?: React.ReactNode;
  description?: React.ReactNode;
  action?: ToastActionElement;
};

const actionTypes = {
  ADD_TOAST: "ADD_TOAST",
  UPDATE_TOAST: "UPDATE_TOAST",
  DISMISS_TOAST: "DISMISS_TOAST",
  REMOVE_TOAST: "REMOVE_TOAST",
} as const;

let count = 0;

function genId() {
  count = (count + 1) % Number.MAX_SAFE_INTEGER;
  return count.toString();
}

type ActionType = typeof actionTypes;

type Action =
  | {
      type: ActionType["ADD_TOAST"];
      toast: ToasterToast;
    }
  | {
      type: ActionType["UPDATE_TOAST"];
      toast: Partial<ToasterToast>;
    }
  | {
      type: ActionType["DISMISS_TOAST"];
      toastId?: ToasterToast["id"];
    }
  | {
      type: ActionType["REMOVE_TOAST"];
      toastId?: ToasterToast["id"];
    };

interface State {
  toasts: ToasterToast[];
}

const toastTimeouts = new Map<string, ReturnType<typeof setTimeout>>();

const addToRemoveQueue = (toastId: string) => {
  if (toastTimeouts.has(toastId)) {
    return;
  }

  const timeout = setTimeout(() => {
    toastTimeouts.delete(toastId);
    dispatch({
      type: "REMOVE_TOAST",
      toastId: toastId,
    });
  }, TOAST_REMOVE_DELAY);

  toastTimeouts.set(toastId, timeout);
};

export const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "ADD_TOAST":
      return {
        ...state,
        toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),
      };

    case "UPDATE_TOAST":
      return {
        ...state,
        toasts: state.toasts.map((t) => (t.id === action.toast.id ? { ...t, ...action.toast } : t)),
      };

    case "DISMISS_TOAST": {
      const { toastId } = action;

      // ! Side effects ! - This could be extracted into a dismissToast() action,
      // but I'll keep it here for simplicity
      if (toastId) {
        addToRemoveQueue(toastId);
      } else {
        state.toasts.forEach((toast) => {
          addToRemoveQueue(toast.id);
        });
      }

      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === toastId || toastId === undefined
            ? {
                ...t,
                open: false,
              }
            : t,
        ),
      };
    }
    case "REMOVE_TOAST":
      if (action.toastId === undefined) {
        return {
          ...state,
          toasts: [],
        };
      }
      return {
        ...state,
        toasts: state.toasts.filter((t) => t.id !== action.toastId),
      };
  }
};

const listeners: Array<(state: State) => void> = [];

let memoryState: State = { toasts: [] };

function dispatch(action: Action) {
  memoryState = reducer(memoryState, action);
  listeners.forEach((listener) => {
    listener(memoryState);
  });
}

type Toast = Omit<ToasterToast, "id">;

function toast({ ...props }: Toast) {
  const id = genId();

  const update = (props: ToasterToast) =>
    dispatch({
      type: "UPDATE_TOAST",
      toast: { ...props, id },
    });
  const dismiss = () => dispatch({ type: "DISMISS_TOAST", toastId: id });

  dispatch({
    type: "ADD_TOAST",
    toast: {
      ...props,
      id,
      open: true,
      onOpenChange: (open) => {
        if (!open) dismiss();
      },
    },
  });

  return {
    id: id,
    dismiss,
    update,
  };
}

function useToast() {
  const [state, setState] = React.useState<State>(memoryState);

  React.useEffect(() => {
    listeners.push(setState);
    return () => {
      const index = listeners.indexOf(setState);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    };
  }, [state]);

  return {
    ...state,
    toast,
    dismiss: (toastId?: string) => dispatch({ type: "DISMISS_TOAST", toastId }),
  };
}

export { useToast, toast };

```

---

### `frontend\bildofy-lms-lovable\src\contexts\AuthContext.tsx`

```tsx
import React, { createContext, useContext, useEffect, useState } from 'react';

type User = {
  id: number;
  role: string;
  class_id?: number;
};

type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  login: () => {},
  logout: () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /* ================= REHYDRATE ON BOOT ================= */
  useEffect(() => {
    const storedUser = localStorage.getItem('auth_user');
    const token = localStorage.getItem('access_token');

    if (storedUser && token) {
      try {
        setUser(JSON.parse(storedUser));
      } catch {
        localStorage.removeItem('auth_user');
        localStorage.removeItem('access_token');
      }
    }

    setIsLoading(false);
  }, []);

  /* ================= LOGIN ================= */
  const login = (userData: User, token: string) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('auth_user', JSON.stringify(userData));
    setUser(userData);
  };

  /* ================= LOGOUT ================= */
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('auth_user');
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: Boolean(user),
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

```

---

### `frontend\bildofy-lms-lovable\src\contexts\OnlineContext.tsx`

```tsx
import React, { createContext, useContext, useEffect, useState } from 'react';

interface OnlineContextType {
  isOnline: boolean;
}

const OnlineContext = createContext<OnlineContextType>({ isOnline: true });

export const useOnlineStatus = () => useContext(OnlineContext);

export const OnlineProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <OnlineContext.Provider value={{ isOnline }}>
      {children}
    </OnlineContext.Provider>
  );
};

```

---

### `frontend\bildofy-lms-lovable\src\hooks\use-mobile.tsx`

```tsx
import * as React from "react";

const MOBILE_BREAKPOINT = 768;

export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(undefined);

  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`);
    const onChange = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    };
    mql.addEventListener("change", onChange);
    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    return () => mql.removeEventListener("change", onChange);
  }, []);

  return !!isMobile;
}

```

---

### `frontend\bildofy-lms-lovable\src\lib\utils.ts`

```ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

```

---

### `frontend\bildofy-lms-lovable\src\pages\Index.tsx`

```tsx
import { Navigate } from "react-router-dom";

// Redirect to Role Selection
const Index = () => {
  return <Navigate to="/" replace />;
};

export default Index;

```

---

### `frontend\bildofy-lms-lovable\src\pages\NotFound.tsx`

```tsx
import { useLocation } from "react-router-dom";
import { useEffect } from "react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted">
      <div className="text-center">
        <h1 className="mb-4 text-4xl font-bold">404</h1>
        <p className="mb-4 text-xl text-muted-foreground">Oops! Page not found</p>
        <a href="/" className="text-primary underline hover:text-primary/90">
          Return to Home
        </a>
      </div>
    </div>
  );
};

export default NotFound;

```

---

### `frontend\bildofy-lms-lovable\src\pages\RoleSelection.tsx`

```tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { RoleCard } from '@/components/cards/RoleCard';
import { GraduationCap, Users, UserCheck, Sparkles } from 'lucide-react';

const RoleSelection: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-accent/5 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-0 w-64 h-64 bg-success/5 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12 min-h-screen flex flex-col items-center justify-center">
        {/* Logo & Tagline */}
        <div className="text-center mb-12 animate-fade-up">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-hero shadow-glow mb-6">
            <Sparkles className="w-10 h-10 text-primary-foreground" />
          </div>
          <h1 className="text-4xl md:text-5xl font-display font-bold text-foreground mb-4">
            LearnSphere
          </h1>
          <p className="text-lg text-muted-foreground max-w-md mx-auto">
            Your AI-powered learning companion. Choose your role to begin your journey.
          </p>
        </div>

        {/* Role Cards */}
        <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="animate-fade-up" style={{ animationDelay: '0.1s' }}>
            <RoleCard
              title="Student Dashboard"
              description="Track progress, earn XP, and master your subjects with AI-powered learning."
              icon={GraduationCap}
              gradient="primary"
              onClick={() => navigate('/student')}
            />
          </div>

          <div className="animate-fade-up" style={{ animationDelay: '0.2s' }}>
            <RoleCard
              title="Teacher Dashboard"
              description="Create assignments, track student performance, and leverage AI tools."
              icon={Users}
              gradient="accent"
              onClick={() => navigate('/teacher')}
            />
          </div>

          <div className="animate-fade-up" style={{ animationDelay: '0.3s' }}>
            <RoleCard
              title="Parent Dashboard"
              description="Monitor your child's progress with detailed insights and weekly reports."
              icon={UserCheck}
              gradient="success"
              onClick={() => navigate('/parent')}
            />
          </div>
        </div>

        {/* Footer */}
        <p className="mt-12 text-sm text-muted-foreground animate-fade-in" style={{ animationDelay: '0.5s' }}>
          Designed for Indian students • Grades 9-12 • CBSE, ICSE & State Boards
        </p>
      </div>
    </div>
  );
};

export default RoleSelection;

```

---

### `frontend\bildofy-lms-lovable\src\pages\auth\LoginPage.tsx`

```tsx
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";

  const LoginPage = () => {
    const { login } = useAuth();
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleLogin = async () => {
    const res = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    login(
      {
        id: data.user.id,
        role: data.user.role,
        class_id: data.user.class_id,
      },
      data.access_token
    );

    // 2️⃣ Navigate based on role
    if (data.user.role === "student") {
      navigate("/student");
    } else if (data.user.role === "teacher") {
      navigate("/teacher");
    } else if (data.user.role === "admin") {
      navigate("/admin");
    } else {
      navigate("/");
    }
  };




  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background gap-6">
      
      {/* LearnSphere Logo */}
      <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
        LearnSphere
      </h1>

      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Login</CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <Input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}

          <Button
            className="w-full bg-gradient-to-r from-primary to-purple-600"
            onClick={handleLogin}
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </Button>

          <p className="text-sm text-center text-muted-foreground">
            Don’t have an account?{" "}
            <Link to="/signup" className="underline">
              Sign up
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\auth\SignupPage.tsx`

```tsx
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Link, useNavigate } from "react-router-dom";

const SignupPage = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<"student" | "teacher">("student");
  const [registrationCode, setRegistrationCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSignup = async () => {
    setError(null);
    setLoading(true);

    try {
      const payload: any = { email, password, role };
      if (role === "student") {
        payload.registration_code = registrationCode;
      }

      const res = await fetch("http://localhost:8000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Signup failed");
      }

      navigate("/login");
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background gap-6">
      
      {/* LearnSphere Logo */}
      <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
        LearnSphere
      </h1>

      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Create Account</CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <Input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <select
            className="w-full border rounded-md px-3 py-2 text-sm bg-background"
            value={role}
            onChange={(e) => setRole(e.target.value as "student" | "teacher")}
          >
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
          </select>

          {role === "student" && (
            <Input
              placeholder="6-digit Registration Code"
              value={registrationCode}
              onChange={(e) => setRegistrationCode(e.target.value)}
            />
          )}

          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}

          <Button
            className="w-full bg-gradient-to-r from-primary to-purple-600"
            onClick={handleSignup}
            disabled={loading}
          >
            {loading ? "Creating account..." : "Create Account"}
          </Button>

          <p className="text-sm text-center text-muted-foreground">
            Already have an account?{" "}
            <Link to="/login" className="underline">
              Login
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default SignupPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\parent\ParentDashboard.tsx`

```tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { StatCard } from '@/components/cards/StatCard';
import { ProgressRing } from '@/components/progress/ProgressRing';
import { XPBar } from '@/components/gamification/XPBar';
import {
  BookOpen,
  Clock,
  Trophy,
  TrendingUp,
  Calendar,
  Settings,
  LogOut,
  Target,
  Flame,
  Star,
} from 'lucide-react';

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
  assignmentsCompleted: 6,
};

const weeklyInsights = [
  { id: '1', insight: 'Arjun spent 3 hours more on Physics this week compared to last week.', type: 'positive' },
  { id: '2', insight: 'Math practice test score improved by 12% from previous attempt.', type: 'positive' },
  { id: '3', insight: 'Chemistry chapter review is pending. Due in 2 days.', type: 'warning' },
];

const ParentDashboard: React.FC = () => {
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
            Monitor {mockChildData.name}'s learning progress and achievements.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Child Overview Card */}
            <section className="p-6 rounded-xl bg-card border border-border shadow-sm animate-fade-up" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-16 h-16 rounded-full bg-gradient-primary flex items-center justify-center text-2xl font-bold text-primary-foreground">
                  {mockChildData.name.charAt(0)}
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-display font-bold text-foreground">{mockChildData.name}</h2>
                  <p className="text-muted-foreground">{mockChildData.grade} • {mockChildData.board}</p>
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

            {/* Weekly Stats */}
            <section className="animate-fade-up" style={{ animationDelay: '0.2s' }}>
              <h2 className="text-lg font-display font-semibold text-foreground mb-4">This Week's Performance</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <StatCard
                  title="Study Time"
                  value={mockChildData.weeklyStudyTime}
                  icon={Clock}
                />
                <StatCard
                  title="Tests Taken"
                  value={mockChildData.testsThisWeek}
                  icon={Target}
                />
                <StatCard
                  title="Average Score"
                  value={`${mockChildData.avgScore}%`}
                  icon={Trophy}
                  trend={{ value: 8, isPositive: true }}
                />
                <StatCard
                  title="Assignments"
                  value={mockChildData.assignmentsCompleted}
                  icon={BookOpen}
                />
              </div>
            </section>

            {/* AI Insights */}
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

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Subject Progress */}
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

            {/* Upcoming */}
            <div className="p-5 rounded-xl bg-card border border-border shadow-sm animate-fade-up" style={{ animationDelay: '0.25s' }}>
              <h3 className="font-display font-semibold text-foreground mb-4 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-primary" />
                Upcoming
              </h3>
              <div className="space-y-3">
                <div className="p-3 rounded-lg bg-secondary/50">
                  <p className="font-medium text-foreground text-sm">Physics Test</p>
                  <p className="text-xs text-muted-foreground">Tomorrow • Chapter 5</p>
                </div>
                <div className="p-3 rounded-lg bg-secondary/50">
                  <p className="font-medium text-foreground text-sm">Math Assignment</p>
                  <p className="text-xs text-muted-foreground">In 2 days • Calculus</p>
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

```

---

### `frontend\bildofy-lms-lovable\src\pages\student\AssignmentsPage.tsx`

```tsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { XPBadge } from '@/components/gamification/XPBadge';
import {
  ArrowLeft,
  BookOpen,
  Calendar,
  CheckCircle,
  Clock,
  Upload,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { format, isPast, isToday, isTomorrow } from 'date-fns';

type AssignmentStatus = 'pending' | 'submitted' | 'graded';
type ViewState = 'list' | 'detail' | 'submit' | 'complete';

type Assignment = {
  id: string;
  title: string;
  subject: string;
  dueDate: Date;
  status: AssignmentStatus;
  xpReward: number;
  submittedAt?: Date;
  grade?: string;
  xpEarned?: number;
};

const mockAssignments: Assignment[] = [
  {
    id: '1',
    title: 'Solve Quadratic Equations Set',
    subject: 'Mathematics',
    dueDate: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000),
    status: 'pending',
    xpReward: 50,
  },
  {
    id: '2',
    title: 'Newton Laws Essay',
    subject: 'Physics',
    dueDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
    status: 'pending',
    xpReward: 75,
  },
  {
    id: '3',
    title: 'Chemical Reactions Lab Report',
    subject: 'Chemistry',
    dueDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    status: 'submitted',
    xpReward: 60,
    submittedAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
  },
  {
    id: '4',
    title: 'Poetry Analysis',
    subject: 'English',
    dueDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
    status: 'graded',
    xpReward: 40,
    grade: 'A',
    xpEarned: 40,
  },
];

const formatDueDate = (date: Date) => {
  if (isToday(date)) return 'Due Today';
  if (isTomorrow(date)) return 'Due Tomorrow';
  if (isPast(date)) return `Was due ${format(date, 'MMM d')}`;
  return `Due ${format(date, 'MMM d')}`;
};

const statusConfig = {
  pending: { label: 'Pending', color: 'bg-warning/10 text-warning' },
  submitted: { label: 'Submitted', color: 'bg-primary/10 text-primary' },
  graded: { label: 'Graded', color: 'bg-success/10 text-success' },
};

const AssignmentsPage: React.FC = () => {
  const [filter, setFilter] = useState<'all' | 'pending' | 'submitted'>('all');
  const [view, setView] = useState<ViewState>('list');
  const [selectedAssignment, setSelectedAssignment] =
    useState<Assignment | null>(null);

  const filteredAssignments = mockAssignments.filter((a) => {
    if (filter === 'all') return true;
    if (filter === 'pending') return a.status === 'pending';
    if (filter === 'submitted') return a.status !== 'pending';
    return true;
  });

  const pendingCount = mockAssignments.filter(
    (a) => a.status === 'pending'
  ).length;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Link to="/student">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <div>
              <h1 className="text-xl font-display font-bold text-foreground">
                Assignments
              </h1>
              <p className="text-sm text-muted-foreground">
                {pendingCount} pending
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* ================= LIST VIEW ================= */}
        {view === 'list' && (
          <>
            {/* Filter Tabs */}
            <div className="flex gap-2 mb-6">
              {(['all', 'pending', 'submitted'] as const).map((tab) => (
                <Button
                  key={tab}
                  variant={filter === tab ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setFilter(tab)}
                  className="capitalize"
                >
                  {tab}
                </Button>
              ))}
            </div>

            {/* Assignments List */}
            <div className="grid gap-4">
              {filteredAssignments.map((assignment, index) => {
                const status = statusConfig[assignment.status];
                const isOverdue =
                  assignment.status === 'pending' &&
                  isPast(assignment.dueDate);

                return (
                  <div
                    key={assignment.id}
                    className={cn(
                      'p-5 rounded-xl bg-card border border-border shadow-sm transition-all duration-200 animate-fade-up',
                      'hover:shadow-md hover:border-primary/30',
                      isOverdue && 'border-destructive/30'
                    )}
                    style={{ animationDelay: `${index * 0.05}s` }}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-4">
                        <div
                          className={cn(
                            'w-12 h-12 rounded-xl flex items-center justify-center',
                            assignment.status === 'graded'
                              ? 'bg-success/10'
                              : 'bg-primary/10'
                          )}
                        >
                          {assignment.status === 'graded' ? (
                            <CheckCircle className="w-6 h-6 text-success" />
                          ) : (
                            <BookOpen className="w-6 h-6 text-primary" />
                          )}
                        </div>
                        <div>
                          <span
                            className={cn(
                              'text-xs font-medium px-2 py-0.5 rounded-full',
                              status.color
                            )}
                          >
                            {status.label}
                          </span>
                          <h3 className="font-semibold text-foreground mt-1">
                            {assignment.title}
                          </h3>
                          <p className="text-sm text-muted-foreground">
                            {assignment.subject}
                          </p>
                          <div className="flex items-center gap-2 mt-2 text-sm">
                            <Calendar className="w-4 h-4 text-muted-foreground" />
                            <span
                              className={cn(
                                isOverdue
                                  ? 'text-destructive'
                                  : 'text-muted-foreground'
                              )}
                            >
                              {formatDueDate(assignment.dueDate)}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="flex flex-col items-end gap-2">
                        {assignment.status === 'pending' ? (
                          <>
                            <XPBadge xp={assignment.xpReward} />
                            <Button
                              size="sm"
                              className="gap-1"
                              onClick={() => {
                                setSelectedAssignment(assignment);
                                setView('detail');
                              }}
                            >
                              <Upload className="w-4 h-4" />
                              Submit
                            </Button>
                          </>
                        ) : assignment.status === 'graded' ? (
                          <div className="text-right">
                            <span className="text-2xl font-bold text-success">
                              {assignment.grade}
                            </span>
                            <p className="text-xs text-muted-foreground">
                              +{assignment.xpEarned} XP
                            </p>
                          </div>
                        ) : (
                          <div className="flex items-center gap-1 text-sm text-primary">
                            <Clock className="w-4 h-4" />
                            <span>Awaiting grade</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}

        {/* ================= DETAIL VIEW ================= */}
        {view === 'detail' && selectedAssignment && (
          <div className="max-w-2xl mx-auto space-y-6">
            <h2 className="text-2xl font-bold">
              {selectedAssignment.title}
            </h2>
            <p className="text-muted-foreground">
              Subject: {selectedAssignment.subject}
            </p>
            <p>{formatDueDate(selectedAssignment.dueDate)}</p>

            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setView('list')}>
                Back
              </Button>
              <Button onClick={() => setView('submit')}>
                Proceed to Submit
              </Button>
            </div>
          </div>
        )}

        {/* ================= SUBMIT VIEW ================= */}
        {view === 'submit' && selectedAssignment && (
          <div className="max-w-xl mx-auto space-y-6">
            <h2 className="text-xl font-semibold">Upload Assignment</h2>
            <input type="file" accept=".pdf" />
            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setView('detail')}>
                Back
              </Button>
              <Button onClick={() => setView('complete')}>
                Submit Assignment
              </Button>
            </div>
          </div>
        )}

        {/* ================= COMPLETE VIEW ================= */}
        {view === 'complete' && selectedAssignment && (
          <div className="text-center space-y-4 py-12">
            <CheckCircle className="w-12 h-12 mx-auto text-success" />
            <h2 className="text-2xl font-bold">
              Assignment Submitted ✅
            </h2>
            <p className="text-muted-foreground">
              {selectedAssignment.title}
            </p>
            <Button
              onClick={() => {
                setView('list');
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

export default AssignmentsPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\student\DoubtChatPage.tsx`

```tsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { XPBadge } from '@/components/gamification/XPBadge';
import { useOnlineStatus } from '@/contexts/OnlineContext';
import { ArrowLeft, MessageCircleQuestion, Send, Bot, User, WifiOff, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

const mockMessages: Message[] = [
  {
    id: '1',
    content: 'Hello! I\'m your AI study assistant. Ask me any question about your subjects, and I\'ll help you understand better. You earn XP for meaningful interactions!',
    role: 'assistant',
    timestamp: new Date(),
  },
];

const DoubtChatPage: React.FC = () => {
  const { isOnline } = useOnlineStatus();
  const [messages, setMessages] = useState<Message[]>(mockMessages);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // Simulate AI response (in production, this calls the API)
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: isOnline
          ? 'Great question! Let me explain this concept in detail...\n\nThe answer involves understanding the fundamental principles involved. Would you like me to break it down further or provide an example?'
          : 'I\'m currently in offline mode. I can only provide basic responses. For detailed explanations, please connect to the internet.',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiResponse]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link to="/student">
                <Button variant="ghost" size="icon">
                  <ArrowLeft className="w-5 h-5" />
                </Button>
              </Link>
              <div>
                <h1 className="text-xl font-display font-bold text-foreground flex items-center gap-2">
                  <MessageCircleQuestion className="w-5 h-5 text-primary" />
                  AI Doubt Assistant
                </h1>
                <p className="text-sm text-muted-foreground">
                  {isOnline ? 'Online • Full capabilities' : 'Offline • Limited responses'}
                </p>
              </div>
            </div>
            <XPBadge xp={10} size="sm" />
          </div>
        </div>
      </header>

      {/* Offline Banner */}
      {!isOnline && (
        <div className="bg-offline/10 border-b border-offline/30 px-4 py-2 flex items-center justify-center gap-2 text-sm">
          <WifiOff className="w-4 h-4 text-offline" />
          <span className="text-foreground">Limited AI responses in offline mode</span>
        </div>
      )}

      {/* Messages */}
      <main className="flex-1 overflow-y-auto p-4">
        <div className="container mx-auto max-w-2xl space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                'flex gap-3 animate-fade-up',
                message.role === 'user' && 'flex-row-reverse'
              )}
            >
              <div
                className={cn(
                  'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                  message.role === 'assistant'
                    ? 'bg-gradient-primary text-primary-foreground'
                    : 'bg-secondary text-secondary-foreground'
                )}
              >
                {message.role === 'assistant' ? (
                  <Bot className="w-4 h-4" />
                ) : (
                  <User className="w-4 h-4" />
                )}
              </div>
              <div
                className={cn(
                  'max-w-[80%] p-4 rounded-2xl',
                  message.role === 'assistant'
                    ? 'bg-card border border-border rounded-tl-sm'
                    : 'bg-primary text-primary-foreground rounded-tr-sm'
                )}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex gap-3 animate-fade-up">
              <div className="w-8 h-8 rounded-full bg-gradient-primary text-primary-foreground flex items-center justify-center">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-card border border-border p-4 rounded-2xl rounded-tl-sm">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Input */}
      <footer className="sticky bottom-0 bg-card border-t border-border p-4">
        <div className="container mx-auto max-w-2xl">
          <div className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask your doubt..."
              className="flex-1"
            />
            <Button onClick={handleSend} disabled={!input.trim()}>
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <p className="text-xs text-center text-muted-foreground mt-2">
            <Sparkles className="w-3 h-3 inline mr-1" />
            Earn XP for meaningful questions and interactions
          </p>
        </div>
      </footer>
    </div>
  );
};

export default DoubtChatPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\student\FlashcardsPage.tsx`

```tsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { XPBadge } from '@/components/gamification/XPBadge';
import { ProgressRing } from '@/components/progress/ProgressRing';
import {
  ArrowLeft,
  Play,
  ChevronLeft,
  ChevronRight,
  Check,
  X,
  Cloud,
  CloudOff,
  CheckCircle,
} from 'lucide-react';
import { cn } from '@/lib/utils';

type ViewState = 'list' | 'study' | 'complete';

const mockFlashcardSets = [
  {
    id: '1',
    title: 'Physics Formulas',
    subject: 'Physics',
    cards: 25,
    mastered: 15,
    xpReward: 15,
    isOfflineAvailable: true,
  },
  {
    id: '2',
    title: 'Chemistry Elements',
    subject: 'Chemistry',
    cards: 30,
    mastered: 20,
    xpReward: 15,
    isOfflineAvailable: true,
  },
  {
    id: '3',
    title: 'Math Theorems',
    subject: 'Mathematics',
    cards: 18,
    mastered: 5,
    xpReward: 15,
    isOfflineAvailable: false,
  },
];

const mockCards = [
  {
    id: '1',
    front: "What is Newton's First Law?",
    back:
      'An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an external force.',
  },
  { id: '2', front: 'Formula for Kinetic Energy?', back: 'KE = ½mv²' },
  {
    id: '3',
    front: 'What is acceleration?',
    back: 'The rate of change of velocity with respect to time.',
  },
];

const FlashcardsPage: React.FC = () => {
  const [view, setView] = useState<ViewState>('list');
  const [selectedSet, setSelectedSet] = useState<string | null>(null);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  const currentCard = mockCards[currentCardIndex];

  /* ---------------- RESET HELPERS ---------------- */
  const resetStudy = () => {
    setCurrentCardIndex(0);
    setIsFlipped(false);
    setSelectedSet(null);
    setView('list');
  };

  /* ================= STUDY VIEW ================= */
  if (view === 'study' && selectedSet) {
    return (
      <div className="min-h-screen bg-background">
        <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
          <div className="container mx-auto px-4 py-4 flex justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={resetStudy}>
                <ArrowLeft className="w-5 h-5" />
              </Button>
              <div>
                <h1 className="text-xl font-bold">Review Mode</h1>
                <p className="text-sm text-muted-foreground">
                  Card {currentCardIndex + 1} of {mockCards.length}
                </p>
              </div>
            </div>
            <XPBadge xp={15} size="sm" />
          </div>
        </header>

        <main className="container mx-auto px-4 py-8">
          {/* Progress */}
          <div className="flex justify-center mb-6 gap-1">
            {mockCards.map((_, index) => (
              <div
                key={index}
                className={cn(
                  'w-8 h-2 rounded-full',
                  index < currentCardIndex
                    ? 'bg-success'
                    : index === currentCardIndex
                    ? 'bg-primary'
                    : 'bg-secondary'
                )}
              />
            ))}
          </div>

          {/* Flashcard */}
          <div
            className="max-w-lg mx-auto cursor-pointer"
            onClick={() => setIsFlipped(!isFlipped)}
          >
            <div
              className="relative w-full aspect-[3/2] transition-all duration-500"
              style={{
                transformStyle: 'preserve-3d',
                transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
              }}
            >
              {/* Front */}
              <div
                className="absolute inset-0 p-8 rounded-2xl bg-gradient-primary text-primary-foreground shadow-lg flex flex-col items-center justify-center text-center"
                style={{ backfaceVisibility: 'hidden' }}
              >
                <p className="text-xs uppercase opacity-70 mb-4">Question</p>
                <p className="text-xl font-semibold">{currentCard.front}</p>
                <p className="text-sm opacity-70 mt-4">Tap to reveal</p>
              </div>

              {/* Back */}
              <div
                className="absolute inset-0 p-8 rounded-2xl bg-card border shadow-lg flex flex-col items-center justify-center text-center"
                style={{
                  backfaceVisibility: 'hidden',
                  transform: 'rotateY(180deg)',
                }}
              >
                <p className="text-xs uppercase text-muted-foreground mb-4">
                  Answer
                </p>
                <p className="text-lg font-medium">{currentCard.back}</p>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-center gap-4 mt-8">
            <Button
              variant="outline"
              size="lg"
              disabled={currentCardIndex === 0}
              onClick={() => {
                setIsFlipped(false);
                setCurrentCardIndex((i) => i - 1);
              }}
            >
              <ChevronLeft />
            </Button>

            <Button
              variant="destructive"
              size="lg"
              onClick={() => {
                setIsFlipped(false);
                if (currentCardIndex === mockCards.length - 1) {
                  setView('complete');
                } else {
                  setCurrentCardIndex((i) => i + 1);
                }
              }}
            >
              <X className="mr-1" /> Didn’t Know
            </Button>

            <Button
              variant="success"
              size="lg"
              onClick={() => {
                setIsFlipped(false);
                if (currentCardIndex === mockCards.length - 1) {
                  setView('complete');
                } else {
                  setCurrentCardIndex((i) => i + 1);
                }
              }}
            >
              <Check className="mr-1" /> Got It
            </Button>

            <Button
              variant="outline"
              size="lg"
              disabled={currentCardIndex === mockCards.length - 1}
              onClick={() => {
                setIsFlipped(false);
                setCurrentCardIndex((i) => i + 1);
              }}
            >
              <ChevronRight />
            </Button>
          </div>
        </main>
      </div>
    );
  }

  /* ================= COMPLETE VIEW ================= */
  if (view === 'complete') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-4">
          <CheckCircle className="w-12 h-12 mx-auto text-success" />
          <h2 className="text-2xl font-bold">Session Complete 🎉</h2>
          <p className="text-muted-foreground">You earned XP for studying!</p>
          <Button onClick={resetStudy}>Back to Flashcards</Button>
        </div>
      </div>
    );
  }

  /* ================= LIST VIEW ================= */
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
            <h1 className="text-xl font-bold">Flashcards</h1>
            <p className="text-sm text-muted-foreground">
              Review and memorize concepts
            </p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 grid gap-4">
        {mockFlashcardSets.map((set) => {
          const progress = Math.round((set.mastered / set.cards) * 100);
          return (
            <div
              key={set.id}
              className="p-5 rounded-xl bg-card border hover:shadow-md transition"
            >
              <div className="flex justify-between">
                <div className="flex gap-4">
                  <ProgressRing progress={progress} size={60} />
                  <div>
                    <h3 className="font-semibold">{set.title}</h3>
                    <p className="text-sm text-muted-foreground">
                      {set.subject} • {set.mastered}/{set.cards} mastered
                    </p>
                    <p className="text-xs mt-1 flex items-center gap-1">
                      {set.isOfflineAvailable ? (
                        <>
                          <Cloud className="w-3 h-3" /> Offline available
                        </>
                      ) : (
                        <>
                          <CloudOff className="w-3 h-3" /> Online only
                        </>
                      )}
                    </p>
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <XPBadge xp={set.xpReward} size="sm" />
                  <Button
                    size="sm"
                    onClick={() => {
                      setSelectedSet(set.id);
                      setView('study');
                    }}
                  >
                    <Play className="w-4 h-4 mr-1" />
                    Review
                  </Button>
                </div>
              </div>
            </div>
          );
        })}
      </main>
    </div>
  );
};

export default FlashcardsPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\student\NotesPage.tsx`

```tsx
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { XPBadge } from "@/components/gamification/XPBadge";
import { useOnlineStatus } from "@/contexts/OnlineContext";
import {
  ArrowLeft,
  FileText,
  Plus,
  Download,
  Search,
  WifiOff,
  CheckCircle,
  CloudOff,
  Eye,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

/* === KaTeX + Markdown support (non-visual) === */
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

const NOTES_CACHE_KEY = "student_notes_cache_v1";

type NoteItem = {
  id: string;
  title: string;
  subject: string;
  chapter: string;
  createdAt: Date;
  xpEarned: number;
  isOfflineAvailable: boolean;
  pages: number;
};

const NotesPage: React.FC = () => {
  const { isOnline } = useOnlineStatus();

  const [searchQuery, setSearchQuery] = useState("");
  const [showGenerateForm, setShowGenerateForm] = useState(false);
  const [notesList, setNotesList] = useState<NoteItem[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const [subject, setSubject] = useState("");
  const [chapter, setChapter] = useState("");
  const [difficulty, setDifficulty] = useState("medium");

  /* === Load cached notes on boot === */
  useEffect(() => {
    const cached = localStorage.getItem(NOTES_CACHE_KEY);
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        setNotesList(
          parsed.map((n: any) => ({
            ...n,
            createdAt: new Date(n.createdAt),
          }))
        );
      } catch {
        localStorage.removeItem(NOTES_CACHE_KEY);
      }
    }
  }, []);

  /* === Persist cache === */
  useEffect(() => {
    if (notesList.length > 0) {
      localStorage.setItem(NOTES_CACHE_KEY, JSON.stringify(notesList));
    }
  }, [notesList]);

  const filteredNotes = notesList.filter(
    (note) =>
      note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      note.subject.toLowerCase().includes(searchQuery.toLowerCase())
  );

  /* === Backend integration: Generate Notes === */
  const handleGenerateNotes = async () => {
    if (!subject || !chapter) return;

    setIsGenerating(true);

    try {
      const res = await fetch(
        "http://localhost:8000/api/student/notes/generate",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            subject,
            chapter,
            difficulty,
            context: {
              client_type: window.innerWidth < 768 ? "mobile" : "desktop",
              connectivity: navigator.onLine ? "online" : "offline",
              model_capability: navigator.onLine ? "heavy" : "light",
            },
          }),
        }
      );

      if (!res.ok) throw new Error("Failed to generate notes");

      const data = await res.json();

      const newNote: NoteItem = {
        id: data.content_id ?? crypto.randomUUID(),
        title: chapter,
        subject,
        chapter,
        createdAt: new Date(),
        xpEarned: 25,
        isOfflineAvailable: true,
        pages: Math.max(5, Math.ceil((data.content?.length || 1000) / 800)),
      };

      setNotesList((prev) => [newNote, ...prev]);
      setShowGenerateForm(false);

      setSubject("");
      setChapter("");
      setDifficulty("medium");
    } catch (err) {
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  /* === PDF export (KaTeX-safe, UI-neutral) === */
  const exportNoteAsPDF = () => {
    const win = window.open("", "_blank");
    if (!win) return;

    win.document.write(`
      <html>
        <head>
          <title>Notes</title>
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
          <style>
            body { font-family: serif; padding: 24px; }
          </style>
        </head>
        <body>
          <p>Rendered notes content will appear here.</p>
        </body>
      </html>
    `);

    win.document.close();
    win.print();
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Link to="/student">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <div>
              <h1 className="text-xl font-display font-bold text-foreground">
                Notes
              </h1>
              <p className="text-sm text-muted-foreground">
                AI-generated study notes
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search notes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>

          <Button
            className="flex items-center gap-2"
            onClick={() => setShowGenerateForm(true)}
            disabled={!isOnline}
          >
            {!isOnline ? (
              <WifiOff className="w-4 h-4" />
            ) : (
              <Plus className="w-4 h-4" />
            )}
            Generate Notes
            <XPBadge xp={25} />
          </Button>
        </div>

        {/* Generate Modal */}
        {showGenerateForm && (
          <div className="mb-6 p-6 rounded-xl bg-card border border-border shadow-lg animate-scale-in">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Generate Notes</h2>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setShowGenerateForm(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              <div className="space-y-4">
                <Input
                  placeholder="Subject"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                />
                <Input
                  placeholder="Chapter / Topic"
                  value={chapter}
                  onChange={(e) => setChapter(e.target.value)}
                />
                <Input
                  placeholder="Difficulty (easy / medium / hard)"
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                />

                <Button
                  className="w-full"
                  onClick={handleGenerateNotes}
                  disabled={isGenerating}
                >
                  {isGenerating ? "Generating..." : "Generate (+25 XP)"}
                </Button>
              </div>
            </div>
        )}

        {/* Notes List */}
        <div className="grid gap-4">
          {filteredNotes.map((note) => (
            <div
              key={note.id}
              className="p-4 rounded-xl bg-card border hover:shadow-sm transition"
            >
              <div className="flex justify-between">
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-lg bg-primary/10">
                    <FileText className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">
                      {note.title}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {note.subject} • {note.chapter} • {note.pages} pages
                    </p>
                    <div className="flex items-center gap-3 mt-2">
                      <div className="flex items-center gap-1 text-xs text-success">
                        <CheckCircle className="w-3 h-3" />
                        <span>+{note.xpEarned} XP earned</span>
                      </div>
                      {note.isOfflineAvailable ? (
                        <div className="flex items-center gap-1 text-xs text-muted-foreground">
                          <CheckCircle className="w-3 h-3" />
                          <span>Available offline</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1 text-xs text-muted-foreground">
                          <CloudOff className="w-3 h-3" />
                          <span>Online only</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="icon">
                    <Eye className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={exportNoteAsPDF}
                  >
                    <Download className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredNotes.length === 0 && (
          <div className="text-center py-12">
            <FileText className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold text-foreground mb-2">
              No notes found
            </h3>
            <p className="text-muted-foreground">
              Try adjusting your search or generate new notes.
            </p>
          </div>
        )}
      </main>
    </div>
  );
};

export default NotesPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\student\StudentDashboard.tsx`

```tsx
import React, { useState } from 'react';
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
  Clock,
  TrendingUp,
  Zap,
  Trophy,
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
  weeklyStudyTime: '12h 30m',
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
                  value={`${mockStats.accuracy}%`}
                  icon={Trophy}
                  trend={{ value: 3, isPositive: true }}
                />
                <StatCard
                  title="Study Time"
                  value={mockStats.weeklyStudyTime}
                  icon={Clock}
                  description="This week"
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

```

---

### `frontend\bildofy-lms-lovable\src\pages\student\TestsPage.tsx`

```tsx
import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { XPBadge } from '@/components/gamification/XPBadge';
import { ProgressRing } from '@/components/progress/ProgressRing';
import { useOnlineStatus } from '@/contexts/OnlineContext';
import MarkdownKatexRenderer from '@/components/MarkdownKatexRenderer';
import {
  ArrowLeft,
  ClipboardCheck,
  Clock,
  Target,
  Play,
  Trophy,
  Zap,
  WifiOff,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2 } from "lucide-react";


type Difficulty = 'easy' | 'medium' | 'hard';

type TestSummary = {
  id: number;
  title: string;
  subject: string;
  difficulty: Difficulty;
  total_questions: number;
  duration: number;
  xp_reward: number;
  is_completed: boolean;
  best_score: number | null;
};

type Question = {
  question: string;
  options: string[];
};

type FullTest = {
  id: number;
  title: string;
  questions: Question[];
};

const SUBJECTS = {
  Science: ["Electrostatics", "Magnetism"],
  Mathematics: ["Trigonometry", "Differential Calculus"],
  "Computer Science": ["Basics of Python", "Basics of SQL"],
};
const SUBJECT_ID_MAP: Record<string, number> = {
  Science: 2,
};

const DIFFICULTIES = ["easy", "medium", "hard"] as const;

const difficultyConfig = {
  easy: { label: 'Easy', color: 'bg-success/10 text-success border-success/30' },
  medium: { label: 'Medium', color: 'bg-warning/10 text-warning border-warning/30' },
  hard: { label: 'Hard', color: 'bg-destructive/10 text-destructive border-destructive/30' },
};

const TestsPage: React.FC = () => {
  const { isOnline } = useOnlineStatus();
  const navigate = useNavigate();
  const { testId } = useParams();
  const token = localStorage.getItem('access_token');

  const [tests, setTests] = useState<TestSummary[]>([]);
  const [test, setTest] = useState<FullTest | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [score, setScore] = useState<number | null>(null);
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [showLoadingModal, setShowLoadingModal] = useState(false);

  const [subject, setSubject] = useState<string | null>(null);
  const [chapter, setChapter] = useState<string | null>(null);
  const [difficulty, setDifficulty] = useState<string | null>(null);

  const GENERATION_COOLDOWN_MS = 60 * 1000; // 1 minute (UI only)
  const [lastGeneratedAt, setLastGeneratedAt] = useState<number | null>(null);

  const isOnCooldown =
    lastGeneratedAt !== null &&
    Date.now() - lastGeneratedAt < GENERATION_COOLDOWN_MS;

  const cooldownRemaining = lastGeneratedAt
    ? Math.max(
        0,
        Math.ceil(
          (GENERATION_COOLDOWN_MS - (Date.now() - lastGeneratedAt)) / 1000
        )
      )
    : 0;
  
  const handleGenerateTest = async () => {
    if (!subject || !chapter || !difficulty || isOnCooldown) return;

    setShowGenerateModal(false);
    setShowLoadingModal(true);

    try {
      const res = await fetch(
        "http://localhost:8000/student/tests/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
             title: `${subject} – ${chapter} (${difficulty})`,
              subject_id: SUBJECT_ID_MAP[subject], // always 2
              subject: subject,
              chapter: chapter,
              difficulty: difficulty,
          }),
        }
      );

      if (!res.ok) {
        throw new Error("Failed to generate test");
      }

      // mark cooldown
      setLastGeneratedAt(Date.now());

      // refresh test list
      await fetchTests();
    } catch (err) {
      console.error(err);
    } finally {
      setShowLoadingModal(false);
    }
  };

  /* ================= LIST TESTS ================= */
  const fetchTests = async () => {
  const res = await fetch("http://localhost:8000/student/tests", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();
    setTests(data);
  };

  useEffect(() => {
    if (!token || testId) return;
    fetchTests();
  }, [token, testId]);


  /* ================= LOAD TEST BY ID ================= */
  useEffect(() => {
    if (!token || !testId) return;

    fetch(`http://localhost:8000/student/tests/${testId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => {
        setTest(data);
        setAnswers({});
        setCurrentIndex(0);
        setScore(null);
      });
  }, [token, testId]);

  /* ================= SUBMIT ================= */
  const submitTest = async () => {
    if (!test) return;

    const orderedAnswers = test.questions.map((_, i) => answers[i] ?? '');

    const res = await fetch(
      `http://localhost:8000/student/tests/${test.id}/submit`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ answers: orderedAnswers }),
      }
    );

    const data = await res.json();
    setScore(data.score);
  };

  /* ================= OFFLINE ================= */
  if (!isOnline) {
    return (
      <div className="p-6 text-center text-sm text-muted-foreground">
        <WifiOff className="mx-auto mb-2" />
        Tests require an internet connection.
      </div>
    );
  }

  if (testId && !test) {
    return (
      <div className="p-6 text-center text-muted-foreground">
        Loading test…
      </div>
    );
  }

  /* ================= TEST INTERFACE ================= */
  if (testId && test) {
    const q = test.questions[currentIndex];

    return (
      <div className="min-h-screen bg-background p-6 space-y-6">
        <Button variant="ghost" onClick={() => navigate(`/student/tests/${test.id}`)}>
          <ArrowLeft className="w-4 h-4 mr-1" />
          Back
        </Button>

        {score === null ? (
          <>
            <MarkdownKatexRenderer content={q.question} />

            <div className="space-y-2">
              {q.options.map((opt, idx) => (
                <Button
                  key={idx}
                  variant={answers[currentIndex] === opt ? 'default' : 'outline'}
                  className="w-full justify-start"
                  onClick={() =>
                    setAnswers((a) => ({ ...a, [currentIndex]: opt }))
                  }
                >
                  <MarkdownKatexRenderer content={opt} />
                </Button>
              ))}
            </div>

            <div className="flex justify-between">
              <Button
                variant="outline"
                disabled={currentIndex === 0}
                onClick={() => setCurrentIndex((i) => i - 1)}
              >
                Previous
              </Button>

              {currentIndex === test.questions.length - 1 ? (
                <Button onClick={submitTest}>Submit</Button>
              ) : (
                <Button onClick={() => setCurrentIndex((i) => i + 1)}>
                  Next
                </Button>
              )}
            </div>
          </>
        ) : (
          <div className="text-center">
            <h2 className="text-2xl font-bold">Result</h2>
            <p className="text-lg">
              Score: {score} / {test.questions.length}
            </p>
          </div>
        )}
      </div>
    );
  }

  /* ================= TEST LIST ================= */
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
            <h1 className="text-xl font-display font-bold text-foreground">Tests</h1>
            <p className="text-sm text-muted-foreground">Practice and earn XP</p>
          </div>
        </div>
      </header>
      

      <main className="container mx-auto px-4 py-6">
       <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-display font-semibold text-foreground">
          Available Tests
        </h2>

        <div className="relative">
          <Button
            onClick={() => setShowGenerateModal(true)}
            disabled={isOnCooldown}
          >
            Generate Test
          </Button>


            {/* XP Overlay */}
            <div className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs px-2 py-0.5 rounded-full flex items-center gap-1 shadow">
              <Zap className="w-3 h-3" />
              {isOnCooldown ? `${cooldownRemaining}s` : "+250 XP"}
            </div>
          </div>
        </div>
        <Dialog open={showGenerateModal} onOpenChange={setShowGenerateModal}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Generate Test</DialogTitle>
            </DialogHeader>

            <div className="space-y-4">
              {/* Subject */}
              <Select
                value={subject ?? ""}
                onValueChange={(val) => {
                  setSubject(val);
                  setChapter(null);
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Subject" />
                </SelectTrigger>
                <SelectContent>
                  {Object.keys(SUBJECTS).map((subj) => (
                    <SelectItem key={subj} value={subj}>
                      {subj}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              {/* Chapter */}
              <Select
                value={chapter ?? ""}
                onValueChange={setChapter}
                disabled={!subject}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Chapter" />
                </SelectTrigger>
                <SelectContent>
                  {subject &&
                    SUBJECTS[subject].map((chap) => (
                      <SelectItem key={chap} value={chap}>
                        {chap}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>

              {/* Difficulty */}
              <Select
                value={difficulty ?? ""}
                onValueChange={setDifficulty}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Difficulty" />
                </SelectTrigger>
                <SelectContent>
                  {DIFFICULTIES.map((diff) => (
                    <SelectItem key={diff} value={diff}>
                      {diff.charAt(0).toUpperCase() + diff.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Button
                className="w-full"
                disabled={!subject || !chapter || !difficulty}
                onClick={handleGenerateTest}
              >
                Generate Test
              </Button>
            </div>
          </DialogContent>
        </Dialog>
        
        <Dialog open={showLoadingModal}>
          <DialogContent className="sm:max-w-sm text-center">
            <div className="flex flex-col items-center gap-4 py-6">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
              <p className="text-sm text-muted-foreground">
                Generating your test…
              </p>
            </div>
          </DialogContent>
        </Dialog>


        <div className="grid gap-4">
          {tests.map((test, index) => {
            const difficulty =
              difficultyConfig[test.difficulty as keyof typeof difficultyConfig] ??
              difficultyConfig.medium;

            return (
              <div
                key={test.id}
                className={cn(
                  'p-5 rounded-xl bg-card border border-border shadow-sm transition-all duration-200',
                  'hover:shadow-md hover:border-primary/30',
                  test.is_completed && 'bg-success/5 border-success/20'
                )}
              >

                <div className="flex items-start justify-between gap-4">
                  <div>
                    <span className={cn('text-xs px-2 py-0.5 rounded-full border', difficulty.color)}>
                      {difficulty.label}
                    </span>
                    <h3 className="font-semibold mt-1">{test.title}</h3>
                    <div className="text-sm text-muted-foreground flex gap-4">
                      <span>{test.total_questions} questions</span>
                      <span>{test.duration} min</span>
                    </div>
                  </div>

                  <div className="flex flex-col items-end gap-2">
                    {test.is_completed ? (
                      <>
                        <ProgressRing
                          progress={test.best_score ?? 0}
                          size={50}
                          color="success"
                        />
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => navigate(`/student/tests/${test.id}`)}
                        >
                          Retry
                        </Button>
                      </>
                    ) : (
                      <>
                        <XPBadge xp={test.xp_reward} />
                        <Button
                          size="sm"
                          onClick={() => navigate(`/student/tests/${test.id}`)}
                        >
                          Start Test
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
};

export default TestsPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\student\WatchVideosPage.tsx`

```tsx
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Video } from 'lucide-react';

const WatchVideosPage = () => {
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
            <h1 className="text-xl font-bold">Watch Videos</h1>
            <p className="text-sm text-muted-foreground">
              Visual explanations for better understanding
            </p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12 text-center">
        <Video className="w-14 h-14 mx-auto text-muted-foreground mb-4" />
        <h2 className="text-2xl font-semibold mb-2">
          Video Lessons Coming Soon 🎬
        </h2>
        <p className="text-muted-foreground max-w-md mx-auto">
          This section will include topic-wise video explanations to help you
          learn visually and revise faster.
        </p>

        <Button className="mt-6" asChild>
          <Link to="/student">Back to Dashboard</Link>
        </Button>
      </main>
    </div>
  );
};

export default WatchVideosPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\teacher\AIContentPage.tsx`

```tsx
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Sparkles } from 'lucide-react';

const AIContentPage = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/teacher">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-xl font-bold text-foreground">AI Content</h1>
            <p className="text-sm text-muted-foreground">
              Generate smart teaching materials using AI
            </p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12 text-center">
        <Sparkles className="w-14 h-14 mx-auto text-muted-foreground mb-4" />
        <h2 className="text-2xl font-semibold mb-2">
          AI Content Tools – Coming Soon ✨
        </h2>
        <p className="text-muted-foreground max-w-md mx-auto">
          This section will allow teachers to generate notes, questions,
          assignments, and explanations using AI assistance.
        </p>

        <Button className="mt-6" asChild>
          <Link to="/teacher">Back to Dashboard</Link>
        </Button>
      </main>
    </div>
  );
};

export default AIContentPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\teacher\AnalyticsPage.tsx`

```tsx
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft, BarChart3 } from 'lucide-react';

const AnalyticsPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card border-b">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/teacher">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <h1 className="text-xl font-bold">Class Analytics</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-10 text-center">
        <BarChart3 className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
        <p className="text-muted-foreground">
          Analytics and performance insights will be available here.
        </p>
      </main>
    </div>
  );
};

export default AnalyticsPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\teacher\CreateAssignmentPage.tsx`

```tsx
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ArrowLeft, FileText } from 'lucide-react';

const CreateAssignmentPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card border-b">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/teacher">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <h1 className="text-xl font-bold">Create Assignment</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-xl space-y-4">
        <Input placeholder="Assignment Title" />
        <Input placeholder="Subject" />
        <Input placeholder="Description" />
        <Input type="date" />
        <Input type="number" placeholder="XP Reward" />

        <Button className="w-full gap-2">
          <FileText className="w-4 h-4" />
          Create Assignment
        </Button>
      </main>
    </div>
  );
};

export default CreateAssignmentPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\teacher\CreateTestPage.tsx`

```tsx
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ArrowLeft, ClipboardCheck } from 'lucide-react';

const CreateTestPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card border-b">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/teacher">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <h1 className="text-xl font-bold">Create Test</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-xl space-y-4">
        <Input placeholder="Test Title" />
        <Input placeholder="Subject" />
        <Input type="number" placeholder="Number of Questions" />
        <Input type="number" placeholder="Duration (minutes)" />
        <Input type="number" placeholder="XP Reward" />

        <Button className="w-full gap-2">
          <ClipboardCheck className="w-4 h-4" />
          Create Test
        </Button>
      </main>
    </div>
  );
};

export default CreateTestPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\teacher\SubmissionsPage.tsx`

```tsx
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

const SubmissionsPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card border-b">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/teacher">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <h1 className="text-xl font-bold">Student Submissions</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-10 text-center">
        <p className="text-muted-foreground">
          Student submissions will appear here.
        </p>
      </main>
    </div>
  );
};

export default SubmissionsPage;

```

---

### `frontend\bildofy-lms-lovable\src\pages\teacher\TeacherDashboard.tsx`

```tsx
import React from 'react';
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

const mockStats = {
  totalStudents: 156,
  activeAssignments: 8,
  testsCreated: 24,
  avgClassScore: 72,
};

const recentActivity = [
  { id: '1', action: 'Created test', item: 'Physics Chapter 5', time: '2 hours ago' },
  { id: '2', action: 'Graded assignment', item: 'Math Homework Set 3', time: '4 hours ago' },
  { id: '3', action: 'AI generated notes', item: 'Chemistry Bonding', time: 'Yesterday' },
];

const TeacherDashboard: React.FC = () => {
  const navigate = useNavigate();

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
        <div className="mb-8 animate-fade-up">
          <h1 className="text-2xl md:text-3xl font-display font-bold text-foreground">
            Teacher Dashboard
          </h1>
          <p className="text-muted-foreground mt-1">
            Manage your classes, create content, and track student progress.
          </p>
        </div>

        {/* Quick Actions */}
        <section className="mb-8 animate-fade-up" style={{ animationDelay: '0.1s' }}>
          <h2 className="text-lg font-display font-semibold text-foreground mb-4">
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

        {/* Stats */}
        <section className="mb-8 animate-fade-up" style={{ animationDelay: '0.2s' }}>
          <h2 className="text-lg font-display font-semibold text-foreground mb-4">
            Overview
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Students"
              value={mockStats.totalStudents}
              icon={Users}
            />
            <StatCard
              title="Active Assignments"
              value={mockStats.activeAssignments}
              icon={BookOpen}
            />
            <StatCard
              title="Tests Created"
              value={mockStats.testsCreated}
              icon={ClipboardCheck}
            />
            <StatCard
              title="Class Average"
              value={`${mockStats.avgClassScore}%`}
              icon={TrendingUp}
              trend={{ value: 5, isPositive: true }}
            />
          </div>
        </section>

        {/* Recent Activity */}
        <section className="animate-fade-up" style={{ animationDelay: '0.3s' }}>
          <h2 className="text-lg font-display font-semibold text-foreground mb-4">
            Recent Activity
          </h2>
          <div className="bg-card border border-border rounded-xl divide-y divide-border">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="p-4 flex items-center justify-between">
                <div>
                  <p className="font-medium text-foreground">{activity.action}</p>
                  <p className="text-sm text-muted-foreground">{activity.item}</p>
                </div>
                <span className="text-sm text-muted-foreground">
                  {activity.time}
                </span>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default TeacherDashboard;

```

---

### `backend\app\config.py`

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI LMS Backend"
    APP_ENV: Literal["local", "staging", "production"] = "local"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_TIMEOUT_SECONDS: int = 120

    # Model routing
    OFFLINE_MODEL_NAME: str = "phi3:mini"
    ONLINE_MODEL_NAME: str = "mistral:7b-instruct"

    # Payload limits
    MAX_RESPONSE_KB_MOBILE: int = 256
    MAX_RESPONSE_KB_DESKTOP: int = 1024

    # Database
    DATABASE_URL: str

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # ✅ THIS IS THE IMPORTANT PART
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",   # <-- ignore unknown env vars
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7



@lru_cache
def get_settings() -> Settings:
    return Settings()

```

---

### `backend\app\loop_fix.py`

```python
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

```

---

### `backend\app\main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.logging.middleware import logging_middleware
from app.middleware.audit import AuditMiddleware

# 🔹 Routers
from app.routers import auth
from app.routers import subjects
from app.routers import teacher_tests

from app.routers.student import (
    notes_router,
    flashcards_router,
    tests_router,
    ai_chat_router,
    progress_router,
    sync_router,
    teacher_notes_router,
    subjects as student_subjects,
)

from app.routers.teacher import (
    assignments_router,
    tests_router as teacher_tests_router,
    ai_tools_router,
    reports_router,
    students as teacher_students,
)

from app.routers.parent import (
    overview_router as parent_overview_router,
    progress_router as parent_progress_router,
    insights_router as parent_insights_router,
)

from app.routers.admin import (
    users_router as admin_users_router,
    content_router as admin_content_router,
    system_router as admin_system_router,
)



# -------------------------------------------------------------------

settings = get_settings()

# ✅ CREATE FASTAPI APP
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# -------------------------------------------------------------------
# 🔹 Middleware
# -------------------------------------------------------------------

app.middleware("http")(logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuditMiddleware)


# -------------------------------------------------------------------
# 🔹 Routers
# -------------------------------------------------------------------

# Auth
app.include_router(auth.router)

# Subjects (admin-only)
app.include_router(subjects.router)

# Student routers
app.include_router(notes_router)
app.include_router(flashcards_router)
app.include_router(tests_router)
app.include_router(ai_chat_router)
app.include_router(progress_router)
app.include_router(sync_router)
app.include_router(teacher_notes_router)
app.include_router(student_subjects.router)

# Teacher routers
app.include_router(assignments_router)
app.include_router(teacher_tests_router)
app.include_router(ai_tools_router)
app.include_router(reports_router)
app.include_router(teacher_students.router)

# Parent routers
app.include_router(parent_overview_router)
app.include_router(parent_progress_router)
app.include_router(parent_insights_router)

# Admin routers
app.include_router(admin_users_router)
app.include_router(admin_content_router)
app.include_router(admin_system_router)
app.include_router(teacher_tests.router)

# -------------------------------------------------------------------
# 🔹 Health & Meta
# -------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/version")
async def version():
    return {
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
    }

```

---

### `backend\app\__init__.py`

```python

```

---

### `backend\app\ai\__init__.py`

```python
from app.ai.ollama_client import OllamaClient
from app.ai.model_router import select_model

```

---

### `backend\app\logging\__init__.py`

```python
from app.logging.logger import logger
from app.logging.middleware import logging_middleware

```

---

### `backend\app\models\__init__.py`

```python
from app.models.users import User
from app.models.notes import GeneratedNote
from app.models.tests import Test
from app.models.assignments import Assignment
from app.models.flashcards import FlashcardSet
from app.models.progress import Progress

```

---

### `backend\app\rag\__init__.py`

```python
from app.rag.context_builder import build_context
from app.rag.retriever import VectorRetriever
from app.rag.guardrails import validate_context

```

---

### `backend\app\routers\admin\__init__.py`

```python
from app.routers.admin.users import router as users_router
from app.routers.admin.content import router as content_router
from app.routers.admin.system import router as system_router

```

---

### `backend\app\routers\parent\__init__.py`

```python
from app.routers.parent.overview import router as overview_router
from app.routers.parent.progress import router as progress_router
from app.routers.parent.insights import router as insights_router

```

---

### `backend\app\routers\student\__init__.py`

```python
from app.routers.student.notes import router as notes_router
from app.routers.student.flashcards import router as flashcards_router
from app.routers.student.tests import router as tests_router
from app.routers.student.ai_chat import router as ai_chat_router
from app.routers.student.progress import router as progress_router
from app.routers.student.sync import router as sync_router
from app.routers.student.teacher_notes import router as teacher_notes_router

```

---

### `backend\app\routers\teacher\__init__.py`

```python
from app.routers.teacher.assignments import router as assignments_router
from app.routers.teacher.tests import router as tests_router
from app.routers.teacher.ai_tools import router as ai_tools_router
from app.routers.teacher.reports import router as reports_router
from app.routers.teacher.notes import router as notes_router

```

---

### `backend\app\schemas\__init__.py`

```python
from app.schemas.common import ClientContext
from app.schemas.user import UserResponse
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.schemas.tests import TestCreateRequest, TestResponse
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse
from app.schemas.flashcards import FlashcardSetResponse
from app.schemas.progress import ProgressResponse

```

---

### `backend\app\security\__init__.py`

```python
from app.security.guards import enforce_client_capabilities
from app.security.rate_limiter import rate_limit
from app.security.admin_guard import require_admin
from app.security.roles import Role
from app.security.dependencies import get_current_user, require_role

```

---

### `backend\app\services\__init__.py`

```python
from app.services.notes_service import generate_notes
from app.services.flashcards_service import generate_flashcards
from app.services.test_service import generate_test
from app.services.ai_service import chat_with_ai
from app.services.xp_service import apply_xp_event

from app.services.teacher_assignment_service import create_assignment
from app.services.teacher_test_service import (
    create_test_manual,
    create_test_ai_assisted,
)
from app.services.teacher_ai_service import (
    suggest_test_questions,
    suggest_assignment_outline,
)
from app.services.teacher_report_service import get_student_report

from app.services.parent_overview_service import (
    get_parent_overview,
    get_detailed_progress,
)
from app.services.parent_insights_service import get_parent_insights

from app.services.admin_user_service import (
    list_users,
    get_user,
    update_user_role,
    disable_user,
)
from app.services.admin_system_service import get_system_status
from app.services.teacher_notes_service import (
    create_manual_notes,
    create_ai_assisted_notes,
    upload_notes_file,
)
from app.services.file_validation import validate_upload

```

---

### `backend\app\ai\model_router.py`

```python
from app.schemas.common import ClientContext
from app.config import get_settings

settings = get_settings()


def select_model(context: ClientContext) -> str:
    """
    Determines which model to use based on client capabilities.
    """

    # Offline or light-capability clients always use the lightweight model
    if context.connectivity == "offline" or context.model_capability == "light":
        return settings.OFFLINE_MODEL_NAME

    # Online + heavy-capability clients use the server-grade model
    return settings.ONLINE_MODEL_NAME

```

---

### `backend\app\ai\ollama_client.py`

```python
import httpx
from typing import Dict, Any
from app.config import get_settings

settings = get_settings()


class OllamaClient:
    def __init__(self) -> None:
        self.base_url = settings.OLLAMA_BASE_URL
        self.timeout = settings.OLLAMA_TIMEOUT_SECONDS

    async def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def generate(
        self,
        prompt: str,
        model_name: str,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> str:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "stream": False,
        }

        result = await self._post(payload)
        return result.get("response", "").strip()

```

---

### `backend\app\db\base.py`

```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# existing imports
from app.models.user import User
from app.models.subject import Subject
from app.models.classroom import Classroom

# WC-2 imports
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.test_attempt import TestAttempt
from app.models.test_answer import TestAnswer

```

---

### `backend\app\db\base_imports.py`

```python
# Import all models here so Base.metadata knows about them\
from app.models.user import User
from app.models.progress import Progress
from app.models.classroom import Classroom
# add others as needed
from app.models.subject import Subject
from app.models.subject_student import SubjectStudent

```

---

### `backend\app\db\init_db.py`

```python
import asyncio
from app.db.session import engine
from app.db.base import Base
import app.db.base_imports  # IMPORTANT

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())

```

---

### `backend\app\db\session.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

```

---

### `backend\app\logging\logger.py`

```python
from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "{message}",
)

```

---

### `backend\app\logging\middleware.py`

```python
from fastapi import Request
from app.logging.logger import logger
import time


async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = int((time.time() - start_time) * 1000)

    logger.info(
        f"{request.method} {request.url.path} "
        f"{response.status_code} {duration}ms"
    )

    return response

```

---

### `backend\app\middleware\audit.py`

```python
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.session import AsyncSessionLocal
from app.models.audit_log import AuditLog


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        user_id = getattr(request.state, "user_id", None)

        async with AsyncSessionLocal() as db:
            db.add(
                AuditLog(
                    user_id=user_id,
                    action=request.method,
                    endpoint=request.url.path,
                )
            )
            await db.commit()

        return response

```

---

### `backend\app\models\assignments.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.session import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)

    due_date = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\routers\student\assignments.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...db.session import get_db
from ...repositories.assignment_repo import AssignmentRepo
from ...schemas.assignments import AssignmentOut
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/assignments", tags=["student.assignments"], dependencies=[student_guard])
repo = AssignmentRepo()


@router.get("/", response_model=list[AssignmentOut])
async def list_assignments(db: AsyncSession = Depends(get_db)):
    rows = await repo.list(db)
    return rows

```

---

### `backend\app\routers\teacher\assignments.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse
from app.services.teacher_assignment_service import create_assignment
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/assignments", tags=["Teacher Assignments"])


@router.post("/create", response_model=AssignmentResponse)
async def create_assignment_endpoint(
    payload: AssignmentCreateRequest,
    assignment_type: Literal["LMS_ATTEMPT", "PDF_UPLOAD"],
    db: AsyncSession = Depends(get_db),
):
    """
    assignment_type:
    - LMS_ATTEMPT → student answers inside LMS
    - PDF_UPLOAD → student uploads a PDF
    """
    return await create_assignment(payload, assignment_type, db)

```

---

### `backend\app\schemas\assignments.py`

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class AssignmentCreateRequest(BaseModel):
    title: str
    subject: str
    description: Optional[str] = None
    due_date: datetime


class AssignmentResponse(BaseModel):
    id: int
    title: str
    subject: str
    due_date: datetime

```

---

### `backend\app\models\audit_log.py`

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\models\classroom.py`

```python
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Classroom(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Integer, nullable=False)
    section = Column(String, nullable=False)  # A, B, C
    code_prefix = Column(String, unique=True, nullable=False)  # e.g. "1103"

```

---

### `backend\app\models\flashcards.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class FlashcardSet(Base):
    __tablename__ = "flashcard_sets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    subject = Column(String(100), nullable=False)
    chapter = Column(String(200), nullable=False)

    cards = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\routers\student\flashcards.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.common import ClientContext
from app.services.flashcards_service import generate_flashcards
from app.services.xp_service import apply_xp_event
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/flashcards", tags=["Student Flashcards"], dependencies=[student_guard])


@router.post("/generate")
async def generate_flashcards_endpoint(
    subject: str,
    chapter: str,
    context: ClientContext,
    db: AsyncSession = Depends(get_db),
):
    response = await generate_flashcards(subject, chapter, context)
    await apply_xp_event(db, user_id=1, event="FLASHCARDS_REVIEWED")
    return response

```

---

### `backend\app\schemas\flashcards.py`

```python
from pydantic import BaseModel
from typing import List


class Flashcard(BaseModel):
    front: str
    back: str


class FlashcardSetResponse(BaseModel):
    set_id: int
    subject: str
    chapter: str
    cards: List[Flashcard]

```

---

### `backend\app\models\notes.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class GeneratedNote(Base):
    __tablename__ = "generated_notes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    subject = Column(String(100), nullable=False)
    chapter = Column(String(200), nullable=False)
    difficulty = Column(String(20), nullable=False)

    pdf_url = Column(String(500), nullable=False)

    # 🔑 renamed from `metadata`
    extra_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\routers\student\notes.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.services.notes_service import generate_notes
from app.services.xp_service import apply_xp_event
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/notes", tags=["Student Notes"], dependencies=[student_guard])


@router.post("/generate")
async def generate_notes_endpoint(
    payload: NotesGenerateRequest,
     db: AsyncSession = Depends(get_db),
):
    response = await generate_notes(payload, db)
    await apply_xp_event(db, user_id=1, event="NOTES_GENERATED")
    return response

```

---

### `backend\app\routers\teacher\notes.py`

```python
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.routers.teacher._guards import teacher_guard
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.services.teacher_notes_service import (
    create_manual_notes,
    create_ai_assisted_notes,
    upload_notes_file,
)

router = APIRouter(
    prefix="/api/teacher/notes",
    tags=["Teacher Notes"],
    dependencies=[teacher_guard],
)


@router.post("/create")
async def create_notes(
    payload: NotesGenerateRequest,
    creation_mode: Literal["MANUAL", "AI_ASSISTED"],
    db: AsyncSession = Depends(get_db),
):
    """
    MANUAL → teacher writes content fully
    AI_ASSISTED → teacher provides outline, AI expands
    """
    if creation_mode == "AI_ASSISTED":
        return await create_ai_assisted_notes(payload, db)

    return await create_manual_notes(payload, db)


@router.post("/upload")
async def upload_notes(
    subject: str,
    chapter: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload teacher-created notes (PDF).
    """
    return await upload_notes_file(subject, chapter, file, db)

```

---

### `backend\app\schemas\notes.py`

```python
from pydantic import BaseModel
from typing import Optional
from app.schemas.common import ClientContext


class NotesGenerateRequest(BaseModel):
    subject: str
    chapter: str
    difficulty: str
    context: ClientContext


class NotesResponse(BaseModel):
    content_id: str
    summary: str
    pdf_url: Optional[str] = None
    offline_ready: bool
    expires_at: Optional[str] = None
```

---

### `backend\app\models\progress.py`

```python
from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    stats = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress")

```

---

### `backend\app\routers\parent\progress.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.parent_overview_service import get_detailed_progress

router = APIRouter(prefix="/api/parent/progress", tags=["Parent Progress"])


@router.get("/child/{student_id}")
async def parent_child_progress(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Detailed progress breakdown for a parent.
    """
    return await get_detailed_progress(student_id, db)

```

---

### `backend\app\routers\student\progress.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.progress import Progress
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/progress", tags=["Student Progress"], dependencies=[student_guard])


@router.get("/")
async def get_progress(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Progress).where(Progress.user_id == 1))
    progress = result.scalar_one_or_none()

    return progress or {"xp": 0, "level": 1, "stats": {}}

```

---

### `backend\app\schemas\progress.py`

```python
from pydantic import BaseModel


class ProgressResponse(BaseModel):
    xp: int
    level: int
    stats: dict | None = None

```

---

### `backend\app\models\subject.py`

```python
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.base import Base


class SubjectType(str, enum.Enum):
    core = "core"
    elective = "elective"
    extracurricular = "extracurricular"


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    type = Column(Enum(SubjectType), nullable=False)

    # Core subjects only
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)

    # Exactly one teacher
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 🔽 Phase 2.4 additions (nullable by design)
    max_students = Column(Integer, nullable=True)
    enrollment_open_at = Column(DateTime, nullable=True)
    enrollment_close_at = Column(DateTime, nullable=True)

    teacher = relationship("User", foreign_keys=[teacher_id])

```

---

### `backend\app\schemas\subject.py`

```python
from pydantic import BaseModel
from typing import Optional
from enum import Enum


class SubjectType(str, Enum):
    core = "core"
    elective = "elective"


class SubjectCreateRequest(BaseModel):
    name: str
    type: SubjectType
    class_id: Optional[int] = None
    teacher_id: int


class SubjectResponse(BaseModel):
    id: int
    name: str
    type: SubjectType
    class_id: Optional[int]
    teacher_id: int

```

---

### `backend\app\models\subject_student.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.db.base import Base


class SubjectStudent(Base):
    __tablename__ = "subject_students"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("subject_id", "student_id", name="uq_subject_student"),
    )

```

---

### `backend\app\models\test.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_by_student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    difficulty = Column(String(length=20), nullable=False)

    total_questions = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


```

---

### `backend\app\models\tests.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255), nullable=False)
    subject = Column(String(100), nullable=False)
    difficulty = Column(String(20), nullable=False)

    questions = Column(JSON, nullable=False)
    total_marks = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\routers\student\tests.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.test_attempt import TestAttempt

from app.db.session import get_db
from app.services.teacher_test_service import create_test_ai_assisted
from app.schemas.tests import TestCreateRequest
from app.security import get_current_user
from app.models.user import User, UserRole
from app.models.tests import Test
from app.schemas.test_submission import (
    TestSubmissionRequest,
    TestSubmissionResponse,
)
from app.services.test_evaluation_service import TestEvaluationService


router = APIRouter(prefix="/student/tests", tags=["Student Tests"])


@router.get("/{test_id}")
async def get_test_for_student(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can access tests",
        )

    result = await db.execute(
        select(Test).where(Test.id == test_id)
    )
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found",
        )

    return {
        "id": test.id,
        "title": test.title,
        "subject": test.subject,
        "difficulty": test.difficulty,
        "questions": test.questions or []
    }


@router.post(
    "/{test_id}/submit",
    response_model=TestSubmissionResponse,
)
async def submit_test(
    test_id: int,
    payload: TestSubmissionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can submit tests",
        )

    try:
        result = await TestEvaluationService.submit_test(
            db=db,
            test_id=test_id,
            student=current_user,
            submitted_answers=payload.answers,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return result

@router.get("")
async def list_tests_for_student(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view tests",
        )

    tests_result = await db.execute(
        select(Test).order_by(Test.created_at.desc())
    )
    tests = tests_result.scalars().all()

    response = []

    for t in tests:
        # Fetch attempts for this student & test
        attempts_result = await db.execute(
            select(
                func.max(TestAttempt.score),
                func.count(TestAttempt.id),
            ).where(
                TestAttempt.test_id == t.id,
                TestAttempt.student_id == current_user.id,
            )
        )
        best_score, attempt_count = attempts_result.one()

        questions = t.questions or []

        response.append(
            {
                "id": t.id,
                "title": t.title,
                "subject": t.subject,
                "difficulty": t.difficulty,
                "total_questions": len(questions),

                # --------- Aggregated fields ---------
                "duration": len(questions),
                "xp_reward": 0,                 # XP shell untouched
                "is_completed": attempt_count > 0,
                "best_score": best_score,
            }
        )

    return response

@router.post("/generate")
async def generate_test_for_student(
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can generate tests",
        )

    subject_id = payload.get("subject_id")
    chapter = payload.get("chapter")
    subject = payload.get("subject")

    if not subject_id or not chapter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="subject_id and chapter are required",
        )

    # Reuse existing AI-assisted test creation
    test_request = TestCreateRequest(
        title=f"Practice Test - {chapter}",
        subject_id=subject_id,
        subject = subject,
        difficulty="medium",
        chapter=chapter,
        ai_assisted=True,
    )

    test = await create_test_ai_assisted(test_request, db)
    return {"id": test.id, "title": test.title}



```

---

### `backend\app\routers\teacher\tests.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.db.session import get_db
from app.schemas.tests import TestCreateRequest, TestResponse
from app.services.teacher_test_service import (
    create_test_manual,
    create_test_ai_assisted,
)
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/tests", tags=["Teacher Tests"])


@router.post("/create", response_model=TestResponse)
async def create_test_endpoint(
    payload: TestCreateRequest,
    creation_mode: Literal["MANUAL", "AI_ASSISTED"],
    db: AsyncSession = Depends(get_db),
):
    """
    creation_mode:
    - MANUAL → teacher provides all questions
    - AI_ASSISTED → AI suggests questions & answers
    """
    if creation_mode == "AI_ASSISTED":
        return await create_test_ai_assisted(payload, db)

    return await create_test_manual(payload, db)

```

---

### `backend\app\schemas\tests.py`

```python
from pydantic import BaseModel
from typing import List


class TestQuestion(BaseModel):
    question: str
    options: List[str]
    correct_option: int


class TestCreateRequest(BaseModel):
    title: str
    subject_id: int
    subject: str
    chapter: str
    difficulty: str
    ai_assisted: bool


class TestResponse(BaseModel):
    test_id: int
    title: str
    total_marks: int

```

---

### `backend\app\models\test_answer.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class TestAnswer(Base):
    __tablename__ = "test_answers"

    id = Column(Integer, primary_key=True, index=True)

    test_attempt_id = Column(
        Integer,
        ForeignKey("test_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question_index = Column(Integer, nullable=False)
    
    selected_answer = Column(String(length=255), nullable=False)

    is_correct = Column(Boolean, nullable=False)

```

---

### `backend\app\models\test_attempt.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class TestAttempt(Base):
    __tablename__ = "test_attempts"

    id = Column(Integer, primary_key=True, index=True)

    test_id = Column(
        Integer,
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    score = Column(Integer, nullable=False)

    submitted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

```

---

### `backend\app\models\test_question.py`

```python
from sqlalchemy import Column, Integer, ForeignKey, Text, JSON, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)

    test_id = Column(
        Integer,
        ForeignKey("tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question_text = Column(Text, nullable=False)

    options = Column(JSON, nullable=False)

    correct_answer = Column(String(length=255), nullable=False)

    question_order = Column(Integer, nullable=False)
    
```

---

### `backend\app\models\user.py`

```python
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    parent = "parent"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)

    progress = relationship("Progress", back_populates="user", uselist=False)

```

---

### `backend\app\schemas\user.py`

```python
from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    role: str
    full_name: str
    email: str
    grade: str | None = None
    board: str | None = None


class UserResponse(UserBase):
    pass

```

---

### `backend\app\models\users.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20), nullable=False)  # student | teacher | parent
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)

    grade = Column(String(20), nullable=True)
    board = Column(String(50), nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

```

---

### `backend\app\routers\admin\users.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.admin_user_service import (
    list_users,
    get_user,
    update_user_role,
    disable_user,
)

router = APIRouter(prefix="/api/admin/users", tags=["Admin Users"])


@router.get("/")
async def admin_list_users(
    db: AsyncSession = Depends(get_db),
):
    return await list_users(db)


@router.get("/{user_id}")
async def admin_get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_user(user_id, db)


@router.post("/{user_id}/role")
async def admin_update_user_role(
    user_id: int,
    role: str,
    db: AsyncSession = Depends(get_db),
):
    return await update_user_role(user_id, role, db)


@router.post("/{user_id}/disable")
async def admin_disable_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await disable_user(user_id, db)

```

---

### `backend\app\rag\context_builder.py`

```python
from typing import List


def build_context(chunks: List[str], max_tokens: int = 1500) -> str:
    """
    Builds a bounded context string from retrieved chunks.
    Hard token budgeting to prevent prompt overflow.
    """

    context = []
    token_estimate = 0

    for chunk in chunks:
        chunk_tokens = len(chunk.split())
        if token_estimate + chunk_tokens > max_tokens:
            break
        context.append(chunk)
        token_estimate += chunk_tokens

    return "\n\n".join(context)

```

---

### `backend\app\rag\guardrails.py`

```python
def validate_context(context: str) -> str:
    """
    Basic safety guardrails for injected context.
    Prevents empty or malformed prompts.
    """

    if not context.strip():
        raise ValueError("Empty retrieval context")

    return context

```

---

### `backend\app\rag\retriever.py`

```python
from typing import List


class VectorRetriever:
    """
    Abstract retriever interface.
    Concrete implementations can use FAISS, pgvector, etc.
    """

    async def retrieve(self, query: str, limit: int = 5) -> List[str]:
        raise NotImplementedError("Vector retrieval not implemented")

```

---

### `backend\app\repositories\assignment_repo.py`

```python
from ..models.assignments import Assignment
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession


class AssignmentRepo(BaseRepo[Assignment]):
    def __init__(self):
        super().__init__(Assignment)

```

---

### `backend\app\repositories\base_repo.py`

```python
from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import as_declarative

T = TypeVar("T")


class BaseRepo(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get(self, db: AsyncSession, id: int):
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def list(self, db: AsyncSession, limit: int = 100):
        stmt = select(self.model).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj):
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
```

---

### `backend\app\repositories\flashcard_repo.py`

```python
from ..models.flashcards import FlashcardSet
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession
import json


class FlashcardRepo(BaseRepo[FlashcardSet]):
    def __init__(self):
        super().__init__(FlashcardSet)

    async def create_set(self, db: AsyncSession, user_id: int, title: str, subject: str, cards: list):
        obj = FlashcardSet(user_id=user_id, title=title, subject=subject, metadata=json.dumps(cards, ensure_ascii=False))
        return await self.create(db, obj)

```

---

### `backend\app\repositories\note_repo.py`

```python
from ..models.notes import Note
from .base_repo import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession


class NoteRepo(BaseRepo[Note]):
    def __init__(self):
        super().__init__(Note)

    async def create_note(self, db: AsyncSession, **kwargs):
        n = Note(**kwargs)
        return await self.create(db, n)

```

---

### `backend\app\routers\auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import SignupRequest, LoginRequest, AuthResponse
from app.services.auth_service import signup_user, login_user
from sqlalchemy import select
from app.models.user import User
from app.security.jwt import create_access_token, create_refresh_token
from jose import JWTError
from app.security.passwords import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(
    data: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await signup_user(data, db)
    return {"id": user.id, "role": user.role}


@router.post("/login")
async def login(payload: dict, db: AsyncSession = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )
    refresh_token = create_refresh_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "role": user.role,
            "class_id": user.class_id,
        },
    }


@router.post("/refresh")
async def refresh(payload: dict):
    from app.security.jwt import decode_token

    token = payload.get("refresh_token")

    try:
        data = decode_token(token)
        if data.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = data.get("sub")
        access_token = create_access_token({"sub": user_id})

        return {"access_token": access_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Expired refresh token")
```

---

### `backend\app\schemas\auth.py`

```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.security.roles import Role


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    role: str  # student | teacher
    registration_code: Optional[str] = None  # student only


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: Role
    class_id: Optional[int]

```

---

### `backend\app\routers\subjects.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.subject import SubjectCreateRequest, SubjectResponse
from app.services.subject_service import create_subject
from app.security.dependencies import require_role
from app.models.user import UserRole

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)


@router.post(
    "",
    response_model=SubjectResponse,
    dependencies=[Depends(require_role(UserRole.admin))]
)
async def create_subject_endpoint(
    payload: SubjectCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await create_subject(payload, db)

```

---

### `backend\app\routers\student\subjects.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.models.subject import Subject


router = APIRouter(prefix="/student/subjects", tags=["Student Subjects"])


@router.get("")
async def list_subjects_for_student(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view subjects",
        )

    result = await db.execute(select(Subject))
    subjects = result.scalars().all()

    return [{"id": s.id, "name": s.name} for s in subjects]

```

---

### `backend\app\routers\teacher_tests.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.security import get_current_user
from app.models.user import User, UserRole
from app.models.subject import Subject
from app.models.tests import Test
from app.models.test_attempt import TestAttempt
from app.schemas.teacher_results import StudentTestResult


router = APIRouter(prefix="/teacher/tests", tags=["Teacher Tests"])


@router.get(
    "/subject/{subject_id}/results",
    response_model=list[StudentTestResult],
)
async def get_subject_results(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # -------------------------------------------------
    # Role check
    # -------------------------------------------------
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view test results",
        )

    # -------------------------------------------------
    # Validate subject ownership
    # -------------------------------------------------
    subject_result = await db.execute(
        select(Subject).where(
            Subject.id == subject_id,
            Subject.teacher_id == current_user.id,
        )
    )
    subject = subject_result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found or not assigned to teacher",
        )

    # -------------------------------------------------
    # Fetch tests for subject
    # -------------------------------------------------
    tests_result = await db.execute(
        select(Test).where(Test.subject == subject.name)
    )
    tests = tests_result.scalars().all()

    if not tests:
        return []

    test_ids = [t.id for t in tests]

    # -------------------------------------------------
    # Fetch attempts + student info
    # -------------------------------------------------
    attempts_result = await db.execute(
        select(
            TestAttempt,
            User.id,
            User.name,
            Test.title,
        )
        .join(User, User.id == TestAttempt.student_id)
        .join(Test, Test.id == TestAttempt.test_id)
        .where(TestAttempt.test_id.in_(test_ids))
    )

    results: list[StudentTestResult] = []

    for attempt, student_id, student_name, test_title in attempts_result.all():
        results.append(
            StudentTestResult(
                student_id=student_id,
                student_name=student_name,
                test_id=attempt.test_id,
                test_title=test_title,
                score=attempt.score,
                submitted_at=attempt.submitted_at,
            )
        )

    return results

```

---

### `backend\app\routers\admin\content.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.assignments import Assignment
from app.models.tests import Test

router = APIRouter(prefix="/api/admin/content", tags=["Admin Content"])


@router.get("/assignments")
async def admin_list_assignments(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Assignment))
    return result.scalars().all()


@router.get("/tests")
async def admin_list_tests(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Test))
    return result.scalars().all()

```

---

### `backend\app\routers\admin\system.py`

```python
from fastapi import APIRouter
from app.config import get_settings

router = APIRouter(prefix="/api/admin/system", tags=["Admin System"])


@router.get("/config")
async def admin_system_config():
    """
    Returns non-sensitive runtime configuration.
    """
    settings = get_settings()
    return {
        "app_name": settings.APP_NAME,
        "env": settings.APP_ENV,
        "debug": settings.DEBUG,
        "log_level": settings.LOG_LEVEL,
    }

```

---

### `backend\app\routers\admin\_guards.py`

```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role

admin_guard = Depends(require_role(Role.admin))

```

---

### `backend\app\routers\parent\_guards.py`

```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role

parent_guard = Depends(require_role(Role.parent))

```

---

### `backend\app\routers\student\_guards.py`

```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role

student_guard = Depends(require_role(Role.student))

```

---

### `backend\app\routers\teacher\_guards.py`

```python
from fastapi import Depends
from app.security import require_role
from app.security.roles import Role

teacher_guard = Depends(require_role(Role.teacher))

```

---

### `backend\app\routers\parent\insights.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.parent_insights_service import get_parent_insights

router = APIRouter(prefix="/api/parent/insights", tags=["Parent Insights"])


@router.get("/child/{student_id}")
async def parent_ai_insights(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    AI-generated academic insights for parents.
    """
    return await get_parent_insights(student_id, db)

```

---

### `backend\app\routers\parent\overview.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.parent_overview_service import get_parent_overview

router = APIRouter(prefix="/api/parent/overview", tags=["Parent Overview"])


@router.get("/child/{student_id}")
async def parent_child_overview(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    High-level academic overview for a parent.
    """
    return await get_parent_overview(student_id, db)

```

---

### `backend\app\routers\student\ai_chat.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.student._guards import student_guard

from app.db.session import get_db
from app.schemas.common import ClientContext
from app.services.ai_service import chat_with_ai
from app.services.xp_service import apply_xp_event

router = APIRouter(prefix="/api/student/ai", tags=["Student AI Chat"], dependencies=[student_guard])


@router.post("/chat")
async def ai_chat_endpoint(
    messages: list[dict],
    context: ClientContext,
    db: AsyncSession = Depends(get_db),
):
    response = await chat_with_ai(messages, context)
    await apply_xp_event(db, user_id=1, event="AI_CHAT_INTERACTION")
    return {"response": response}

```

---

### `backend\app\routers\student\sync.py`

```python
from fastapi import APIRouter
from app.schemas.sync import SyncRequest, SyncResponse
from app.services.sync_service import get_available_sync_items
from app.routers.student._guards import student_guard

router = APIRouter(prefix="/api/student/sync", tags=["Student Sync"], dependencies=[student_guard])


@router.post("/available", response_model=SyncResponse)
async def available_sync_items(payload: SyncRequest):
    return await get_available_sync_items(
        last_sync_at=payload.last_sync_at,
        client_known_ids=payload.client_known_ids,
    )

```

---

### `backend\app\schemas\sync.py`

```python
from pydantic import BaseModel
from typing import List, Optional


class SyncItem(BaseModel):
    content_id: str
    content_type: str  # notes | flashcards | tests
    version: str
    updated_at: str


class SyncRequest(BaseModel):
    last_sync_at: Optional[str] = None
    client_known_ids: List[str] = []


class SyncResponse(BaseModel):
    available: List[SyncItem]

```

---

### `backend\app\routers\student\teacher_notes.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.routers.student._guards import student_guard
from app.models.notes import GeneratedNote

router = APIRouter(
    prefix="/api/student/notes/teacher",
    tags=["Student Teacher Notes"],
    dependencies=[student_guard],
)


@router.get("/")
async def list_teacher_notes(
    db: AsyncSession = Depends(get_db),
):
    """
    List all teacher-created notes available to students.
    """
    result = await db.execute(
        select(GeneratedNote)
    )
    notes = result.scalars().all()

    return [
        {
            "id": n.id,
            "subject": n.subject,
            "chapter": n.chapter,
            "difficulty": n.difficulty,
            "mode": n.extra_data.get("mode") if n.extra_data else None,
            "pdf_url": n.pdf_url,
        }
        for n in notes
    ]


@router.get("/{note_id}")
async def get_teacher_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Fetch a specific teacher note.
    """
    result = await db.execute(
        select(GeneratedNote).where(GeneratedNote.id == note_id)
    )
    note = result.scalar_one_or_none()

    if not note:
        return {"error": "Note not found"}

    return {
        "id": note.id,
        "subject": note.subject,
        "chapter": note.chapter,
        "difficulty": note.difficulty,
        "content": note.extra_data.get("content") if note.extra_data else None,
        "pdf_url": note.pdf_url,
    }

```

---

### `backend\app\routers\teacher\ai_tools.py`

```python
from fastapi import APIRouter
from app.schemas.common import ClientContext
from app.services.teacher_ai_service import (
    suggest_test_questions,
    suggest_assignment_outline,
)
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/ai", tags=["Teacher AI Tools"])


@router.post("/suggest/test")
async def ai_suggest_test_questions(
    subject: str,
    difficulty: str,
    context: ClientContext,
):
    return await suggest_test_questions(subject, difficulty, context)


@router.post("/suggest/assignment")
async def ai_suggest_assignment(
    subject: str,
    topic: str,
    context: ClientContext,
):
    return await suggest_assignment_outline(subject, topic, context)

```

---

### `backend\app\routers\teacher\reports.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.teacher_report_service import get_student_report
from app.routers.teacher._guards import teacher_guard

router = APIRouter(prefix="/api/teacher/reports", tags=["Teacher Reports"])


@router.get("/student/{student_id}")
async def get_detailed_student_report(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a detailed academic + behavioral report for a student.
    """
    return await get_student_report(student_id, db)

```

---

### `backend\app\routers\teacher\students.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.security.dependencies import require_role, get_current_user
from app.models.user import UserRole
from app.services.teacher_context import get_teacher_subject
from app.services.teacher_student_service import get_students_for_subject

router = APIRouter(
    prefix="/teacher/students",
    tags=["Teacher"],
    dependencies=[Depends(require_role(UserRole.teacher))],
)


@router.get("")
async def list_students_for_teacher(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    subject = await get_teacher_subject(current_user.id, db)
    students = await get_students_for_subject(subject, db)

    return [
        {
            "id": student.id,
            "email": student.email,
            "class_id": student.class_id,
        }
        for student in students
    ]

```

---

### `backend\app\schemas\common.py`

```python
from pydantic import BaseModel
from typing import Literal, Optional


class ClientContext(BaseModel):
    client_type: Literal["mobile", "desktop"]
    connectivity: Literal["online", "offline"]
    model_capability: Literal["light", "heavy"]
    cache_allowed: bool = True
    max_payload_kb: Optional[int] = None

```

---

### `backend\app\schemas\teacher_results.py`

```python
from pydantic import BaseModel
from datetime import datetime


class StudentTestResult(BaseModel):
    student_id: int
    student_name: str
    test_id: int
    test_title: str
    score: int
    submitted_at: datetime

```

---

### `backend\app\schemas\test_submission.py`

```python
from pydantic import BaseModel
from typing import List


class TestSubmissionRequest(BaseModel):
    answers: List[str]


class TestSubmissionResponse(BaseModel):
    score: int
    total_questions: int

```

---

### `backend\app\security\admin_guard.py`

```python
from fastapi import HTTPException, status


def require_admin(role: str):
    """
    Enforces admin-only access.
    Replace role source with auth context later.
    """
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

```

---

### `backend\app\security\dependencies.py`

```python
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError
from app.security.oauth2 import bearer_scheme
from fastapi.security import OAuth2PasswordBearer

from app.db.session import get_db
from app.models.user import User
from app.security.roles import Role
from app.security.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


def require_role(*roles: Role):
    async def role_guard(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user

    return role_guard

```

---

### `backend\app\security\guards.py`

```python
from fastapi import HTTPException
from app.schemas.common import ClientContext


def enforce_client_capabilities(context: ClientContext) -> None:
    """
    Prevents misuse of heavy models or server-only features.
    """

    if context.connectivity == "offline" and context.model_capability == "heavy":
        raise HTTPException(
            status_code=400,
            detail="Heavy model access not allowed in offline mode",
        )

```

---

### `backend\app\security\jwt.py`

```python
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ------------------------------------------------------------------
# Token creators
# ------------------------------------------------------------------

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["type"] = "access"
    to_encode["exp"] = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode["type"] = "refresh"
    to_encode["exp"] = datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ------------------------------------------------------------------
# Token decoder
# ------------------------------------------------------------------

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

---

### `backend\app\security\oauth2.py`

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer(auto_error=True)

```

---

### `backend\app\security\passwords.py`

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash password using Argon2.
    - No length limits
    - Secure against GPU attacks
    - Compatible with bcrypt>=4 (Chromadb)
    """
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

```

---

### `backend\app\security\rate_limiter.py`

```python
import time
from fastapi import HTTPException, Request

# Simple in-memory rate limiter (replace with Redis in production)
RATE_LIMIT = 30  # requests
WINDOW_SECONDS = 60

_client_requests: dict[str, list[float]] = {}


def rate_limit(request: Request) -> None:
    client_ip = request.client.host
    now = time.time()

    timestamps = _client_requests.get(client_ip, [])
    timestamps = [t for t in timestamps if now - t < WINDOW_SECONDS]

    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
        )

    timestamps.append(now)
    _client_requests[client_ip] = timestamps

```

---

### `backend\app\security\roles.py`

```python
from app.models.user import UserRole as Role
from fastapi import Depends, HTTPException
from app.models.user import User
from app.security.dependencies import get_current_user


def require_role(*roles: str):
    async def role_guard(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_guard
```

---

### `backend\app\services\admin_system_service.py`

```python
from app.config import get_settings


async def get_system_status():
    settings = get_settings()

    return {
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG,
        "ollama_base": settings.OLLAMA_BASE_URL,
    }

```

---

### `backend\app\services\admin_user_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.users import User


async def list_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}
    return user


async def update_user_role(
    user_id: int,
    role: str,
    db: AsyncSession,
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}

    user.role = role
    await db.commit()
    await db.refresh(user)

    return {
        "user_id": user.id,
        "new_role": user.role,
    }


async def disable_user(
    user_id: int,
    db: AsyncSession,
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}

    user.is_active = False
    await db.commit()

    return {
        "user_id": user.id,
        "disabled": True,
    }

```

---

### `backend\app\services\ai_service.py`

```python
from typing import List, Dict
from app.ai import OllamaClient, select_model
from app.schemas.common import ClientContext

ollama = OllamaClient()


def _build_chat_prompt(messages: List[Dict[str, str]]) -> str:
    """
    Converts chat history into a single prompt.
    Expected message format:
    { "role": "user" | "assistant", "content": str }
    """

    prompt_lines = [
        "You are a helpful, accurate AI tutor for school students.",
        "Follow the syllabus strictly.",
        "Do not hallucinate.",
        "Explain concepts clearly and simply.",
        "",
        "Conversation:",
    ]

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "").strip()
        if not content:
            continue
        prompt_lines.append(f"{role.capitalize()}: {content}")

    prompt_lines.append("Assistant:")

    return "\n".join(prompt_lines)


async def chat_with_ai(
    messages: List[Dict[str, str]],
    context: ClientContext,
) -> str:
    """
    Main AI chat entry point for students.
    """

    model = select_model(context)
    prompt = _build_chat_prompt(messages)

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.25,
        max_tokens=900 if context.client_type == "mobile" else 1400,
    )

    return response.strip()

```

---

### `backend\app\services\auth_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User, UserRole
from app.models.classroom import Classroom
from app.models.progress import Progress
from app.schemas.auth import SignupRequest, LoginRequest
from app.security.passwords import hash_password, verify_password
from app.security.jwt import create_access_token

def parse_registration_code(code: str):
    if len(code) != 6 or not code.isdigit():
        raise HTTPException(status_code=400, detail="Invalid registration code")

    grade = int(code[:2])
    section_num = code[2:4]
    roll = int(code[4:])

    section_map = {"01": "A", "02": "B", "03": "C"}
    if section_num not in section_map:
        raise HTTPException(status_code=400, detail="Invalid section code")

    return grade, section_map[section_num], roll


async def signup_user(payload: SignupRequest, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    class_id = None

    if payload.role == "student":
        if not payload.registration_code:
            raise HTTPException(status_code=400, detail="Registration code required")

        grade, section, _ = parse_registration_code(payload.registration_code)
        prefix = payload.registration_code[:4]

        result = await db.execute(
            select(Classroom).where(Classroom.code_prefix == prefix)
        )
        classroom = result.scalar()

        if not classroom:
            classroom = Classroom(
                grade=grade,
                section=section,
                code_prefix=prefix,
            )
            db.add(classroom)
            await db.flush()

        class_id = classroom.id

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole(payload.role),
        class_id=class_id,
    )
    db.add(user)
    await db.flush()

    if payload.role == "student":
        progress = Progress(user_id=user.id)
        db.add(progress)

    await db.commit()

    return {
        "user_id": user.id,
        "role": user.role.value,
        "class_id": user.class_id,
    }


async def login_user(data: LoginRequest, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token({
        "sub": user.id,
        "role": user.role,
        "class_id": user.class_id
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role,
        "class_id": user.class_id
    }
```

---

### `backend\app\services\elective_enrollment_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subject import Subject
from app.models.subject_student import SubjectStudent
from app.services.enrollment_guard import validate_enrollment_allowed


async def enroll_student_in_subject(
    subject_id: int,
    student_id: int,
    db: AsyncSession,
):
    subject = await db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    await validate_enrollment_allowed(subject, db)

    # Prevent duplicate enrollment
    result = await db.execute(
        select(SubjectStudent).where(
            SubjectStudent.subject_id == subject_id,
            SubjectStudent.student_id == student_id,
        )
    )
    if result.scalar():
        raise HTTPException(
            status_code=400,
            detail="Student already enrolled in subject",
        )

    enrollment = SubjectStudent(
        subject_id=subject_id,
        student_id=student_id,
    )

    db.add(enrollment)
    await db.commit()

```

---

### `backend\app\services\enrollment_guard.py`

```python
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent


async def validate_enrollment_allowed(
    subject: Subject,
    db: AsyncSession,
):
    """
    Validates whether enrollment is allowed for a subject.
    Does NOT perform enrollment.
    """

    # Core subjects cannot be manually enrolled
    if subject.type == SubjectType.core:
        raise HTTPException(
            status_code=400,
            detail="Enrollment not allowed for core subjects",
        )

    now = datetime.utcnow()

    # Enrollment window validation
    if subject.enrollment_open_at and now < subject.enrollment_open_at:
        raise HTTPException(
            status_code=403,
            detail="Enrollment window has not opened yet",
        )

    if subject.enrollment_close_at and now > subject.enrollment_close_at:
        raise HTTPException(
            status_code=403,
            detail="Enrollment window has closed",
        )

    # Capacity validation
    if subject.max_students is not None:
        result = await db.execute(
            select(func.count())
            .select_from(SubjectStudent)
            .where(SubjectStudent.subject_id == subject.id)
        )
        enrolled_count = result.scalar()

        if enrolled_count >= subject.max_students:
            raise HTTPException(
                status_code=409,
                detail="Subject enrollment is full",
            )

```

---

### `backend\app\services\file_validation.py`

```python
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE_MB = 10


async def validate_upload(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail="File exceeds 10MB limit",
        )

    file.file.seek(0)

```

---

### `backend\app\services\flashcards_service.py`

```python
from app.ai import OllamaClient, select_model
from app.schemas.flashcards import FlashcardSetResponse
from app.schemas.common import ClientContext

ollama = OllamaClient()


async def generate_flashcards(
    subject: str,
    chapter: str,
    context: ClientContext,
) -> FlashcardSetResponse:
    model = select_model(context)

    prompt = f"""
Generate high-quality flashcards.

Subject: {subject}
Chapter: {chapter}

Rules:
- Short
- Fact-based
- Exam-focused
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.3,
        max_tokens=800,
    )

    cards = [
        {"front": line.split(" - ")[0], "back": line.split(" - ")[1]}
        for line in response.split("\n")
        if " - " in line
    ]

    return FlashcardSetResponse(
        set_id=1,
        subject=subject,
        chapter=chapter,
        cards=cards,
    )

```

---

### `backend\app\services\notes_service.py`

```python
from app.ai import OllamaClient, select_model
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.rag import build_context, validate_context
from sqlalchemy.ext.asyncio import AsyncSession

ollama = OllamaClient()


ollama = OllamaClient()

LATEX_SAFE_NOTES_PROMPT = """
You are an expert textbook author writing high-quality academic notes.

TASK:
Generate clear, structured, textbook-quality study notes for students.

SUBJECT: {subject}
CHAPTER: {chapter}
DIFFICULTY: {difficulty}

MANDATORY FORMATTING RULES (STRICT):
1. ALL mathematical expressions MUST be written in valid LaTeX.
2. Inline math MUST use: \\( ... \\)
   Example: \\( F = ma \\)
3. Display math MUST use:
   \\[
   ... 
   \\]
4. DO NOT use:
   - $...$
   - $$...$$
   - Unicode math symbols (×, ÷, √, →, ∑, etc.)
5. DO NOT explain LaTeX syntax.
6. DO NOT escape LaTeX unnecessarily.
7. Ensure all LaTeX is KaTeX-compatible.

CONTENT STRUCTURE:
- Clear headings
- Step-by-step explanations
- Worked examples (with LaTeX math)
- Bullet points where appropriate

STYLE:
- Formal textbook tone
- Precise and unambiguous
- No conversational language
- No emojis

IMPORTANT:
If mathematics is involved, LaTeX formatting is NOT optional.
If no math is required, proceed normally without forcing equations.
"""


async def generate_notes(
    payload: NotesGenerateRequest,
    db: AsyncSession,
) -> NotesResponse:
    model = select_model(payload.context)

    prompt = LATEX_SAFE_NOTES_PROMPT.format(
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
    )

    content = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.2,   # lower = more deterministic LaTeX
        max_tokens=1800,
    )

    # Store LaTeX-safe content exactly as generated
    note = {
        "content": content,
        "format": "markdown+latex",
        "renderer": "katex",
    }

    return NotesResponse(
        content_id="temp",   # replaced by DB ID later
        summary=content[:300],
        pdf_url=None,
        offline_ready=False,
        expires_at=None,
    )

```

---

### `backend\app\services\parent_insights_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.progress import Progress
from app.ai import OllamaClient

ollama = OllamaClient()


async def get_parent_insights(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    Generates read-only academic insights for parents.
    """

    result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = result.scalar_one_or_none()

    if not progress:
        return {"insights": "No data available yet."}

    prompt = f"""
You are an educational analyst.

Analyze this student's academic progress and provide insights
for parents in simple, reassuring language.

XP: {progress.xp}
Level: {progress.level}
Stats: {progress.stats}

Rules:
- No recommendations to change syllabus
- No grading judgments
- Supportive tone
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name="mistral:7b-instruct",
        temperature=0.2,
        max_tokens=600,
    )

    return {"insights": response}

```

---

### `backend\app\services\parent_overview_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.progress import Progress
from app.models.assignments import Assignment
from app.models.tests import Test


async def get_parent_overview(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    High-level snapshot for parents.
    """

    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress_result.scalar_one_or_none()

    assignments_result = await db.execute(
        select(Assignment).where(Assignment.created_by == student_id)
    )
    assignments = assignments_result.scalars().all()

    tests_result = await db.execute(
        select(Test).where(Test.created_by == student_id)
    )
    tests = tests_result.scalars().all()

    return {
        "student_id": student_id,
        "xp": progress.xp if progress else 0,
        "level": progress.level if progress else 1,
        "assignments_assigned": len(assignments),
        "tests_attempted": len(tests),
    }


async def get_detailed_progress(
    student_id: int,
    db: AsyncSession,
) -> dict:
    """
    Detailed academic breakdown.
    """

    progress_result = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress_result.scalar_one_or_none()

    return {
        "student_id": student_id,
        "xp": progress.xp if progress else 0,
        "level": progress.level if progress else 1,
        "stats": progress.stats if progress else {},
    }

```

---

### `backend\app\services\pdf_generator.py`

```python
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT


def generate_notes_pdf(
    title: str,
    subject: str,
    chapter: str,
    content: str,
) -> BytesIO:
    """
    Generates a PDF for AI-generated notes and returns an in-memory buffer.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1 * inch,
        leftMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="TitleStyle",
            fontSize=18,
            spaceAfter=16,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyStyle",
            fontSize=11,
            leading=15,
            spaceAfter=10,
        )
    )

    story = []

    story.append(Paragraph(title, styles["TitleStyle"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(f"<b>Subject:</b> {subject}", styles["BodyStyle"]))
    story.append(Paragraph(f"<b>Chapter:</b> {chapter}", styles["BodyStyle"]))
    story.append(Spacer(1, 0.3 * inch))

    for line in content.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["BodyStyle"]))
            story.append(Spacer(1, 0.1 * inch))

    doc.build(story)
    buffer.seek(0)

    return buffer

```

---

### `backend\app\services\subject_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subject import Subject, SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import User, UserRole
from app.schemas.subject import SubjectCreateRequest


async def create_subject(payload: SubjectCreateRequest, db: AsyncSession):
    # Core subjects MUST have class_id
    if payload.type == SubjectType.core and payload.class_id is None:
        raise HTTPException(
            status_code=400,
            detail="Core subjects must be linked to a class",
        )

    subject = Subject(
        name=payload.name,
        type=payload.type,
        class_id=payload.class_id,
        teacher_id=payload.teacher_id,
    )

    db.add(subject)
    await db.flush()

    # AUTO-ENROLL students for CORE subjects
    if payload.type == SubjectType.core:
        result = await db.execute(
            select(User).where(
                User.role == UserRole.student,
                User.class_id == payload.class_id,
            )
        )
        students = result.scalars().all()

        for student in students:
            enrollment = SubjectStudent(
                subject_id=subject.id,
                student_id=student.id,
            )
            db.add(enrollment)

    await db.commit()
    await db.refresh(subject)

    return subject

```

---

### `backend\app\services\sync_service.py`

```python
from typing import List
from datetime import datetime
from app.schemas.sync import SyncItem, SyncResponse


async def get_available_sync_items(
    last_sync_at: str | None,
    client_known_ids: List[str],
) -> SyncResponse:
    """
    Returns only content that is new or updated since last sync.
    """

    # Placeholder canonical content registry
    canonical_items = [
        {
            "content_id": "phy_motion_notes_v3",
            "content_type": "notes",
            "version": "3.0",
            "updated_at": "2025-01-01T00:00:00Z",
        },
        {
            "content_id": "chem_atoms_flashcards_v1",
            "content_type": "flashcards",
            "version": "1.0",
            "updated_at": "2025-01-02T00:00:00Z",
        },
    ]

    items = []

    for item in canonical_items:
        if item["content_id"] not in client_known_ids:
            items.append(SyncItem(**item))

    return SyncResponse(available=items)

```

---

### `backend\app\services\teacher_ai_service.py`

```python
from app.ai import OllamaClient, select_model
from app.schemas.common import ClientContext

ollama = OllamaClient()


async def suggest_test_questions(
    subject: str,
    difficulty: str,
    context: ClientContext,
) -> dict:
    model = select_model(context)

    prompt = f"""
Suggest exam-quality questions WITH answers.

Subject: {subject}
Difficulty: {difficulty}

Rules:
- Accurate
- Syllabus-aligned
- Teacher will review
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.35,
        max_tokens=1000,
    )

    return {"suggestions": response}


async def suggest_assignment_outline(
    subject: str,
    topic: str,
    context: ClientContext,
) -> dict:
    model = select_model(context)

    prompt = f"""
Create an assignment outline for students.

Subject: {subject}
Topic: {topic}

Rules:
- Clear objectives
- Structured tasks
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.3,
        max_tokens=800,
    )

    return {"outline": response}

```

---

### `backend\app\services\teacher_assignment_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.assignments import Assignment
from app.schemas.assignments import AssignmentCreateRequest, AssignmentResponse


async def create_assignment(
    payload: AssignmentCreateRequest,
    assignment_type: str,
    db: AsyncSession,
) -> AssignmentResponse:
    assignment = Assignment(
        created_by=1,  # teacher_id (auth wired later)
        title=payload.title,
        subject=payload.subject,
        description=payload.description,
        due_date=payload.due_date,
    )

    # Store assignment type in metadata-like pattern (future-proof)
    assignment.metadata = {
        "assignment_type": assignment_type
    }

    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)

    return AssignmentResponse(
        id=assignment.id,
        title=assignment.title,
        subject=assignment.subject,
        due_date=assignment.due_date,
    )

```

---

### `backend\app\services\teacher_context.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.subject import Subject
from app.models.user import User, UserRole


async def get_teacher_subject(
    teacher_id: int,
    db: AsyncSession,
) -> Subject:
    """
    Returns the subject taught by the teacher.
    Enforces exactly one subject per teacher (current system rule).
    """
    result = await db.execute(
        select(Subject).where(Subject.teacher_id == teacher_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(
            status_code=403,
            detail="Teacher is not assigned to any subject",
        )

    return subject

```

---

### `backend\app\services\teacher_notes_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notes import GeneratedNote
from app.schemas.notes import NotesGenerateRequest, NotesResponse
from app.ai import OllamaClient, select_model
from app.services.file_validation import validate_upload
from fastapi import UploadFile
import uuid
import os

ollama = OllamaClient()

UPLOAD_DIR = "app/uploads/teacher_notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def create_manual_notes(
    payload: NotesGenerateRequest,
    db: AsyncSession,
) -> NotesResponse:
    """
    Teacher provides full content manually.
    """

    note = GeneratedNote(
        user_id=1,  # replaced by auth later
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        pdf_url="",
        extra_data={
            "mode": "manual",
            "content": payload.context.get("manual_content", ""),
        },
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return NotesResponse(
        content_id=str(note.id),
        summary="Manual notes created",
        pdf_url=None,
        offline_ready=False,
        expires_at=None,
    )


async def create_ai_assisted_notes(
    payload: NotesGenerateRequest,
    db: AsyncSession,
) -> NotesResponse:
    """
    Teacher provides outline → AI expands.
    """

    model = select_model(payload.context)

    prompt = f"""
You are assisting a teacher.

Expand the following outline into
clear, syllabus-aligned notes.

Outline:
{payload.context.get("outline")}

Rules:
- Accurate
- Structured
- Teacher-reviewed
"""

    ai_content = await ollama.generate(
        prompt=prompt,
        model_name=model,
        temperature=0.25,
        max_tokens=1200,
    )

    note = GeneratedNote(
        user_id=1,
        subject=payload.subject,
        chapter=payload.chapter,
        difficulty=payload.difficulty,
        pdf_url="",
        extra_data={
            "mode": "ai_assisted",
            "content": ai_content,
        },
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return NotesResponse(
        content_id=str(note.id),
        summary=ai_content[:300],
        pdf_url=None,
        offline_ready=False,
        expires_at=None,
    )


async def upload_notes_file(
    subject: str,
    chapter: str,
    file: UploadFile,
    db: AsyncSession,
) -> NotesResponse:
    """
    Upload teacher-created PDF notes.
    """
    await validate_upload(file)

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    note = GeneratedNote(
        user_id=1,
        subject=subject,
        chapter=chapter,
        difficulty="custom",
        pdf_url=path,
        extra_data={
            "mode": "upload",
            "original_filename": file.filename,
        },
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return NotesResponse(
        content_id=str(note.id),
        summary="Uploaded notes",
        pdf_url=path,
        offline_ready=True,
        expires_at=None,
    )

```

---

### `backend\app\services\teacher_report_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress
from app.models.tests import Test
from app.models.assignments import Assignment


async def get_student_report(
    student_id: int,
    db: AsyncSession,
) -> dict:
    progress = await db.execute(
        select(Progress).where(Progress.user_id == student_id)
    )
    progress = progress.scalar_one_or_none()

    tests = await db.execute(
        select(Test).where(Test.created_by == student_id)
    )
    assignments = await db.execute(
        select(Assignment).where(Assignment.created_by == student_id)
    )

    return {
        "student_id": student_id,
        "progress": progress,
        "tests_attempted": tests.scalars().all(),
        "assignments": assignments.scalars().all(),
    }

```

---

### `backend\app\services\teacher_student_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.subject import SubjectType
from app.models.subject_student import SubjectStudent
from app.models.user import User, UserRole


async def get_students_for_subject(
    subject,
    db: AsyncSession,
):
    """
    Returns students visible to the teacher based on subject type.
    """

    # CORE SUBJECT → all students in the class
    if subject.type == SubjectType.core:
        result = await db.execute(
            select(User).where(
                User.role == UserRole.student,
                User.class_id == subject.class_id,
            )
        )
        return result.scalars().all()

    # ELECTIVE SUBJECT → only enrolled students
    result = await db.execute(
        select(User)
        .join(SubjectStudent, SubjectStudent.student_id == User.id)
        .where(SubjectStudent.subject_id == subject.id)
    )
    return result.scalars().all()

```

---

### `backend\app\services\teacher_test_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tests import Test
from app.schemas.tests import TestCreateRequest, TestResponse
from app.ai import OllamaClient
import json

ollama = OllamaClient()


async def create_test_manual(
    payload: TestCreateRequest,
    db: AsyncSession,
) -> TestResponse:
    test = Test(
        created_by=1,  # teacher_id
        title=payload.title,
        subject=payload.subject,
        difficulty=payload.difficulty,
        questions=[],  # manually provided later
        total_marks=100,
    )

    db.add(test)
    await db.commit()
    await db.refresh(test)

    return TestResponse(
        test_id=test.id,
        title=test.title,
        total_marks=test.total_marks,
    )


async def create_test_ai_assisted(
    payload: TestCreateRequest,
    db: AsyncSession,
) -> TestResponse:
    prompt = f"""
Generate multiple-choice questions in JSON ONLY.

Format:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "A"
  }}
]

Subject: {payload.subject}
Difficulty: {payload.difficulty}
Chapter: {payload.chapter}
"""

    raw = await ollama.generate(
        prompt=prompt,
        model_name="mistral:7b-instruct",
        temperature=0.2,
        max_tokens=1200,
    )

    questions = json.loads(raw)

    test = Test(
        created_by=1,
        title=payload.title,
        subject=payload.subject,
        difficulty=payload.difficulty,
        questions=questions,
        total_marks=len(questions),
    )

    db.add(test)
    await db.commit()
    await db.refresh(test)

    return test
```

---

### `backend\app\services\test_evaluation_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.tests import Test
from app.models.test_attempt import TestAttempt
from app.models.test_answer import TestAnswer
from app.models.user import User


class TestEvaluationService:
    @staticmethod
    async def submit_test(
        *,
        db: AsyncSession,
        test_id: int,
        student: User,
        submitted_answers: list[str],
    ) -> dict:
        """
        Evaluate a submitted test and persist the attempt.
        """

        # -------------------------------------------------
        # Fetch test
        # -------------------------------------------------
        result = await db.execute(
            select(Test).where(Test.id == test_id)
        )
        test = result.scalar_one_or_none()

        if not test:
            raise ValueError("Test not found")

        # -------------------------------------------------
        # Validate question count
        # -------------------------------------------------
        questions = test.questions

        if len(submitted_answers) != len(questions):
            raise ValueError("Answer count does not match question count")

        # -------------------------------------------------
        # Evaluate answers
        # -------------------------------------------------
        score = 0
        answer_rows: list[TestAnswer] = []

        for index, question in enumerate(questions):
            correct_answer = question["correct_answer"]
            selected_answer = submitted_answers[index]

            is_correct = selected_answer == correct_answer

            if is_correct:
                score += 1

            answer_rows.append(
                TestAnswer(
                    question_index=index,
                    selected_answer=selected_answer,
                    is_correct=is_correct,
                )
            )

        # -------------------------------------------------
        # Persist attempt
        # -------------------------------------------------
        attempt = TestAttempt(
            test_id=test.id,
            student_id=student.id,
            score=score,
        )

        db.add(attempt)
        await db.flush()  # get attempt.id

        # -------------------------------------------------
        # Attach answers to attempt
        # -------------------------------------------------
        for answer in answer_rows:
            answer.test_attempt_id = attempt.id
            db.add(answer)

        await db.commit()

        return {
            "score": score,
            "total_questions": len(questions),
        }

```

---

### `backend\app\services\test_service.py`

```python
from app.ai import OllamaClient
from app.schemas.tests import TestCreateRequest, TestResponse

ollama = OllamaClient()


async def generate_test(request: TestCreateRequest) -> TestResponse:
    prompt = f"""
Create an exam-style test.

Subject: {request.subject}
Difficulty: {request.difficulty}

Rules:
- Multiple choice
- One correct answer
- Clear options
"""

    response = await ollama.generate(
        prompt=prompt,
        model_name="mistral:7b-instruct",
        temperature=0.4,
        max_tokens=1500,
    )

    return TestResponse(
        test_id=1,
        title=request.title,
        total_marks=100,
    )

```

---

### `backend\app\services\xp_service.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress


# XP rules (authoritative, backend-only)
XP_RULES = {
    "TEST_COMPLETED": 100,
    "ASSIGNMENT_SUBMITTED": 75,
    "NOTES_GENERATED": 40,
    "FLASHCARDS_REVIEWED": 30,
    "AI_CHAT_INTERACTION": 10,
    "DAILY_STREAK_BONUS": 50,
}


def calculate_level(xp: int) -> int:
    """
    Simple level curve:
    Level increases every 500 XP.
    """
    return max(1, xp // 500 + 1)


async def apply_xp_event(
    db: AsyncSession,
    user_id: int,
    event: str,
) -> Progress:
    """
    Applies XP for a given event and updates user progress.
    """

    xp_gain = XP_RULES.get(event)
    if xp_gain is None:
        raise ValueError(f"Unknown XP event: {event}")

    result = await db.execute(
        select(Progress).where(Progress.user_id == user_id)
    )
    progress = result.scalar_one_or_none()

    if progress is None:
        progress = Progress(
            user_id=user_id,
            xp=0,
            level=1,
            stats={},
        )
        db.add(progress)

    progress.xp += xp_gain
    progress.level = calculate_level(progress.xp)

    await db.commit()
    await db.refresh(progress)

    return progress

```

---

### `backend\app\utils\ai_client.py`

```python
# backend/app/utils/ai_client.py

import json
import re
import os
from typing import Any, Dict
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)


# ============================================================
# 1. FUNCTION CALLING SUPPORT (CORRECT FOR CHAT COMPLETIONS)
# ============================================================

async def call_json_function(model: str, messages: list, function_schema: dict) -> Dict[str, Any]:
    """
    Calls OpenAI chat.completions.create() using function-calling
    and returns the parsed JSON arguments.
    """

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        tools=[{
            "type": "function",
            "function": function_schema
        }],
        tool_choice={"type": "function", "function": {"name": function_schema["name"]}},
        temperature=0.2
    )

    try:
        # Correct extraction for ChatCompletionMessageFunctionToolCall
        tool_call = response.choices[0].message.tool_calls[0]
        args_str = tool_call.function.arguments  # <-- this is a string
        return json.loads(args_str)

    except Exception as e:
        raise ValueError(
            f"Function call JSON parse failed: {e}\n"
            f"Raw: {response}"
        )


# ============================================================
# 2. FLASHCARD LEGACY SUPPORT (UNCHANGED)
# ============================================================

def _extract_text_from_response(response: Any) -> str:
    try:
        return response.choices[0].message.content
    except Exception:
        return ""


def _strip_code_fences(text: str) -> str:
    cleaned = re.sub(r"^```(?:json)?\s*", "", text)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _extract_first_json(text: str) -> str:
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON found in AI output.")
    for end in range(len(text) - 1, start, -1):
        try:
            json.loads(text[start:end])
            return text[start:end]
        except:
            pass
    raise ValueError("Unable to extract JSON from AI output.")


async def generate_flashcard_ai_output(subject: str, chapter: str, max_cards: int = 20) -> Dict[str, Any]:
    """
    Legacy flashcard generator — kept EXACTLY as your flashcards expect.
    """

    prompt = f"""
Generate up to {max_cards} flashcards for subject '{subject}' and chapter '{chapter}'.

Respond ONLY with valid JSON in this format:

{{
    "cards": [
        {{
            "front": "Question text",
            "back": "Answer text"
        }}
    ]
}}
"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a flashcard generator that outputs ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    text = _extract_text_from_response(response)
    if not text:
        raise ValueError("AI returned empty response.")

    cleaned = _strip_code_fences(text)

    try:
        return json.loads(cleaned)
    except:
        candidate = _extract_first_json(cleaned)
        return json.loads(candidate)

```

---

### `backend\app\utils\sanitize.py`

```python
import re


def sanitize_markdown(md: str) -> str:
    # Basic sanitization to avoid unsupported chars
    if not md:
        return ""
    # Replace some unicode chars that fpdf may struggle with
    replacements = {
        "\u2013": "-",  # en dash
        "\u2014": "-",  # em dash
        "\u2022": "-",  # bullet
        "\u00b2": "^2",  # superscript 2
    }
    for k, v in replacements.items():
        md = md.replace(k, v)
    # Trim repeated blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()

```
