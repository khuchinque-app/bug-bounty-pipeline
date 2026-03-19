#!/usr/bin/env python3
import argparse
import sys
import os
import yaml
from .menu import interactive_menu
from .pipeline import run_pipeline

def load_config():
    with open('config/config.yaml') as f:
        return yaml.safe_load(f)

def main():
    # If no arguments, run interactive menu
    if len(sys.argv) == 1:
        interactive_menu()
        return 0

    parser = argparse.ArgumentParser(description='Bug Bounty Pipeline')
    parser.add_argument('target', help='Target domain or URL')
    parser.add_argument('--pipeline', choices=['full', 'recon', 'scan'], default='full',
                        help='Pipeline to run')
    parser.add_argument('--scope', help='JSON scope file for validation')
    parser.add_argument('--output', help='Output directory (default: auto)')
    parser.add_argument('--parallel', type=int, default=3,
                        help='Maximum parallel tools per phase')
    args = parser.parse_args()

    config = load_config()
    run_pipeline(
        target=args.target,
        pipeline_name=args.pipeline,
        scope_file=args.scope,
        output_dir=args.output,
        max_workers=args.parallel,
        config=config
    )
    return 0
