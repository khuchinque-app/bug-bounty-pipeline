# tools_config.py
TOOLS = {
    "1. Subdomain Enumeration": [
        {"name": "subfinder", "template": "subfinder -d {target} -silent", "desc": "Fast passive subdomain finder"},
        {"name": "assetfinder", "template": "assetfinder --subs-only {target}", "desc": "Asset + subdomain finder"},
        {"name": "amass", "template": "amass enum -passive -d {target}", "desc": "OWASP Amass (passive)"},
        {"name": "findomain", "template": "findomain -t {target} -q", "desc": "Findomain subdomain enum"},
        {"name": "httpx", "template": "httpx -u {target} -silent", "desc": "Live host probe"},
    ],
    "2. URL Collection & Crawling": [
        {"name": "gau", "template": "gau {target} --subs", "desc": "GetAllUrls from archives"},
        {"name": "waybackurls", "template": "echo {target} | waybackurls", "desc": "Wayback machine URLs"},
        {"name": "katana", "template": "katana -u {target} -silent -jc -kf all -aff", "desc": "Modern web crawler"},
        {"name": "hakrawler", "template": "echo {target} | hakrawler -subs -plain", "desc": "Hakrawler"},
    ],
    "3. JavaScript Analysis": [
        {"name": "linkfinder", "template": "linkfinder -i {target} -o cli", "desc": "Extract endpoints (use JS URL)"},
        {"name": "secretfinder", "template": "secretfinder -i {target} -o cli", "desc": "Find secrets in JS (use JS URL)"},
        {"name": "mantra", "template": "mantra {target}", "desc": "Mantra JS secret hunter"},
    ],
    "4. Directory & Parameter Discovery": [
        {"name": "ffuf", "template": "ffuf -u {target}/FUZZ -w wordlists/directory-list-2.3-medium.txt -t 50 -ac", "desc": "Fast directory brute"},
        {"name": "feroxbuster", "template": "feroxbuster -u {target} -w wordlists/directory-list-2.3-medium.txt -t 50", "desc": "Recursive directory brute"},
        {"name": "arjun", "template": "arjun -u {target} -oT arjun_params.txt", "desc": "Hidden parameter finder"},
        {"name": "paramspider", "template": "paramspider -d {target} -l high", "desc": "Parameter spider"},
        {"name": "x8", "template": "x8 -u {target}", "desc": "Parameter fuzzer"},
    ],
    "5. Vulnerability Scanning": [
        {"name": "nuclei", "template": "nuclei -u {target} -t ~/nuclei-templates/ -severity low,medium,high,critical", "desc": "Nuclei template scanner"},
        {"name": "dalfox", "template": "dalfox url {target}", "desc": "Powerful XSS scanner"},
        {"name": "crlfuzz", "template": "crlfuzz -u {target}", "desc": "CRLF injection tester"},
    ],
    "6. API & GraphQL Testing": [
        {"name": "graphqlmap", "template": "graphqlmap -u {target}", "desc": "GraphQL mapping (use /graphql endpoint)"},
    ],
    "7. Cloud Misconfiguration": [
        {"name": "s3scanner", "template": "s3scanner -bucket {target}", "desc": "S3 bucket checker"},
    ],
}
# ====================== FULL PIPELINE CONFIG ======================
# Add / remove / reorder phases here — super easy!
FULL_PIPELINE = [
    {"phase": "1. Subdomain Enumeration", "name": "subfinder", "template": "subfinder -d {target} -silent"},
    {"phase": "2. URL Collection & Crawling", "name": "katana", "template": "katana -u {target} -silent -jc -kf all -aff"},
    {"phase": "3. JavaScript Analysis", "name": "linkfinder", "template": "linkfinder -i {target} -o cli"},
    {"phase": "4. Directory Bruteforcing", "name": "ffuf", "template": "ffuf -u {target}/FUZZ -w wordlists/directory-list-2.3-medium.txt -t 50 -ac"},
    {"phase": "5. Parameter Discovery", "name": "arjun", "template": "arjun -u {target}"},
    {"phase": "6. Vulnerability Scanning", "name": "nuclei", "template": "nuclei -u {target} -t ~/nuclei-templates/ -severity low,medium,high,critical"},
    {"phase": "7. API & GraphQL Testing", "name": "graphqlmap", "template": "graphqlmap -u {target}"},
    {"phase": "8. Cloud Misconfiguration", "name": "s3scanner", "template": "s3scanner -bucket {target}"},
]
# ====================== FULL PIPELINE CONFIG ======================
# Add / remove / reorder phases here — super easy!
FULL_PIPELINE = [
    {"phase": "1. Subdomain Enumeration", "name": "subfinder", "template": "subfinder -d {target} -silent"},
    {"phase": "2. URL Collection & Crawling", "name": "katana", "template": "katana -u {target} -silent -jc -kf all -aff"},
    {"phase": "3. JavaScript Analysis", "name": "linkfinder", "template": "linkfinder -i {target} -o cli"},
    {"phase": "4. Directory Bruteforcing", "name": "ffuf", "template": "ffuf -u {target}/FUZZ -w wordlists/directory-list-2.3-medium.txt -t 50 -ac"},
    {"phase": "5. Parameter Discovery", "name": "arjun", "template": "arjun -u {target}"},
    {"phase": "6. Vulnerability Scanning", "name": "nuclei", "template": "nuclei -u {target} -t ~/nuclei-templates/ -severity low,medium,high,critical"},
    {"phase": "7. API & GraphQL Testing", "name": "graphqlmap", "template": "graphqlmap -u {target}"},
    {"phase": "8. Cloud Misconfiguration", "name": "s3scanner", "template": "s3scanner -bucket {target}"},
]
