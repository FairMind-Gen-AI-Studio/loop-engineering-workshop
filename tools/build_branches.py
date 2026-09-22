"""Regenerate every exercise starting branch from main plus its overlays.

Facilitator only. Run from the `solutions` branch after changing main or an overlay:

    python3 tools/build_branches.py        # rewrites the branches locally
    git push --force origin ex2-start ex3-goal-start ex3-loop-start ex4-start

A starting branch is always main plus the layers named below, never hand-edited,
so a fix to main reaches every exercise. Overlays keep `.fairmind/` as `_fairmind/`
so the tree that holds them is not mistaken for a loop workspace.
"""

import pathlib
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
OVERLAYS = ROOT / "tools" / "overlays"
BRANCHES = {
    "ex2-start": ["ex2-start"],
    "ex3-goal-start": ["ex3-goal-start"],
    "ex3-loop-start": ["ex3-goal-start", "ex3-loop-start"],
    "ex4-start": ["ex4-start"],
}


def git(*args, cwd=ROOT):
    return subprocess.run(["git", *args], cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()


def apply_layer(layer, tree):
    source = OVERLAYS / layer
    for path in sorted(p for p in source.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
        rel = path.relative_to(source)
        if rel.parts[0] == "_fairmind":
            rel = pathlib.Path(".fairmind", *rel.parts[1:])
        target = tree / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def main():
    for branch, layers in BRANCHES.items():
        tree = pathlib.Path(tempfile.mkdtemp(prefix=f"workshop-{branch}-"))
        git("worktree", "add", "--detach", str(tree), "main")
        try:
            for layer in layers:
                apply_layer(layer, tree)
            git("add", "-A", cwd=tree)
            git("commit", "-m", f"{branch}: starting point for the exercise", cwd=tree)
            sha = git("rev-parse", "HEAD", cwd=tree)
            git("branch", "-f", branch, sha)
            print(f"{branch:16} {sha[:7]}  main + {', '.join(layers)}")
        finally:
            git("worktree", "remove", "--force", str(tree))


if __name__ == "__main__":
    main()
