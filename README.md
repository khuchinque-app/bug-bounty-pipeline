# 🕵️ Bug Bounty Pipeline (Enhanced)

for those who are very lazy and one to run a single command to all
A professional, modular automation framework for bug bounty reconnaissance and vulnerability scanning. Built with safety, scalability, and ease‑of‑use in mind.

## ✨ Features

- **Interactive menu** – quick tool selection (easy menu - auto save to folder)
- **CLI mode** – for automation and CI/CD integration (`python3 main.py <target> ...`)
- **Scope validation** – integrates `goodfaith` to prevent out‑of‑scope scans
- **Parallel execution** – run multiple tools simultaneously per phase
- **Result persistence** – stores all outputs in SQLite for later querying
- **Notification system** – Slack/Discord alerts for critical findings
- **YAML configuration** – easily add/modify tools and pipelines
- **Docker support** – reproducible environment

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
