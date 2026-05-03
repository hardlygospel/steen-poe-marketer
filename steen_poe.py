#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Steen POE Marketer — Path of Exile market analysis tool.
Powered by poe.ninja · Optional PoE Trade API · No affiliation with GGG.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


# ── Auto-install dependencies ─────────────────────────────────────────────────

def _pip_install(packages: list[str]) -> None:
    import subprocess
    for extra in ([], ["--user"], ["--user", "--break-system-packages"]):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet"] + extra + packages,
                stderr=subprocess.DEVNULL,
            )
            return
        except subprocess.CalledProcessError:
            continue
    print(f"[!] Could not install: {' '.join(packages)}")
    sys.exit(1)


def _ensure_deps() -> None:
    missing = []
    try:
        import rich      # noqa: F401
    except ImportError:
        missing.append("rich>=13.7.0")
    try:
        import requests  # noqa: F401
    except ImportError:
        missing.append("requests>=2.31.0")
    if missing:
        print(f"Installing: {', '.join(missing)} …")
        _pip_install(missing)


_ensure_deps()

import requests                                                   # noqa: E402
from rich import box                                              # noqa: E402
from rich.console import Console                                  # noqa: E402
from rich.markdown import Markdown                                # noqa: E402
from rich.padding import Padding                                  # noqa: E402
from rich.panel import Panel                                      # noqa: E402
from rich.progress import Progress, SpinnerColumn, TextColumn     # noqa: E402
from rich.prompt import Confirm, Prompt                           # noqa: E402
from rich.rule import Rule                                        # noqa: E402
from rich.table import Table                                      # noqa: E402
from rich.text import Text                                        # noqa: E402

console = Console()

# ── Constants ─────────────────────────────────────────────────────────────────

APP_VERSION   = "1.0.0"
APP_NAME      = "Steen POE Marketer"
POE_NINJA_API = "https://poe.ninja/api/data"
POE_API       = "https://api.pathofexile.com"
CONFIG_DIR    = Path.home() / ".steen_poe"
CONFIG_FILE   = CONFIG_DIR / "config.json"
CACHE_DIR     = CONFIG_DIR / "cache"
CACHE_TTL     = 15   # minutes
USER_AGENT    = f"SteenPOEMarketer/{APP_VERSION} (github.com/hardlygospel)"


# ── Config ────────────────────────────────────────────────────────────────────

