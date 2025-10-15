import xml.etree.ElementTree as ET
import pandas as pd
import os
from gen_utils import *

# def get_xml_files(data_dir):
#     """
#     Return a list of absolute paths to all XML files in the given folder.
#     Automatically resolves relative paths and filters out non-XML files.
#     """
#     abs_dir = os.path.abspath(data_dir)  # convert to absolute path

#     if not os.path.exists(abs_dir):
#         raise FileNotFoundError(f"Directory not found: {abs_dir}")

#     xml_files = [
#         os.path.join(abs_dir, f)
#         for f in os.listdir(abs_dir)
#         if f.lower().endswith('.xml')
#     ]

#     if not xml_files:
#         print(f"No XML files found in {abs_dir}")
#     else:
#         print(f"Found {len(xml_files)} XML files in {abs_dir}")

#     return xml_files


def flatten_element_iterative(element, parent_path=''):
    """Iteratively flattens an XML element and its children into key-value pairs."""
    flat_data = {}
    stack = [(element, parent_path)]

    while stack:
        elem, parent = stack.pop()
        path = f"{parent}_{elem.tag}" if parent else elem.tag

        # Capture text value
        if elem.text and elem.text.strip():
            flat_data[path] = elem.text.strip()

        # Capture attributes
        for key, value in elem.attrib.items():
            flat_data[f"{path}_{key}"] = value

        # Add children to stack
        for child in reversed(list(elem)):  # reversed for natural XML order
            stack.append((child, path))

    return flat_data


def convert_to_csv_iterative(xml_path, csv_path):
    """Parse and flatten XML file iteratively — safe for very large files."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    records = []
    for child in root:
        records.append(flatten_element_iterative(child))

    df = pd.DataFrame(records)
    df.to_csv(csv_path, index=False)
    print(f"Flattened XML saved to: {csv_path}")


if __name__ == "__main__":
    xml_folder = "../../sample_xml_files"
    xml_files = get_xml_files(xml_folder)

    for xml_file in xml_files:
        print(f"Processing: {xml_file}")
        convert_to_csv_iterative(xml_file, xml_file.replace('.xml', '_flattened.csv'))

