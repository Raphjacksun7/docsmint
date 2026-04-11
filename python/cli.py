"""mkdocx — Minimal markdown documentation builder.

Convention:
  mkdocx commands run from the project root.
  Documentation lives in ./docs/ with this structure:

    docs/
    ├── mkdocx.config.js
    └── src/
        └── content/
            └── docs/
                └── *.md

  The rendering system (Astro, components, styles) is bundled
  inside the mkdocx package. Users never touch it.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(
    name="mkdocx",
    help="Minimal markdown documentation builder.",
    no_args_is_help=True,
)

console = Console()

# ── Paths ──────────────────────────────────────────────────────────────────────

TEMPLATE_DIR = Path(__file__).parent / "template"

DEFAULT_CONFIG = """\
export default {
  name: '%s',
  description: '',
  nav: [
    { label: 'docs', href: '/docs/getting-started' },
  ],
  footer: [],
}
"""

DEFAULT_INDEX = """\
---
title: Getting started
description: Welcome to the documentation.
order: 1
---

## Welcome

This is the first page. Edit it at `docs/src/content/docs/getting-started.md`.
"""


def _find_docs() -> Path:
    """Find the docs/ directory. Walks up from cwd looking for docs/mkdocx.config.js."""
    cwd = Path.cwd()
    for d in [cwd, *cwd.parents]:
        candidate = d / "docs"
        if (candidate / "mkdocx.config.js").exists():
            return candidate
    return cwd / "docs"


def _workdir(docs: Path) -> Path:
    """The .mkdocx working directory inside docs/."""
    return docs / ".mkdocx"


def _ensure_initialized(docs: Path) -> bool:
    """Check if docs/ is initialized. If not, offer to scaffold it."""
    if (docs / "mkdocx.config.js").exists():
        return True

    console.print()
    console.print(f"  [bold]No mkdocx project found at[/bold] {docs.relative_to(Path.cwd())}/")
    console.print()

    init = typer.confirm("  Initialize mkdocx here?", default=True)
    if not init:
        raise typer.Exit(1)

    project_name = docs.parent.name or "my-project"
    _scaffold(docs, project_name)
    return True


def _scaffold(docs: Path, name: str) -> None:
    """Create the minimal docs structure."""
    content_dir = docs / "src" / "content" / "docs"
    content_dir.mkdir(parents=True, exist_ok=True)

    config_path = docs / "mkdocx.config.js"
    if not config_path.exists():
        config_path.write_text(DEFAULT_CONFIG % name)
        console.print(f"  [green]Created[/green] {config_path.relative_to(docs.parent)}")

    index_path = content_dir / "getting-started.md"
    if not index_path.exists():
        index_path.write_text(DEFAULT_INDEX)
        console.print(f"  [green]Created[/green] {index_path.relative_to(docs.parent)}")

    # Ensure .mkdocx is gitignored
    gitignore = docs / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(".mkdocx/\n")
    elif ".mkdocx" not in gitignore.read_text():
        with open(gitignore, "a") as f:
            f.write("\n.mkdocx/\n")

    console.print()
    console.print("  [bold]Done.[/bold] Run [cyan]mkdocx preview[/cyan] to see your docs.")
    console.print()


def _prepare_workdir(docs: Path) -> Path:
    """Set up the .mkdocx working directory with the template and symlinks."""
    work = _workdir(docs)

    # Copy template if not present or if template is newer
    template_marker = work / ".template-version"
    needs_copy = not template_marker.exists()

    if needs_copy:
        if work.exists():
            shutil.rmtree(work)
        shutil.copytree(TEMPLATE_DIR, work, dirs_exist_ok=True)
        template_marker.write_text("1")
        console.print("  [dim]Template installed.[/dim]")

    # Symlink user content into the working directory
    _ensure_symlink(work / "mkdocx.config.js", docs / "mkdocx.config.js")
    _ensure_symlink(work / "src" / "content", docs / "src" / "content")

    # Install Node.js deps if needed
    if not (work / "node_modules").exists():
        console.print("  [dim]Installing dependencies (first run)...[/dim]")
        result = subprocess.run(
            ["pnpm", "install", "--prefer-offline"],
            cwd=work,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # Try npm as fallback
            result = subprocess.run(
                ["npm", "install"],
                cwd=work,
                capture_output=True,
                text=True,
            )
        if result.returncode != 0:
            console.print("  [red]Failed to install Node.js dependencies.[/red]")
            console.print("  Ensure pnpm or npm is available: [cyan]npm install -g pnpm[/cyan]")
            raise typer.Exit(1)
        console.print("  [dim]Dependencies installed.[/dim]")

    return work


def _ensure_symlink(link: Path, target: Path) -> None:
    """Create or update a symlink. Overwrites stale links."""
    if link.is_symlink():
        if link.resolve() == target.resolve():
            return
        link.unlink()
    elif link.exists():
        # Real file/dir exists — remove it so we can symlink
        if link.is_dir():
            shutil.rmtree(link)
        else:
            link.unlink()
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target.resolve())


def _run(cmd: list[str], work: Path) -> None:
    """Run a command in the working directory."""
    result = subprocess.run(cmd, cwd=work)
    sys.exit(result.returncode)


# ── Commands ───────────────────────────────────────────────────────────────────


@app.command()
def init():
    """Initialize a docs/ directory in the current project."""
    docs = Path.cwd() / "docs"
    name = Path.cwd().name or "my-project"
    _scaffold(docs, name)


@app.command()
def dev(port: int = typer.Option(4321, help="Port to listen on")):
    """Start the local development server."""
    docs = _find_docs()
    _ensure_initialized(docs)
    work = _prepare_workdir(docs)
    console.print(f"  [dim]Serving docs from {docs.relative_to(Path.cwd())}[/dim]")
    console.print()
    _run(["pnpm", "dev", "--port", str(port)], work)


@app.command()
def build():
    """Build the documentation site for production."""
    docs = _find_docs()
    _ensure_initialized(docs)
    work = _prepare_workdir(docs)
    console.print(f"  [dim]Building docs from {docs.relative_to(Path.cwd())}[/dim]")
    _run(["pnpm", "build"], work)


@app.command()
def preview():
    """Preview the production build locally."""
    docs = _find_docs()
    _ensure_initialized(docs)
    work = _prepare_workdir(docs)
    console.print(f"  [dim]Previewing docs from {docs.relative_to(Path.cwd())}[/dim]")
    _run(["pnpm", "preview"], work)


@app.command()
def clean():
    """Remove the .mkdocx working directory. Next run will reinstall."""
    docs = _find_docs()
    work = _workdir(docs)
    if work.exists():
        shutil.rmtree(work)
        console.print("  [green]Cleaned[/green] .mkdocx/")
    else:
        console.print("  Nothing to clean.")


@app.command()
def deploy(bucket: str = typer.Argument(..., help="GCS bucket (e.g. gs://my-docs)")):
    """Build and deploy to Google Cloud Storage."""
    docs = _find_docs()
    _ensure_initialized(docs)
    work = _prepare_workdir(docs)

    console.print("  [dim]Building...[/dim]")
    result = subprocess.run(["pnpm", "build"], cwd=work)
    if result.returncode != 0:
        console.print("  [red]Build failed.[/red]")
        raise typer.Exit(1)

    dist = work / "dist"
    console.print(f"  [dim]Deploying to {bucket}[/dim]")
    result = subprocess.run(
        ["gsutil", "-m", "rsync", "-r", "-d", str(dist) + "/", f"gs://{bucket}/"],
    )
    if result.returncode == 0:
        console.print(f"  [green]Deployed[/green] to gs://{bucket}/")
    else:
        console.print("  [red]Deploy failed.[/red]")
        raise typer.Exit(1)


def main():
    app()
