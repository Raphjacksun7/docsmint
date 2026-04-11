"""mkdocx Python CLI — wraps the Node.js build system."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import typer

app = typer.Typer(
    name="mkdocx",
    help="Minimal markdown documentation builder.",
    no_args_is_help=True,
)

def _root() -> Path:
    """Find project root by walking up from cwd to find mkdocx.config.js."""
    cwd = Path.cwd()
    for d in [cwd, *cwd.parents]:
        if (d / "mkdocx.config.js").exists():
            return d
    return cwd

def _run(cmd: list[str], root: Path) -> None:
    result = subprocess.run(cmd, cwd=root)
    sys.exit(result.returncode)


@app.command()
def dev(port: int = typer.Option(4321, help="Port to listen on")):
    """Start the local development server."""
    _run(["pnpm", "dev", "--port", str(port)], _root())


@app.command()
def build():
    """Build the documentation site for production."""
    _run(["pnpm", "build"], _root())


@app.command()
def preview():
    """Preview the production build locally."""
    _run(["pnpm", "preview"], _root())


@app.command()
def deploy(bucket: str = typer.Argument(..., help="GCS bucket name (e.g. my-docs)")):
    """Deploy to Google Cloud Storage."""
    root = _root()
    _run(["pnpm", "build"], root)
    _run(["gsutil", "-m", "rsync", "-r", "-d", "dist/", f"gs://{bucket}/"], root)
    typer.echo(f"  Deployed to gs://{bucket}/")


def main():
    app()
