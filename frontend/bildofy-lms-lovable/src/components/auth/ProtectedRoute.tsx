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
