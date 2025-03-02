package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Parser struct {
	People *People

	currentPerson *Person
	currentFamily *Family

	// current record type, to enforce allowed transitions.
	currentType string

	// lists which record types may follow a given record.
	allowedTransitions map[string][]string
}

func NewParser() *Parser {
	return &Parser{
		People: &People{},
		allowedTransitions: map[string][]string{
			"P": {"T", "A", "F"},
			"F": {"T", "A"},
		},
	}
}

// checks whether a record type may follow the current record.
func (p *Parser) isTransitionAllowed(nextType string) bool {
	if p.currentType == "" {
		return true
	}
	if allowed, ok := p.allowedTransitions[p.currentType]; ok {
		for _, t := range allowed {
			if t == nextType {
				return true
			}
		}
		return false
	}
	return true
}

func (p *Parser) ProcessLine(line string) {
	parts := strings.Split(line, "|")
	if len(parts) == 0 {
		return
	}

	recType := parts[0]
	if !p.isTransitionAllowed(recType) {
		fmt.Fprintf(os.Stderr, "Invalid transition: '%s' cannot follow '%s' in line: %s\n", recType, p.currentType, line)
		return
	}

	switch recType {
	case "P":
		p.handlePerson(parts, line)
	case "T":
		p.handlePhone(parts, line)
	case "A":
		p.handleAddress(parts, line)
	case "F":
		p.handleFamily(parts, line)
	default:
		fmt.Fprintln(os.Stderr, "Unknown record type in line:", line)
		return
	}

	p.currentType = recType
}

// handlePerson processes a person record.
func (p *Parser) handlePerson(parts []string, line string) {
	if len(parts) < 3 {
		fmt.Fprintln(os.Stderr, "Invalid P line:", line)
		return
	}
	if p.currentPerson != nil {
		p.People.Persons = append(p.People.Persons, *p.currentPerson)
	}
	p.currentPerson = &Person{
		Firstname: parts[1],
		Lastname:  parts[2],
	}
	p.currentFamily = nil
}

// handlePhone processes a phone record.
func (p *Parser) handlePhone(parts []string, line string) {
	if len(parts) < 3 {
		fmt.Fprintln(os.Stderr, "Invalid T line:", line)
		return
	}
	phone := &Phone{
		Mobile:   parts[1],
		Landline: parts[2],
	}
	if p.currentType == "F" && p.currentFamily != nil {
		p.currentFamily.Phone = phone
	} else if p.currentPerson != nil {
		p.currentPerson.Phone = phone
	} else {
		fmt.Fprintln(os.Stderr, "T record with no active person:", line)
	}
}

// handleAddress processes an address record.
func (p *Parser) handleAddress(parts []string, line string) {
	if len(parts) < 3 {
		fmt.Fprintln(os.Stderr, "Invalid A line:", line)
		return
	}
	street := parts[1]
	city := parts[2]
	postal := ""
	if len(parts) >= 4 {
		postal = parts[3]
	}
	address := &Address{
		Street: street,
		City:   city,
		Postal: postal,
	}
	if p.currentType == "F" && p.currentFamily != nil {
		p.currentFamily.Address = address
	} else if p.currentPerson != nil {
		p.currentPerson.Address = address
	} else {
		fmt.Fprintln(os.Stderr, "A record with no active person:", line)
	}
}

// handleFamily processes a family record.
func (p *Parser) handleFamily(parts []string, line string) {
	if len(parts) < 3 {
		fmt.Fprintln(os.Stderr, "Invalid F line:", line)
		return
	}
	if p.currentPerson == nil {
		fmt.Fprintln(os.Stderr, "F record with no active person:", line)
		return
	}
	family := Family{
		Name: parts[1],
		Born: parts[2],
	}
	p.currentPerson.Families = append(p.currentPerson.Families, family)
	p.currentFamily = &p.currentPerson.Families[len(p.currentPerson.Families)-1]
}

// ParseFile processes a file line by line.
func (p *Parser) ParseFile(filename string) error {
	file, err := os.Open(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		p.ProcessLine(scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return err
	}

	if p.currentPerson != nil {
		p.People.Persons = append(p.People.Persons, *p.currentPerson)
	}
	return nil
}
