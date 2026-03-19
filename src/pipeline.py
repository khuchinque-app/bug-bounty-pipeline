import yaml
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from .runner import run_tool
from .scope import ScopeValidator
from .notifications import notify
from .utils import validate_target

def run_pipeline(target, pipeline_name='full', scope_file=None,
                 output_dir=None, max_workers=3, config=None):
    """Execute a full pipeline with parallel phases."""
    target = validate_target(target)

    # Load pipeline definition
    with open('config/pipeline.yaml') as f:
        pipelines = yaml.safe_load(f)
    phases = pipelines.get(pipeline_name, [])
    if not phases:
        print(f"❌ Pipeline '{pipeline_name}' not found.")
        return

    # Scope validation
    if scope_file:
        validator = ScopeValidator(scope_file)
        if not validator.is_in_scope(target):
            print(f"❌ Target {target} is out of scope!")
            return

    # Create output directory
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    else:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"output/{target}_{pipeline_name}_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"🚀 Starting pipeline: {pipeline_name} on {target}")
    print(f"📁 Output: {output_dir}")
    print(f"{'='*60}\n")

    all_results = []
    for phase in phases:
        phase_name = phase['name']
        tools = phase['tools']
        print(f"\n=== {phase_name} ===")

        # Load tool commands from tools.yaml
        with open('config/tools.yaml') as f:
            tools_config = yaml.safe_load(f)

        # Prepare list of (name, command) tuples
        commands = []
        for t in tools:
            tool_name = t['name']
            tool_data = tools_config.get(tool_name)
            if not tool_data:
                print(f"⚠️  Tool {tool_name} not defined in tools.yaml, skipping.")
                continue
            command = tool_data['command']
            commands.append((tool_name, command))

        # Run tools in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_tool = {
                executor.submit(run_tool, name, cmd, target): name
                for name, cmd in commands
            }
            for future in as_completed(future_to_tool):
                tool_name = future_to_tool[future]
                try:
                    result = future.result()
                    if result and result.exit_code == 0:
                        all_results.append(result)
                        # Optional notification for critical findings
                        # (You could add a tag in tools.yaml)
                except Exception as e:
                    print(f"❌ Tool {tool_name} failed: {e}")

    print(f"\n🎉 Pipeline completed! Results in {output_dir}")
    return all_results
