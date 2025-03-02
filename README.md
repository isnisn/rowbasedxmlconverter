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

   - Create a file named `input`(one is provided) in the same directory as your code.
   - Format your file with a pipe (`|`) as the delimiter. For example:

     ```text
     P|förnamn|efternamn
     T|mobilnummer|fastnätsnummer
     A|gata|stad|postnummer
     F|namn|födelseår
     ```

2. **Run the Application**

     ```bash
     python main.py
     ```

3. **Output**

   - After running, a file named `output.xml` will be generated in the same directory.
   - The generated XML file will contain the XML representation of your row based data.

4. **Run the Tests**
 
   - Use the `unittest` module to run the tests:

     ```bash
     python -m unittest discover tests
     ```

5. **Test Assertions**

   - The tests will check the basic functionality of the `RowBasedToXMLConverter`, ensuring that it correctly processes and converts the input data to XML.

6. **Shortcomings**
   - More extensive tests
   - Constants and tags in `data_format` in `utils/converter.py` could be loaded dynamically via a yaml-file to increase the flexibility and scalability.
   - Logging features
   - Dockerize the application and put it behind an API-endpoint for deployment as a microservice or similiar in the cloud
