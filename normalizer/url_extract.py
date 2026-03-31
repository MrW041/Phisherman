import re
from utils_url import normalize_url

def extract_urls(packet):
    """
    Layer 4: URL Extraction
    - Extracts raw URLs
    - Normalizes them
    - Stores BOTH as a dictionary
    """
    raw_text = packet.get("raw_text", "")
    
    # 1. Extract Raw
    url_pattern = r'(?:https?://|hxxps?://|www\.)\S+'
    raw_matches = re.findall(url_pattern, raw_text,flags=re.IGNORECASE)
    
    url_data_list = []
    
    # 2. Process each URL
    for raw in raw_matches:
        clean = normalize_url(raw)
        
        # Store both together
        url_entry = {
            "raw": raw,
            "clean": clean,
            "obfuscated": raw != clean  # Boolean flag: Did they try to hide it?
        }
        url_data_list.append(url_entry)
    
    # 3. Update Packet
    packet["urls"] = url_data_list    
    return packet