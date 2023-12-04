package main

import (
	"log"

	"github.com/johndlong/advent-of-code/2023/04/common"
)

func main() {
	cards, err := common.ProcessLines("part1.txt")
	if err != nil {
		log.Fatal(err)
	}

	total := 0
	for _, card := range cards {
		total += card.WinningTotal()
	}

	log.Printf("Result: %d", total)
}