def load_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_config(cfg: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


# ── Cache ─────────────────────────────────────────────────────────────────────

def _cache_key(s: str) -> Path:
    return CACHE_DIR / f"{re.sub(r'[^\\w]', '_', s)}.json"


def cache_get(key: str, ttl: int = CACHE_TTL) -> Optional[object]:
    p = _cache_key(key)
    if not p.exists():
        return None
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        if datetime.now() - datetime.fromisoformat(d["at"]) < timedelta(minutes=ttl):
            return d["v"]
    except Exception:
        pass
    return None


def cache_set(key: str, value: object) -> None:
    p = _cache_key(key)
    p.write_text(
        json.dumps({"at": datetime.now().isoformat(), "v": value}, ensure_ascii=False),
        encoding="utf-8",
    )


# ── HTTP ──────────────────────────────────────────────────────────────────────

def _headers(cfg: dict) -> dict:
    h = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if cfg.get("poesessid"):
        h["Cookie"] = f"POESESSID={cfg['poesessid']}"
    return h


def _get(url: str, cfg: dict, params: dict | None = None) -> Optional[dict]:
    try:
        r = requests.get(url, headers=_headers(cfg), params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        console.print(f"[red]HTTP {e.response.status_code}: {url}[/red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Request error: {e}[/red]")
    return None


# ── poe.ninja wrapper ─────────────────────────────────────────────────────────

def ninja_fetch(league: str, endpoint: str, type_: str, cfg: dict) -> list[dict]:
    key    = f"ninja_{league}_{endpoint}_{type_}"
    cached = cache_get(key)
    if cached is not None:
        return cached
    data = _get(f"{POE_NINJA_API}/{endpoint}", cfg, {"league": league, "type": type_})
    lines = (data or {}).get("lines", [])
    if lines:
        cache_set(key, lines)
    return lines


def fetch_leagues(cfg: dict) -> list[str]:
    cached = cache_get("leagues", ttl=60)
    if cached:
        return cached
    data = _get(f"{POE_API}/leagues", cfg, {"type": "main", "compact": "1"})
    if not data:
        return ["Settlers", "Standard", "Hardcore"]
    names = [
        lg["id"] for lg in data
        if "SSF" not in lg["id"] and "Ruthless" not in lg["id"]
    ]
    cache_set("leagues", names)
    return names


# ── Shared helpers ────────────────────────────────────────────────────────────

def _cv(item: dict) -> float:
    return float(item.get("chaosValue") or item.get("chaosEquivalent") or 0)


def _change(item: dict) -> float:
    sl = item.get("sparkline") or item.get("receiveSparkLine") or {}
    return float(sl.get("totalChange") or 0)


def _fmt(val: float) -> str:
    if val >= 1000: return f"{val/1000:.1f}k"
    if val >= 1:    return f"{val:.1f}"
    return f"{val:.2f}"


def _chg_style(v: float) -> str:
    if v > 10:  return "bold bright_green"
    if v > 0:   return "green"
    if v > -10: return "yellow"
    return "red"


# ── Module 1 — Currency Analysis ─────────────────────────────────────────────

def run_currency_analysis(league: str, cfg: dict) -> list[dict]:
    """
    For every non-chaos currency show:
    - ninja median (chaosEquivalent)
    - buy price  (receive.value = chaos you spend to get 1 unit)
    - sell price (pay.value     = chaos you receive when selling 1 unit)
    - spread %   = (buy - sell) / buy × 100  — tighter is more liquid
    - discount % = (buy - median) / median × 100  — negative = cheaper than median
    """
    lines = ninja_fetch(league, "currencyoverview", "Currency", cfg)
    out   = []
    for item in lines:
        name   = item.get("currencyTypeName", "")
        median = float(item.get("chaosEquivalent") or 0)
        if name == "Chaos Orb" or median < 0.5:
            continue
        pay     = item.get("pay")     or {}
        receive = item.get("receive") or {}
        # receive.value = chaos per 1 unit (buy price)
        # pay.value     = chaos per 1 unit (sell price)
        buy  = float(receive.get("value") or median)
        sell = float(pay.get("value")     or median)
        if buy  <= 0: buy  = median
        if sell <= 0: sell = median
        spread   = (buy - sell) / buy    * 100 if buy   > 0 else 0
        discount = (buy - median) / median * 100 if median > 0 else 0
        out.append({
            "name":        name,
            "median":      round(median, 2),
            "buy":         round(buy, 2),
            "sell":        round(sell, 2),
            "spread_pct":  round(spread, 1),
            "discount_pct": round(discount, 1),
            "change_7d":   round(_change(item), 1),
        })
    out.sort(key=lambda x: x["discount_pct"])   # biggest discount first (most negative)
    return out


# ── Module 2 — Arbitrage Finder ───────────────────────────────────────────────

def run_arbitrage(league: str, cfg: dict) -> list[dict]:
    """
    Find round-number trade opportunities between currency pairs.
    When 1 Divine = 195.7c and players trade 1:195, that's a 0.36% gain for the buyer.
    We surface pairs where the nearest whole-number ratio gives ≥ 2% margin.
    """
    lines = ninja_fetch(league, "currencyoverview", "Currency", cfg)
    cmap  = {"Chaos Orb": 1.0}
    for item in lines:
        n = item.get("currencyTypeName", "")
        v = float(item.get("chaosEquivalent") or 0)
        if n and v > 0:
            cmap[n] = v

    results = []
    pairs   = [(n, v) for n, v in cmap.items() if n != "Chaos Orb" and v >= 2.0]

    for i, (a, av) in enumerate(pairs):
        for b, bv in pairs[i + 1:]:
            ratio = av / bv   # how many B per 1 A (exact)
            if ratio < 1:     # always compare bigger:smaller
                a, av, b, bv, ratio = b, bv, a, av, 1 / ratio
            floor_r = int(ratio)
            ceil_r  = floor_r + 1
            if floor_r < 1:
                continue
            # Profit if you trade A→B at floor (get floor_r B for 1 A)
            pf = (floor_r * bv - av) / av * 100
            # Profit if you trade A→B at ceil (get ceil_r B for 1 A)
            pc = (ceil_r  * bv - av) / av * 100
            best_pct  = pf if abs(pf) >= abs(pc) else pc
            trade_at  = floor_r if abs(pf) >= abs(pc) else ceil_r
            if abs(best_pct) < 2.0:
                continue
            direction = f"{a} → {b}" if best_pct > 0 else f"{b} → {a}"
            results.append({
                "pair":      direction,
                "a_name":    a,
                "b_name":    b,
                "a_val":     round(av, 1),
                "b_val":     round(bv, 1),
                "exact":     round(ratio, 2),
                "trade_at":  trade_at,
                "margin_pct": round(abs(best_pct), 2),
            })

    results.sort(key=lambda x: x["margin_pct"], reverse=True)
    return results[:30]


# ── Module 3 — Divination Cards ───────────────────────────────────────────────

def run_div_cards(league: str, cfg: dict) -> list[dict]:
    lines = ninja_fetch(league, "itemoverview", "DivinationCard", cfg)
    out   = []
    for item in lines:
        price = _cv(item)
        if price < 0.1:
            continue
        stack  = int(item.get("stackSize") or 1)
        expl   = item.get("explicitModifiers") or []
        reward = expl[0].get("text", "—")[:70] if expl else "—"
        out.append({
            "name":     item.get("name", ""),
            "stack":    stack,
            "per_card": round(price, 2),
            "set_cost": round(price * stack, 1),
            "change_7d": round(_change(item), 1),
            "listings": int(item.get("count") or 0),
            "reward":   reward,
        })
    out.sort(key=lambda x: x["set_cost"], reverse=True)
    return out


# ── Module 4 — Gem Flipper ────────────────────────────────────────────────────

def run_gem_flipper(league: str, cfg: dict) -> list[dict]:
    lines  = ninja_fetch(league, "itemoverview", "SkillGem", cfg)
    groups: dict[str, list[dict]] = defaultdict(list)
    for item in lines:
        groups[item.get("name", "")].append(item)

    out = []
    for name, variants in groups.items():
        base_candidates = [
            g for g in variants
            if (g.get("gemLevel") or 1) <= 1
            and (g.get("gemQuality") or 0) == 0
            and not g.get("corrupted")
        ]
        top_candidates = [g for g in variants if (g.get("gemLevel") or 1) >= 20]
        if not base_candidates or not top_candidates:
            continue
        base_price = _cv(min(base_candidates, key=_cv))
        top_item   = max(top_candidates, key=_cv)
        top_price  = _cv(top_item)
        if base_price < 1 or top_price < 5:
            continue
        profit = top_price - base_price
        if profit < 5 or profit / base_price < 0.2:
            continue
        out.append({
            "name":       name,
            "base_price": round(base_price, 1),
            "max_lvl":    top_item.get("gemLevel") or 20,
            "max_q":      top_item.get("gemQuality") or 0,
            "corrupted":  bool(top_item.get("corrupted")),
            "max_price":  round(top_price, 1),
            "profit":     round(profit, 1),
            "roi_pct":    round(profit / base_price * 100, 0),
            "change_7d":  round(_change(top_item), 1),
        })
    out.sort(key=lambda x: x["profit"], reverse=True)
    return out[:40]


# ── Module 5 — Economy Overview ───────────────────────────────────────────────

ECONOMY_CATEGORIES = [
    ("Currency",        "currencyoverview", "Currency",        "currencyTypeName"),
    ("DivinationCard",  "itemoverview",     "DivinationCard",  "name"),
    ("UniqueWeapon",    "itemoverview",     "UniqueWeapon",    "name"),
    ("UniqueArmour",    "itemoverview",     "UniqueArmour",    "name"),
    ("UniqueAccessory", "itemoverview",     "UniqueAccessory", "name"),
    ("SkillGem",        "itemoverview",     "SkillGem",        "name"),
    ("UniqueFlask",     "itemoverview",     "UniqueFlask",     "name"),
    ("UniqueJewel",     "itemoverview",     "UniqueJewel",     "name"),
]


def run_economy_overview(league: str, cfg: dict) -> dict:
    overview = {}
    with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                  console=console, transient=True) as prog:
        task = prog.add_task("Fetching market data…", total=len(ECONOMY_CATEGORIES))
        for cat, endpoint, type_, _ in ECONOMY_CATEGORIES:
            prog.update(task, description=f"Fetching {cat}…")
            lines = ninja_fetch(league, endpoint, type_, cfg)
            if lines:
                overview[cat] = {
                    "top_value": sorted(lines, key=_cv, reverse=True)[:6],
                    "top_gain":  sorted(lines, key=_change, reverse=True)[:4],
                    "top_loss":  sorted(lines, key=_change)[:4],
                    "count":     len(lines),
                }
            prog.advance(task)
    return overview


# ── Module 6 — Stash Pricer ───────────────────────────────────────────────────

def run_stash_pricer(league: str, cfg: dict) -> list[dict]:
    console.print(
        "\n[bold cyan]Stash Tab Pricer[/bold cyan]\n"
        "[dim]Enter item names one per line.  "
        "Type [bold]done[/bold] when finished.[/dim]\n"
    )

    # Build a name → chaos lookup from every category
    lookup: dict[str, float] = {}
    with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                  console=console, transient=True) as prog:
        task = prog.add_task("Building price database…")
        for _, endpoint, type_, name_key in ECONOMY_CATEGORIES:
            for item in ninja_fetch(league, endpoint, type_, cfg):
                n = item.get(name_key, "")
                v = _cv(item)
                if n and v > 0:
                    lookup[n.lower()] = v
        prog.update(task, description=f"Ready — {len(lookup):,} items loaded")

    inputs: list[str] = []
    while True:
        try:
            line = Prompt.ask("[bold bright_green]Item[/bold bright_green]").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not line or line.lower() in ("done", "/done"):
            break
        inputs.append(line)

    results = []
    for raw in inputs:
        key   = raw.lower()
        price = lookup.get(key)
        label = raw
        # Fuzzy partial-match fallback
        if price is None:
            matches = [(n, v) for n, v in lookup.items() if key in n or n in key]
            if len(matches) == 1:
                price = matches[0][1]
                label = f"{raw}  [dim](~{matches[0][0]})[/dim]"
        results.append({"name": label, "price": price, "found": price is not None})
    return results


