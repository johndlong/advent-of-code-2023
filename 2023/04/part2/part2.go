// 1539876 - too low

package main

import (
	"fmt"
	"log"

	"github.com/johndlong/advent-of-code/2023/04/common"
)

func processCards(cards []common.Card) (int, error) {
	totals := []int{}
	for i := 1; i <= len(cards); i++ {
		totals = append(totals, 1)
	}
	index := 0
	for {
		if index >= len(cards) {
			break
		}
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
	return total, nil
}

func main() {
	cards, err := common.ProcessLines("part2.txt")
	if err != nil {
		log.Fatal(err)
	}

	total, err := processCards(cards)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Result: %d", total)
}
