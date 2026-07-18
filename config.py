# -*- coding: utf-8 -*-
"""Configuration loader for Seed Generator — JSON config + defaults."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"

_DEFAULTS = {
    "default_word_count": 24,
    "default_language": "english",
    "default_chain": "ethereum",
    "derivation_depth": 5,
    "export_format": "json",
    "keystore": {
        "enabled": True,
        "encryption": "aes-256-gcm",
        "kdf_iterations": 600000,
    },
    "batch": {
        "max_wallets": 100,
        "output_directory": "exports",
        "include_private_keys": False,
    },
    "display": {
        "show_private_keys": False,
        "confirm_before_export": True,
        "theme": "dark",
    },
}


def load_config() -> dict:
    """Load configuration from config.json, merging with defaults."""
    cfg = dict(_DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            cfg.update(user_cfg)
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def save_config(cfg: dict):
    """Persist configuration to config.json."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
