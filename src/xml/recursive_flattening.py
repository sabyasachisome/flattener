import os
import xml.etree.ElementTree as ET
import pandas as pd
from gen_utils import *


# -------------------------------------------------------
# Recursive XML flattener
# -------------------------------------------------------
def flatten_element(element, parent_path=''):
    flat_data = {}
    path = f"{parent_path}_{element.tag}" if parent_path else element.tag

    # Add text value
    if element.text and element.text.strip():
        flat_data[path] = element.text.strip()

    # Add attributes
    for key, value in element.attrib.items():
        flat_data[f"{path}_{key}"] = value

    # Recurse into children
    for child in element:
        flat_data.update(flatten_element(child, path))

    return flat_data

# -------------------------------------------------------
# Main: Parse and flatten all XML files
# -------------------------------------------------------
if __name__ == "__main__":
    # Relative to the project root
    data_folder = os.path.join(os.path.dirname(__file__), "../../sample_xml_files")

    xml_files = get_xml_files(data_folder)

    for xml_file in xml_files:
        print(f"\nProcessing file: {xml_file}")
        try:
            # Parse XML
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Flatten each child element
            records = [flatten_element(child) for child in root]

            # Convert to DataFrame
            df = pd.DataFrame(records)

            # Output CSV file
            output_csv = xml_file.replace(".xml", "_flattened.csv")
            df.to_csv(output_csv, index=False)
            print(f" Flattened XML saved to {output_csv}")

        except Exception as e:
            print(f" Error processing {xml_file}: {e}")
