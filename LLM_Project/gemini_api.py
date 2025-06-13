import json
import time
from setup import genai
from try_fix import try_fix_json

model = genai.GenerativeModel("gemini-1.5-flash")


def extract_structured_data(text, current_state=None, retries=3, delay=30):
    prompt = f"""
Your task is to meticulously extract logistics rate information from the provided text. The text may contain both unstructured paragraphs and structured tables (potentially in HTML or Markdown format).

The following text is from a freight contract table listing cities and rates.
States are listed once (like NC or SC) and apply to all cities below them until the next state is mentioned.

**Current State Context**: {current_state if current_state else "Not specified - look for state headers like 'NC TERRITORY'"}

**Overall Document Context (apply these if not explicitly overridden per entry):**
- **AgreementName**: "Carolina Custom Carrier Rate Sheet"
- **AgreementType**: "Rate Sheet"
- **CarrierName**: "Carolina Custom Carrier"
- **EffectiveDate**: "2019-06-05"

**Extraction Requirements (for each rate entry):**
Extract a JSON list of objects. Each object must represent a unique rate entry and contain the following fields:

- **ST**: The two-letter state abbreviation (e.g., 'NC', 'SC'). This is derived from territory headers (e.g., "NC TERRITORY"). If no state is specified in this chunk, use "{current_state}" if available. This is a mandatory field.
- **LOC NAME**: The full name of the location (e.g., 'ABERDEEN', 'CHARLOTTE'). This is a mandatory field.
- **EquipmentType**: The type of equipment (e.g., 'VAN', 'ST', 'TT', 'FLATBED', 'REEFER'). These are usually column headers. This is a mandatory field.
- **Charge**: The numerical price (float or integer) associated with the specific `LOC NAME` and `EquipmentType` combination. If multiple charges are listed for the same combination, identify the primary or most prominent one. This is a mandatory numerical field.
- **AgreementName**: (From overall context). Use `null` if not applicable or inferable.
- **AgreementType**: (From overall context). Use `null` if not applicable or inferable.
- **CarrierName**: (From overall context). Use `null` if not applicable or inferable.
- **EffectiveDate**: (From overall context). Format as `YYYY-MM-DD`. Use `null` if not applicable or inferable.
- **Notes**: Any specific notes or conditions related to the charge or entry. Use `null` if not found.

**State Detection Rules**:
1. If you see text like "NC TERRITORY" or "SC TERRITORY", extract the state abbreviation (NC, SC) and use it for all following entries.
2. If no state is specified in this chunk, use the provided current_state ("{current_state}") if available.
3. If no state can be determined, set ST to null (but this should be avoided if possible).

**Output Format**:
Return a dictionary with two keys:
- "entries": The extracted rate entries (same format as before)
- "current_state": The last detected state in this chunk (to be used for the next chunk)

Strictly output only a JSON object with these two keys. Do not include any additional text, explanations, or formatting outside the JSON object.

Example output:
```json
{{
    "entries": [
        {{
            "ST": "NC",
            "LOC NAME": "ABERDEEN",
            "EquipmentType": "VAN",
            "Charge": 210.00,
            "AgreementName": "Carolina Custom Carrier Rate Sheet",
            "AgreementType": "Rate Sheet",
            "CarrierName": "Carolina Custom Carrier",
            "EffectiveDate": "2019-06-05",
            "Notes": null
        }}
    ],
    "current_state": "NC"
}}

Input:
{text}
"""
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            if result.startswith("```json"):
                result = result.replace("```json", "").replace("```", "").strip()
            elif result.startswith("```"):
                result = result.replace("```", "").strip()
            
            # Expecting a dictionary now, not a list
            parsed = json.loads(result)
            if not isinstance(parsed, dict) or "entries" not in parsed:
                raise ValueError("Expected a dictionary with 'entries' key")
            return parsed
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON error: {e}")
            # Try to fix the JSON
            fixed = try_fix_json(result)
            if fixed:
                if isinstance(fixed, dict) and "entries" in fixed:
                    return fixed
                elif isinstance(fixed, list):
                    # If we get a list (old format), convert to new format
                    return {"entries": fixed, "current_state": current_state}
        except Exception as e:
            print(f"⚠️ Exception: {e}")
        time.sleep(delay)
    return {"entries": [], "current_state": current_state}
