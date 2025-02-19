
import csv
from lxml import etree as ET

# Constants for tag identifiers.
PERSON_TAG = "P"
ADDRESS_TAG = "A"
PHONE_TAG = "T"
FAMILY_TAG = "F"
ROOT_TAG = "people"

# Data format mapping.
data_format = {
    PERSON_TAG: {
        "xml_tag": "person",
        "fields": ["firstname", "lastname"]
    },
    ADDRESS_TAG: {
        "xml_tag": "address",
        "fields": ["street", "city", "zipcode"]
    },
    PHONE_TAG: {
        "xml_tag": "phone",
        "fields": ["mobile", "landline"]
    },
    FAMILY_TAG: {
        "xml_tag": "family",
        "fields": ["name", "born"]
    }
}


class RowBasedToXMLConverter:
    def __init__(self, csv_filepath, output_filepath):
        """
        Initialize the converter with a row based file and output file paths.
        """
        self.csv_filepath = csv_filepath
        self.output_filepath = output_filepath
        self.root = ET.Element(ROOT_TAG)
        # The current parent element, initially None
        self.parent = None

    def add_sub_element(self, node, tag, row):
        """
        Create and append sub-elements to the given node based on the row.
        Skips the first column which is the tag identifier.
        """
        for col in range(1, len(row)):
            field_name = data_format[tag]['fields'][col - 1]
            ET.SubElement(node, field_name).text = row[col]

    def process_row(self, row):
        """
        Process a single row and create the corresponding XML element.
        Updates the current parent node as necessary.
        Returns False if an error is encountered, True otherwise.
        """
        if not row or len(row) == 0:
            return False

        current_tag = row[0]
        try:
            current_xml_tag = data_format[current_tag]['xml_tag']
        except KeyError:
            print(f"Error: Unknown tag '{current_tag}' in row: {row}", flush=True)
            return False

        target_node = None

        if current_tag == PERSON_TAG:
            self.parent = ET.SubElement(self.root, current_xml_tag)
            target_node = self.parent

        elif current_tag in (ADDRESS_TAG, PHONE_TAG):
            if self.parent is None:
                print(f"Error: No parent found for tag {current_tag} in row: {row}", flush=True)
                return False
            target_node = ET.SubElement(self.parent, current_xml_tag)

        elif current_tag == FAMILY_TAG:
            if self.parent is None:
                print(f"Error: No parent found for {current_tag} in row: {row}", flush=True)
                return False
            # Avoid nesting family elements inside family elements
            if self.parent.tag == data_format[FAMILY_TAG]['xml_tag']:
                self.parent = self.parent.getparent()
            target_node = ET.SubElement(self.parent, current_xml_tag)
            # Update parent to the new family element
            self.parent = target_node

        else:
            print(f"Unknown tag {current_tag} in row: {row}", flush=True)
            return False

        if target_node is not None:
            self.add_sub_element(target_node, current_tag, row)
        return True

    def build_tree(self):
        """
        Read the row based file and build the XML tree.
        Only the file opening is wrapped in try/except for FileNotFoundError.
        Other errors during processing will propagate.
        """
        try:
            csvfile = open(self.csv_filepath, newline='', encoding='utf-8')
        except FileNotFoundError as e:
            print(f"Error reading row based file: {e}", flush=True)
            return False

        reader = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)
        # Reset parent for a new file (if needed)
        self.parent = ET.Element(data_format[PERSON_TAG]['xml_tag'])
        
        for row in reader:
            # Skip empty rows
            if not row or len(row) == 0:
                continue
            result = self.process_row(row)
            if not result:
                # Optionally, continue processing or break; here we break on first error.
                csvfile.close()
                return False
        
        csvfile.close()
        return True

    def write_xml(self):
        """
        Write the XML tree to the output file.
        """
        tree_out = ET.tostring(self.root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        with open(self.output_filepath, 'wb') as f:
            f.write(tree_out)
        print(f"XML file generated successfully: {self.output_filepath}", flush=True)


def main():
    csv_filepath = 'input'    # input file path.
    output_filepath = 'output.xml'  # output XML file path.

    converter = RowBasedToXMLConverter(csv_filepath, output_filepath) 
    tree = converter.build_tree()

    if tree:
        converter.write_xml()


if __name__ == '__main__':
    main()
