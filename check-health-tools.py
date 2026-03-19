#!/usr/bin/env python3
"""
Bug Bounty Pipeline - System Checker
Verifies that all required tools are installed and accessible.
"""

import subprocess
import shutil
import sys
from typing import Dict, List, Tuple

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

# List of required tools with their version command (if any)
# Format: (command_name, version_flag, optional_display_name)
REQUIRED_TOOLS: List[Tuple[str, str, str]] = [
    ("subfinder", "-version", "subfinder"),
    ("assetfinder", "-h", "assetfinder"),  # assetfinder has no version flag, just -h
    ("amass", "-version", "amass"),
    ("findomain", "--version", "findomain"),
    ("httpx", "-version", "httpx"),
    ("gau", "--version", "gau"),
    ("waybackurls", "-h", "waybackurls"),
    ("katana", "-version", "katana"),
    ("hakrawler", "-h", "hakrawler"),
    ("linkfinder", "-h", "linkfinder"),   # symlinked script
    ("secretfinder", "-h", "secretfinder"), # symlinked script
    ("ffuf", "-V", "ffuf"),
    ("feroxbuster", "--version", "feroxbuster"),
    ("arjun", "-h", "arjun"),
    ("paramspider", "-h", "paramspider"),
    ("x8", "--help", "x8"),
    ("nuclei", "-version", "nuclei"),
    ("dalfox", "--version", "dalfox"),
    ("crlfuzz", "-h", "crlfuzz"),
    ("tplmap", "-h", "tplmap"),
    ("graphqlmap", "-h", "graphqlmap"),
    ("s3scanner", "-h", "s3scanner"),
    ("interlace", "-h", "interlace"),
    ("anew", "-h", "anew"),
    ("mantra", "-h", "mantra"),
    # Optional but recommended
    ("tmux", "-V", "tmux"),
]

def get_version(cmd: str, flag: str) -> str:
    """Run tool with version flag and return first line of output."""
    try:
        result = subprocess.run([cmd, flag], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Return first non-empty line
            for line in result.stdout.splitlines():
                if line.strip():
                    return line.strip()[:60]  # truncate long lines
        return "version unknown"
    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
        return "error"

def check_tool(name: str, version_flag: str, display: str) -> Dict:
    """Check if tool exists and get version."""
    path = shutil.which(name)
    if path:
        version = get_version(name, version_flag) if version_flag != "-h" else "N/A"
        return {"name": display, "installed": True, "path": path, "version": version}
    else:
        return {"name": display, "installed": False, "path": None, "version": None}

def print_summary(results: List[Dict]) -> None:
    """Print a formatted table of results."""
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}BUG BOUNTY PIPELINE - SYSTEM CHECK{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    # Determine column widths
    name_width = max(len(r["name"]) for r in results) + 2
    status_width = 12
    version_width = 40

    # Header
    print(f"{'Tool'.ljust(name_width)} {'Status'.ljust(status_width)} {'Version/Path'}")
    print("-" * (name_width + status_width + version_width + 2))

    all_installed = True
    for r in results:
        name = r["name"]
        if r["installed"]:
            status = f"{GREEN}✓ Installed{RESET}"
            version_info = r["version"] if r["version"] else r["path"]
        else:
            status = f"{RED}✗ Missing{RESET}"
            version_info = "not found"
            all_installed = False

        # Truncate version info if too long
        if len(version_info) > version_width:
            version_info = version_info[:version_width-3] + "..."

        print(f"{name.ljust(name_width)} {status.ljust(status_width)} {version_info}")

    print(f"\n{BOLD}{'='*60}{RESET}")
    if all_installed:
        print(f"{GREEN}All required tools are installed!{RESET}")
    else:
        print(f"{RED}Some tools are missing. Please install them using install.sh or manually.{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

def main() -> None:
    """Main entry point."""
    print(f"{BLUE}[*] Checking system for required tools...{RESET}")
    results = []
    for cmd, flag, display in REQUIRED_TOOLS:
        results.append(check_tool(cmd, flag, display))

    print_summary(results)

    # Exit code: 0 if all required installed, 1 otherwise
    required_only = [r for r in results if r["name"] != "tmux"]  # tmux is optional
    if all(r["installed"] for r in required_only):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
