import os

def get_xml_files(data_dir):
    """
    Return a list of absolute paths to all XML files in the given folder.
    Automatically resolves relative paths and filters out non-XML files.
    """
    abs_dir = os.path.abspath(data_dir)

    if not os.path.exists(abs_dir):
        raise FileNotFoundError(f"Directory not found: {abs_dir}")

    xml_files = [
        os.path.join(abs_dir, f)
        for f in os.listdir(abs_dir)
        if f.lower().endswith('.xml')
    ]

    if not xml_files:
        print(f"No XML files found in {abs_dir}")
    else:
        print(f"Found {len(xml_files)} XML files in {abs_dir}")

    return xml_files
