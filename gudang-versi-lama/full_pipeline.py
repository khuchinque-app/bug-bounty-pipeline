import os
from datetime import datetime
from runner import run_tool
from colors import PURPLE, GREEN, BLUE, NC, YELLOW
from tools_config import FULL_PIPELINE   

def run_full_pipeline(target: str):
    clean = target.replace("http://", "").replace("https://", "").split("/")[0].replace(":", "_").replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pipeline_dir = f"output/{clean}_FULL_PIPELINE_{timestamp}"
    os.makedirs(pipeline_dir, exist_ok=True)

    print(f"\n{PURPLE}🚀 STARTING FULL RECON PIPELINE on {target}{NC}")
    print(f"{BLUE}📁 Pipeline folder: {pipeline_dir}{NC}\n")
    print(f"{YELLOW}───────────────────────────────────────────────────────{NC}")

    for phase in FULL_PIPELINE:
        print(f"\n{GREEN}=== {phase['phase']} ==={NC}")
        run_tool(phase['name'], phase['template'], target)

    print(f"\n{GREEN}🎉 FULL PIPELINE COMPLETED!{NC}")
    print(f"{BLUE}Check all results in: {pipeline_dir}{NC}")
