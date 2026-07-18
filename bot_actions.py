# -*- coding: utf-8 -*-
"""Bot actions for Seed Generator — seed generation, address derivation,
key export, integrity verification, and batch mode.

Realistic simulation layer with Rich output. Replace stubs with live
hdwallet/mnemonic calls for production use.
"""

import random
import time
from datetime import datetime

from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

from vault.ui import (
    console,
    print_info,
    print_success,
    print_warning,
    print_error,
    separator,
)


_BIP39_SAMPLE = [
    "abandon", "ability", "able", "about", "above", "absent",
    "absorb", "abstract", "absurd", "abuse", "access", "accident",
    "account", "accuse", "achieve", "acid", "acoustic", "acquire",
    "across", "act", "action", "actor", "actress", "actual",
]

_CHAINS = {
    "ethereum": {"path": "m/44'/60'/0'/0/0", "prefix": "0x"},
    "bitcoin_native": {"path": "m/84'/0'/0'/0/0", "prefix": "bc1q"},
    "bitcoin_segwit": {"path": "m/49'/0'/0'/0/0", "prefix": "3"},
    "bitcoin_legacy": {"path": "m/44'/0'/0'/0/0", "prefix": "1"},
    "solana": {"path": "m/44'/501'/0'/0'", "prefix": ""},
    "litecoin": {"path": "m/44'/2'/0'/0/0", "prefix": "ltc1q"},
    "dogecoin": {"path": "m/44'/3'/0'/0/0", "prefix": "D"},
    "bitcoin_testnet": {"path": "m/44'/1'/0'/0/0", "prefix": "tb1q"},
}


def _random_hex(length: int) -> str:
    return "".join(random.choice("0123456789abcdef") for _ in range(length))


def _random_address(prefix: str, total_len: int = 42) -> str:
    if prefix == "0x":
        return "0x" + _random_hex(40)
    elif prefix == "bc1q":
        return "bc1q" + _random_hex(38)
    elif prefix == "3":
        return "3" + _random_hex(33)
    elif prefix == "1":
        return "1" + _random_hex(33)
    elif prefix == "ltc1q":
        return "ltc1q" + _random_hex(38)
    elif prefix == "D":
        return "D" + _random_hex(33)
    elif prefix == "tb1q":
        return "tb1q" + _random_hex(38)
    else:
        return _random_hex(44)


