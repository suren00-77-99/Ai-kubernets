#!/usr/bin/env python3
"""Run file-aware, deterministic checks before packaging the application."""
from pathlib import Path
import ast
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".venv", "__pycache__", "node_modules"}


def project_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and not (set(path.parts) & IGNORED):
            yield path


def report(command, relative, input_text=None):
    result = subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, input=input_text
    )
    if result.returncode:
        print(f"FAIL {relative}\n{result.stdout}{result.stderr}".rstrip())
        return False
    print(f"OK {relative}")
    return True


def main():
    ok = True
    for path in project_files():
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() == ".html":
            ok = report([sys.executable, "checks/check_html.py", relative], relative) and ok
        elif path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=relative)
                print(f"OK Python syntax: {relative}")
            except (SyntaxError, UnicodeError) as exc:
                print(f"FAIL {relative}: {exc}")
                ok = False
        elif path.suffix.lower() in {".yml", ".yaml"}:
            if "templates" in path.parts:
                # Helm templates contain Go template expressions that are not
                # valid YAML until Helm renders them. Helm lint/template below
                # validates these files after rendering.
                print(f"SKIP raw YAML lint (Helm template): {relative}")
            else:
                ok = report(["yamllint", "-d", "{extends: relaxed, rules: {line-length: disable, truthy: disable}}", relative], relative) and ok
        elif path.suffix == ".sh":
            ok = report(["bash", "-n", relative], relative) and ok
    dockerfile = ROOT / "Dockerfile"
    if dockerfile.exists():
        ok = report(
            ["docker", "run", "--rm", "-i", "hadolint/hadolint:v2.15.1"],
            "Dockerfile",
            input_text=dockerfile.read_text(encoding="utf-8"),
        ) and ok
    chart = ROOT / "helm/app"
    if chart.exists():
        ok = report(["helm", "lint", "helm/app"], "helm/app") and ok
        ok = report(["helm", "template", "self-healing-demo", "helm/app"], "helm/app render") and ok
    print("\nAll project checks passed." if ok else "\nOne or more project checks failed.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
