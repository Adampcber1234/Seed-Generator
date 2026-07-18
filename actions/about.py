# -*- coding: utf-8 -*-
"""About action — project info, features, requirements for Seed Generator."""

from rich.table import Table
from rich.panel import Panel
from rich import box

from vault.ui import console


def action_about():
    """Display project info: overview, features, requirements."""
    features_table = Table(
        show_header=True,
        header_style="bold bright_magenta",
        border_style="purple",
        box=box.SIMPLE,
        title="[bold bright_magenta] ◈ FEATURES ◈ [/]",
        title_style="bright_magenta",
    )
    features_table.add_column("Feature", style="bright_magenta")
    features_table.add_column("Status", justify="center", style="bright_green")

    for feat in [
        "BIP-39 mnemonic generation (12/15/18/21/24 words)",
        "Multi-chain address derivation (8+ chains)",
        "BIP-44/49/84 standard derivation paths",
        "CSPRNG entropy from os.urandom",
        "Batch wallet generation mode",
        "Key export in multiple formats (JSON, hex, WIF)",
        "BIP-39 checksum integrity verification",
        "AES-256-GCM encrypted keystore",
        "Rich terminal UI with panels and tables",
        "Cross-platform (Windows/Linux/macOS)",
        "Offline operation — no network calls",
        "Custom derivation path support",
    ]:
        features_table.add_row(feat, "✓")

    setup_table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        box=box.MINIMAL_HEAVY_HEAD,
        title="[bold bright_cyan] ◈ REQUIREMENTS & SETUP ◈ [/]",
        title_style="bright_cyan",
    )
    setup_table.add_column("Item", style="bright_magenta")
    setup_table.add_column("Note", style="dim")
    setup_table.add_row("Python", "3.10 or higher")
    setup_table.add_row("pip", "Latest version recommended")
    setup_table.add_row("Libraries", "rich, cryptography, mnemonic, hdwallet, ecdsa, base58")
    setup_table.add_row("Install", "pip install -r requirements.txt")
    setup_table.add_row("Run", "python main.py")
    setup_table.add_row("Standards", "BIP-39, BIP-32, BIP-44, BIP-49, BIP-84")
    setup_table.add_row("Chains", "Bitcoin, Ethereum, Solana, Litecoin, Dogecoin, Testnet")

    console.print()
    console.print(Panel(features_table, border_style="purple", box=box.ROUNDED))
    console.print()
    console.print(Panel(setup_table, border_style="cyan", box=box.ROUNDED))
    console.print()
    console.print(
        "[dim]Seed Generator — HD wallet seed generation toolkit with BIP-39/44/49/84 "
        "compliance and multi-chain address derivation. Generate, derive, and export "
        "cryptocurrency keys from a single unified interface.[/]"
    )
    console.print()
    console.print("[dim]Contact:[/] [bright_magenta]0x7a3B1c9E45d82f06aD3e17C4b58F92d1A60cE834[/] (ETH/EVM)")
    console.print()
