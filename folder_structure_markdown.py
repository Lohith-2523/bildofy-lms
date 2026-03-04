import os

# ==========================
# CONFIGURATION
# ==========================

# Root folders
BACKEND_ROOT = "backend"       # change only if your backend folder has a different name
FRONTEND_ROOT = "frontend"     # parent folder containing multiple frontend options

# Choose which frontend folder to export (ONLY ONE)
# Example: "web", "nextjs", "client", etc.
SELECTED_FRONTEND_FOLDER = "bildofy-lms-lovable"

# Output file
OUTPUT_FILE = "fullstack_structure.md"

# Valid file extensions to include
VALID_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx",
    ".json", ".css", ".html",
    ".yml", ".yaml", ".md"
}

# Folders that MUST be excluded
EXCLUDED_FOLDERS = {
    "node_modules", "lms_venv", "venv", ".venv",
    "__pycache__", "dist", "build", ".next"
}


# ==========================
# INTERNAL HELPERS
# ==========================

def is_excluded(path: str) -> bool:
    parts = path.split(os.sep)
    return any(part in EXCLUDED_FOLDERS for part in parts)


def has_valid_extension(filename: str) -> bool:
    return os.path.splitext(filename)[1] in VALID_EXTENSIONS


def tree(dir_path: str, prefix: str = ""):
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return

    entries = [
        e for e in entries
        if not is_excluded(os.path.join(dir_path, e))
    ]

    for index, name in enumerate(entries):
        full_path = os.path.join(dir_path, name)

        connector = "└── " if index == len(entries) - 1 else "├── "
        is_dir = os.path.isdir(full_path)

        if is_dir:
            yield prefix + connector + name + "/"
            extension = "    " if index == len(entries) - 1 else "│   "
            yield from tree(full_path, prefix + extension)
        else:
            if has_valid_extension(name):
                yield prefix + connector + name


def extract_imports(file_path: str, max_lines: int = 15):
    imports = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    imports.append(line)
                if len(imports) >= max_lines:
                    break
    except Exception:
        pass
    return imports


def scan_code_files(root: str):
    results = []
    for current_root, dirs, files in os.walk(root):
        if is_excluded(current_root):
            continue

        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]

        for file in files:
            if has_valid_extension(file):
                path = os.path.join(current_root, file)
                imports = extract_imports(path)
                results.append((path, imports))
    return results


# ==========================
# MAIN EXPORT LOGIC
# ==========================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    f.write("# Full Stack Project Structure\n\n")

    # --------------------------
    # BACKEND
    # --------------------------
    f.write("## Backend Folder Structure\n\n")
    f.write("```\n")
    for line in tree(BACKEND_ROOT):
        f.write(line + "\n")
    f.write("```\n\n")

    f.write("## Backend Code Imports Overview\n\n")
    for path, imports in scan_code_files(BACKEND_ROOT):
        f.write(f"### {path}\n")
        if imports:
            f.write("```python\n")
            for imp in imports:
                f.write(imp + "\n")
            f.write("```\n\n")
        else:
            f.write("_No imports detected_\n\n")

    # --------------------------
    # FRONTEND
    # --------------------------
    frontend_path = os.path.join(FRONTEND_ROOT, SELECTED_FRONTEND_FOLDER)

    f.write("## Frontend Folder Structure\n\n")
    f.write("```\n")
    for line in tree(frontend_path):
        f.write(line + "\n")
    f.write("```\n\n")

    f.write("## Frontend Code Imports Overview\n\n")
    for path, imports in scan_code_files(frontend_path):
        f.write(f"### {path}\n")
        if imports:
            f.write("```text\n")
            for imp in imports:
                f.write(imp + "\n")
            f.write("```\n\n")
        else:
            f.write("_No imports detected_\n\n")

print(f"Full stack structure exported to: {OUTPUT_FILE}")
