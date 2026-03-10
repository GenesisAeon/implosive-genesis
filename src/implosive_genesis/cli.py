"""Implosive Genesis CLI – scaffold, validate and inspect project templates."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .core.physics import PHI
from .core.type6 import Type6Implosive
from .core.vrig import V_RIG_KMS, compute_vrig
from .preset import scaffold as _scaffold
from .simulation.cosmic_moments import CosmicMomentsSimulator
from .simulation.entropy_governance import EntropyGovernance
from .templates import REGISTRY
from .theory.frameprinciple import FramePrinciple, OIPKernel
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
    beta0: Annotated[float, typer.Option("--beta0", help="Basis-Kopplungskonstante β₀")] = 1.0,
    n: Annotated[int, typer.Option("--n", help="Phi-Skalierungsstufe für β_n")] = 3,
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
            f"[bold cyan]V_RIG Berechnung[/bold cyan]  (β₀={beta0}, n={n}, Φ={PHI:.6f})",
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
    steps: Annotated[int, typer.Option("--steps", help="Anzahl der Simulationsschritte")] = 11,
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
# simulate
# ---------------------------------------------------------------------------


@app.command()
def simulate(
    n_max: Annotated[
        int, typer.Option("--n-max", "-n", help="Maximale Rekursionsstufe (inklusiv)")
    ] = 7,
    temperature: Annotated[
        float, typer.Option("--temperature", "-T", help="Temperatur in Kelvin (CMB = 2.725 K)")
    ] = 2.725,
    t_0: Annotated[float, typer.Option("--t0", help="Grundzeitscheibe t₀ (normiert)")] = 1.0,
) -> None:
    """[bold]Implosive Genesis Simulation[/bold] – Phi-skalierte Zeitevolution.

    Berechnet kosmische Momente für n = 0, …, n_max mit Zeitscheiben,
    Resonanzfrequenzen, entropischen Preisen und CREP-Beiträgen.

    Examples:

      ig simulate

      ig simulate --n-max 10 --temperature 2.725

      ig simulate --n-max 5 --t0 1e-15
    """
    sim = CosmicMomentsSimulator(n_max=n_max, temperature=temperature, t_0=t_0)
    moments = sim.run()

    console.print(
        Panel(
            f"[bold cyan]Implosive Genesis Simulation[/bold cyan]  "
            f"(n_max={n_max}, T={temperature} K, t₀={t_0}, Φ={PHI:.6f})",
            expand=False,
        )
    )

    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("n", style="bold magenta", no_wrap=True)
    table.add_column("T_n", style="cyan")
    table.add_column("f_R [Hz]", style="yellow")
    table.add_column("P_E [J]", style="blue")
    table.add_column("I_n [J]", style="green")
    table.add_column("Φ^n", style="dim")

    for m in moments:
        table.add_row(
            str(m.n),
            f"{m.time_slice:.4e}",
            f"{m.resonance_freq:.4e}",
            f"{m.entropy_price_j:.4e}",
            f"{m.impulse_energy_j:.4e}",
            f"{m.expansion_ratio:.6f}",
        )

    console.print(table)

    peak = sim.peak_moment()
    total_ep = sim.total_entropy_price()
    console.print(
        f"\n[bold]Peak-Resonanz:[/bold] n={peak.n}  "
        f"f_R = [cyan]{peak.resonance_freq:.4e}[/cyan] Hz\n"
        f"[bold]Gesamt P_E:[/bold]    [blue]{total_ep:.4e}[/blue] J"
    )


# ---------------------------------------------------------------------------
# entropy-price
# ---------------------------------------------------------------------------


@app.command(name="entropy-price")
def entropy_price(
    n_max: Annotated[
        int, typer.Option("--n-max", "-n", help="Maximale Rekursionsstufe (inklusiv)")
    ] = 7,
    temperature: Annotated[
        float, typer.Option("--temperature", "-T", help="Temperatur in Kelvin")
    ] = 2.725,
    ceiling: Annotated[
        float | None,
        typer.Option("--ceiling", "-c", help="Optionale Entropiedecke in Joule"),
    ] = None,
) -> None:
    """[bold]Entropischer Preis[/bold] – Governance-Bericht der Rekursionsstufen.

    P_E(n, T) = n · k_B · T · ln(Φ)

    Zeigt Budget-Anteile, CREP-Beiträge und optionale Überschreitungen
    einer Entropiedecke (--ceiling).

    Examples:

      ig entropy-price

      ig entropy-price --n-max 10 --temperature 2.725

      ig entropy-price --ceiling 1e-23
    """
    gov = EntropyGovernance(n_max=n_max, temperature=temperature, ceiling_j=ceiling)
    report = gov.governance_report()

    ceiling_str = f"{ceiling:.3e} J" if ceiling is not None else "—"
    console.print(
        Panel(
            f"[bold cyan]Entropy-Price Governance[/bold cyan]  "
            f"(n_max={n_max}, T={temperature} K, ceiling={ceiling_str})",
            expand=False,
        )
    )

    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("n", style="bold magenta", no_wrap=True)
    table.add_column("P_E [J]", style="blue")
    table.add_column("Budget %", style="cyan")
    table.add_column("CREP", style="yellow")
    table.add_column("Overflow [J]", style="red")

    for b in report.budgets:
        overflow_str = f"{b.overflow_j:.3e}" if b.is_overflow else "[green]—[/green]"
        table.add_row(
            str(b.n),
            f"{b.entropy_price_j:.4e}",
            f"{b.budget_fraction * 100:.2f}%",
            f"{b.crep_contribution:.4e}",
            overflow_str,
        )

    console.print(table)
    console.print(
        f"\n[bold]Gesamt-Entropie:[/bold] [blue]{report.total_entropy_j:.4e}[/blue] J\n"
        f"[bold]Gesamt-CREP:[/bold]    [yellow]{report.total_crep:.4e}[/yellow]\n"
        f"[bold]Overflow-Stufen:[/bold] {report.n_overflow}"
    )


# ---------------------------------------------------------------------------
# frame-render
# ---------------------------------------------------------------------------


@app.command(name="frame-render")
def frame_render(
    n_max: Annotated[
        int, typer.Option("--n-max", "-n", help="Maximale Rekursionsstufe (inklusiv)")
    ] = 7,
    lambda_m: Annotated[
        float | None,
        typer.Option("--lambda", "-l", help="OIPK-Wellenlänge λ in Metern (Standard: c/V_RIG)"),
    ] = None,
) -> None:
    """[bold]Frame-Render[/bold] – Kohärenzlängen und Stabilität des OIPK-Rahmens.

    Rendert die Frame-Principle-Struktur für n = 0, …, n_max:
    Kohärenzlänge L_n = λ_OIPK · Φ^{n/3}, Impulsenergie I_n und Stabilität S_F(n).

    Examples:

      ig frame-render

      ig frame-render --n-max 10

      ig frame-render --lambda 1e-3
    """
    from .theory.frameprinciple import LAMBDA_OIPK_DEFAULT

    lam = lambda_m if lambda_m is not None else LAMBDA_OIPK_DEFAULT
    from .core.vrig import cosmic_alpha_phi

    kernel = OIPKernel(lambda_m=lam, alpha_phi=cosmic_alpha_phi())
    frame = FramePrinciple(kernel=kernel)

    console.print(
        Panel(
            f"[bold cyan]Frame-Render[/bold cyan]  "
            f"(n_max={n_max}, λ_OIPK={lam:.4e} m, Φ={PHI:.6f})",
            expand=False,
        )
    )

    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("n", style="bold magenta", no_wrap=True)
    table.add_column("L_n [m]", style="cyan")
    table.add_column("I_n [J]", style="green")
    table.add_column("S_F(n)", style="yellow")
    table.add_column("Φ^{n/3}", style="dim")

    for n in range(n_max + 1):
        l_n = frame.coherence_length(n)
        i_n = frame.impulse_energy(n)
        s_n = frame.stability_at(n)
        phi_n3 = PHI ** (n / 3)
        table.add_row(
            str(n),
            f"{l_n:.4e}",
            f"{i_n:.4e}",
            f"{s_n:.4e}",
            f"{phi_n3:.6f}",
        )

    console.print(table)
    console.print(
        f"\n[bold]OIPK Energie:[/bold]    [green]{kernel.energy():.4e}[/green] J\n"
        f"[bold]Frame-Stabilität:[/bold] [yellow]{kernel.frame_stability():.4e}[/yellow]\n"
        f"[bold]θ_⊥:[/bold]            {kernel.orthogonality_angle_deg():.4f}°"
    )


# ---------------------------------------------------------------------------
# entropy-price (SymPy-erweitert, v0.2.0)
# ---------------------------------------------------------------------------


@app.command(name="entropy-price-sympy")
def entropy_price_sympy(
    n_max: Annotated[int, typer.Option("--n-max", "-n", help="Maximale Rekursionsstufe")] = 7,
    temperature: Annotated[
        float, typer.Option("--temperature", "-T", help="Temperatur in Kelvin")
    ] = 2.725,
    steps: Annotated[
        int, typer.Option("--steps", "-s", help="Riemann-Integrations-Schritte")
    ] = 10_000,
    bits: Annotated[float, typer.Option("--bits", help="Informationsgehalt in Bits")] = 1.0,
    show_proof: Annotated[bool, typer.Option("--show-proof", help="Zeige SymPy-Beweise")] = False,
) -> None:
    """[bold]Entropischer Preis (SymPy)[/bold] – Numerische Integration + symbolischer Beweis.

    E_price = ∫(S_V - S_A)dV + k_B · T · ln2 · bits

    Verwendet SymPy für symbolische Ableitung und Riemann-Summe für numerische Integration.

    Examples:

      ig entropy-price-sympy

      ig entropy-price-sympy --steps 10000 --n-max 10

      ig entropy-price-sympy --show-proof --bits 8.0
    """
    from .formalization.entropic_price import EntropicPriceDerivation, integrate_entropic_price

    result = integrate_entropic_price(n_max=n_max, temperature=temperature, bits=bits, steps=steps)
    deriv = EntropicPriceDerivation(n_max_val=n_max, temperature=temperature, bits_val=bits)

    console.print(
        Panel(
            f"[bold cyan]Entropischer Preis (SymPy + Numerisch)[/bold cyan]  "
            f"(n_max={n_max}, T={temperature} K, steps={steps:,}, bits={bits})",
            expand=False,
        )
    )

    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("Komponente", style="bold magenta", no_wrap=True)
    table.add_column("Wert [J]", style="cyan")
    table.add_column("Anteil", style="dim")

    total = result.e_price_j
    frac_int = result.integral_part_j / total if total > 0 else 0.0
    frac_info = result.info_part_j / total if total > 0 else 0.0

    table.add_row("∫(S_V - S_A)dV", f"{result.integral_part_j:.6e}", f"{frac_int * 100:.2f}%")
    table.add_row("k_B·T·ln2·bits", f"{result.info_part_j:.6e}", f"{frac_info * 100:.2f}%")
    table.add_row("[bold]E_price (gesamt)[/bold]", f"[bold]{result.e_price_j:.6e}[/bold]", "100%")

    console.print(table)
    console.print(f"\n[bold]Riemann-Schritte:[/bold] {result.steps:,}")
    console.print(f"[bold]Φ:[/bold] {result.phi:.10f}")

    numerical = deriv.numerical_value()
    console.print(f"[bold]SymPy (geschlossene Form):[/bold] [green]{numerical:.6e}[/green] J")

    if show_proof:
        console.print("\n[bold yellow]SymPy-Beweis: E_price linear in T[/bold yellow]")
        is_linear = deriv.prove_linearity_in_T()
        status = "[green]✔ Bewiesen[/green]" if is_linear else "[red]✘ Fehlgeschlagen[/red]"
        console.print(f"  dE/dT = E/T (linear in T): {status}")
        latex = deriv.latex_expression()
        console.print(f"\n[bold]LaTeX:[/bold] [dim]{latex}[/dim]")


# ---------------------------------------------------------------------------
# tesseract-render (v0.2.0)
# ---------------------------------------------------------------------------


@app.command(name="tesseract-render")
def tesseract_render(
    n_max: Annotated[int, typer.Option("--n-max", "-n", help="Maximale Rekursionsstufe")] = 7,
    temperature: Annotated[
        float, typer.Option("--temperature", "-T", help="Temperatur in Kelvin")
    ] = 2.725,
    save: Annotated[
        str | None, typer.Option("--save", help="Speichere als Datei (z.B. 'png', 'pdf' oder Pfad)")
    ] = None,
    ascii_only: Annotated[
        bool, typer.Option("--ascii", help="Nur ASCII-Vorschau, kein matplotlib")
    ] = False,
) -> None:
    """[bold]Tesseract-Render[/bold] – Matplotlib-Visualisierung + CREP-Heatmap.

    Visualisiert Zeitscheiben T_n = t_0 · Φ^n, CREP-Werte und Phi-Skalierung
    als 3-Panel-Figure (CREP-Heatmap, Balken, Log-Phi-Skalierung).

    Examples:

      ig tesseract-render

      ig tesseract-render --save png

      ig tesseract-render --save tesseract_output.pdf --n-max 10

      ig tesseract-render --ascii
    """
    from .simulation.tesseract_render import TesseractRenderer

    renderer = TesseractRenderer(n_max=n_max, temperature=temperature)

    console.print(
        Panel(
            f"[bold cyan]Tesseract-Visualisierung[/bold cyan]  "
            f"(n_max={n_max}, T={temperature} K, Φ={PHI:.6f})",
            expand=False,
        )
    )

    # ASCII-Vorschau (immer)
    console.print(renderer.ascii_preview())

    if ascii_only:
        return

    # Datei speichern
    if save is not None:
        # Wenn save ein einfaches Format ist (z.B. "png"), Standardname verwenden
        out_path = f"tesseract_n{n_max}.{save}" if save in {"png", "pdf", "svg", "jpg"} else save

        try:
            saved = renderer.save(out_path)
            console.print(f"\n[bold green]Gespeichert:[/bold green] [cyan]{saved}[/cyan]")
        except Exception as e:
            err_console.print(f"[red]Fehler beim Speichern: {e}[/red]")
            raise typer.Exit(code=1) from e
    else:
        # Nur render, nicht speichern
        try:
            import matplotlib.pyplot as plt

            fig = renderer.render()
            console.print(
                "\n[dim]Tipp: Verwende [bold]--save png[/bold] "
                "um die Visualisierung zu speichern.[/dim]"
            )
            plt.close(fig)
        except Exception as e:
            err_console.print(f"[red]Render-Fehler: {e}[/red]")
            raise typer.Exit(code=1) from e


# ---------------------------------------------------------------------------
# cmb-test (v0.2.0)
# ---------------------------------------------------------------------------


@app.command(name="cmb-test")
def cmb_test(
    n_sim: Annotated[
        int, typer.Option("--n-sim", "-n", help="Anzahl Monte-Carlo-Simulationen")
    ] = 5000,
    v_rig: Annotated[
        float, typer.Option("--v-rig", help="V_RIG in km/s (Standard: 1352.0)")
    ] = V_RIG_KMS,
    v_cmb: Annotated[
        float, typer.Option("--v-cmb", help="CMB-Dipolwert in km/s (Planck 2018: 369.82)")
    ] = 369.82,
    alpha: Annotated[
        float, typer.Option("--alpha", help="Signifikanzniveau (Standard: 0.05)")
    ] = 0.05,
    seed: Annotated[int | None, typer.Option("--seed", help="Zufalls-Seed")] = None,
) -> None:
    """[bold]CMB-Falsifikationstest[/bold] – Monte-Carlo gegen realen CMB-Dipol.

    Testet ob V_RIG = 1352 km/s mit dem CMB-Dipol v_CMB = 369.82 km/s
    vereinbar ist. Unter der Modellhypothese v_obs = V_RIG · U(0,1) + N(0,σ²).

    H₀: Modell ist mit CMB-Dipol konsistent
    H₁: p < α → Modell falsifiziert

    Examples:

      ig cmb-test

      ig cmb-test --n-sim 5000

      ig cmb-test --n-sim 10000 --seed 42

      ig cmb-test --v-rig 1352 --alpha 0.01
    """
    from .simulation.cmb_falsification import CMBFalsificationTest

    test = CMBFalsificationTest(
        n_sim=n_sim,
        v_rig_kms=v_rig,
        v_cmb_kms=v_cmb,
        alpha=alpha,
        seed=seed,
    )
    result = test.run()

    verdict_color = "red" if result.is_falsified else "green"
    console.print(
        Panel(
            f"[bold cyan]CMB-Falsifikationstest[/bold cyan]  "
            f"(n_sim={n_sim:,}, V_RIG={v_rig:.1f} km/s, v_CMB={v_cmb:.2f} km/s)",
            expand=False,
        )
    )

    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("Parameter", style="bold magenta", no_wrap=True)
    table.add_column("Wert", style="cyan")
    table.add_column("Einheit / Info", style="dim")

    table.add_row("V_RIG (Modell)", f"{result.v_rig_kms:.2f}", "km/s")
    table.add_row("v_CMB (Planck 2018)", f"{result.v_cmb_kms:.2f}", "km/s")
    table.add_row("E[v] unter Modell", f"{result.expected_v_kms:.2f}", "km/s (V_RIG/2)")
    table.add_row("μ_MC (Mittelwert)", f"{result.mean_sim_kms:.2f}", "km/s")
    table.add_row("σ_MC", f"{result.std_sim_kms:.2f}", "km/s")
    table.add_row(
        "|μ - v_CMB|",
        f"{result.deviation_kms:.2f}",
        f"km/s ({result.deviation_sigma:.2f}σ)",
    )
    table.add_row("n_konsistent", f"{result.n_consistent:,}", f"von {result.n_sim:,}")
    table.add_row("Toleranz", f"{result.tolerance_kms:.2f}", "km/s (3σ + 1 km/s)")
    table.add_row(
        "[bold]p-Wert[/bold]",
        f"[bold]{result.p_value:.6f}[/bold]",
        f"α = {result.alpha}",
    )

    console.print(table)
    console.print(f"\n[bold {verdict_color}]Urteil: {result.verdict}[/bold {verdict_color}]")


# ---------------------------------------------------------------------------
# phi-proof (v0.2.0)
# ---------------------------------------------------------------------------


@app.command(name="phi-proof")
def phi_proof(
    beta_0: Annotated[float, typer.Option("--beta0", help="Basis-Kopplungskonstante β₀")] = 1.0,
    n_max: Annotated[int, typer.Option("--n-max", "-n", help="β_n-Reihe bis n_max")] = 7,
) -> None:
    """[bold]Phi-Beweis[/bold] – SymPy-Formalisierung von β_n = β_0 · Φ^{n/3}.

    Beweist symbolisch:
      - β_{n+3} = Φ · β_n (Rekursionsrelation)
      - β_{n+1}/β_n = Φ^{1/3} (konstantes Verhältnis)
      - Φ² = Φ + 1 (Goldene-Schnitt-Identität)
      - λ = ln(Φ)/3 (Lyapunov-Exponent)

    Examples:

      ig phi-proof

      ig phi-proof --beta0 0.5 --n-max 10
    """
    from .formalization.phi_scaling import PhiScalingProof, stability_analysis

    console.print(
        Panel(
            f"[bold cyan]Phi-Skalierungs-Beweis (SymPy)[/bold cyan]  "
            f"(β₀={beta_0}, n_max={n_max}, Φ={PHI:.10f})",
            expand=False,
        )
    )

    sa = stability_analysis(beta_0=beta_0)
    proof = PhiScalingProof(beta_0_val=beta_0)

    # Beweise
    proof_table = Table(title="SymPy-Beweise", show_header=True, box=None, padding=(0, 2))
    proof_table.add_column("Theorem", style="bold magenta")
    proof_table.add_column("Status", style="cyan")

    proofs_map = {
        "β_{n+3} = Φ · β_n": sa.recursion_proved,
        "β_{n+1}/β_n = Φ^{1/3}": sa.ratio_proved,
        "Φ² = Φ + 1 (Goldene-Schnitt-ID)": sa.golden_id_proved,
    }
    for theorem, ok in proofs_map.items():
        icon = "[green]✔ Bewiesen[/green]" if ok else "[red]✘ Fehlgeschlagen[/red]"
        proof_table.add_row(theorem, icon)

    console.print(proof_table)

    # β_n-Reihe
    console.print("\n[bold]β_n-Reihe:[/bold]")
    beta_table = Table(show_header=True, box=None, padding=(0, 2))
    beta_table.add_column("n", style="bold magenta")
    beta_table.add_column("β_n = β₀·Φ^{n/3}", style="cyan")
    beta_table.add_column("Φ^{n/3}", style="dim")

    for n, beta in proof.numerical_beta_series(n_max):
        phi_n3 = PHI ** (n / 3.0)
        beta_table.add_row(str(n), f"{beta:.8f}", f"{phi_n3:.8f}")

    console.print(beta_table)
    console.print(
        f"\n[bold]Lyapunov-Exponent:[/bold] λ = [cyan]{sa.lyapunov_exponent:.10f}[/cyan]  "
        f"({'exponentiell' if sa.is_exponential else 'stabil'})\n"
        f"[bold]β_n (LaTeX):[/bold] [dim]{sa.beta_n_latex}[/dim]"
    )


# ---------------------------------------------------------------------------
# oipk-calc (v0.3.0)
# ---------------------------------------------------------------------------


@app.command(name="oipk-calc")
def oipk_calc(
    lambda_nm: Annotated[
        float | None,
        typer.Option("--lambda", "-l", help="OIPK-Wellenlänge λ in Nanometern (Standard: c/V_RIG)"),
    ] = None,
    n_max: Annotated[
        int, typer.Option("--n-max", "-n", help="Dimension-Reihe bis Stufe n_max")
    ] = 7,
    show_tau: Annotated[bool, typer.Option("--tau", help="τ ⊥ t Prozesszeiten anzeigen")] = False,
) -> None:
    """[bold]OIPK-Kalkulator[/bold] – Orthogonal Impulse Photon Kernel.

    Berechnet alle Kerngrößen des OIPK: τ ⊥ t, ω, E_OIPK, S_F, CREP
    sowie die emergenten Dimensionen D_n für n = 0..n_max.

    Leitprinzip: [italic]„A dimension emerges when information would otherwise collapse."[/italic]

    Examples:

      ig oipk-calc

      ig oipk-calc --lambda 500 --n-max 10

      ig oipk-calc --tau
    """
    from .oipk.kernel import OIPKKernel, compute_crep_oipk

    kernel = OIPKKernel(lambda_m=lambda_nm * 1e-9) if lambda_nm is not None else OIPKKernel()

    result = kernel.compute()

    console.print(
        Panel(
            f"[bold cyan]OIPK-Kalkulator[/bold cyan]  "
            f"λ = [yellow]{result.lambda_m:.4e}[/yellow] m  |  "
            f"α_Φ = [yellow]{result.alpha_phi:.6f}[/yellow]",
            expand=False,
        )
    )
    axiom = "A dimension emerges when information would otherwise collapse."
    doc0 = OIPKKernel.__doc__.splitlines()[0] if OIPKKernel.__doc__ else ""
    console.print(
        f"\n[dim italic]{doc0}[/dim italic]\n[bold]Leitprinzip:[/bold] [italic]{axiom}[/italic]\n"
    )

    # Kerngrößen-Tabelle
    core_table = Table(title="Kerngrößen", show_header=True, box=None, padding=(0, 2))
    core_table.add_column("Größe", style="bold magenta")
    core_table.add_column("Wert", style="cyan")
    core_table.add_column("Einheit", style="dim")

    core_table.add_row("λ_OIPK", f"{result.lambda_m:.6e}", "m")
    if show_tau:
        core_table.add_row("τ_OIPK", f"{result.tau_oipk:.6e}", "s")
        core_table.add_row("τ_⊥ (τ ⊥ t)", f"{result.tau_perp:.6e}", "s")
    core_table.add_row("ω", f"{result.omega:.6e}", "rad/s")
    core_table.add_row("E_OIPK", f"{result.energy_j:.6e}", "J")
    core_table.add_row("S_F", f"{result.frame_stability:.4f}", "–")
    crep_val = compute_crep_oipk(kernel)
    core_table.add_row("CREP", f"{crep_val:.6e}", "kg·m/s")
    core_table.add_row("τ ⊥ t", str(result.is_orthogonal), "–")

    console.print(core_table)

    # Dimension-Reihe
    dims = kernel.dimension_series(n_max)
    dim_table = Table(
        title=f"Emergente Dimensionen (n = 0..{n_max})", show_header=True, box=None, padding=(0, 2)
    )
    dim_table.add_column("n", style="bold magenta")
    dim_table.add_column("I_n [J]", style="cyan")
    dim_table.add_column("D_n", style="yellow")
    dim_table.add_column("Status", style="dim")

    for d in dims:
        status = "[red]KOLLAPS[/red]" if d.collapsed else "[green]emergent[/green]"
        dim_table.add_row(str(d.n), f"{d.impulse_j:.4e}", str(d.dimension), status)

    console.print(dim_table)


# ---------------------------------------------------------------------------
# anesthesia-test (v0.3.0)
# ---------------------------------------------------------------------------


@app.command(name="anesthesia-test")
def anesthesia_test(
    duration: Annotated[
        float, typer.Option("--duration", "-d", help="Testdauer in Sekunden")
    ] = 300.0,
    tau_m: Annotated[float, typer.Option("--tau-m", help="Medium-Zeitkonstante τ_M [s]")] = 120.0,
    dt: Annotated[float, typer.Option("--dt", help="Zeitschritt [s]")] = 1.0,
    show_timeline: Annotated[
        bool, typer.Option("--timeline", help="Zeitreihe des Frame-Buffers ausgeben")
    ] = False,
) -> None:
    """[bold]Anesthesia-Test[/bold] – Frame-Buffer-Simulation bei Bewusstseinsverlust.

    Simuliert den schrittweisen Kollaps des Frame-Buffers während eines
    Anesthesia-Ereignisses. Zeigt Kohärenzverlust, Wiederherstellungsrate
    und erkannte Anesthesia-Phasen.

    Examples:

      ig anesthesia-test

      ig anesthesia-test --duration 600 --tau-m 90

      ig anesthesia-test --duration 300 --timeline
    """
    from .medium.modulation import run_anesthesia_test

    console.print(
        Panel(
            f"[bold cyan]Anesthesia-Test[/bold cyan]  "
            f"Dauer=[yellow]{duration:.0f}s[/yellow]  "
            f"τ_M=[yellow]{tau_m:.0f}s[/yellow]  "
            f"dt=[yellow]{dt:.1f}s[/yellow]",
            expand=False,
        )
    )

    result = run_anesthesia_test(duration=duration, tau_m=tau_m, dt=dt)

    # Zusammenfassung
    summary_table = Table(title="Testergebnis", show_header=False, box=None, padding=(0, 2))
    summary_table.add_column("Feld", style="bold magenta")
    summary_table.add_column("Wert", style="cyan")

    summary_table.add_row("Dauer", f"{result.duration:.1f} s")
    summary_table.add_row("τ_M", f"{result.tau_m:.1f} s")
    summary_table.add_row("Anesthesia-Ereignisse", str(result.n_events()))
    summary_table.add_row("Anesthesia-Zeit", f"{result.total_anesthesia_time():.1f} s")
    summary_table.add_row(
        "Bewusst-Anteil",
        f"{result.consciousness_fraction():.4f}  ({100 * result.consciousness_fraction():.1f}%)",
    )
    summary_table.add_row("R_loss (Kohärenzverlust)", f"{result.loss_rate:.4f}")
    summary_table.add_row("R_rec (Wiederherstellung)", f"{result.recovery_rate:.4f}")

    console.print(summary_table)

    if result.events:
        ev_table = Table(title="Anesthesia-Ereignisse", show_header=True, box=None, padding=(0, 2))
        ev_table.add_column("#", style="bold magenta")
        ev_table.add_column("t_start [s]", style="cyan")
        ev_table.add_column("t_end [s]", style="cyan")
        ev_table.add_column("Dauer [s]", style="yellow")
        ev_table.add_column("Tiefe", style="dim")
        ev_table.add_column("R_rec", style="green")
        for i, ev in enumerate(result.events, 1):
            t_end_str = f"{ev.t_end:.1f}" if ev.t_end is not None else "–"
            dur_str = f"{ev.duration:.1f}" if ev.duration is not None else "–"
            ev_table.add_row(
                str(i),
                f"{ev.t_start:.1f}",
                t_end_str,
                dur_str,
                f"{ev.depth:.4f}",
                f"{ev.recovery:.4f}",
            )
        console.print(ev_table)
    else:
        console.print("\n[green]Keine Anesthesia-Ereignisse erkannt.[/green]")

    if show_timeline:
        tl_table = Table(
            title="Frame-Buffer Zeitreihe (Auszug)", show_header=True, box=None, padding=(0, 2)
        )
        tl_table.add_column("t [s]", style="bold magenta")
        tl_table.add_column("Φ_buf", style="cyan")
        tl_table.add_column("Status", style="dim")
        from .medium.modulation import ANESTHESIA_THRESHOLD

        step = max(1, len(result.times) // 20)
        for i in range(0, len(result.times), step):
            t_val = result.times[i]
            m_val = result.frame_means[i]
            status = "[green]●[/green]" if m_val > ANESTHESIA_THRESHOLD else "[red]◌[/red]"
            tl_table.add_row(f"{t_val:.1f}", f"{m_val:.5f}", status)
        console.print(tl_table)


# ---------------------------------------------------------------------------
# medium-modulate (v0.3.0)
# ---------------------------------------------------------------------------


@app.command(name="medium-modulate")
def medium_modulate(
    t_max: Annotated[float, typer.Option("--t-max", "-t", help="Endzeit [s]")] = 240.0,
    tau_m: Annotated[float, typer.Option("--tau-m", help="Medium-Zeitkonstante τ_M [s]")] = 120.0,
    m0: Annotated[float, typer.Option("--m0", help="Initial-Amplitude M_0 (normiert)")] = 1.0,
    n_steps: Annotated[int, typer.Option("--steps", "-n", help="Anzahl Zeitschritte")] = 12,
) -> None:
    """[bold]Medium-Modulation[/bold] – Feld-Medium-Wechselwirkung.

    Berechnet die Medium-Amplitude M(t) = M_0·exp(−t/τ_M) und
    Modulationstiefe ΔM(t) für einen linearen Zeitbereich.

    Examples:

      ig medium-modulate

      ig medium-modulate --t-max 600 --tau-m 180 --steps 20
    """
    from .medium.modulation import MediumModulator

    mod = MediumModulator(m0=m0, tau_m=tau_m)

    console.print(
        Panel(
            f"[bold cyan]Medium-Modulation[/bold cyan]  "
            f"M₀=[yellow]{m0:.2f}[/yellow]  "
            f"τ_M=[yellow]{tau_m:.0f}s[/yellow]  "
            f"t_max=[yellow]{t_max:.0f}s[/yellow]",
            expand=False,
        )
    )

    states = mod.modulation_series(t_max=t_max, n_steps=n_steps)

    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("t [s]", style="bold magenta")
    table.add_column("M(t)", style="cyan")
    table.add_column("ΔM(t)", style="yellow")
    table.add_column("norm", style="dim")
    table.add_column("Status", style="dim")
    from .medium.modulation import ANESTHESIA_THRESHOLD

    for s in states:
        status = "[green]CONSCIOUS[/green]" if s.conscious else "[red]ANESTHESIA[/red]"
        table.add_row(
            f"{s.t:.1f}",
            f"{s.m_t:.5f}",
            f"{s.delta_m:.5f}",
            f"{s.normalized:.5f}",
            status,
        )

    console.print(table)
    console.print(
        f"\n[dim]Anesthesia-Schwellwert Θ = [cyan]{ANESTHESIA_THRESHOLD:.6f}[/cyan][/dim]\n"
        f"[dim]R_loss(T={t_max:.0f}s) = [cyan]{mod.frame_loss(t_max):.4f}[/cyan]  "
        f"R_rec = [cyan]{mod.recovery_rate(t_max):.4f}[/cyan][/dim]"
    )


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
