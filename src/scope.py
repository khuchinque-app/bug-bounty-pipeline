import json
import logging
import re
from urllib.parse import urlparse

# Try to import goodfaith with fallback
try:
    from goodfaith import ScopeValidator as GFValidator
    GOODFAITH_AVAILABLE = True
except ImportError:
    try:
        from goodfaith import Validator as GFValidator
        GOODFAITH_AVAILABLE = True
    except ImportError:
        try:
            from goodfaith import GoodFaith as GFValidator
            GOODFAITH_AVAILABLE = True
        except ImportError:
            GOODFAITH_AVAILABLE = False
            logging.warning("goodfaith not installed or incompatible. Scope validation disabled.")

class ScopeValidator:
    def __init__(self, scope_file):
        with open(scope_file) as f:
            self.scope_data = json.load(f)
        if GOODFAITH_AVAILABLE:
            try:
                self.validator = GFValidator(self.scope_data)
            except Exception as e:
                logging.error(f"Failed to initialize goodfaith validator: {e}")
                self.validator = None
        else:
            self.validator = None

    def is_in_scope(self, target):
        if self.validator is not None:
            try:
                if not target.startswith(('http://', 'https://')):
                    target = 'http://' + target
                return self.validator.validate(target)
            except Exception as e:
                logging.error(f"goodfaith validation error: {e}")

        # Fallback simple scope check
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        parsed = urlparse(target)
        domain = parsed.netloc or parsed.path

        for d in self.scope_data.get('domains', []):
            if domain == d or domain.endswith('.' + d):
                return True
        for inc in self.scope_data.get('include', []):
            pattern = inc.replace('.', r'\.').replace('*', r'.*')
            if re.match(pattern, domain):
                return True
        for exc in self.scope_data.get('exclude', []):
            pattern = exc.replace('.', r'\.').replace('*', r'.*')
            if re.match(pattern, domain):
                return False
        return False
