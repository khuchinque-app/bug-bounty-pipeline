# main.py
import os
import sys
from tools_config import TOOLS, FULL_PIPELINE

# ==================== COLORS ====================
RED    = '\033[0;31m'
GREEN  = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE   = '\033[0;34m'
CYAN   = '\033[0;36m'
PURPLE = '\033[0;35m'
NC     = '\033[0m'

# ==================== BANNER ====================
def print_banner():
    banner = f"""
{CYAN}╔══════════════════════════════════════════════════════════════╗
{CYAN}║{NC}               {PURPLE}chinque-bug-bounty v1{NC}                      {CYAN}║
{CYAN}╠══════════════════════════════════════════════════════════════╣
{CYAN}║{NC}   Fast • Modular • Colorful • Real-time Tool Launcher     {CYAN}║
{CYAN}╚══════════════════════════════════════════════════════════════╝{NC}
"""
    print(banner)

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

# ==================== MAIN MENU (Full Scan = 0) ====================
def show_main_menu():
    clear()
    print_banner()
    print(f"{YELLOW}=== MAIN MENU - Choose Category ==={NC}\n")

    categories = list(TOOLS.keys())
    for i, cat in enumerate(categories, 1):
        print(f"{BLUE}{i}.{NC} {cat}")

    print(f"{BLUE}0.{NC} {PURPLE}Full Scan (Full Recon Pipeline){NC}")
    print()

    choice = input(f"{YELLOW}Choose number: {NC}").strip()

    if choice == "0":
        return "full_pipeline"

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(categories):
            return categories[idx]
    except:
        pass

    print(f"{RED}[!] Invalid choice. Use Ctrl + C to exit.{NC}")
    input(f"\n{GREEN}Press Enter...{NC}")
    return None

# ==================== TOOL MENU (0 = Back) ====================
def choose_tool(category: str):
    tools_list = TOOLS[category]
    clear()
    print_banner()
    print(f"{CYAN}=== {category} ==={NC}\n")

    for i, tool in enumerate(tools_list, 1):
        print(f"{BLUE}{i}.{NC} {tool['name']} {YELLOW}→{NC} {tool['desc']}")

    print(f"{BLUE}0.{NC} {GREEN}← Back to Main Menu{NC}")
    print()

    choice = input(f"{YELLOW}Choose tool number: {NC}").strip()

    if choice == "0":
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(tools_list):
            return tools_list[idx]
    except:
        pass
    print(f"{RED}[!] Invalid tool.{NC}")
    input(f"\n{GREEN}Press Enter...{NC}")
    return "retry"

# ==================== MAIN LOOP (Anti-Exit + Clean Ctrl+C) ====================
if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    print(f"{GREEN}Press Ctrl + C anytime to exit the launcher.{NC}\n")

    try:
        while True:
            selection = show_main_menu()

            if selection == "full_pipeline":
                target = input(f"\n{BLUE}Enter target (http://localhost:3010 or domain): {NC}").strip()
                if target:
                    from full_pipeline import run_full_pipeline
                    run_full_pipeline(target)
                input(f"\n{GREEN}Press Enter to return to menu...{NC}")
                continue

            if selection is None:
                continue

            # Normal category flow
            while True:
                tool = choose_tool(selection)
                if tool is None:
                    break
                if tool == "retry":
                    continue

                target = input(f"\n{BLUE}Enter target: {NC}").strip()
                if not target:
                    continue

                from runner import run_tool
                run_tool(tool['name'], tool['template'], target)

                print(f"\n{GREEN}✅ Tool finished! Press Enter for next tool...{NC}")
                input()

    except KeyboardInterrupt:
        print(f"\n{GREEN}👋 Exited cleanly with Ctrl + C. See you next time!{NC}")
        sys.exit(0)
