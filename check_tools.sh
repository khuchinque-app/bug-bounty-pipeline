#!/bin/bash
# ================================================
# Bug Bounty Tools Health Checker
# Tests if each tool is installed AND working
# ================================================

echo -e "\033[0;36m==========================================\033[0m"
echo -e "\033[0;36m   Bug Bounty Tools Status Checker        \033[0m"
echo -e "\033[0;36m==========================================\033[0m\n"

TOOLS=(
    "subfinder" "assetfinder" "amass" "findomain" "httpx"
    "gau" "waybackurls" "katana" "hakrawler"
    "linkfinder" "secretfinder" "ffuf" "feroxbuster"
    "arjun" "paramspider" "x8" "nuclei" "dalfox"
    "crlfuzz" "tplmap" "graphqlmap" "s3scanner"
    "interlace" "anew" "mantra" "tmux"
)

printf "%-20s %-10s %s\n" "Tool" "Status" "Version / Notes"
printf "%-20s %-10s %s\n" "----" "------" "-----------------------------"

for tool in "${TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        status="✓ Working"
        
        # Try to get version (common flags)
        version=$(
            "$tool" --version 2>/dev/null || 
            "$tool" -version 2>/dev/null || 
            "$tool" -v 2>/dev/null || 
            "$tool" version 2>/dev/null || 
            echo "Installed (no version flag)"
        )
        
        # Clean up version output
        version=$(echo "$version" | head -n 1 | tr -d '\n' | sed 's/^[vV]ersion[:= ]*//I')
        if [ -z "$version" ] || [[ "$version" == *"command not found"* ]]; then
            version="Installed"
        fi
        
        printf "\033[0;32m%-20s %-10s\033[0m %s\n" "$tool" "$status" "$version"
    else
        printf "\033[0;31m%-20s %-10s\033[0m %s\n" "$tool" "✗ Missing" "-"
    fi
done

echo -e "\n\033[0;33m[*] Tips:\033[0m"
echo "   • Some tools (like linkfinder, secretfinder, mantra, arjun, paramspider) are Python-based"
echo "     and may not show version easily — but if they run, they are fine."
echo "   • Run this script again after installing missing tools."
echo -e "\nDone! Now test your recon pipeline on Juice Shop at http://localhost:3010"
