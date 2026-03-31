import re
import unicodedata
import os
import html



# --- 1. Global Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYWORDS_FILE = os.path.join(BASE_DIR, "critical_keywords.txt")

# Load keywords once at the top level
if os.path.exists(KEYWORDS_FILE):
    with open(KEYWORDS_FILE, "r") as f:
        CRITICAL_KEYWORDS = [i.strip().lower() for i in f if i.strip()]
else:
    CRITICAL_KEYWORDS = []

# --- 2. Define fix_broken FIRST ---
def fix_broken(text):
    """Scans for broken keywords with spacing (e.g., 'p a y' -> 'pay')"""
    for word in CRITICAL_KEYWORDS:
        pattern_parts = [re.escape(char) for char in word]
        separator = r'[\s._-]*' 
        regex_pattern = r'\b' + separator.join(pattern_parts) + r'\b'
        
        if re.search(regex_pattern, text):
             text = re.sub(regex_pattern, word, text)
    return text

# --- 3. Define norm_txt SECOND ---
def norm_txt_1(raw_text):
    if not isinstance(raw_text, str):
        return ""

    # A. Decode HTML Entities FIRST (Turns &#86;&#69; into VE)
    text = html.unescape(raw_text)
    text = text.lower()

    # B. Symbol & Homoglyph Mapping FIRST (Save them from ASCII deletion)
    leet_map = {
        '@': 'a', '4': 'a', '0': 'o', '1': 'i', '!': 'i', 
        '3': 'e', '5': 's', '$': 's', '7': 't', '9': 'g', '8': 'b', '€': 'e',
        'һ': 'h', 'і': 'i', 'а': 'a', 'с': 'c', 'е': 'e', 'о': 'o', 'р': 'p', 'х': 'x' 
    }
    text = text.translate(str.maketrans(leet_map))

    # C. NOW do Unicode & ASCII Ignore (to strip genuine garbage safely)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    # D. URL Tokenization
    text = re.sub(r'\b(?:https?|hxxps?|www)\S+', ' url_token ', text)

    # E. Clean Non-Alphanumeric (Removed $ and £ since we don't need them anymore)
    text = re.sub(r'[^a-z0-9\s!?_]', ' ', text) 

    # F. Call fix_broken
    text = fix_broken(text)

    # G. Collapse Whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text