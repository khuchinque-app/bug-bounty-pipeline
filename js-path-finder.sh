# Install CeWL first
sudo apt install cewl

# Generate wordlist from target website
cewl https://example.com -d 2 -m 5 -w custom_wordlist.txt

curl -s https://example.com/app.js | grep -oE '["'"'"'](/[a-zA-Z0-9_/-]+)["'"'"']' | tr -d '"'"'"' | sort -u > js_paths.txt