# ── Display ───────────────────────────────────────────────────────────────────

def display_currency_analysis(data: list[dict], limit: int = 35) -> None:
    t = Table(
        title="Currency Analysis — Buy Opportunities",
        box=box.ROUNDED, border_style="cyan", title_style="bold cyan",
    )
    t.add_column("#",         width=4,  justify="right", style="dim")
    t.add_column("Currency",  min_width=22, style="bold yellow")
    t.add_column("Median",    width=10, justify="right", style="white")
    t.add_column("Buy",       width=10, justify="right", style="bright_cyan")
    t.add_column("Sell",      width=10, justify="right", style="bright_green")
    t.add_column("Spread",    width=9,  justify="right")
    t.add_column("Discount",  width=10, justify="right")
    t.add_column("7d",        width=8,  justify="right")

    for i, r in enumerate(data[:limit], 1):
        sp_s = "green" if r["spread_pct"] < 5 else ("yellow" if r["spread_pct"] < 15 else "red")
        dc_s = "bright_green" if r["discount_pct"] < -3 else ("green" if r["discount_pct"] < 0 else "dim")
        t.add_row(
            str(i), r["name"],
            f"{_fmt(r['median'])}c",
            f"{_fmt(r['buy'])}c",
            f"{_fmt(r['sell'])}c",
            Text(f"{r['spread_pct']:.1f}%",   style=sp_s),
            Text(f"{r['discount_pct']:+.1f}%", style=dc_s),
            Text(f"{r['change_7d']:+.1f}%",    style=_chg_style(r["change_7d"])),
        )
    console.print(Padding(t, (1, 0)))
    console.print(
        "[dim]Discount = buy price vs ninja median. "
        "Negative = cheaper than median → buying opportunity.[/dim]\n"
    )


