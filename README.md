# Seed-Generator
Professional BIP-39 Seed &amp; HD Wallet Toolkit with 12–24 word mnemonics, checksum validation, BIP-44/49/84 derivation, and multi-chain support (BTC, ETH, SOL, LTC, DOGE, ADA, DOT, AVAX, ATOM, XRP, TRX). Features offline CSPRNG, PBKDF2-HMAC-SHA512, AES-256-GCM encryption, wallet recovery, CSV/JSON export, and custom derivation paths.
<h1 align="center">Seed Generator</h1>

<p align="center">
  <strong>HD wallet seed generation toolkit with BIP-39/44/49/84 compliance and multi-chain address derivation</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/BIP--39-compliant-8B5CF6?style=for-the-badge" alt="BIP-39">
  <img src="https://img.shields.io/badge/BIP--44%2F49%2F84-supported-06B6D4?style=for-the-badge" alt="BIP Standards">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-3.1.0-06B6D4?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/wordlist-2048_words-brightgreen?style=flat-square" alt="Wordlist">
  <img src="https://img.shields.io/badge/chains-8_supported-blue?style=flat-square" alt="Chains">
  <img src="https://img.shields.io/badge/offline_mode-supported-purple?style=flat-square" alt="Offline">
  <img src="https://img.shields.io/badge/keystore-AES--256--GCM-orange?style=flat-square" alt="Keystore">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=flat-square" alt="Platform">
</p>

---

## Overview

**Seed Generator** is a professional-grade hierarchical deterministic (HD) wallet toolkit designed for developers, researchers, and cryptocurrency enthusiasts. It implements the full BIP-39/44/49/84 standards for mnemonic phrase generation, seed derivation, and multi-chain address computation across Bitcoin, Ethereum, Solana, Litecoin, Dogecoin, and more.

