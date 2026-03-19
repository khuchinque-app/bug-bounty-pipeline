import os
import yaml
from .colors import PURPLE, GREEN, YELLOW, BLUE, CYAN, RED, NC
from .runner import run_tool
from .pipeline import run_pipeline

def print_banner():
    banner = f"""
{CYAN}╔══════════════════════════════════════════════════════════════╗
{CYAN}║{NC}               {PURPLE}chinque-bug-bounty v2{NC}                      {CYAN}║
{CYAN}╠══════════════════════════════════════════════════════════════╣
{CYAN}║{NC}   Fast • Modular • Colorful • Real-time Tool Launcher     {CYAN}║
{CYAN}╚══════════════════════════════════════════════════════════════╝{NC}
"""
    print(banner)

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def interactive_menu():
    # Load tools from YAML
    with open('config/tools.yaml') as f:
        tools_config = yaml.safe_load(f)

    # Organize by category
    TOOLS = {}
    for tool_name, data in tools_config.items():
        cat = data.get('category', 'Other')
        TOOLS.setdefault(cat, []).append({
            'name': tool_name,
            'desc': data.get('desc', ''),
            'template': data['command']
        })

    # Sort categories naturally (by the numeric prefix)
    categories = sorted(TOOLS.keys())

    while True:
        clear()
        print_banner()
        print(f"{YELLOW}=== MAIN MENU - Choose Category ==={NC}\n")
        for i, cat in enumerate(categories, 1):
            print(f"{BLUE}{i}.{NC} {cat}")
        print(f"{BLUE}0.{NC} {PURPLE}Full Scan (Full Recon Pipeline){NC}")
        print()

        choice = input(f"{YELLOW}Choose number: {NC}").strip()

        if choice == "0":
            target = input(f"\n{BLUE}Enter target: {NC}").strip()
            if target:
                run_pipeline(target, pipeline_name='full')
            input(f"\n{GREEN}Press Enter to return to menu...{NC}")
            continue

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                category = categories[idx]
            else:
                print(f"{RED}[!] Invalid choice.{NC}")
                input(f"\n{GREEN}Press Enter...{NC}")
                continue
        except:
            print(f"{RED}[!] Invalid choice.{NC}")
            input(f"\n{GREEN}Press Enter...{NC}")
            continue

        # Show tools in the chosen category
        while True:
            clear()
            print_banner()
            print(f"{CYAN}=== {category} ==={NC}\n")
            tools = TOOLS[category]
            for i, tool in enumerate(tools, 1):
                print(f"{BLUE}{i}.{NC} {tool['name']} {YELLOW}→{NC} {tool['desc']}")
            print(f"{BLUE}0.{NC} {GREEN}← Back{NC}\n")

            tool_choice = input(f"{YELLOW}Choose tool: {NC}").strip()
            if tool_choice == "0":
                break
            try:
                tidx = int(tool_choice) - 1
                if 0 <= tidx < len(tools):
                    tool = tools[tidx]
                    target = input(f"\n{BLUE}Enter target: {NC}").strip()
                    if target:
                        run_tool(tool['name'], tool['template'], target)
                    input(f"\n{GREEN}Press Enter to continue...{NC}")
                else:
                    print(f"{RED}[!] Invalid choice.{NC}")
                    input(f"\n{GREEN}Press Enter...{NC}")
            except:
                print(f"{RED}[!] Invalid choice.{NC}")
                input(f"\n{GREEN}Press Enter...{NC}")
