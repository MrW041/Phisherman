from ingest import ingest_input
from normal import norm_txt_1
from url_extract import extract_urls
import json

class ppl1:
    #pipeline 1

    def __init__(self):
        print("Pipeline initialized...")

    def run(self, raw_text, user_id):
        
        # --- LAYER 0: INGESTION ---
        try:
            packet = ingest_input(raw_text, user_id)
            packet['history'].append("layer0_complete")
        except Exception as e:
            return {"error": f"Layer 0 Failed: {str(e)}"}

        # --- LAYER 1 & 2 (Placeholder) ---
        # Future: packet = layer1_check(packet)


        
        # --- LAYER 3: NORMALIZATION ---
        # We pass the 'raw_text' from the packet into the normalizer
    
        clean_text = norm_txt_1(packet['raw_text'])
        
        # Update the packet with the new data
        packet['normalized_text'] = clean_text
        packet['history'].append("layer1.1_complete")
        
        

        # 3. LAYER 4: URL Extraction
        # We pass the WHOLE packet so it can read 'raw_text' and write to 'url'
        packet = extract_urls(packet)
        packet['history'].append("layer2_complete")
        packet["history"].append("layer2.1_complete")


        #completion of phase 1
        packet["history"].append("phase1_complete")


        # --- RETURN RESULT ---
        return packet