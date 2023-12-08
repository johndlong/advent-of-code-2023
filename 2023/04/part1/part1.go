package main

import (
	"flag"
	"log"

	"github.com/johndlong/advent-of-code/2023/04/common"
)

func main() {
	var inputFlag string
	flag.StringVar(&inputFlag, "filename", "", "input data set")
	flag.Parse()

	if inputFlag == "" {
		panic("file not provided (--filename <path>)")
	}
	cards, err := common.ProcessLines(inputFlag)
	if err != nil {
		log.Fatal(err)
	}

	total := 0
	for _, card := range cards {
		total += card.WinningTotal()
	}

	log.Printf("Result: %d", total)
}
