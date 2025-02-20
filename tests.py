import unittest
import os
import csv
from lxml import etree as ET
from utils.converter import RowBasedToXMLConverter

""" Unit tests for the RowBasedToXMLConverter class. """
class TestRowBasedToXMLConverter(unittest.TestCase):

    def setUp(self):
        """Setup the necessary file paths and instance for testing."""
        self.input_file = 'test_input'
        self.output_file = 'test_output.xml'

    def tearDown(self):
        """Clean up files created during the test."""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def write_test_csv(self, lines):
        """Helper method to write test data."""
        with open(self.input_file, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            for line in lines:
                writer.writerow(line)

    def test_valid_file(self):
        """Test processing with valid data."""
        
        csv_data = [
            ["P", "Victoria", "Bernadotte"],
            ["T", "070-0101010", "0459-123456"],
            ["A", "Haga Slott", "Stockholm", "101"],
            ["F", "Estelle", "2012"],
            ["A", "Solliden", "Öland", "10002"],
            ["F", "Oscar", "2016"],
            ["T", "0702-020202", "02-202020"],
            ["P", "Joe", "Biden"],
            ["A", "White House", "Washington, D.C"],
        ]

        self.write_test_csv(csv_data)
        converter = RowBasedToXMLConverter(self.input_file, self.output_file)
        result = converter.build_tree()
        self.assertTrue(result, "Valid CSV data should return True for build_tree()")

        converter.write_xml()
        self.assertTrue(os.path.exists(self.output_file), "Output XML file should be created")

        # Verify contents, here we could write more extensive tests
        tree = ET.parse(self.output_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "people", "Root XML tag should be 'people'")

        persons = root.findall('person')
        self.assertEqual(len(persons), 2, "There should be one 'person' element")

        self.assertEqual(persons[0].find('firstname').text, "Victoria")
        self.assertEqual(persons[0].find('lastname').text, "Bernadotte")

    def test_missing_file(self):
        """Test processing with a non-existing file."""
        converter = RowBasedToXMLConverter("nonexistent", self.output_file)
        result = converter.build_tree()
        self.assertFalse(result, "Non-existing file should return False for build_tree()")

    def test_unknown_tag(self):
        """Test handling of unknown tags."""
        # Data with an unknown tag
        data = [
            ["X", "Data"]
        ]

        self.write_test_csv(data)
        converter = RowBasedToXMLConverter(self.input_file, self.output_file)
        result = converter.build_tree()
        self.assertFalse(result, "Unknown tag should return False for build_tree()")

if __name__ == '__main__':
    unittest.main()

