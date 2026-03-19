import os
import yaml
import pyfiglet
from .colors import GREEN, LIME, DARK_GREEN, NC, YELLOW, BLUE, CYAN, RED, PURPLE
from .runner import run_tool
from .pipeline import run_pipeline

def print_banner():
    try:
        main_banner = pyfiglet.figlet_format("CHINQUE-SCAN", font="dosrebel")
    except pyfiglet.FontNotFound:
        # Fallback static banner
        main_banner = r"""
  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗ ██╗   ██╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗
 ██╔════╝██║  ██║██║████╗  ██║██╔═══██╗██║   ██║██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║
 ██║     ███████║██║██╔██╗ ██║██║   ██║██║   ██║█████╗      ███████╗██║     ███████║██╔██╗ ██║
 ██║     ██╔══██║██║██║╚██╗██║██║▄▄ ██║██║   ██║██╔══╝      ╚════██║██║     ██╔══██║██║╚██╗██║
 ╚██████╗██║  ██║██║██║ ╚████║╚██████╔╝╚██████╔╝███████╗    ███████║╚██████╗██║  ██║██║ ╚████║
  ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
"""

    # Color each line green
    colored_main = ""
    for line in main_banner.splitlines():
        colored_main += f"{GREEN}{line}{NC}\n"

    # Borders (inner width = 58 characters of '═')
    border_top = f"{LIME}╔══════════════════════════════════════════════════════════════╗{NC}"
    border_bottom = f"{LIME}╚══════════════════════════════════════════════════════════════╝{NC}"

    # New subtitle with exit hint
    subtitle_text = "bug-bounty-pipeline _ full scan 2.0v - exit (ctrl + z or c)"
    inner_width = 58
    subtitle_len = len(subtitle_text)
    left_pad = (inner_width - subtitle_len) // 2
    right_pad = inner_width - subtitle_len - left_pad
    centered_subtitle = f"{DARK_GREEN}{' ' * left_pad}{subtitle_text}{' ' * right_pad}{NC}"
    subtitle_line = f"{LIME}║{centered_subtitle}║"

    print(border_top)
    print(colored_main, end='')
    print(subtitle_line)
    print(border_bottom)
    print()

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def interactive_menu():
    # Load tools from YAML
    with open('config/tools.yaml') as f:
        tools_config = yaml.safe_load(f)

    TOOLS = {}
    for tool_name, data in tools_config.items():
        cat = data.get('category', 'Other')
        TOOLS.setdefault(cat, []).append({
            'name': tool_name,
            'desc': data.get('desc', ''),
            'template': data['command']
        })

    categories = sorted(TOOLS.keys())

    while True:
        clear()
        print_banner()
        print(f"{YELLOW}=== MAIN MENU - Choose Category ==={NC}\n")
        for i, cat in enumerate(categories, 1):
            print(f"{BLUE}{i}.{NC} {cat}")
        # Add Full Scan as option 0 (or as an extra category)
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
