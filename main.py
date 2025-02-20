import csv
from lxml import etree as ET
from utils.converter import RowBasedToXMLConverter

def main():
    csv_filepath = "input"  # input file path.
    output_filepath = "output.xml"  # output XML file path.

    converter = RowBasedToXMLConverter(csv_filepath, output_filepath)
    tree = converter.build_tree()

    if tree:
        converter.write_xml()


if __name__ == "__main__":
    main()
