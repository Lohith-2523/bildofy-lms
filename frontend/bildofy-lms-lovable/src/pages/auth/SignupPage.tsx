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
