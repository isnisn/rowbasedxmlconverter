package main

import "encoding/xml"

type People struct {
	XMLName xml.Name `xml:"people"`
	Persons []Person `xml:"person"`
}

type Person struct {
	XMLName   xml.Name `xml:"person"`
	Firstname string   `xml:"firstname"`
	Lastname  string   `xml:"lastname"`
	Phone     *Phone   `xml:"phone,omitempty"`
	Address   *Address `xml:"address,omitempty"`
	Families  []Family `xml:"family,omitempty"`
}

type Family struct {
	XMLName xml.Name `xml:"family"`
	Name    string   `xml:"name"`
	Born    string   `xml:"born"`
	Phone   *Phone   `xml:"phone,omitempty"`
	Address *Address `xml:"address,omitempty"`
}

type Phone struct {
	XMLName  xml.Name `xml:"phone"`
	Mobile   string   `xml:"mobile"`
	Landline string   `xml:"landline"`
}

type Address struct {
	XMLName xml.Name `xml:"address"`
	Street  string   `xml:"street"`
	City    string   `xml:"city"`
	Postal  string   `xml:"postal,omitempty"`
}
