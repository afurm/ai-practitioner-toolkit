"""Install reviewed local skill files without network access or overwriting edits."""

import argparse
from pathlib import Path
import shutil
import stat
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "ai-practitioner"


def reject_links(path):
    """Reject links/junctions in an installation path, including ancestors."""
    for part in (path, *path.parents):
        junction = getattr(part, "is_junction", lambda: False)()
        try:
            attributes = getattr(part.lstat(), "st_file_attributes", 0)
        except FileNotFoundError:
            attributes = 0
        reparse = attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if part.is_symlink() or junction or reparse:
            raise ValueError(f"Refusing linked installation path: {part}")


def manifest(folder):
    reject_links(folder)
    result = {}
    for path in sorted(folder.rglob("*")):
        reject_links(path)
        if path.is_file():
            result[path.relative_to(folder).as_posix()] = path.read_bytes()
    return result


def installation_plan(tool, project=None, home=None):
    base = Path(project).expanduser().absolute() if project else Path(home or Path.home()).absolute()
    reject_links(base)
    if not base.is_dir():
        raise ValueError(f"Installation base must be an existing directory: {base}")
    selected = ("codex", "claude") if tool == "both" else (tool,)
    parents = {"codex": ".agents", "claude": ".claude"}
    source_files = manifest(SOURCE)
    plan = []
    for item in selected:
        dest = base / parents[item] / "skills" / SOURCE.name
        reject_links(dest)
        if dest.exists():
            if not dest.is_dir() or manifest(dest) != source_files:
                raise ValueError(f"Existing skill differs; preserve and compare it manually: {dest}")
            plan.append((dest, "unchanged"))
        else:
            plan.append((dest, "install"))
    return plan


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=("codex", "claude", "both"), required=True)
    parser.add_argument("--project", type=Path, help="Existing project directory; default is personal scope")
    parser.add_argument("--dry-run", action="store_true", help="Show planned copies without writing")
    args = parser.parse_args(argv)
    try:
        plan = installation_plan(args.tool, args.project)
        for dest, action in plan:
            print(f"{action}: {dest}")
        if args.dry_run:
            print("Dry run: no files written.")
            return 0
        for dest, action in plan:
            if action == "install":
                reject_links(dest)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(SOURCE, dest)
        print("Done. Reopen your assistant session if the skill is not visible.")
        return 0
    except (ValueError, OSError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