def display_arbitrage(data: list[dict], limit: int = 20) -> None:
    if not data:
        console.print("[yellow]No significant arbitrage found for this league.[/yellow]\n")
        return
    t = Table(
        title="Arbitrage — Round-Number Trade Margins",
        box=box.ROUNDED, border_style="magenta", title_style="bold magenta",
    )
    t.add_column("#",        width=4,  justify="right", style="dim")
    t.add_column("Pair",     min_width=34, style="bold yellow")
    t.add_column("Exact",    width=10, justify="right", style="dim white")
    t.add_column("Trade At", width=10, justify="right", style="cyan")
    t.add_column("A (c)",    width=10, justify="right", style="dim")
    t.add_column("B (c)",    width=10, justify="right", style="dim")
    t.add_column("Margin",   width=10, justify="right")
    for i, r in enumerate(data[:limit], 1):
        ms = "bold bright_green" if r["margin_pct"] > 5 else "green"
        t.add_row(
            str(i), r["pair"],
            f"1 : {r['exact']}",
            f"1 : {r['trade_at']}",
            f"{_fmt(r['a_val'])}c",
            f"{_fmt(r['b_val'])}c",
            Text(f"+{r['margin_pct']:.1f}%", style=ms),
        )
    console.print(Padding(t, (1, 0)))
    console.print(
        "[dim]Margin = chaos value gained by trading at the nearest whole-number ratio "
        "vs the exact ninja rate.[/dim]\n"
    )


def display_div_cards(data: list[dict], limit: int = 40) -> None:
    t = Table(
        title="Divination Cards",
        box=box.ROUNDED, border_style="yellow", title_style="bold yellow",
    )
    t.add_column("#",       width=4,  justify="right", style="dim")
    t.add_column("Card",    min_width=26, style="bold yellow")
    t.add_column("Stack",   width=7,  justify="center", style="dim")
    t.add_column("Each",    width=10, justify="right", style="cyan")
    t.add_column("Set",     width=10, justify="right", style="bold white")
    t.add_column("7d",      width=8,  justify="right")
    t.add_column("Listings",width=9,  justify="right", style="dim")
    t.add_column("Reward",  min_width=28, style="dim")
    for i, r in enumerate(data[:limit], 1):
        t.add_row(
            str(i), r["name"], str(r["stack"]),
            f"{_fmt(r['per_card'])}c",
            f"{_fmt(r['set_cost'])}c",
            Text(f"{r['change_7d']:+.1f}%", style=_chg_style(r["change_7d"])),
            str(r["listings"]),
            r["reward"],
        )
    console.print(Padding(t, (1, 0)))


