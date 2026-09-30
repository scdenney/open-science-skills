#!/usr/bin/env python3
"""Install the shared Jev verifier runtime for the existing orchestrate skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import uuid
from typing import Iterator


PACKAGE_NAME = "jev-verifier"
LEGACY_SKILL_NAME = "orchestrate-ver"
MANIFEST = ".oss-jev-installer.json"
REQUIRED_PACKAGE_FILES = (
    Path("ORCHESTRATE.md"),
    Path("tools") / "jev" / "verify.py",
    Path("tools") / "jev" / "contracts" / "orchestrate.json",
)
SOURCE_REQUIRED_FILES = REQUIRED_PACKAGE_FILES + (
    Path("FACT-CHECK.md"),
    Path("CITATION-CHECK.md"),
    # ROUTE.md and the route contract are validated in the source bundle only.
    # REQUIRED_PACKAGE_FILES stays as it was so an already-installed version
    # predating the route path still validates as installer-owned.
    Path("ROUTE.md"),
    Path("tools") / "jev" / "README.md",
    Path("tools") / "jev" / "contracts" / "fact-check.json",
    Path("tools") / "jev" / "contracts" / "citation-check.json",
    Path("tools") / "jev" / "contracts" / "route.json",
    Path("tools") / "jev" / "samples" / "route-state.json",
    Path("tools") / "jev" / "samples" / "route-unavailable-state.json",
    Path("tools") / "jev" / "samples" / "route-mock-response.json",
    Path("tools") / "jev" / "samples" / "fact-check-manifest.json",
    Path("tools") / "jev" / "samples" / "fact-check-not-checked-manifest.json",
    Path("tools") / "jev" / "samples" / "fact-check-mock-response.json",
    Path("tools") / "jev" / "samples" / "fact-check-source.txt",
    Path("tools") / "jev" / "samples" / "citation-check-manifest.json",
    Path("tools") / "jev" / "samples" / "citation-check-mock-response.json",
    Path("tools") / "jev" / "samples" / "citation-check-record.json",
)
# A complete orchestrate skill in either library satisfies the dependency. The
# runtime is shared, so neither vendor is privileged and neither is required: a
# Claude-only host resolves against the plugin skill and needs no Codex checkout.
REQUIRED_ORCHESTRATE_FILES = (
    Path("SKILL.md"),
    Path("scripts") / "check-lead-runtime.sh",
)
CLAUDE_ORCHESTRATE_FILES = (
    Path("SKILL.md"),
    Path("agents") / "deep-reasoner.md",
    Path("agents") / "fast-worker.md",
)
ORCHESTRATE_SHAPES = (CLAUDE_ORCHESTRATE_FILES, REQUIRED_ORCHESTRATE_FILES)
LIBRARY_SKILL_PARENTS = (Path("plugin") / "skills", Path("codex"))
LEGACY_IGNORED_PARTS = {"__pycache__", ".DS_Store", ".git", MANIFEST}
IGNORED_PARTS = LEGACY_IGNORED_PARTS | {".pytest_cache", ".mypy_cache", ".ruff_cache"}


def source_root() -> Path:
    return Path(__file__).resolve().parent


def package_files(root: Path, *, legacy: bool = False) -> Iterator[Path]:
    ignored = LEGACY_IGNORED_PARTS if legacy else IGNORED_PARTS
    for path in sorted(root.rglob("*")):
        if any(part in ignored for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            yield path


def content_hash(root: Path, *, legacy: bool = False) -> str:
    digest = hashlib.sha256()
    for path in package_files(root, legacy=legacy):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def git_commit(root: Path) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return completed.stdout.strip() or None


def validate_package(root: Path) -> list[str]:
    missing = [str(item) for item in SOURCE_REQUIRED_FILES if not (root / item).is_file()]
    verify = root / "tools" / "jev" / "verify.py"
    if verify.is_file() and not os.access(verify, os.X_OK):
        missing.append(f"{verify.relative_to(root)} (not executable)")
    return missing


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def complete_orchestrate(candidate: Path) -> bool:
    return candidate.is_dir() and any(
        all((candidate / item).is_file() for item in shape) for shape in ORCHESTRATE_SHAPES
    )


def resolve_orchestrate(skill_root: Path, root: Path) -> Path | None:
    """Locate a complete orchestrate skill for the target root or source checkout.

    The installed skill under the chosen target wins, so an existing install
    resolves exactly as before. Otherwise each library's counterpart in the
    source checkout is tried, in either shape.
    """
    candidates = [skill_root / "orchestrate"]
    for ancestor in (root, *root.parents):
        for parent in LIBRARY_SKILL_PARENTS:
            counterpart = ancestor / parent / "orchestrate"
            if counterpart not in candidates:
                candidates.append(counterpart)
    for candidate in candidates:
        if complete_orchestrate(candidate):
            return candidate.resolve()
    return None


def valid_installed_version(version_dir: Path, expected_hash: str, *, legacy: bool = False) -> bool:
    if version_dir.name != expected_hash or version_dir.is_symlink() or not version_dir.is_dir():
        return False
    try:
        manifest = json.loads((version_dir / MANIFEST).read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            return False
        required = (
            (Path("skills") / LEGACY_SKILL_NAME / "SKILL.md",
             Path("skills") / LEGACY_SKILL_NAME / "agents" / "openai.yaml",
             *REQUIRED_PACKAGE_FILES[1:])
            if legacy else REQUIRED_PACKAGE_FILES
        )
        complete = all((version_dir / item).is_file() for item in required)
        verified_hash = content_hash(version_dir, legacy=legacy)
    except (OSError, ValueError):
        return False
    return (
        manifest.get("installer") == PACKAGE_NAME
        and manifest.get("content_hash") == expected_hash
        and complete
        and os.access(version_dir / "tools" / "jev" / "verify.py", os.X_OK)
        and verified_hash == expected_hash
    )


def installer_owned(link: Path, data_dir: Path, *, legacy: bool = False) -> bool:
    if not link.is_symlink():
        return False
    try:
        target = link.resolve(strict=True)
        data = data_dir.resolve(strict=True)
    except (OSError, RuntimeError):
        return False
    try:
        target.relative_to(data)
    except ValueError:
        return False
    version_dir = target.parent.parent if legacy else target
    expected_target = data / version_dir.name
    if legacy:
        expected_target = expected_target / "skills" / LEGACY_SKILL_NAME
    if target != expected_target:
        return False
    return valid_installed_version(version_dir, version_dir.name, legacy=legacy)


def copy_package(source: Path, destination: Path) -> None:
    shutil.copytree(
        source, destination,
        ignore=shutil.ignore_patterns(*IGNORED_PARTS),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="show actions without writing")
    parser.add_argument("--target", type=Path, default=Path.home() / ".agents" / "skills",
                        help="skill root used to find orchestrate and migrate an obsolete orchestrate-ver link")
    parser.add_argument("--data-dir", type=Path,
                        default=Path.home() / ".local" / "share" / "oss-experiments" / PACKAGE_NAME,
                        help="versioned installer data directory")
    args = parser.parse_args()
    source = source_root()
    missing = validate_package(source)
    if missing:
        parser.error("incomplete prototype bundle: " + ", ".join(missing))
    skill_root = args.target.expanduser().resolve()
    data_dir = args.data_dir.expanduser().resolve()
    dependency = resolve_orchestrate(skill_root, source)
    if dependency is None:
        parser.error("missing complete orchestrate dependency (need SKILL.md plus either agents/deep-reasoner.md and agents/fast-worker.md, or scripts/check-lead-runtime.sh)")
    digest = content_hash(source)
    version_dir = data_dir / digest
    link = data_dir / "current"
    legacy_link = skill_root / LEGACY_SKILL_NAME
    if link.exists() or link.is_symlink():
        if not installer_owned(link, data_dir):
            parser.error(f"refusing to replace user-owned target: {link}")
    if legacy_link.exists() or legacy_link.is_symlink():
        if not installer_owned(legacy_link, data_dir, legacy=True):
            parser.error(f"refusing to remove user-owned or invalid legacy target: {legacy_link}")
    if version_dir.exists() or version_dir.is_symlink():
        if not valid_installed_version(version_dir, digest):
            parser.error(f"refusing existing invalid or unrecognized version directory: {version_dir}")
    actions = [
        f"validated orchestrate dependency: {dependency}",
        f"install bundle: {source} -> {version_dir}",
        f"link runtime: {link} -> {version_dir}",
    ]
    if legacy_link.is_symlink():
        actions.append(f"remove obsolete installer-owned skill link: {legacy_link}")
    if args.dry_run:
        print("\n".join(actions))
        return 0
    data_dir.mkdir(parents=True, exist_ok=True)
    if not version_dir.exists():
        copy_package(source, version_dir)
        manifest = {
            "installer": PACKAGE_NAME,
            "content_hash": digest,
            "source_commit": git_commit(source),
            "source_path": str(source),
            "orchestrate_dependency": {
                "path": str(dependency),
                "skill_sha256": file_hash(dependency / "SKILL.md"),
                "git_commit": git_commit(dependency),
            },
        }
        (version_dir / MANIFEST).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary_link = data_dir / f".current-{uuid.uuid4().hex}"
    try:
        temporary_link.symlink_to(version_dir, target_is_directory=True)
        temporary_link.replace(link)
    finally:
        if temporary_link.is_symlink():
            temporary_link.unlink()
    if legacy_link.is_symlink():
        legacy_link.unlink()
    print("\n".join(actions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
