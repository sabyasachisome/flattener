import xml.etree.ElementTree as ET
import pandas as pd
 
# Function to recursively flatten XML elements
def flatten_element(element, parent_path=''):
    flat_data = {}
    path = f"{parent_path}/{element.tag}" if parent_path else element.tag
    if element.text and element.text.strip():
        flat_data[path] = element.text.strip()
    for key, value in element.attrib.items():
        flat_data[f"{path}/@{key}"] = value
    for child in element:
        flat_data.update(flatten_element(child, path))
    return flat_data
 
# Load and parse the XML file
tree = ET.parse('test_file.xml')
root = tree.getroot()
 
# Flatten each child element (e.g., ABR records)
records = []
for child in root:
    records.append(flatten_element(child))
 
# Convert to DataFrame and save to CSV
df = pd.DataFrame(records)
df.to_csv('flattened_file1.csv', index=False)
 
print("Flattened XML saved to 'flattened_file1.csv'")