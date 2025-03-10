

import json
from pathlib import Path

# Function to transform JSON structure
def transform_json(self,json_path):
    # This function convert json dict to hjson one
    # Args: json_path
    self.json_path=json_path

    mappings = {
        "struct_head": {
            "d": "dip_column",
            "dd": "dipdir_column",
            "sf": "description_column",
            "otype": "orientation_type",
            "bo": "overturned_column",
            "gi": "objectid_column",
            "Bedding Text": "bedding_text",
            "Overturned Text": "overturned_text"
        },
        "geology_head": {
            "c": "unitname_column",
            "u": "alt_unitname_column",
            "g": "group_column",
            "g2": "supergroup_column",
            "ds": "description_column",
            "min": "minage_column",
            "max": "maxage_column",
            "r1": "rocktype_column",
            "r2": "alt_rocktype_column",
            "Sill Text": "sill_text",
            "Intrusion Text": "intrusive_text",
            "o-geol": "objectid_column"
        },
        "fault_head": {
            "f": "structtype_column",
            "Fault Text": "fault_text",
            "fdip": "dip_column",
            "fdipdir": "dipdir_column",
            "fdipdir_flag": "dipdir_flag",
            "fdipest": "dipestimate_column",
            "fdipest Text": "dipestimate_text",
            "ftype": "orientation_type",
            "o": "objectid_column"
        }
    }
        # Read JSON file
    with open(str(json_path), "r", encoding="utf-8") as f:
        input_json = json.load(f)

    # Transform data
    #transformed_data = transform_json(data)
    transformed_data = {}

    for key, mapping in mappings.items():
        if key in input_json:
            transformed_key = (
                "structure" if key == "struct_head" else
                "geology" if key == "geology_head" else
                "fault" if key == "fault_head" else key
            )
            
            filtered_mapping = {old_key: new_key for old_key, new_key in mapping.items() if old_key in input_json[key]}
            transformed_values = {new_key: input_json[key][old_key] for old_key, new_key in filtered_mapping.items()}
            transformed_data[transformed_key] = json.loads(json.dumps(transformed_values))
    # Add fixed values
    if "geology" in transformed_data:
        transformed_data["geology"]["volcanic_text"] = "volcanic"
        transformed_data["geology"]["ignore_codes"] = ["cover"]

    if "fault" in transformed_data:
        transformed_data["fault"]["dip_null_value"] = "0"
        transformed_data["fault"]["name_column"] = "name"

    # Hardcode the "fold" dictionary
    transformed_data["fold"] = {
        "structtype_column": "feature",
        "fold_text": "Fold axial trace",
        "description_column": "type",
        "synform_text": "syncline",
        "foldname_column": "name",
        "objectid_column": "objectid"
    }
    # Save to HJSON format
    json_data_path =Path(json_path).parent
    with open(str(json_data_path)+"\output.hjson", "w", encoding="utf-8") as f:
        json.dump(transformed_data, f, indent=4)

    print("Transformation complete. Output saved to output.hjson")
    return transformed_data


