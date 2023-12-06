package main

import (
	"log"

	"github.com/johndlong/advent-of-code/2023/06/common"
)

func part1(path string) int {
	races, err := common.ProcessLines(path)
	if err != nil {
		log.Fatal(err)
	}

	total := 1
	for _, race := range races {
		total *= race.NumberWinningOptions()
	}

	return total
}

func main() {
	log.Printf("Result: %d", part1("part1.txt"))
}
