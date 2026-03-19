import subprocess
import os
from datetime import datetime
from colors import PURPLE, GREEN, RED, YELLOW, BLUE, NC

def run_tool(tool_name: str, template: str, target: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = f"output/{tool_name}_{timestamp}"
    os.makedirs(out_dir, exist_ok=True)
    log_file = f"{out_dir}/live_output.log"

    print(f"\n{PURPLE}🚀 Starting {tool_name} on → {target}{NC}")
    print(f"{BLUE}📁 Output folder: {out_dir}{NC}\n")
    print(f"{YELLOW}───────────────────────────────────────────────────────{NC}")

    cmd = template.format(target=target)

    try:
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        with open(log_file, "w") as f:
            for line in proc.stdout:
                print(line, end="", flush=True)
                f.write(line)

        proc.wait()

        if proc.returncode == 0:
            print(f"\n{GREEN}✅ {tool_name} completed successfully!{NC}")
        else:
            print(f"\n{RED}⚠️  {tool_name} exited with code {proc.returncode}{NC}")

    except FileNotFoundError:
        print(f"\n{RED}❌ Tool '{tool_name}' not found in PATH!{NC}")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⏹️  Stopped by user (Ctrl+C){NC}")
    except Exception as e:
        print(f"\n{RED}❌ Error: {e}{NC}")