def display_gem_flipper(data: list[dict], limit: int = 30) -> None:
    if not data:
        console.print("[dim]No gem flip opportunities found.[/dim]\n")
        return
    t = Table(
        title="Gem Flipper — Level / Quality Premiums",
        box=box.ROUNDED, border_style="bright_blue", title_style="bold bright_blue",
    )
    t.add_column("#",       width=4,  justify="right", style="dim")
    t.add_column("Gem",     min_width=26, style="bold cyan")
    t.add_column("Base",    width=9,  justify="right", style="dim white")
    t.add_column("Lvl",     width=5,  justify="center", style="dim")
    t.add_column("Q",       width=5,  justify="center", style="dim")
    t.add_column("Cor",     width=5,  justify="center")
    t.add_column("Max",     width=10, justify="right", style="bold yellow")
    t.add_column("Profit",  width=10, justify="right", style="bold bright_green")
    t.add_column("ROI",     width=7,  justify="right")
    t.add_column("7d",      width=8,  justify="right")
    for i, r in enumerate(data[:limit], 1):
        cor = Text("Y", style="red") if r["corrupted"] else Text("N", style="dim")
        roi_s = "bold bright_green" if r["roi_pct"] > 100 else "green"
        t.add_row(
            str(i), r["name"],
            f"{_fmt(r['base_price'])}c",
            str(r["max_lvl"]), str(r["max_q"]), cor,
            f"{_fmt(r['max_price'])}c",
            f"+{_fmt(r['profit'])}c",
            Text(f"{r['roi_pct']:.0f}%", style=roi_s),
            Text(f"{r['change_7d']:+.1f}%", style=_chg_style(r["change_7d"])),
        )
    console.print(Padding(t, (1, 0)))
    console.print("[dim]ROI = profit as % of base cost. Gems require time to level.[/dim]\n")


def display_economy_overview(data: dict, league: str) -> None:
    console.print()
    console.print(Rule(f"[bold cyan]Economy Overview — {league}[/bold cyan]", style="cyan"))
    for cat, cd in data.items():
        name_key = "currencyTypeName" if cat == "Currency" else "name"
        t = Table(
            title=f"[bold white]{cat}[/bold white]  [dim]({cd['count']} tracked)[/dim]",
            box=box.SIMPLE_HEAD, border_style="dim blue",
            title_style="bold white",
        )
        t.add_column("Item",    min_width=26)
        t.add_column("Value",   width=12, justify="right", style="bold yellow")
        t.add_column("7d",      width=10, justify="right")
        for item in cd["top_value"]:
            n = item.get(name_key, "?")
            v = _cv(item)
            c = _change(item)
            t.add_row(n, f"{_fmt(v)}c", Text(f"{c:+.1f}%", style=_chg_style(c)))
        console.print(Padding(t, (1, 0, 0, 0)))


def display_stash_pricer(data: list[dict]) -> None:
    total = sum(r["price"] for r in data if r["found"] and r["price"])
    found = sum(1 for r in data if r["found"])
    t = Table(
        title="Stash Tab Valuation",
        box=box.ROUNDED, border_style="green", title_style="bold green",
    )
    t.add_column("Item",    min_width=36)
    t.add_column("Value",   width=14, justify="right")
    t.add_column("",        width=12, justify="center")
    for r in data:
        if r["found"]:
            t.add_row(r["name"], Text(f"{_fmt(r['price'])}c", style="bold yellow"),
                      Text("✓", style="green"))
        else:
            t.add_row(r["name"], Text("—", style="dim"), Text("✗ not found", style="red"))
    console.print(Padding(t, (1, 0)))
    console.print(Panel(
        f"[bold green]Total:[/bold green]  [bold yellow]{_fmt(total)}[/bold yellow] chaos  "
        f"[dim]({found}/{len(data)} priced)[/dim]",
        border_style="green", padding=(0, 2),
    ))


# ── Export ────────────────────────────────────────────────────────────────────

