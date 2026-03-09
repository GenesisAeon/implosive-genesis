"""Implosive Genesis CLI – scaffold, validate and inspect project templates."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .core.vrig import V_RIG_KMS, compute_vrig
from .core.type6 import Type6Implosive
from .core.physics import PHI
from .preset import scaffold as _scaffold
from .templates import REGISTRY
from .validator import validate as _validate

app = typer.Typer(
    name="ig",
    help="Implosive Genesis – rekursive Entstehung von Raum, Zeit und Bewusstsein.",
    add_completion=True,
    rich_markup_mode="rich",
)
console = Console()
err_console = Console(stderr=True)


# ---------------------------------------------------------------------------
# scaffold
# ---------------------------------------------------------------------------


@app.command()
def scaffold(
    project_name: Annotated[
        str, typer.Argument(help="Name of the new project (kebab-case recommended)")
    ],
    template: Annotated[str, typer.Option("--template", "-t", help="Template to use")] = "minimal",
    output_dir: Annotated[
        Path | None, typer.Option("--output-dir", "-o", help="Parent directory for the new project")
    ] = None,
    author: Annotated[str | None, typer.Option(help="Author name")] = None,
    description: Annotated[str | None, typer.Option(help="Short project description")] = None,
    python_version: Annotated[
        str | None, typer.Option(help="Minimum Python version (e.g. 3.11)")
    ] = None,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Preview files without writing them")
    ] = False,
) -> None:
    """[bold]Scaffold a new project[/bold] from a template.

    Examples:

      ig scaffold my-tool

      ig scaffold my-tool --template genesis --author "Ada Lovelace"

      ig scaffold my-tool --dry-run
    """
    if template not in REGISTRY:
        err_console.print(
            f"[red]Unknown template '[bold]{template}[/bold]'. "
            f"Run [bold]ig list-templates[/bold] to see available options.[/red]"
        )
        raise typer.Exit(code=1)

    dest = output_dir or Path.cwd()
    project_path = dest / project_name

    if project_path.exists() and not dry_run:
        err_console.print(
            f"[red]Directory [bold]{project_path}[/bold] already exists. "
            "Use a different name or [bold]--output-dir[/bold].[/red]"
        )
        raise typer.Exit(code=1)

    overrides = {
        "author": author,
        "description": description,
        "python_version": python_version,
    }

    tmpl = REGISTRY[template]
    mode = "[yellow]DRY RUN[/yellow] — " if dry_run else ""
    console.print(
        Panel(
            f"{mode}[bold green]Scaffolding[/bold green] [cyan]{project_name}[/cyan] "
            f"with template [magenta]{template}[/magenta]",
            expand=False,
        )
    )

    written = _scaffold(project_name, tmpl, dest, overrides=overrides, dry_run=dry_run)

    table = Table(show_header=False, box=None, padding=(0, 2))
    for path in written:
        rel = path.relative_to(dest)
        icon = "📄" if dry_run else "✅"
        table.add_row(icon, str(rel))
    console.print(table)

    if dry_run:
        console.print("\n[yellow]Dry run — no files were written.[/yellow]")
    else:
        console.print(
            f"\n[bold green]Done![/bold green] Project created at [cyan]{project_path}[/cyan]\n"
            f"\nNext steps:\n"
            f"  [dim]cd[/dim] {project_name}\n"
            f"  [dim]uv sync --dev[/dim]\n"
            f"  [dim]pre-commit install[/dim]\n"
            f"  [dim]uv run pytest[/dim]"
        )


# ---------------------------------------------------------------------------
# list-templates
# ---------------------------------------------------------------------------


@app.command(name="list-templates")
def list_templates() -> None:
    """List all available templates."""
    table = Table(title="Available Templates", show_lines=True)
    table.add_column("Name", style="magenta bold", no_wrap=True)
    table.add_column("Description")
    table.add_column("Extra variables", style="dim")

    for name, tmpl in REGISTRY.items():
        base_vars = {"name", "description", "author", "python_version"}
        extras = sorted(set(tmpl.get("variables", [])) - base_vars)
        table.add_row(name, tmpl["description"], ", ".join(extras) or "—")

    console.print(table)


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------


@app.command()
def validate(
    path: Annotated[Path | None, typer.Argument(help="Project directory to validate")] = None,
) -> None:
    """Validate a project directory against implosive-genesis best practices."""
    target = path or Path.cwd()
    result = _validate(target)

    console.print(f"\nValidating [cyan]{target}[/cyan]\n")

    for msg in result.passed:
        console.print(f"  [green]✔[/green]  {msg}")
    for msg in result.warnings:
        console.print(f"  [yellow]⚠[/yellow]  {msg}")
    for msg in result.errors:
        console.print(f"  [red]✘[/red]  {msg}")

    console.print()
    if result.ok:
        console.print("[bold green]All checks passed.[/bold green]")
    else:
        console.print(f"[bold red]{len(result.errors)} error(s) found.[/bold red]")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# version
# ---------------------------------------------------------------------------


@app.command()
def version() -> None:
    """Show the implosive-genesis version."""
    console.print(f"implosive-genesis [bold]{__version__}[/bold]")


# ---------------------------------------------------------------------------
# vrig-calc
# ---------------------------------------------------------------------------


@app.command(name="vrig-calc")
def vrig_calc(
    beta0: Annotated[
        float, typer.Option("--beta0", help="Basis-Kopplungskonstante β₀")
    ] = 1.0,
    n: Annotated[
        int, typer.Option("--n", help="Phi-Skalierungsstufe für β_n")
    ] = 3,
    samples: Annotated[
        int, typer.Option("--samples", "-s", help="Anzahl Monte-Carlo-Samples")
    ] = 10_000,
    noise_sigma: Annotated[
        float, typer.Option("--sigma", help="Gaußsches Rauschen σ [km/s]")
    ] = 12.0,
    seed: Annotated[
        int | None, typer.Option("--seed", help="Zufalls-Seed (für Reproduzierbarkeit)")
    ] = None,
) -> None:
    """[bold]Berechne V_RIG[/bold] – Rekursive Implosionsgeschwindigkeit mit Monte-Carlo.

    Formel: v = V_RIG · β_n,  β_n = β₀ · Φ^{n/3}

    Examples:

      ig vrig-calc

      ig vrig-calc --n 6 --samples 50000 --seed 42

      ig vrig-calc --beta0 0.5 --sigma 5.0
    """
    result = compute_vrig(beta_0=beta0, n=n, samples=samples, noise_sigma=noise_sigma, seed=seed)

    console.print(
        Panel(
            f"[bold cyan]V_RIG Berechnung[/bold cyan]  "
            f"(β₀={beta0}, n={n}, Φ={PHI:.6f})",
            expand=False,
        )
    )

    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("Parameter", style="bold magenta", no_wrap=True)
    table.add_column("Wert", style="cyan")
    table.add_column("Einheit", style="dim")

    table.add_row("V_RIG (Basis)", f"{V_RIG_KMS:.4f}", "km/s")
    table.add_row("β_n (Phi-skaliert)", f"{result.v_rig / V_RIG_KMS:.6f}", "—")
    table.add_row("V_RIG (Mittelwert MC)", f"[bold]{result.v_rig:.4f}[/bold]", "km/s")
    table.add_row("Standardabweichung σ", f"{result.std_dev:.4f}", "km/s")
    table.add_row("α_Φ (cosmic alpha · Φ)", f"{result.alpha_phi:.10f}", "—")
    table.add_row("Monte-Carlo Samples", f"{result.samples:,}", "—")

    console.print(table)
    console.print(
        f"\n[bold green]V_RIG = {result.v_rig:.2f} ± {result.std_dev:.2f} km/s[/bold green]"
    )


# ---------------------------------------------------------------------------
# type6-sim
# ---------------------------------------------------------------------------


@app.command(name="type6-sim")
def type6_sim(
    steepness: Annotated[
        float, typer.Option("--steepness", "-k", help="Steilheit des invertierten Sigmoids")
    ] = PHI,
    threshold: Annotated[
        float, typer.Option("--threshold", "-t", help="Sprungpunkt des Kubikwurzel-Sprungs")
    ] = 0.0,
    amplitude: Annotated[
        float, typer.Option("--amplitude", "-a", help="Amplitude des Kubikwurzel-Sprungs")
    ] = 1.0,
    xmin: Annotated[float, typer.Option("--xmin", help="Untere Grenze des x-Bereichs")] = -3.0,
    xmax: Annotated[float, typer.Option("--xmax", help="Obere Grenze des x-Bereichs")] = 3.0,
    steps: Annotated[
        int, typer.Option("--steps", help="Anzahl der Simulationsschritte")
    ] = 11,
) -> None:
    """[bold]Simuliere UTAC Type-6[/bold] Implosive Singularität.

    R(x) = inverted_sigmoid(x; k) + cubic_root_jump(x; threshold, amplitude)

    Examples:

      ig type6-sim

      ig type6-sim --xmin -5 --xmax 5 --steps 20

      ig type6-sim --steepness 2.0 --threshold 1.0 --amplitude 0.5
    """
    if xmin >= xmax:
        err_console.print("[red]--xmin muss kleiner als --xmax sein.[/red]")
        raise typer.Exit(code=1)
    if steps < 2:
        err_console.print("[red]--steps muss ≥ 2 sein.[/red]")
        raise typer.Exit(code=1)

    model = Type6Implosive(steepness=steepness, threshold=threshold, amplitude=amplitude)
    points = model.simulate((xmin, xmax), steps=steps)

    console.print(
        Panel(
            f"[bold cyan]Type-6 Simulation[/bold cyan]  "
            f"(k={steepness:.4f}, threshold={threshold}, amplitude={amplitude})",
            expand=False,
        )
    )

    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("x", style="dim", no_wrap=True)
    table.add_column("sigmoid(x)", style="yellow")
    table.add_column("jump(x)", style="blue")
    table.add_column("R(x) = combined", style="bold green")

    for x, r in points:
        sig = model.sigmoid_only(x)
        jmp = model.jump_only(x)
        table.add_row(f"{x:+.4f}", f"{sig:.6f}", f"{jmp:+.6f}", f"{r:+.6f}")

    console.print(table)
    console.print(
        f"\n[bold]Kritischer Punkt:[/bold] x = {model.critical_point():.4f}  "
        f"[dim](Φ-Steilheit = {steepness:.6f})[/dim]"
    )


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
