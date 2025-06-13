import json
import re

def try_fix_json(bad_json_str):
    try:
        # First try to parse as is
        try:
            return json.loads(bad_json_str)
        except json.JSONDecodeError:
            pass
            
        # Try to find either dictionary or array start
        dict_match = re.search(r'\{', bad_json_str)
        array_match = re.search(r'\[', bad_json_str)
        
        if dict_match and (not array_match or dict_match.start() < array_match.start()):
            # Treat as dictionary
            start_index = dict_match.start()
            bad_json_str = bad_json_str[start_index:]
            if not bad_json_str.strip().endswith('}'):
                bad_json_str += '}'
        elif array_match:
            # Treat as array
            start_index = array_match.start()
            bad_json_str = bad_json_str[start_index:]
            if not bad_json_str.strip().endswith(']'):
                bad_json_str += ']'
        
        # Clean up common issues
        bad_json_str = re.sub(r',(\s*[}\]])', r'\1', bad_json_str)  # Trailing commas
        bad_json_str = re.sub(r'([{\[])\s*:', r'\1', bad_json_str)  # Misplaced colons
        
        return json.loads(bad_json_str)
    except Exception as e:
        print(f"⚠️ Failed to fix JSON: {e}")
        return None