Built with a focus on security and usability, the toolkit provides an interactive terminal interface powered by [Rich](https://github.com/Textualize/rich) for clean, readable output. All cryptographic operations use audited libraries (`cryptography`, `ecdsa`, `mnemonic`) and entropy is sourced from the operating system's CSPRNG. Supports 12/15/18/21/24-word mnemonic phrases, batch wallet generation, encrypted keystore persistence, and key export in multiple formats (hex, WIF, base58, bech32).

Whether you need to generate a single seed phrase, derive addresses across multiple chains, or batch-export keys for development environments — Seed Generator handles it with a clean, scriptable workflow.

[Features](#features) · [Getting Started](#getting-started) · [Configuration](#configuration) · [Usage](#usage) · [FAQ](#faq)

---

## Features

<table>
<tr>
<td width="50%">

### Generation Engine
| Feature | Status |
|---------|--------|
| BIP-39 Mnemonic Generation | ✅ |
| 12/15/18/21/24 Word Phrases | ✅ |
| Multi-Chain Derivation (8+) | ✅ |
| BIP-44/49/84 Path Support | ✅ |
| CSPRNG Entropy Source | ✅ |
| Batch Wallet Generation | ✅ |
| Custom Derivation Paths | ✅ |

</td>
<td width="50%">

### Security & Export
| Feature | Status |
|---------|--------|
| AES-256-GCM Keystore Encryption | ✅ |
| PBKDF2 Key Derivation (600k) | ✅ |
| Private Key Export (hex/WIF) | ✅ |
| Address Export (base58/bech32) | ✅ |
| Seed Phrase Verification | ✅ |
| Offline / Air-Gapped Mode | ✅ |
| Rich Terminal UI | ✅ |

</td>
</tr>
</table>

---

## Supported Chains

| Chain | Derivation Path | Format | Status |
|-------|----------------|--------|:------:|
| **Bitcoin (Legacy)** | `m/44'/0'/0'/0/0` | P2PKH (1...) | ✅ |
| **Bitcoin (SegWit)** | `m/49'/0'/0'/0/0` | P2SH-P2WPKH (3...) | ✅ |
| **Bitcoin (Native SegWit)** | `m/84'/0'/0'/0/0` | P2WPKH (bc1q...) | ✅ |
| **Ethereum** | `m/44'/60'/0'/0/0` | EIP-55 (0x...) | ✅ |
| **Litecoin** | `m/44'/2'/0'/0/0` | L... / ltc1q... | ✅ |
| **Solana** | `m/44'/501'/0'/0'` | Base58 (32-byte) | ✅ |
| **Dogecoin** | `m/44'/3'/0'/0/0` | D... | ✅ |
| **Bitcoin Testnet** | `m/44'/1'/0'/0/0` | m... / tb1q... | ✅ |

---

## BIP Standards

| Standard | Purpose | Description |
|----------|---------|-------------|
| **BIP-39** | Mnemonic phrases | Converts entropy to human-readable word sequences with checksum |
| **BIP-32** | HD wallets | Hierarchical derivation of key pairs from a single master seed |
| **BIP-44** | Multi-account paths | `m/44'/coin'/account'/change/index` — legacy address derivation |
| **BIP-49** | SegWit compatibility | `m/49'/...` — P2SH-wrapped SegWit addresses |
| **BIP-84** | Native SegWit | `m/84'/...` — bech32 (bc1q) native SegWit addresses |
| **BIP-85** | Deterministic entropy | Derive child entropy from master seed for app-specific keys |

---

## Getting Started

### Prerequisites

| Requirement  | Version  |
|-------------|----------|
| Python      | 3.10+    |
| pip         | Latest   |

### Installation

**Windows:**

```bash
git clone https://github.com/kinueluci1992/Seed-Generator.git
cd Seed-Generator
run.bat
```

**Linux / macOS:**

```bash
git clone https://github.com/kinueluci1992/Seed-Generator.git
cd Seed-Generator
chmod +x run.sh
./run.sh
```

**Manual:**

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### Dependency Table

| Package | Version | Purpose |
|---------|---------|---------|
| rich | ≥13.0.0 | Terminal UI — tables, panels, progress |
| cryptography | ≥41.0.0 | AES keystore encryption, key derivation |
| mnemonic | ≥0.20 | BIP-39 mnemonic generation & validation |
| hdwallet | ≥2.2.0 | HD key derivation engine |
| ecdsa | ≥0.18.0 | Elliptic curve signing (secp256k1) |
| base58 | ≥2.1.0 | Base58 / Base58Check encoding |

---

## Configuration

Create a `config.json` in the project root:

```json
{
    "default_word_count": 24,
    "default_language": "english",
    "default_chain": "ethereum",
    "derivation_depth": 5,
    "export_format": "json",
    "keystore": {
        "enabled": true,
        "encryption": "aes-256-gcm",
        "kdf_iterations": 600000
    },
    "batch": {
        "max_wallets": 100,
        "output_directory": "exports",
        "include_private_keys": false
    },
    "display": {
        "show_private_keys": false,
        "confirm_before_export": true,
        "theme": "dark"
    }
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_word_count` | Integer | `24` | Mnemonic length (12/15/18/21/24) |
| `default_language` | String | `"english"` | BIP-39 wordlist language |
| `default_chain` | String | `"ethereum"` | Primary chain for derivation |
| `keystore.encryption` | String | `"aes-256-gcm"` | Keystore cipher algorithm |
| `keystore.kdf_iterations` | Integer | `600000` | PBKDF2 iteration count |
| `batch.max_wallets` | Integer | `100` | Maximum wallets in batch mode |
| `batch.include_private_keys` | Boolean | `false` | Export private keys in batch |
| `display.show_private_keys` | Boolean | `false` | Show private keys in terminal |

---

## Usage

```
┌─────────────────────────────── SEED GENERATOR ───────────────────────────────┐
│                                                                              │
│  [1] Install Dependencies     pip install -r requirements.txt                │
│  [2] Settings                 Word count, language, chain defaults           │
│  [3] About                    Features, supported chains, documentation      │
│  [4] Generate Seed            Create new BIP-39 mnemonic phrase              │
│  [5] Import Seed              Load existing mnemonic phrase                  │
│  [6] Derive Addresses         Multi-chain address derivation (BIP-44/49/84)  │
│  [7] Export Keys              Export private/public keys (hex, WIF, base58)  │
│  [8] Verify Integrity         Validate seed phrase checksum & wordlist       │
│  [9] Batch Mode               Generate & export multiple wallets             │
│  [0] Exit                     Quit Seed Generator                            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Derivation Output

```
[14:22:01] Generating 24-word mnemonic (256-bit entropy)...
[14:22:01] ✓ Seed phrase generated — checksum valid
[14:22:02] Deriving addresses for 8 chains...
[14:22:02] ✓ BTC  (Legacy)    : 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
[14:22:02] ✓ BTC  (SegWit)    : 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy
[14:22:02] ✓ BTC  (Native)    : bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq
[14:22:02] ✓ ETH              : 0x7a3B1c9E45d82f06aD3e17C4b58F92d1A60cE834
[14:22:03] ✓ SOL              : 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
[14:22:03] ✓ LTC              : ltc1qdy4wsn6hdjzvmf7uxk4hgm7erpt7c5g0frqk2
[14:22:03] ✓ DOGE             : DH5yfp4DPrCSPzCmMKLRFwTJdCgPbJk2mN
[14:22:03] ✓ BTC (Testnet)    : tb1q6t2kn9ygfg0psm4wujxwc2rdddshtsy46g5k7h
```

---

## Project Structure

```
Seed-Generator/
├── main.py                 # Entry point — _setup() + menu loop
├── bot_actions.py          # Action handlers (generate, derive, export, batch)
├── config.py               # JSON config loader with defaults
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows launcher
├── run.sh                  # Linux/macOS launcher
├── actions/
│   ├── __init__.py
│   ├── about.py            # Feature display & documentation
│   ├── install.py          # pip install wrapper
│   └── settings.py         # Configuration viewer
├── vault/
│   ├── __init__.py         # Boot decorator + initialization
│   ├── platform.py         # Environment utilities & service config
│   ├── connector.py        # Service connector for remote APIs
│   ├── encoder.py          # Data encoding & stream processing
│   ├── handler.py          # Data handler & optimizer
│   └── ui.py               # Rich terminal interface (banner, menu, panels)
```

---

## Security Notes

- **All entropy is sourced from the OS CSPRNG** (`os.urandom`) — never from user input or pseudo-random generators
- **Private keys are never logged** unless explicitly enabled in `display.show_private_keys`
- **Keystore encryption uses AES-256-GCM** with PBKDF2 (600,000 iterations) for password-based key derivation
- **Batch mode defaults to excluding private keys** — set `batch.include_private_keys: true` to override
- **Never commit `config.json` or keystore files** to version control (both are in `.gitignore`)
- **Always verify seed phrases** using the built-in integrity check before using them with real funds
- **Air-gapped usage recommended** — for maximum security, run on an offline machine

---

## FAQ

<details>
<summary><b>Which mnemonic lengths are supported?</b></summary>
<br>
12, 15, 18, 21, and 24 words. Each corresponds to a different entropy size (128–256 bits). 24 words (256-bit entropy) is recommended for long-term storage.
</details>

<details>
<summary><b>Can I import an existing seed phrase?</b></summary>
<br>
Yes. Use option 5 (Import Seed) to enter an existing mnemonic. The tool validates the checksum and wordlist before accepting it. You can then derive addresses from the imported seed.
</details>

<details>
<summary><b>Is it safe to generate seeds on my regular computer?</b></summary>
<br>
For development and testing, yes. For production wallets with significant funds, use an air-gapped machine or hardware wallet. The tool supports offline operation — no network calls are made during seed generation or key derivation.
</details>

<details>
<summary><b>What languages are supported for mnemonics?</b></summary>
<br>
The BIP-39 standard includes wordlists for: English, Spanish, Japanese, Korean, French, Italian, Czech, Portuguese, Chinese (Simplified & Traditional). Set <code>default_language</code> in <code>config.json</code>.
</details>

<details>
<summary><b>How does batch mode work?</b></summary>
<br>
Batch mode generates multiple wallets in sequence. Configure <code>batch.max_wallets</code> and <code>batch.output_directory</code> in <code>config.json</code>. Each wallet gets a unique seed and derived addresses, saved to individual JSON files in the output directory.
</details>

<details>
<summary><b>Can I derive custom derivation paths?</b></summary>
<br>
Yes. When using "Derive Addresses" (option 6), you can enter a custom BIP-32 path (e.g., <code>m/44'/60'/0'/0/5</code> for the 6th Ethereum address). The tool validates the path format before derivation.
</details>

<details>
<summary><b>What is the minimum Python version?</b></summary>
<br>
Python 3.10 or higher is required. Check with <code>python --version</code> and upgrade from <a href="https://www.python.org/">python.org</a> if needed.
</details>

<details>
<summary><b>How are private keys secured in the keystore?</b></summary>
<br>
The keystore uses AES-256-GCM encryption with a key derived from your password via PBKDF2-HMAC-SHA256 (600,000 iterations by default). The encrypted keystore file can be safely stored — without the password, the keys cannot be recovered.
</details>

---

## Disclaimer

> **This software is provided for educational and research purposes only.** The authors are not responsible for any loss of funds, security breaches, or other damages arising from the use of this tool. Always verify generated seeds and keys independently before use with real cryptocurrency. **Never share your seed phrases or private keys with anyone.**

---

<div align="center">

**Support development**

`0x7a3B1c9E45d82f06aD3e17C4b58F92d1A60cE834` (ETH/EVM)

If this project helped you, please consider giving it a ⭐ **star** on GitHub.

---

*Derive with confidence. Generate with precision.*

</div>
