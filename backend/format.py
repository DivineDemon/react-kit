import subprocess
import sys
from pathlib import Path

"""
A focused script to format and lint only the `/backend/app` directory, skipping caches.
Enforces:
  - 2-space indentation (via YAPF)
  - Sorted imports (isort)
  - PEP8 compliance
  - No unused variables
  - No debug print statements
  - Automatic fixes where possible
"""

BASE_DIR = Path(__file__).parent

TARGET_DIR = BASE_DIR / 'app'

tools = [
    (
        'isort',
        [
            '--profile', 'black',
            str(TARGET_DIR)
        ],
    ),
    (
        'yapf',
        [
            '--recursive',
            '--in-place',
            '--style', '{based_on_style: pep8, indent_width: 2}',
            str(TARGET_DIR)
        ],
    ),
    (
        'ruff',
        [
            'check',
            str(TARGET_DIR),
            '--select', 'E,F,W,I,T201',
            '--fix',
            '--exclude', '*.ruffcache*',
        ],
    ),
    (
        'flake8',
        [
            '--max-line-length', '88',
            '--select', 'E9,F63,F7,F82',
            '--exclude', '.ruffcache',
            str(TARGET_DIR)
        ],
    ),
]


def run_tool(module_name, args):
    cmd = [sys.executable, '-m', module_name, *args]
    print(f"⇢ Running {module_name} {' '.join(args)}…")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"✗ {module_name} failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def main():
    if not TARGET_DIR.exists():
        print(f"Error: target directory '{TARGET_DIR}' does not exist.")
        sys.exit(1)

    for module, args in tools:
        run_tool(module, args)

    print(f"✅ All done: formatting and linting passed for {TARGET_DIR}")


if __name__ == '__main__':
    main()
