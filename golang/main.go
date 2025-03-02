package main

import (
	"encoding/xml"
	"fmt"
	"os"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "Usage: program <input-file>")
		os.Exit(1)
	}
	inputFile := os.Args[1]

	parser := NewParser()
	err := parser.ParseFile(inputFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing file: %v\n", err)
		os.Exit(1)
	}

	xmlData, err := xml.MarshalIndent(parser.People, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error marshalling to XML: %v\n", err)
		os.Exit(1)
	}

	out := string(xml.Header) + string(xmlData)

	fmt.Println(out)
}
