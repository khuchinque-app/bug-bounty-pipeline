#!/usr/bin/env python3
"""
Main entry point. Usage:
    python3 main.py               # Interactive menu
    python3 main.py <target> ...  # CLI mode
"""
import sys
from src.cli import main

if __name__ == "__main__":
    sys.exit(main())
