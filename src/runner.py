import subprocess
import os
from datetime import datetime
from .colors import PURPLE, GREEN, RED, YELLOW, BLUE, NC
from .models import ToolRun, session

def run_tool(tool_name: str, template: str, target: str, timeout: int = 3600):
    """Run a tool with live output and timeout handling."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = f"output/{tool_name}_{timestamp}"
    os.makedirs(out_dir, exist_ok=True)
    log_file = f"{out_dir}/live_output.log"
    cmd = template.format(target=target)

    print(f"\n{PURPLE}🚀 Starting {tool_name} on → {target}{NC}")
    print(f"{BLUE}📁 Output folder: {out_dir}{NC}\n")
    print(f"{YELLOW}───────────────────────────────────────────────────────{NC}")

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

        try:
            exit_code = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            print(f"\n{RED}⏰ Tool {tool_name} timed out after {timeout}s{NC}")
            return

        if exit_code == 0:
            print(f"\n{GREEN}✅ {tool_name} completed successfully!{NC}")
        else:
            print(f"\n{RED}⚠️  {tool_name} exited with code {exit_code}{NC}")

        # Save to database
        run = ToolRun(
            tool_name=tool_name,
            target=target,
            exit_code=exit_code,
            output_path=log_file
        )
        session.add(run)
        session.commit()
        return run

    except FileNotFoundError:
        print(f"\n{RED}❌ Tool '{tool_name}' not found in PATH!{NC}")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⏹️  Stopped by user{NC}")
        proc.kill()
    except Exception as e:
        print(f"\n{RED}❌ Error: {e}{NC}")
