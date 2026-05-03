#!/usr/bin/env bash
# Steen POE Marketer — launcher for macOS / Linux
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Colours ───────────────────────────────────────────────────────────────────
R='\033[0;31m'; Y='\033[1;33m'; G='\033[0;32m'; C='\033[0;36m'; W='\033[1;37m'; N='\033[0m'

echo -e "${C}"
echo "  ███████╗████████╗███████╗███████╗███╗   ██╗  ██████╗  ██████╗ ███████╗"
echo "  ██╔════╝╚══██╔══╝██╔════╝██╔════╝████╗  ██║  ██╔══██╗██╔═══██╗██╔════╝"
echo "  ███████╗   ██║   █████╗  █████╗  ██╔██╗ ██║  ██████╔╝██║   ██║█████╗"
echo "  ╚════██║   ██║   ██╔══╝  ██╔══╝  ██║╚██╗██║  ██╔═══╝ ██║   ██║██╔══╝"
echo "  ███████║   ██║   ███████╗███████╗██║ ╚████║  ██║     ╚██████╔╝███████╗"
echo "  ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═══╝  ╚═╝      ╚═════╝ ╚══════╝"
echo -e "${Y}"
echo "  ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗███████╗████████╗███████╗██████╗"
echo "  ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗"
echo "  ██╔████╔██║███████║██████╔╝█████╔╝ █████╗     ██║   █████╗  ██████╔╝"
echo "  ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝     ██║   ██╔══╝  ██╔══██╗"
echo "  ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗███████╗   ██║   ███████╗██║  ██║"
echo "  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝"
echo -e "${N}"

# ── Python check ──────────────────────────────────────────────────────────────
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo -e "${R}[✗] Python 3 not found.${N}"
    echo -e "    Install from https://python.org or via your package manager."
    exit 1
fi

PY_VER=$("$PYTHON" -c "import sys; print(sys.version_info.major*10+sys.version_info.minor)")
if [ "$PY_VER" -lt 39 ]; then
    echo -e "${R}[✗] Python 3.9+ required (found $("$PYTHON" --version)).${N}"
    exit 1
fi
echo -e "${G}[✓] Python: $("$PYTHON" --version)${N}"

# ── Launch ────────────────────────────────────────────────────────────────────
exec "$PYTHON" "$SCRIPT_DIR/steen_poe.py" "$@"
