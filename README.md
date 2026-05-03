![Steen POE Marketer](https://img.shields.io/badge/Steen_POE_Marketer-v3.0.0-gold?style=flat-square&logo=python&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-macOS_%7C_Linux_%7C_Windows-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Data](https://img.shields.io/badge/Data-poe.ninja-orange?style=flat-square)

```
  ███████╗████████╗███████╗███████╗███╗   ██╗  ██████╗  ██████╗ ███████╗
  ██╔════╝╚══██╔══╝██╔════╝██╔════╝████╗  ██║  ██╔══██╗██╔═══██╗██╔════╝
  ███████╗   ██║   █████╗  █████╗  ██╔██╗ ██║  ██████╔╝██║   ██║█████╗
  ╚════██║   ██║   ██╔══╝  ██╔══╝  ██║╚██╗██║  ██╔═══╝ ██║   ██║██╔══╝
  ███████║   ██║   ███████╗███████╗██║ ╚████║  ██║     ╚██████╔╝███████╗
  ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═══╝  ╚═╝      ╚═════╝ ╚══════╝

  ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗███████╗████████╗███████╗██████╗
  ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
  ██╔████╔██║███████║██████╔╝█████╔╝ █████╗     ██║   █████╗  ██████╔╝
  ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝     ██║   ██╔══╝  ██╔══██╗
  ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗███████╗   ██║   ███████╗██║  ██║
  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

**Path of Exile market analysis in your terminal.** 10 modules covering currency arbitrage, divination cards, gem flipping, economy snapshots, stash pricing, bulk calculation, watchlists, top movers, and item search — all powered by [poe.ninja](https://poe.ninja). No login required. Tab autocomplete on every input. Export to CSV, JSON, or HTML.

---

## Terminal preview

```
╭──────────────────── Main Menu ─ League: Settlers ──────────────────────╮
│  ⚡ Market Pulse — Settlers                                              │
│  Divine Orb  145.2c  ▲ +2.3%  │  Exalted Orb  2.1c  ─  │  Mirror  47k │
╰─────────────────────────────────────────────────────────────────────────╯

  1  ⚖  Currency Analysis    Buy/sell spreads · discount flags
  2  🔄  Arbitrage Finder    Round-number margins · 🔥 hot picks
  3  🃏  Divination Cards    Set costs · rewards · trend
  4  💎  Gem Flipper         Base→max margins · ROI
  5  📊  Economy Overview    Top items across 8 categories
  6  🏦  Stash Pricer        Price your tab items
  7  🧮  Bulk Calculator     Value stacks (40 div, 200c …)
  8  👁  Watchlist (3)       Track items · price deltas
  9  📈  Top Movers          Biggest gainers & losers (7d)
  10 🔍  Item Search         Fuzzy search all categories

  ↑/↓  history  ·  Tab  complete  ·  Ctrl+C  cancel

Select: _
```

```
┌─────────────────── 🔍 Item Search ─────────────────────┐
│ Search: head█                                           │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Headhunter                  Unique Armour            │ │
│ │ Head Hunter Deerstalker     Unique Armour            │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Quick start

```bash
# macOS / Linux
chmod +x setup.sh && ./setup.sh

# Or directly with Python 3.9+
python3 steen_poe.py

# Jump straight to a league
python3 steen_poe.py --league "Settlers"

# Search immediately without the menu
python3 steen_poe.py --search "Headhunter"
```

All three dependencies install automatically on first run.

---

## Tab autocomplete

Every input field supports **Tab** for autocomplete and **↑/↓** to recall history.

| Where | What completes |
|---|---|
| **Main menu** | `1`–`10`, `L`, `W`, `S`, `H`, `Q` |
| **Item Search** | All item names (fuzzy — type `head` → `Headhunter`) |
| **Stash Pricer** | All item names |
| **Watchlist Add** | All item names |
| **Bulk Calculator** | Currency aliases (`div`, `ex`, `c`, `mir` …) + full names |
| **League Select** | League names |
| **Export** | `csv`, `json`, `html` |

**Controls inside any prompt:**

| Key | Action |
|---|---|
| `Tab` | Show / cycle completions |
| `↑` / `↓` | Scroll through input history |
| `→` | Accept the current suggestion |
| `Ctrl+C` | Cancel the current input / go back |

> Completions are sourced from the disk cache. Run any module once to populate them — after that every subsequent session has full suggestions without waiting.

---

## CLI flags

| Flag | Short | Description |
|---|---|---|
| `--league NAME` | `-l` | Start with this league, skip the selection prompt |
| `--search QUERY` | `-s` | Jump straight to Item Search with this query |
| `--version` | | Print version and exit |
| `--help` | `-h` | Show built-in help |

---

## The 10 modules

### 1 — Currency Analysis ⚖
Live buy/sell spreads for every currency on poe.ninja. Shows chaos equivalent, discount vs median, and ▲/▼/─ 7-day trend. Items marked **★** are trading below the median — a potential buy opportunity.

### 2 — Arbitrage Finder 🔄
Finds profitable round-number trades between currency pairs. Surfaces pairs where the nearest whole-number exchange ratio gives a better deal than the exact ninja rate. Items marked **🔥** have >10% margin.

### 3 — Divination Cards 🃏
All divination cards with set cost (in chaos), reward description, stack size, and 7-day trend. Filter by minimum set cost. Cards worth ≥100c are highlighted in gold.

### 4 — Gem Flipper 💎
Profit margin between a base gem and its max level (20) / quality (20%) version. Filter by minimum profit. Shows ROI %, highlighted green (>100% ROI) or bright green (massive flip).

### 5 — Economy Overview 📊
Top-10 snapshot across 8 categories: Currency, Divination Cards, Unique Weapons, Unique Armours, Unique Accessories, Skill Gems, Unique Flasks, Unique Jewels.

### 6 — Stash Pricer 🏦
Enter item names one at a time. Fuzzy-matches against the full poe.ninja database. Shows price per item and a grand total.

### 7 — Bulk Calculator 🧮
Enter stacks using shorthand aliases (e.g. `40 div`, `200 chaos`) to get the total value in both chaos and divine. Accepts one entry per line; empty line or `done` to calculate.

### 8 — Watchlist 👁
Track any items across sessions. Each time you open the watchlist it shows the current price alongside the last-seen price and the delta — green for gains, red for losses.

### 9 — Top Movers 📈
Scans every category for the biggest % gainers and losers over the last 7 days. Good for spotting early meta shifts before the price peaks.

### 10 — Item Search 🔍
Fuzzy search by partial name across all categories simultaneously. Ranked by price. Also accessible directly via `--search` on the command line.

---

## Bulk calculator shortcuts

| Alias | Full name |
|---|---|
| `div` / `divine` | Divine Orb |
| `ex` / `exalt` | Exalted Orb |
| `c` / `chaos` | Chaos Orb |
| `mir` / `mirror` | Mirror of Kalandra |
| `fuse` / `fusing` | Orb of Fusing |
| `alt` | Orb of Alteration |
| `alch` | Orb of Alchemy |
| `regal` | Regal Orb |
| `annul` | Orb of Annulment |
| `vaal` | Vaal Orb |
| `chrome` | Chromatic Orb |
| `jew` / `jeweller` | Jeweller's Orb |
| `gcp` | Gemcutter's Prism |
| `blessed` | Blessed Orb |
| `scour` | Orb of Scouring |
| `regret` | Orb of Regret |
| `chisel` | Cartographer's Chisel |

Any name not in this list is looked up by its full name (case-insensitive).

---

## Reading the data

| Symbol | Meaning |
|---|---|
| `▲ +X.X%` | Price rising over 7 days |
| `▼ −X.X%` | Price falling over 7 days |
| `─ 0.0%` | Stable price |
| `★` | Buying below median — opportunity |
| `🔥` | Arbitrage margin >10% |
| `c` | Chaos Orb |
| `div` | Divine Orb |
| `k` / `M` | Thousands / millions |

**Column guide:**

| Column | Module | Meaning |
|---|---|---|
| Spread | Currency | Buy/sell gap — lower = more liquid |
| Discount | Currency | vs median — negative = bargain |
| Margin | Arbitrage | Profit % from round-number trade |
| Set Cost | Div Cards | Full card set value in chaos |
| ROI | Gem Flipper | Profit as % of base cost |
| Delta | Watchlist | Price change since last check |

---

## POESESSID authentication

POESESSID is **completely optional**. All 10 modules work without it — poe.ninja is a public API.

POESESSID is only used for `api.pathofexile.com` requests (league enumeration). Without it, leagues come from a poe.ninja fallback list.

**To find your POESESSID:**
1. Log in at [pathofexile.com](https://www.pathofexile.com)
2. Open DevTools → `F12` → Application → Cookies
3. Copy the value next to `POESESSID`

**To add it:** run the app → press `S` for Settings → option `1`.

Stored in `~/.steen_poe/config.json`. Never sent to poe.ninja — only to GGG's official API.

---

## Configuration and cache

| Path | Contents |
|---|---|
| `~/.steen_poe/config.json` | League, POESESSID, watchlist, last-seen prices |
| `~/.steen_poe/cache/` | poe.ninja responses (15-min TTL, one file per endpoint) |

The Market Pulse panel in the main menu shows cache age so you always know how fresh the data is. Clear the cache via `S → Settings → 2`.

---

## Requirements

- Python 3.9+
- `rich >= 13.7.0`
- `requests >= 2.31.0`
- `prompt_toolkit >= 3.0.0`

All installed automatically on first run, or manually:

```bash
pip install -r requirements.txt
```

---

## Disclaimer

Independent community tool. Not affiliated with or endorsed by Grinding Gear Games. All market data from [poe.ninja](https://poe.ninja). Prices are estimates — actual trade prices may differ. This tool does not automate trades or interact with the game client.

---

## Licence

MIT — built by Tony · [github.com/hardlygospel](https://github.com/hardlygospel)
