// 1539876 - too low

package main

import (
	"flag"
	"log"

	"github.com/johndlong/advent-of-code/2023/04/common"
)

func processCards(cards []common.Card) int {
	index := 0
	totals := []int{}
	for i := 1; i <= len(cards); i++ {
		totals = append(totals, 1)
	}
	for index < len(cards) {
		card := cards[index]
		winningTotal := card.WinningTotal()

		if winningTotal > 0 {
			for i := 1; i <= winningTotal; i++ {
				totals[index+i] += totals[index]
			}
		}
		index++
	}

	total := 0
	for _, count := range totals {
		total += count
	}

	return total
}

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

	total := processCards(cards)
	log.Printf("Result: %d", total)
}