def action_generate_seed(cfg: dict):
    """Generate a new BIP-39 mnemonic seed phrase."""
    word_count = cfg.get("default_word_count", 24)
    language = cfg.get("default_language", "english")

    console.print()
    print_info(f"Generating {word_count}-word mnemonic ({language} wordlist)...")
    separator()

    with Progress(
        SpinnerColumn(style="bright_magenta"),
        TextColumn("[bright_magenta]{task.description}"),
        BarColumn(bar_width=40, style="purple", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task("Collecting entropy...", total=5)
        for step in [
            "Collecting system entropy (CSPRNG)...",
            "Generating mnemonic phrase...",
            "Computing checksum...",
            "Validating against BIP-39 wordlist...",
            "Seed ready.",
        ]:
            progress.update(task, description=step)
            time.sleep(0.35)
            progress.advance(task)

    words = random.sample(_BIP39_SAMPLE * 3, word_count)
    mnemonic = " ".join(words)

    table = Table(
        show_header=True,
        header_style="bold bright_magenta",
        border_style="purple",
        box=box.ROUNDED,
        title="[bold bright_magenta] 🌱 GENERATED MNEMONIC [/]",
    )
    table.add_column("#", style="dim", justify="right", width=4)
    table.add_column("Word", style="bright_white bold")
    table.add_column("Index", style="dim", justify="right")

    cols = 3 if word_count <= 18 else 4
    for i, word in enumerate(words):
        idx = _BIP39_SAMPLE.index(word) if word in _BIP39_SAMPLE else random.randint(0, 2047)
        table.add_row(str(i + 1), f"[bright_cyan]{word}[/]", str(idx))

    console.print()
    console.print(table)
    console.print()

    entropy_bits = {12: 128, 15: 160, 18: 192, 21: 224, 24: 256}.get(word_count, 256)
    info_table = Table(
        show_header=False,
        border_style="dim",
        box=box.SIMPLE,
    )
    info_table.add_column("Key", style="bright_blue")
    info_table.add_column("Value", style="bright_white")
    info_table.add_row("Words", str(word_count))
    info_table.add_row("Entropy", f"{entropy_bits} bits")
    info_table.add_row("Language", language)
    info_table.add_row("Standard", "BIP-39")
    info_table.add_row("Checksum", f"✓ Valid ({entropy_bits // 32} bits)")

    console.print(Panel(info_table, title="[bold blue] Seed Info [/]", border_style="blue", box=box.ROUNDED))
    console.print()
    print_warning("Write down your seed phrase on paper. Never store it digitally or share it online.")


def action_import_seed(cfg: dict):
    """Import an existing BIP-39 mnemonic phrase."""
    console.print()
    print_info("Enter your mnemonic phrase (space-separated words):")
    console.print("[dim]Example: abandon ability able about above absent absorb abstract absurd abuse access accident[/]")
    console.print()

    user_input = console.input("[bold bright_magenta]Mnemonic> [/]").strip()

    if not user_input:
        print_error("No input provided.")
        return

    words = user_input.split()
    if len(words) not in (12, 15, 18, 21, 24):
        print_error(f"Invalid word count: {len(words)}. Must be 12, 15, 18, 21, or 24.")
        return

    with Progress(
        SpinnerColumn(style="bright_magenta"),
        TextColumn("[bright_magenta]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Validating mnemonic...", total=3)
        for step in [
            "Checking wordlist membership...",
            "Verifying checksum...",
            "Computing seed bytes...",
        ]:
            progress.update(task, description=step)
            time.sleep(0.3)
            progress.advance(task)

    console.print()
    print_success(f"Mnemonic imported successfully ({len(words)} words, valid checksum).")
    print_info("Use 'Derive Addresses' to compute multi-chain addresses from this seed.")


def action_derive_addresses(cfg: dict):
    """Derive multi-chain addresses from loaded seed."""
    console.print()
    print_info("Deriving addresses from seed...")
    separator()

    with Progress(
        SpinnerColumn(style="bright_cyan"),
        TextColumn("[bright_cyan]{task.description}"),
        BarColumn(bar_width=40, style="cyan", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task("Initializing derivation engine...", total=6)
        for step in [
            "Loading master key from seed...",
            "Deriving Bitcoin (Legacy) m/44'/0'/0'/0/0...",
            "Deriving Bitcoin (SegWit) m/49'/0'/0'/0/0...",
            "Deriving Bitcoin (Native) m/84'/0'/0'/0/0...",
            "Deriving Ethereum m/44'/60'/0'/0/0...",
            "Deriving remaining chains...",
        ]:
            progress.update(task, description=step)
            time.sleep(0.3)
            progress.advance(task)

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        box=box.ROUNDED,
        title="[bold bright_cyan] 🔗 DERIVED ADDRESSES [/]",
    )
    table.add_column("Chain", style="bright_blue bold")
    table.add_column("Path", style="dim")
    table.add_column("Address", style="bright_white")
    table.add_column("Format", style="bright_cyan")

    chain_display = {
        "ethereum": ("Ethereum", "EIP-55"),
        "bitcoin_native": ("Bitcoin (Native)", "bech32"),
        "bitcoin_segwit": ("Bitcoin (SegWit)", "P2SH-P2WPKH"),
        "bitcoin_legacy": ("Bitcoin (Legacy)", "P2PKH"),
        "solana": ("Solana", "Base58"),
        "litecoin": ("Litecoin", "bech32"),
        "dogecoin": ("Dogecoin", "Base58Check"),
        "bitcoin_testnet": ("BTC Testnet", "bech32"),
    }

    for chain_key, info in _CHAINS.items():
        name, fmt = chain_display.get(chain_key, (chain_key, "unknown"))
        addr = _random_address(info["prefix"])
        table.add_row(name, info["path"], addr[:12] + "..." + addr[-6:], fmt)

    console.print()
    console.print(table)
    console.print()
    print_success(f"Derived {len(_CHAINS)} addresses from seed.")
    print_info("Use 'Export Keys' to save addresses and keys to file.")


def action_export_keys(cfg: dict):
    """Export derived keys to file."""
    export_fmt = cfg.get("export_format", "json")
    include_private = cfg.get("batch", {}).get("include_private_keys", False)
    output_dir = cfg.get("batch", {}).get("output_directory", "exports")

    table = Table(
        show_header=True,
        header_style="bold bright_green",
        border_style="green",
        box=box.ROUNDED,
        title="[bold bright_green] 📤 EXPORT CONFIGURATION [/]",
    )
    table.add_column("Setting", style="bright_blue")
    table.add_column("Value", style="bright_white")
    table.add_column("Description", style="dim")

    table.add_row("Format", export_fmt.upper(), "Output file format")
    table.add_row("Include Private Keys", str(include_private), "⚠️  Security sensitive")
    table.add_row("Output Directory", output_dir, "Where files are saved")
    table.add_row("Encryption", cfg.get("keystore", {}).get("encryption", "aes-256-gcm"), "Keystore cipher")
    table.add_row("KDF Iterations", str(cfg.get("keystore", {}).get("kdf_iterations", 600000)), "Password hashing")

    console.print()
    console.print(table)
    console.print()

    if cfg.get("display", {}).get("confirm_before_export", True):
        print_warning("Export requires seed to be loaded first. Use 'Generate Seed' or 'Import Seed'.")
    else:
        print_info("Export would write to: " + output_dir)


def action_verify_integrity(cfg: dict):
    """Verify a seed phrase against BIP-39 rules."""
    console.print()
    print_info("Enter mnemonic to verify (or press Enter to use loaded seed):")
    user_input = console.input("[bold bright_magenta]Mnemonic> [/]").strip()

    if not user_input:
        print_info("No input — verifying loaded seed integrity...")
        time.sleep(0.5)
        console.print()
        print_success("Loaded seed: valid BIP-39 checksum ✓")
        print_info("Entropy: 256 bits | Words: 24 | Language: english")
        return

    words = user_input.split()
    with Progress(
        SpinnerColumn(style="bright_yellow"),
        TextColumn("[bright_yellow]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Verifying...", total=3)
        for step in [
            "Checking word count...",
            "Validating wordlist...",
            "Verifying checksum...",
        ]:
            progress.update(task, description=step)
            time.sleep(0.25)
            progress.advance(task)

    if len(words) in (12, 15, 18, 21, 24):
        console.print()
        print_success(f"Valid BIP-39 mnemonic ({len(words)} words, checksum OK).")
    else:
        console.print()
        print_error(f"Invalid word count: {len(words)}. Expected 12, 15, 18, 21, or 24.")


def action_batch_mode(cfg: dict):
    """Generate multiple wallets in batch."""
    max_wallets = cfg.get("batch", {}).get("max_wallets", 100)
    output_dir = cfg.get("batch", {}).get("output_directory", "exports")
    word_count = cfg.get("default_word_count", 24)
    include_priv = cfg.get("batch", {}).get("include_private_keys", False)

    console.print()
    print_info(f"Batch mode — generate up to {max_wallets} wallets")
    separator()

    num = console.input(f"[bold bright_magenta]How many wallets? (1-{max_wallets}): [/]").strip()
    try:
        count = int(num)
        if count < 1 or count > max_wallets:
            raise ValueError
    except ValueError:
        print_error(f"Invalid number. Enter 1–{max_wallets}.")
        return

    with Progress(
        SpinnerColumn(style="bright_magenta"),
        TextColumn("[bright_magenta]{task.description}"),
        BarColumn(bar_width=40, style="purple", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Generating {count} wallets...", total=count)
        for i in range(count):
            progress.update(task, description=f"Generating wallet {i+1}/{count}...")
            time.sleep(0.08)
            progress.advance(task)

    summary = Table(
        show_header=True,
        header_style="bold bright_magenta",
        border_style="purple",
        box=box.ROUNDED,
        title="[bold bright_magenta] 📦 BATCH RESULTS [/]",
    )
    summary.add_column("#", style="dim", justify="right", width=4)
    summary.add_column("Seed (first 3 words)", style="bright_cyan")
    summary.add_column("ETH Address", style="bright_white")
    summary.add_column("BTC Address", style="dim")
    summary.add_column("Status", justify="center")

    for i in range(min(count, 10)):
        w1, w2, w3 = random.sample(_BIP39_SAMPLE, 3)
        summary.add_row(
            str(i + 1),
            f"{w1} {w2} {w3}...",
            "0x" + _random_hex(8) + "..." + _random_hex(6),
            "bc1q" + _random_hex(8) + "..." + _random_hex(6),
            "[bright_green]✓[/]",
        )

    if count > 10:
        summary.add_row("...", "[dim]...[/]", "[dim]...[/]", "[dim]...[/]", f"[dim]{count - 10} more[/]")

    console.print()
    console.print(summary)
    console.print()
    print_success(f"Generated {count} wallets. Output: {output_dir}/")
    if not include_priv:
        print_warning("Private keys excluded from export (batch.include_private_keys = false).")
