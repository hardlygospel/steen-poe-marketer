![Steen POE Marketer](https://img.shields.io/badge/Steen_POE_Marketer-v2.0.0-gold?style=flat-square&logo=python&logoColor=white)
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

**Path of Exile market analysis in your terminal.** 10 modules covering currency arbitrage, divination cards, gem flipping, economy snapshots, stash pricing, bulk calculation, watchlists, top movers, and item search — all powered by [poe.ninja](https://poe.ninja). No login required for any feature. Export everything to CSV, JSON, or HTML.

---

## Quick start

```bash
# macOS / Linux
chmod +x setup.sh && ./setup.sh

# Windows
python setup.bat

# Or directly with Python
python3 steen_poe.py

# Jump straight to a league
python3 steen_poe.py --league "Settlers"

# Search for an item immediately
python3 steen_poe.py --search "Headhunter"
```

Dependencies (`rich`, `requests`) are auto-installed on first run if missing.

---

## CLI flags

| Flag | Short | Description |
|---|---|---|
| `--league NAME` | `-l` | Start with this league, skip the selection prompt |
| `--search QUERY` | `-s` | Jump straight to Item Search with this query |
| `--version` | | Print version and exit |
| `--help` | `-h` | Show help and exit |

---

## The 10 modules

### 1 — Currency Analysis ⚖
Live buy/sell spreads for every currency on poe.ninja. Shows the chaos equivalent value, the discount vs. median price, and a ▲/▼/─ 7-day trend arrow for each item. Sorted by value descending. Export-ready.

### 2 — Arbitrage Finder 🔄
Finds profitable round-number trades between currency pairs. Uses `chaosEquivalent` as a common denominator and computes the nearest whole-number exchange ratio for each pair, then surfaces the pairs where the round-number rate is meaningfully better than the exact rate. Focus on trades with the highest margin percentage.

### 3 — Divination Cards 🃏
Lists all divination cards with their set cost (in chaos), reward description, stack size, and 7-day trend. Prompts for a minimum set cost filter so you can focus on the cards worth trading. High-value cards are highlighted in gold.

### 4 — Gem Flipper 💎
Shows the profit margin between buying a base gem and selling it at max level (20) or max quality (20%). Displays base cost, max cost, profit in chaos, and ROI percentage. Prompts for a minimum profit threshold (default: 5c) to cut noise. Gems with negative margins are hidden.

### 5 — Economy Overview 📊
A top-10 snapshot across every tracked item category: Currency, Divination Cards, Unique Weapons, Unique Armours, Unique Accessories, Unique Flasks, Unique Jewels, and Skill Gems. Each section shows value and 7-day trend. Good for a fast meta read.

### 6 — Stash Pricer 🏦
Type your item names one at a time (or paste a list). Searches all categories for each name and returns the chaos value. Totals everything up. Type `done` when finished. Great for pricing tabs before listing them.

### 7 — Bulk Calculator 🧮
Enter stacks of currency using shorthand aliases (e.g. `40 div`, `200 chaos`) and get the total chaos value. Supports entering multiple items separated by commas or one per line. Useful for large trades or comparing stash tab offers.

**Currency shortcuts:**

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
| `augment` | Orb of Augmentation |
| `transmute` | Orb of Transmutation |
| `whetstone` | Blacksmith's Whetstone |
| `armourer` | Armourer's Scrap |
| `bauble` | Glassblower's Bauble |
| `chisel` | Cartographer's Chisel |

Any name not in this list is looked up by its full name (case-insensitive).

### 8 — Watchlist 👁
Track specific items and see their price change since you last checked. Add items by name (partial match accepted), remove them individually, or clear the entire list. The watchlist is saved to disk and persists between sessions. Price deltas show green for gains, red for losses.

### 9 — Top Movers 📈📉
Scans every tracked category and surfaces the biggest percentage gainers and losers over the last 7 days. Useful for spotting early meta shifts and spec-into opportunities before they peak.

### 10 — Item Search 🔍
Fuzzy-search by partial name across all categories simultaneously. Returns every match with its chaos value, category, and trend. Can also be used directly from the command line with `--search`.

---

## Menu navigation

From the main menu, type the number of the module you want, or one of these shortcuts:

| Key | Action |
|---|---|
| `1`–`10` | Open that module |
| `L` | Change the active league |
| `W` | Add / remove / clear watchlist items |
| `S` | Settings (auth, cache, league) |
| `H` | Help |
| `Q` | Quit |
| `Ctrl+C` | Quit from anywhere |

---

## Export formats

After every module that returns data, you are asked whether you want to export. Options:

| Format | What you get |
|---|---|
| **CSV** | Flat spreadsheet, opens in Excel / Google Sheets |
| **JSON** | Full structured data with metadata header |
| **HTML** | Styled table with app name, league, and timestamp — ready to share |

Files are saved to the current working directory with a timestamped filename, e.g. `currency_analysis_20260503_142233.csv`.

---

## POESESSID authentication

POESESSID is **completely optional**. All 10 modules work without it — poe.ninja is a public API.

POESESSID is only used for requests to `api.pathofexile.com` (e.g., league enumeration via your account). Without it, leagues are fetched from a poe.ninja fallback list.

**To find your POESESSID:**

1. Log in at [pathofexile.com](https://www.pathofexile.com)
2. Open browser DevTools → Application → Cookies → `www.pathofexile.com`
3. Copy the value of the `POESESSID` cookie

**To add it to Steen POE Marketer:**

- Run the app → press `S` for Settings → `Auth`
- Or paste it when prompted on first run

The session ID is stored in `~/.steen_poe/config.json`. It is never sent to poe.ninja — only to GGG's official API.

---

## Configuration and cache

| Path | Contents |
|---|---|
| `~/.steen_poe/config.json` | League preference, POESESSID, watchlist, last-seen watchlist prices |
| `~/.steen_poe/cache/` | Cached poe.ninja responses (JSON, one file per endpoint) |

Cache TTL is **15 minutes**. The main menu shows the age of the current Divine Orb price snapshot so you always know how fresh the data is. To force a fresh fetch, use Settings → Clear Cache.

---

## Rate limits and fair use

- poe.ninja does not publish a formal rate limit, but the app caches all responses for 15 minutes to avoid hammering the API.
- Requests include a `User-Agent` header identifying this tool (`SteenPOEMarketer/2.0.0`).
- Do not disable or lower the cache TTL in production use.

---

## Requirements

- Python 3.9 or later
- `rich >= 13.7.0`
- `requests >= 2.31.0`

Both dependencies are installed automatically on first run. Or install manually:

```bash
pip install -r requirements.txt
```

---

## Disclaimer

Steen POE Marketer is an independent community tool. It is not affiliated with or endorsed by Grinding Gear Games. All market data is sourced from [poe.ninja](https://poe.ninja). Prices are estimates — actual trade prices may differ. This tool does not automate trades or interact with the game client.

---

## Licence

MIT — see [LICENSE](LICENSE) for details.

Built by Tony · [github.com/hardlygospel](https://github.com/hardlygospel)
