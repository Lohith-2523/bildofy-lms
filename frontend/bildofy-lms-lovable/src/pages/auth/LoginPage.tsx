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
