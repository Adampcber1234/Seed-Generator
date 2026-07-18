# -*- coding: utf-8 -*-
"""Settings action — configuration viewer for Seed Generator."""

from pathlib import Path

from rich.table import Table
from rich.panel import Panel
from rich import box

from vault.ui import console, print_info, print_warning


def action_settings():
    """Display setup instructions: config.json, keystore settings."""
    table = Table(
        show_header=True,
        header_style="bold bright_magenta",
        border_style="purple",
        box=box.ROUNDED,
        title="[bold bright_magenta] ◈ CONFIGURATION ◈ [/]",
        title_style="bright_magenta",
    )
    table.add_column("Setting", style="bright_magenta")
    table.add_column("Description", style="dim")
    table.add_column("Default", style="bright_black")

    table.add_row("default_word_count", "Mnemonic length (12/15/18/21/24)", "24")
    table.add_row("default_language", "BIP-39 wordlist language", "english")
    table.add_row("default_chain", "Primary chain for derivation", "ethereum")
    table.add_row("derivation_depth", "Max BIP-32 path depth", "5")
    table.add_row("export_format", "Key export file format", "json")
    table.add_row("keystore.encryption", "Keystore cipher algorithm", "aes-256-gcm")
    table.add_row("keystore.kdf_iterations", "PBKDF2 iteration count", "600000")
    table.add_row("batch.max_wallets", "Max wallets in batch mode", "100")
    table.add_row("batch.include_private_keys", "Export private keys in batch", "false")
    table.add_row("display.show_private_keys", "Show private keys in terminal", "false")
    table.add_row("display.confirm_before_export", "Confirm before key export", "true")

    panel = Panel(
        table,
        title="[bold purple] Seed Generator Settings [/]",
        border_style="bright_magenta",
        box=box.DOUBLE,
    )

    console.print()
    console.print(panel)

    base_dir = Path(__file__).parent.parent
    config_path = base_dir / "config.json"

    console.print()
    console.print("[dim]Configuration file:[/]")
    console.print(f"  [bright_magenta]config.json[/] → {config_path}")
    console.print()
    console.print(
        "[bright_magenta]Supported chains:[/]\n"
        "  • [dim]Bitcoin (Legacy / SegWit / Native SegWit)[/]\n"
        "  • [dim]Ethereum (EIP-55 checksummed addresses)[/]\n"
        "  • [dim]Solana (Base58 public keys)[/]\n"
        "  • [dim]Litecoin, Dogecoin, Bitcoin Testnet[/]"
    )
    console.print()
    print_warning("Never share your seed phrases or private keys. Keep config.json and keystores secure.")
    print_info("Edit config.json with any text editor (e.g. VS Code, Notepad).")
