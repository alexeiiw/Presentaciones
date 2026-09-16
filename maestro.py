from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def main() -> int:
    comando = [sys.executable, "-m", "streamlit", "run", "app.py"]
    return subprocess.call(comando, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
