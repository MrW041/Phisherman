import re
from urllib.parse import urlparse, urlunparse

def normalize_url(raw_url):
    """
    Standardizes a single URL string.
    - Defeats basic obfuscation (hxxps, zero-width spaces)
    - Lowercases scheme/domain
    - Removes default ports
    - Standardizes empty paths
    """
    # 1. Pre-Clean: Remove zero-width spaces often used in phishing
    # (e.g., the invisible space in 'citi​zen-bank')
    clean_url = re.sub(r'[\u200B-\u200D\uFEFF]', '', raw_url)
    
    # 2. Pre-Clean: Fix malicious schemes BEFORE parsing
    clean_url = re.sub(r'^hxxps', 'https', clean_url, flags=re.IGNORECASE)
    clean_url = re.sub(r'^hxxp', 'http', clean_url, flags=re.IGNORECASE)

    # NEW: Fix defanged dots (e.g., [.] or (.) -> .)
    clean_url = clean_url.replace('[.]', '.')
    clean_url = clean_url.replace('(', '.').replace(')', '.')
    
    # If it starts with www but has no scheme, add http:// so urlparse works
    if clean_url.lower().startswith('www.'):
        clean_url = 'http://' + clean_url

    try:
        # 3. Parse the URL (now that it's clean)
        parsed = urlparse(clean_url)
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc 
        port = parsed.port
                 

        final_netloc = netloc.lower() if netloc else ""
        
        if port:
            if not ((scheme == 'http' and port == 80) or 
                    (scheme == 'https' and port == 443)):
                final_netloc += f":{port}"

        # 4. Reconstruct
        normalized = urlunparse((
            scheme, 
            final_netloc, 
            parsed.path, 
            parsed.params, 
            parsed.query, 
            parsed.fragment
        ))
        
        # 5. Standardize empty path
        if normalized.endswith(final_netloc) and final_netloc:
             normalized += '/'
             
        return normalized

    except Exception as e:
        return clean_url