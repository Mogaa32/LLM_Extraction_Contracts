from collections import defaultdict

location_data = defaultdict(lambda: defaultdict(dict))


def add_entry(entry):
    try:
        st = entry.get("ST")
        loc = entry.get("LOC NAME")
        eq = entry.get("EquipmentType")
        if not all([st, loc, eq]):
            print(f"⚠️ Skipping entry: {entry}")
            return
        charge = entry.get("Charge")
        if charge is not None:
            try:
                charge = float(charge)
            except (ValueError, TypeError):
                print(f"⚠️ Invalid charge: {entry}")
                charge = None

        location_data[st][loc][eq] = {
            "Charge": charge,
            "AgreementName": entry.get("AgreementName"),
            "AgreementType": entry.get("AgreementType"),
            "CarrierName": entry.get("CarrierName"),
            "EffectiveDate": entry.get("EffectiveDate"),
            "Notes": entry.get("Notes")
        }
    except Exception as e:
        print(f"⚠️ Unexpected error: {entry}, Error: {e}")
