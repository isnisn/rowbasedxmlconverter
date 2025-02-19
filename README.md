# Row Based to XML Converter

This application converts a pipe-delimited row based file into an XML file.

## Prerequisites

- Python 3.x installed on your system.
- The `lxml` library installed. If you haven't installed it yet, you can do so using pip:

  ```bash
  pip install lxml
  ```

## Usage

1. **Prepare your Row Based File**

   - Create a file named `input` in the same directory as your code.
   - Format your file with a pipe (`|`) as the delimiter. For example:

     ```text
     P|förnamn|efternamn
     T|mobilnummer|fastnätsnummer
     A|gata|stad|postnummer
     F|namn|födelseår
     ```

2. **Run the Application**

   - Open a terminal in the project directory.
   - Run the `main.py` file using Python:

     ```bash
     python main.py
     ```

3. **Output**

   - After running, a file named `output.xml` will be generated in the same directory.
   - The generated XML file will contain the XML representation of your row based data.
