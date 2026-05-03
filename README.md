<div align="center">

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

<br>

<img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyModValues.png" height="36" title="Divine Orb" alt="Divine Orb">
&nbsp;
<img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyRerollRare.png" height="36" title="Chaos Orb" alt="Chaos Orb">
&nbsp;
<img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyAddModToRare.png" height="36" title="Exalted Orb" alt="Exalted Orb">
&nbsp;
<img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyDuplicate.png" height="36" title="Mirror of Kalandra" alt="Mirror of Kalandra">
&nbsp;
<img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyGemQuality.png" height="36" title="Gemcutter's Prism" alt="Gemcutter's Prism">
&nbsp;
<img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyVaal.png" height="36" title="Vaal Orb" alt="Vaal Orb">
&nbsp;
<img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyRerollSocketLinks.png" height="36" title="Orb of Fusing" alt="Orb of Fusing">

<br><br>

![Version](https://img.shields.io/badge/version-v3.0.0-gold?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-GPL--3.0-red?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-macOS_%7C_Linux_%7C_Windows-555?style=flat-square)
![Data](https://img.shields.io/badge/Data-poe.ninja-E97B2B?style=flat-square)
![Autocomplete](https://img.shields.io/badge/Tab-Autocomplete-00D7FF?style=flat-square)

<br>

**Path of Exile market analysis in your terminal.**<br>
10 modules · Tab autocomplete · poe.ninja data · Export to CSV / JSON / HTML

</div>

---

## Features at a glance

<table>
<tr>
<td width="50%">

**Market data**
- ⚖ Currency buy/sell spreads with discount flags
- 🔄 Arbitrage — round-number trade margins
- 🃏 Divination card set costs and rewards
- 💎 Gem flip margins and ROI
- 📊 Economy snapshot across 8 item categories

</td>
<td width="50%">

**Tools**
- 🏦 Stash tab pricer — total your tab in seconds
- 🧮 Bulk calculator — value stacks of currency
- 👁 Watchlist — track items with price deltas
- 📈 Top movers — biggest gainers and losers
- 🔍 Item search — fuzzy search all categories

</td>
</tr>
<tr>
<td>

**Input**
- Tab autocomplete on every input field
- Fuzzy matching (type `head` → `Headhunter`)
- ↑/↓ history recall within each session
- Currency shorthand (`div`, `ex`, `c`, `mir` …)

</td>
<td>

**Output**
- Rich colour-coded terminal tables
- ▲/▼/─ 7-day trend arrows
- ★ buy-below-median flags, 🔥 hot arbitrage
- Export to CSV, JSON, or styled HTML

</td>
</tr>
</table>

---

## Quick start

```bash
# macOS / Linux
chmod +x setup.sh && ./setup.sh

# Any platform — Python 3.9+
python3 steen_poe.py

# Skip league selection
python3 steen_poe.py --league "Settlers"

# Jump straight to search
python3 steen_poe.py --search "Headhunter"
```

Dependencies install automatically on first run. Or manually:

```bash
pip install -r requirements.txt
```

---

## Terminal preview

```
  ███████╗████████╗███████╗███████╗ ...
  ...

  v3.0.0  ·  poe.ninja data  ·  Tab autocomplete  ·  GPL-3.0

✓  poe.ninja online

────────────────── Main Menu  League: Settlers ──────────────────────

╭─── ⚡ Market Pulse — Settlers ──────────────────────────────────────╮
│  Divine Orb  145.2c  ▲ +2.3%  │  Exalted Orb  2.1c  ─  │  5m ago  │
╰─────────────────────────────────────────────────────────────────────╯

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
╭─── ⚖ Currency Analysis — Buy Opportunities ───────────────────────────────╮
│  #   Currency            Median     Buy      Sell    Spread  Discount   7d  │
│ ─────────────────────────────────────────────────────────────────────────── │
│  1   Divine Orb ★        145.2c   140.0c   148.0c    5.4%    -3.6%  ▲ +2.3% │
│  2   Mirror of Kalandra  47.2kc   46.0kc   48.0kc    4.2%    -2.5%  ─ 0.0%  │
│  3   Exalted Orb          2.1c     2.0c     2.2c     9.1%    -4.8%  ▼ -1.2% │
╰─────────────────────────────────────────────────────────────────────────────╯
  Discount < 0% = buying below median = opportunity  ·  Spread < 5% = liquid
```

---

## Tab autocomplete

Every input field supports **Tab** for autocomplete and **↑/↓** to recall history — powered by [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/).

| Where | What completes |
|---|---|
| **Main menu** | `1`–`10`, `L`, `W`, `S`, `H`, `Q` |
| **Item Search** | All item names — fuzzy (type `head` → `Headhunter`) |
| **Stash Pricer** | All item names |
| **Watchlist Add** | All item names |
| **Bulk Calculator** | Currency aliases + full currency names |
| **League Select** | League names |
| **Export** | `csv` / `json` / `html` |

| Key | Action |
|---|---|
| `Tab` | Open or cycle through completions |
| `↑` / `↓` | Scroll input history |
| `→` | Accept current suggestion |
| `Ctrl+C` | Cancel / go back to menu |

> Completions draw from the disk cache. Run any module once to populate them — every session after that has full suggestions instantly.

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

### ⚖ 1 — Currency Analysis
Live buy/sell spreads for every currency. Shows chaos equivalent, discount vs median, and ▲/▼/─ 7-day trend. Items marked **★** are trading below the median — a potential buy opportunity.

### 🔄 2 — Arbitrage Finder
Finds profitable round-number trades between currency pairs. Items marked **🔥** have >10% margin.

### 🃏 3 — Divination Cards
All divination cards with set cost (in chaos), reward text, stack size, and 7-day trend. Filter by minimum set cost on entry. Cards worth ≥ 100c are highlighted in gold.

### 💎 4 — Gem Flipper
Profit margin between a base gem and its max level / quality version. Shows ROI %. Filter by minimum profit (default: 5c).

### 📊 5 — Economy Overview
Top-value snapshot across 8 categories: Currency, Divination Cards, Unique Weapons, Unique Armours, Unique Accessories, Skill Gems, Unique Flasks, Unique Jewels.

### 🏦 6 — Stash Pricer
Enter item names one at a time with Tab completion. Fuzzy-matches the full poe.ninja database. Shows price per item and a grand total.

### 🧮 7 — Bulk Calculator
Enter stacks like `40 div` or `200 chaos` to get the total in chaos and divine. See the full alias list below.

### 👁 8 — Watchlist
Track items across sessions. Shows current price, last-seen price, and the delta — green for gains, red for losses.

### 📈 9 — Top Movers
Scans every category for the biggest % gainers and losers over 7 days. Useful for spotting meta shifts early.

### 🔍 10 — Item Search
Fuzzy name search across all categories, ranked by price. Also accessible via `--search` on the command line.

---

## Bulk calculator shortcuts

<table>
<thead>
<tr><th></th><th>Alias</th><th>Full name</th></tr>
</thead>
<tbody>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyModValues.png" height="22" alt="Divine Orb"></td>
  <td><code>div</code> &nbsp;/&nbsp; <code>divine</code></td>
  <td>Divine Orb</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyAddModToRare.png" height="22" alt="Exalted Orb"></td>
  <td><code>ex</code> &nbsp;/&nbsp; <code>exalt</code></td>
  <td>Exalted Orb</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyRerollRare.png" height="22" alt="Chaos Orb"></td>
  <td><code>c</code> &nbsp;/&nbsp; <code>chaos</code></td>
  <td>Chaos Orb</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyDuplicate.png" height="22" alt="Mirror of Kalandra"></td>
  <td><code>mir</code> &nbsp;/&nbsp; <code>mirror</code></td>
  <td>Mirror of Kalandra</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyRerollSocketLinks.png" height="22" alt="Orb of Fusing"></td>
  <td><code>fuse</code> &nbsp;/&nbsp; <code>fusing</code></td>
  <td>Orb of Fusing</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyUpgradeToRare.png" height="22" alt="Orb of Alchemy"></td>
  <td><code>alch</code></td>
  <td>Orb of Alchemy</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyRerollMagic.png" height="22" alt="Orb of Alteration"></td>
  <td><code>alt</code></td>
  <td>Orb of Alteration</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyGemQuality.png" height="22" alt="Gemcutter's Prism"></td>
  <td><code>gcp</code></td>
  <td>Gemcutter's Prism</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyUpgradeMagicToRare.png" height="22" alt="Regal Orb"></td>
  <td><code>regal</code></td>
  <td>Regal Orb</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/AnnulmentOrb.png" height="22" alt="Orb of Annulment"></td>
  <td><code>annul</code></td>
  <td>Orb of Annulment</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyVaal.png" height="22" alt="Vaal Orb"></td>
  <td><code>vaal</code></td>
  <td>Vaal Orb</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyRecolour.png" height="22" alt="Chromatic Orb"></td>
  <td><code>chrome</code></td>
  <td>Chromatic Orb</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyRerollSocketNumbers.png" height="22" alt="Jeweller's Orb"></td>
  <td><code>jew</code> &nbsp;/&nbsp; <code>jeweller</code></td>
  <td>Jeweller's Orb</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyConvertToNormal.png" height="22" alt="Orb of Scouring"></td>
  <td><code>scour</code></td>
  <td>Orb of Scouring</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyPassiveRefund.png" height="22" alt="Orb of Regret"></td>
  <td><code>regret</code></td>
  <td>Orb of Regret</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyMapQuality.png" height="22" alt="Cartographer's Chisel"></td>
  <td><code>chisel</code></td>
  <td>Cartographer's Chisel</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyImplicitMod.png" height="22" alt="Blessed Orb"></td>
  <td><code>blessed</code></td>
  <td>Blessed Orb</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyWeaponQuality.png" height="22" alt="Blacksmith's Whetstone"></td>
  <td><code>whetstone</code></td>
  <td>Blacksmith's Whetstone</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyArmourQuality.png" height="22" alt="Armourer's Scrap"></td>
  <td><code>armourer</code></td>
  <td>Armourer's Scrap</td>
</tr>
<tr>
  <td align="center"><img src="https://web.poecdn.com/image/Art/2DItems/Currency/CurrencyFlaskQuality.png" height="22" alt="Glassblower's Bauble"></td>
  <td><code>bauble</code></td>
  <td>Glassblower's Bauble</td>
</tr>
</tbody>
</table>

Any name not in this list is looked up by its full name (case-insensitive).

---

## Reading the data

| Symbol | Meaning |
|---|---|
| `▲ +X.X%` | Price rising over 7 days |
| `▼ −X.X%` | Price falling over 7 days |
| `─  0.0%` | Stable price |
| **★** | Discount > 5% below median — buy opportunity |
| **🔥** | Arbitrage margin > 10% |

| Column | Module | Meaning |
|---|---|---|
| Spread | Currency | Buy/sell gap — lower = more liquid |
| Discount | Currency | vs median — negative = bargain |
| Margin | Arbitrage | Profit % from round-number trade |
| Set Cost | Div Cards | Full card set value in chaos |
| ROI | Gem Flipper | Profit as % of base cost |
| Delta | Watchlist | Price change since last check |

`c` = chaos orb · `div` = divine orb · `k` = thousands · `M` = millions

---

## POESESSID authentication

**Completely optional** — all 10 modules work without it. poe.ninja is a public API.

A POESESSID is only used for `api.pathofexile.com` (live league enumeration). Without it, leagues come from a poe.ninja fallback list.

<details>
<summary><strong>How to find your POESESSID</strong></summary>

1. Log in at [pathofexile.com](https://www.pathofexile.com)
2. Open DevTools → `F12` → **Application** tab → **Cookies** → `www.pathofexile.com`
3. Copy the value next to `POESESSID`

</details>

To add it: press `S` in the main menu → option `1`. Stored in `~/.steen_poe/config.json`. Never sent to poe.ninja — only to GGG's official API.

---

## Configuration

| Path | Contents |
|---|---|
| `~/.steen_poe/config.json` | League preference, POESESSID, watchlist, last-seen prices |
| `~/.steen_poe/cache/` | poe.ninja responses — 15-min TTL, one file per endpoint |

The **⚡ Market Pulse** panel in the main menu shows cache age so you always know how fresh the data is. Clear the cache via `S → Settings → 2`.

---

## Requirements

- Python 3.9 or later
- `rich >= 13.7.0`
- `requests >= 2.31.0`
- `prompt_toolkit >= 3.0.0`

---

## Disclaimer

Independent community tool. Not affiliated with or endorsed by Grinding Gear Games. All market data from [poe.ninja](https://poe.ninja). Prices are estimates — actual trade prices may differ. Does not automate trades or interact with the game client.

---

<div align="center">

[![poe.ninja](https://img.shields.io/badge/Powered_by-poe.ninja-E97B2B?style=flat-square)](https://poe.ninja)
&nbsp;
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0)

*Built by Tony · [github.com/hardlygospel](https://github.com/hardlygospel)*

</div>
