package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type card struct {
	number         int
	winningNumbers []int
	actualNumbers  []int
}

func (c *card) winningTotal() int {
	retval := 0
	winningNumbers := map[int]bool{}
	for _, winningNumber := range c.winningNumbers {
		winningNumbers[winningNumber] = true

	}
	for _, number := range c.actualNumbers {
		if _, ok := winningNumbers[number]; ok {
			retval += 1
		}
	}
	if retval == 0 {
		return 0
	}
	return int(math.Pow(2, float64(retval-1)))
}

func getNumbers(sequence string) ([]int, error) {
	retval := []int{}
	resultRegexp := regexp.MustCompile(`(\d+)`)
	resultMatch := resultRegexp.FindAllStringSubmatch(sequence, -1)
	for _, results := range resultMatch {
		number, err := strconv.Atoi(results[0])
		if err != nil {
			return []int{}, err
		}
		retval = append(retval, number)
	}
	return retval, nil

}

func processLine(line string) (card, error) {
	gameSeparators := strings.Split(line, ":")
	gameRegexp := regexp.MustCompile(`Card\s+(\d+)`)
	gameMatch := gameRegexp.FindStringSubmatch(gameSeparators[0])

	gameNumInt, err := strconv.Atoi(gameMatch[1])
	if err != nil {
		return card{}, err
	}

	separators := strings.Split(gameSeparators[1], "|")

	winningNumbers, err := getNumbers(separators[0])
	if err != nil {
		return card{}, err
	}
	numbers, err := getNumbers(separators[1])
	if err != nil {
		return card{}, err
	}

	return card{number: gameNumInt, winningNumbers: winningNumbers, actualNumbers: numbers}, nil
}

func main() {
	file, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	cards := []card{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		game, err := processLine(scanner.Text())
		if err != nil {
			log.Fatal(err)
		}
		cards = append(cards, game)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	total := 0
	for _, card := range cards {
		total += card.winningTotal()
	}

	fmt.Printf("Result: %d", total)
}
