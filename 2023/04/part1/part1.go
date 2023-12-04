package main

import (
	"fmt"
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

	fmt.Printf("Result: %d", total)
}
