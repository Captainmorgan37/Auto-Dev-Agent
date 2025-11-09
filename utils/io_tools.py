from pathlib import Path

def write_app_code(code, filename, sandbox_path):
    Path(sandbox_path).mkdir(parents=True, exist_ok=True)
    file_path = Path(sandbox_path) / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    return str(file_path)
