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
import AnalyticsPage from './pages/teacher/AnalyticsPage';

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
    <Route path="/" element={<RootRedirect />} />

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
    <Route
      path="/teacher/analytics"
      element={
        <ProtectedRoute role="teacher">
          <AnalyticsPage />
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