def export_csv(data: list[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=data[0].keys())
        w.writeheader()
        w.writerows(data)
    return path


def export_json_data(data: list[dict], title: str, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({
            "meta": {"title": title, "app": APP_NAME,
                     "version": APP_VERSION,
                     "exported_at": datetime.now().isoformat()},
            "data": data,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def export_html_data(data: list[dict], title: str, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys    = list(data[0].keys())
    headers = "".join(f"<th>{k.replace('_',' ').title()}</th>" for k in keys)
    rows    = ""
    for row in data:
        cells = ""
        for k in keys:
            v = row[k]
            cells += f"<td>{f'{v:.2f}' if isinstance(v, float) else v}</td>"
        rows += f"<tr>{cells}</tr>"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>{title} — {APP_NAME}</title>
<style>
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
       background:#1a1b1e;color:#c1c2c5;padding:2rem;}}
  h1{{color:#4dabf7;}} p.meta{{color:#5c5f66;font-size:.85rem;margin-bottom:1.5rem;}}
  table{{border-collapse:collapse;width:100%;}}
  th{{background:#2c2e33;color:#a9b7d0;padding:.6rem 1rem;text-align:left;
      border-bottom:2px solid #373a40;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;}}
  td{{padding:.5rem 1rem;border-bottom:1px solid #2c2e33;font-size:.9rem;}}
  tr:hover td{{background:#25262b;}}
</style></head>
<body>
<h1>⚔️  {title}</h1>
<p class="meta">Generated by {APP_NAME} v{APP_VERSION} · {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>
</body></html>"""
    path.write_text(html, encoding="utf-8")
    return path


def prompt_export(data: list[dict], slug: str) -> None:
    if not data:
        return
    console.print("[dim]Export? Enter [bold]csv[/bold] / [bold]json[/bold] / [bold]html[/bold] or press Enter to skip:[/dim]")
    try:
        fmt = Prompt.ask("[cyan]Format[/cyan]", default="").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return
    if not fmt:
        return
    ext = {"csv": ".csv", "json": ".json", "html": ".html"}.get(fmt)
    if not ext:
        console.print("[red]Unknown format.[/red]")
        return
    out = Path.cwd() / f"steen_poe_{slug}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}{ext}"
    if fmt == "csv":
        export_csv(data, out)
    elif fmt == "json":
        export_json_data(data, slug, out)
    else:
        export_html_data(data, slug.replace("_", " ").title(), out)
    console.print(Panel(f"[bold green]✓ Saved:[/bold green] [cyan]{out}[/cyan]",
                        border_style="green", padding=(0, 2)))


# ── Auth setup ────────────────────────────────────────────────────────────────

def setup_auth(cfg: dict) -> dict:
    console.print(Panel(
        Markdown(
            "## POESESSID Login (Optional)\n\n"
            "A **POESESSID** cookie gives access to the official PoE Trade API.\n"
            "All current features use poe.ninja and work without it.\n\n"
            "**How to get it:**\n"
            "1. Log into **pathofexile.com** in your browser\n"
            "2. Open DevTools → F12 → Application tab → Cookies\n"
            "3. Copy the value next to `POESESSID`\n\n"
            "Stored locally in `~/.steen_poe/config.json` — only sent to GGG servers."
        ),
        title="[bold cyan]Authentication[/bold cyan]",
        border_style="cyan", padding=(1, 2),
    ))
    try:
        sessid = Prompt.ask(
            "\n[cyan]POESESSID[/cyan] [dim](paste or Enter to skip)[/dim]",
            default="",
        ).strip()
    except (KeyboardInterrupt, EOFError):
        return cfg
    if sessid:
        cfg["poesessid"] = sessid
        save_config(cfg)
        console.print("[green]✓  POESESSID saved.[/green]")
    else:
        console.print("[dim]Skipped.[/dim]")
    return cfg


# ── League selector ───────────────────────────────────────────────────────────

def select_league(cfg: dict) -> str:
    current = cfg.get("league", "")
    leagues = fetch_leagues(cfg)
    t = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    t.add_column("#", style="bold white", width=4, justify="right")
    t.add_column("League", style="bold yellow")
    for i, lg in enumerate(leagues, 1):
        mark = " [bold green]← current[/bold green]" if lg == current else ""
        t.add_row(str(i), f"{lg}{mark}")
    console.print()
    console.print(Rule("[bold cyan]Select League[/bold cyan]", style="cyan"))
    console.print(Padding(t, (1, 2)))
    while True:
        try:
            choice = Prompt.ask(
                "[cyan]League[/cyan] [dim](number or name)[/dim]",
                default=current or leagues[0],
            ).strip()
        except (KeyboardInterrupt, EOFError):
            return current or leagues[0]
        if choice.isdigit() and 1 <= int(choice) <= len(leagues):
            league = leagues[int(choice) - 1]
        elif choice in leagues:
            league = choice
        else:
            console.print("[red]Invalid selection.[/red]")
            continue
        cfg["league"] = league
        save_config(cfg)
        return league


# ── Settings ──────────────────────────────────────────────────────────────────

def settings_menu(cfg: dict) -> dict:
    while True:
        console.print()
        console.print(Rule("[bold cyan]Settings[/bold cyan]", style="cyan"))
        cache_count = len(list(CACHE_DIR.glob("*.json"))) if CACHE_DIR.exists() else 0
        auth_status = "[bold green]✓ Set[/bold green]" if cfg.get("poesessid") else "[dim]Not set[/dim]"
        t = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        t.add_column("#", style="bold white", width=4, justify="right")
        t.add_column("", style="bold yellow")
        t.add_column("", style="dim")
        t.add_row("1", "Set / update POESESSID",  auth_status)
        t.add_row("2", "Change default league",    cfg.get("league", "not set"))
        t.add_row("3", "Clear cache",              f"{cache_count} file(s)")
        t.add_row("4", "Back",                     "")
        console.print(Padding(t, (1, 2)))
        try:
            choice = Prompt.ask("[cyan]Option[/cyan]", default="4").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if choice == "1":
            cfg = setup_auth(cfg)
        elif choice == "2":
            select_league(cfg)
        elif choice == "3":
            for f in CACHE_DIR.glob("*.json"):
                f.unlink()
            console.print(f"[green]✓  Cleared {cache_count} cache file(s).[/green]")
        elif choice == "4":
            break
    return cfg


# ── Help ──────────────────────────────────────────────────────────────────────

def print_help() -> None:
    console.print(Panel(
        Markdown("""## Steen POE Marketer — Help

### Modules
| # | Module | Description |
|---|---|---|
| 1 | Currency Analysis | Buy/sell prices vs ninja median — spot cheap buys |
| 2 | Arbitrage Finder | Whole-number trade margins between currency pairs |
| 3 | Divination Cards | Set costs, reward text, 7-day trend |
| 4 | Gem Flipper | Base → max level/quality profit margins |
| 5 | Economy Overview | Top-value items & movers across all categories |
| 6 | Stash Pricer | Enter item names to value your stash |

### Reading the data
- **7d** column — price change over the last 7 days (green = rising, red = falling)
- **Discount** (Currency Analysis) — negative = buying below median = opportunity
- **Spread** — difference between buy and sell price; tighter = more liquid market
- **ROI** (Gems) — profit as % of your upfront cost

### Export (after every module)
Type `csv`, `json`, or `html` at the export prompt.
Files are saved to the current directory.

### Login
A `POESESSID` cookie is optional — all poe.ninja features work without it.
Configure via **Settings (S)** from the main menu.

### Cache
Price data is cached for **15 minutes** in `~/.steen_poe/cache/`.
Clear it from Settings if you need fresh data immediately.

### Disclaimer
Data is sourced from **poe.ninja** (community price index).
Prices reflect median trade values — actual listings may vary.
Not affiliated with Grinding Gear Games.
"""),
        title="[bold cyan]Help[/bold cyan]",
        border_style="cyan", padding=(1, 2),
    ))


# ── Banner ────────────────────────────────────────────────────────────────────

BANNER_LINES = [
    ("bold bright_cyan",   "  ███████╗████████╗███████╗███████╗███╗   ██╗"),
    ("bold cyan",          "  ██╔════╝╚══██╔══╝██╔════╝██╔════╝████╗  ██║"),
    ("bold blue",          "  ███████╗   ██║   █████╗  █████╗  ██╔██╗ ██║"),
    ("bold bright_blue",   "  ╚════██║   ██║   ██╔══╝  ██╔══╝  ██║╚██╗██║"),
    ("bold magenta",       "  ███████║   ██║   ███████╗███████╗██║ ╚████║"),
    ("bold bright_magenta","  ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═══╝"),
    ("bold bright_yellow", ""),
    ("bold bright_yellow", "  ██████╗  ██████╗ ███████╗    ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗███████╗████████╗███████╗██████╗"),
    ("bold yellow",        "  ██╔══██╗██╔═══██╗██╔════╝    ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗"),
    ("bold white",         "  ██████╔╝██║   ██║█████╗      ██╔████╔██║███████║██████╔╝█████╔╝ █████╗     ██║   █████╗  ██████╔╝"),
    ("bold yellow",        "  ██╔═══╝ ██║   ██║██╔══╝      ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝     ██║   ██╔══╝  ██╔══██╗"),
    ("bold bright_yellow", "  ██║     ╚██████╔╝███████╗    ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗███████╗   ██║   ███████╗██║  ██║"),
    ("dim yellow",         "  ╚═╝      ╚═════╝ ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝"),
]


def print_banner() -> None:
    console.print()
    for style, line in BANNER_LINES:
        console.print(line, style=style)
    console.print()
    grid = Table.grid(expand=True)
    grid.add_column(justify="center")
    grid.add_row(Text("⚔️  Path of Exile Market Analysis Tool", style="bold white"))
    grid.add_row(Text(
        f"v{APP_VERSION}  ·  poe.ninja data  ·  Optional PoE login  ·  MIT Licence",
        style="dim white",
    ))
    console.print(Panel(grid, border_style="bright_cyan", padding=(0, 2)))
    console.print()


# ── Main menu ─────────────────────────────────────────────────────────────────

def main_menu(cfg: dict, league: str) -> None:
    while True:
        console.print()
        console.print(Rule(
            f"[bold cyan]Main Menu[/bold cyan]  [dim]League: [yellow]{league}[/yellow][/dim]",
            style="cyan",
        ))
        auth_dot = " [bold green]●[/bold green]" if cfg.get("poesessid") else ""
        t = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        t.add_column("#",  style="bold white", width=4, justify="right")
        t.add_column("",   style="bold yellow")
        t.add_column("",   style="dim", min_width=44)
        for row in [
            ("1", "Currency Analysis",  "Buy/sell spreads · discount vs median · 7-day trend"),
            ("2", "Arbitrage Finder",   "Profitable round-number trades between pairs"),
            ("3", "Divination Cards",   "Set costs · reward text · trend"),
            ("4", "Gem Flipper",        "Base → max level/quality profit margins"),
            ("5", "Economy Overview",   "Top-value items & movers across all categories"),
            ("6", "Stash Pricer",       "Type item names → get chaos values & total"),
            ("",  "",                   ""),
            ("L", "Change League",      f"Currently: {league}"),
            ("S", "Settings",           f"Auth{auth_dot} · Cache · League"),
            ("H", "Help",               "How to use each module"),
            ("Q", "Quit",               ""),
        ]:
            t.add_row(*row)
        console.print(Padding(t, (1, 2)))

        try:
            choice = Prompt.ask("[bold cyan]Select[/bold cyan]").strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye, Exile.[/dim]")
            break

        if choice in ("q", "/quit", "/exit"):
            console.print("[dim]Goodbye, Exile.[/dim]")
            break

        elif choice == "1":
            with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                          console=console, transient=True) as p:
                p.add_task("Fetching currency data…")
                data = run_currency_analysis(league, cfg)
            display_currency_analysis(data)
            prompt_export(data, "currency_analysis")

        elif choice == "2":
            with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                          console=console, transient=True) as p:
                p.add_task("Analysing arbitrage opportunities…")
                data = run_arbitrage(league, cfg)
            display_arbitrage(data)
            prompt_export(data, "arbitrage")

        elif choice == "3":
            with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                          console=console, transient=True) as p:
                p.add_task("Fetching divination card data…")
                data = run_div_cards(league, cfg)
            display_div_cards(data)
            prompt_export(data, "div_cards")

        elif choice == "4":
            with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                          console=console, transient=True) as p:
                p.add_task("Analysing gem margins…")
                data = run_gem_flipper(league, cfg)
            display_gem_flipper(data)
            prompt_export(data, "gem_flipper")

        elif choice == "5":
            overview = run_economy_overview(league, cfg)
            display_economy_overview(overview, league)

        elif choice == "6":
            data = run_stash_pricer(league, cfg)
            if data:
                display_stash_pricer(data)
                prompt_export([r for r in data if r["found"]], "stash_pricer")

        elif choice == "l":
            league = select_league(cfg)

        elif choice == "s":
            cfg = settings_menu(cfg)

        elif choice == "h":
            print_help()

        else:
            console.print("[red]Invalid selection — enter a number or letter.[/red]")


# ── Entry point ───────────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="steen_poe",
        description="Steen POE Marketer — Path of Exile market analysis.",
    )
    p.add_argument("-l", "--league", help="Start with this league (skip selection)")
    p.add_argument("--version", action="version", version=f"{APP_NAME} v{APP_VERSION}")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    cfg  = load_config()

    print_banner()

    # First-run welcome
    if not cfg:
        console.print(Panel(
            "[bold white]Welcome to Steen POE Marketer![/bold white]\n\n"
            "All features use [cyan]poe.ninja[/cyan] data — no login required.\n"
            "A POESESSID cookie is optional and can be added any time via Settings.\n",
            title="[bold cyan]First Run[/bold cyan]",
            border_style="cyan", padding=(1, 2),
        ))
        if Confirm.ask("[cyan]Set up POESESSID now?[/cyan]", default=False):
            cfg = setup_auth(cfg)
        else:
            save_config(cfg)

    # League selection
    if args.league:
        league = args.league
        cfg["league"] = league
        save_config(cfg)
    elif not cfg.get("league"):
        league = select_league(cfg)
    else:
        league = cfg["league"]
        console.print(
            f"[dim]League: [yellow]{league}[/yellow]  "
            "(change with [bold]L[/bold] in the menu)[/dim]\n"
        )

    main_menu(cfg, league)


if __name__ == "__main__":
    main()
