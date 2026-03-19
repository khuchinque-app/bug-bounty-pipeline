import re
from urllib.parse import urlparse

def validate_target(target):
    """Sanitize and validate target string."""
    # Remove dangerous characters
    if re.search(r'[;&|`$]', target):
        raise ValueError("Target contains unsafe characters")
    # Ensure scheme for proper parsing
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    parsed = urlparse(target)
    # Return netloc (domain) or path if netloc empty (e.g., localhost)
    return parsed.netloc or parsed.path
