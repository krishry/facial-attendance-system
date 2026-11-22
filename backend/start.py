import os
import sys
import subprocess

print("Running database migrations...", flush=True)

subprocess.run(
    [sys.executable, "-m", "alembic", "upgrade", "head"],
    check=True,
)

print("Migrations completed. Starting FastAPI...", flush=True)

port = os.environ.get("PORT", "10000")

os.execv(
    sys.executable,
    [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", port,
    ],
)
