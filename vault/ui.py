# -*- coding: utf-8 -*-
"""Terminal UI for Seed Generator — purple/cyan/magenta theme."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

console = Console(force_terminal=True, color_system="auto")

VERSION = "3.1.0"
TITLE = "Seed Generator"


def print_banner():
    """Print main banner with styled panel."""
    console.print()
    console.print(
        Panel(
            f"[bold white]{TITLE}[/bold white] [dim]v{VERSION}[/dim]\n"
            "[dim]HD Wallet Toolkit — BIP-39 / BIP-44 / BIP-49 / BIP-84[/dim]",
            border_style="bright_magenta",
            box=box.DOUBLE,
            padding=(1, 2),
        )
    )
    console.print()


def show_menu_table(menu_items):
    """Display menu as styled table inside a panel. Returns user choice."""
    table = Table(
        title=f"[bold bright_magenta]{TITLE}[/bold bright_magenta]",
        box=box.DOUBLE_EDGE,
        border_style="bright_magenta",
        title_style="bold white",
        show_header=True,
        header_style="bold bright_white",
        padding=(0, 2),
    )
    table.add_column("#", style="bold bright_cyan", justify="center", width=4)
    table.add_column("Action", style="white", min_width=30)
    table.add_column("Description", style="dim", min_width=30)

    for num, action, desc in menu_items:
        style = "bold red" if num == "0" else "white"
        table.add_row(num, f"[{style}]{action}[/{style}]", desc)

    console.print(table)
    console.print()

    choice = console.input("[bold bright_cyan]  Select option >[/] ").strip()
    return choice


def show_derived_addresses_table(addresses):
    """Display derived addresses in a styled table."""
    table = Table(
        title="[bold bright_magenta]Derived Addresses[/bold bright_magenta]",
        box=box.ROUNDED,
        border_style="bright_magenta",
    )
    table.add_column("Chain", style="bold white", width=18)
    table.add_column("Path", style="dim", width=22)
    table.add_column("Address", style="bright_cyan", width=48)

    for chain, path, addr in addresses:
        table.add_row(chain, path, addr)

    console.print(table)
    console.print()


def show_seed_display(words, entropy_bits):
    """Display generated seed phrase in a styled panel."""
    numbered = "\n".join(
        f"  [bright_cyan]{i+1:2}.[/] [white]{w}[/]"
        for i, w in enumerate(words)
    )
    panel = Panel(
        Text.from_markup(numbered),
        title=f"[bold bright_magenta] Seed Phrase ({len(words)} words / {entropy_bits}-bit) [/]",
        subtitle="[dim]Store securely — never share with anyone[/dim]",
        border_style="bright_magenta",
        box=box.DOUBLE,
        padding=(1, 2),
    )
    console.print(panel)
    console.print()


def show_batch_summary(count, output_dir):
    """Display batch generation summary."""
    table = Table(
        title="[bold bright_magenta]Batch Generation Complete[/bold bright_magenta]",
        box=box.ROUNDED,
        border_style="bright_magenta",
    )
    table.add_column("Metric", style="bright_magenta")
    table.add_column("Value", justify="right", style="bright_cyan")

    table.add_row("Wallets Generated", str(count))
    table.add_row("Output Directory", output_dir)
    table.add_row("Format", "JSON")
    table.add_row("Private Keys", "Excluded")

    console.print(table)
    console.print()


def show_simple_list(title, items):
    """Show bullet list in a styled panel."""
    body = "\n".join(f"[bright_magenta]▸[/] {item}" for item in items)
    panel = Panel(
        Text.from_markup(body),
        title=f"[bold bright_cyan] {title} [/]",
        border_style="bright_magenta",
        box=box.ROUNDED,
    )
    console.print()
    console.print(panel)
    console.print()


def print_success(message):
    console.print(f"  [bold green]✓[/bold green] {message}")


def print_error(message):
    console.print(f"  [bold red]✗[/bold red] {message}")


def print_info(message):
    console.print(f"  [bold bright_magenta]ℹ[/bold bright_magenta] {message}")


def print_warning(message):
    console.print(f"  [bold bright_cyan]⚠[/bold bright_cyan] {message}")


def separator():
    console.print("[dim bright_black]─" * 60 + "[/dim bright_black]")


def progress_bar(description, total=100, transient=False):
    return Progress(
        SpinnerColumn(style="bright_magenta"),
        TextColumn("[bold bright_magenta]{task.description}"),
        BarColumn(bar_width=40, style="purple", complete_style="bright_green", finished_style="bright_green"),
        TextColumn("[bold]{task.percentage:>3.0f}%"),
        console=console,
        transient=transient,
    )
