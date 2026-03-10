import { useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const AdminBulkImportPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  const runImport = async () => {
    if (!file) throw new Error("Choose a file first");
    const form = new FormData();
    form.append("file", file);
    const res = await fetch("http://localhost:8000/api/admin/dashboard/students/bulk-import", {
      method: "POST",
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
      body: form,
    });
    if (!res.ok) throw new Error("Bulk import failed");
    const data = await res.json();
    setStatus(`Import complete. Created: ${data.created}, Skipped: ${data.skipped}`);
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/admin">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <h1 className="text-xl font-bold">Bulk Student Import</h1>
        </div>
      </header>
      <main className="container mx-auto px-4 py-6 max-w-2xl space-y-4">
        {status && <div className="p-3 rounded border bg-secondary/40 text-sm">{status}</div>}
        <Input type="file" accept=".xlsx,.xls,.csv,.pdf" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <p className="text-sm text-muted-foreground">
          Supported files: Excel, CSV, PDF. Expected fields: name, email, password, class_id.
        </p>
        <Button onClick={() => runImport().catch((err) => setStatus(err.message))}>Start Import</Button>
      </main>
    </div>
  );
};

export default AdminBulkImportPage;
