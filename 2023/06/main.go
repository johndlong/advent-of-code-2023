package main

import (
	"flag"
	"log"

	"github.com/johndlong/advent-of-code/2023/06/common"
)

func part1(path string) int {
	races, err := common.ProcessLines(path, false)
	if err != nil {
		log.Fatal(err)
	}

	total := 1
	for _, race := range races {
		total *= race.NumberWinningOptions()
	}

	return total
}

func part2(path string) int {
	races, err := common.ProcessLines(path, true)
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
	var inputFlag string
	flag.StringVar(&inputFlag, "filename", "", "input data set")
	flag.Parse()

	if inputFlag == "" {
		panic("file not provided (--filename <path>)")
	}
	log.Printf("Result: %d", part1(inputFlag))
	log.Printf("Result: %d", part2(inputFlag))
}
