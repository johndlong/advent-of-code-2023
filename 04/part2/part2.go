// 1539876 - too low

package main

import (
	"bufio"
	"fmt"
	"log"
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
	return retval
}

func processCards(cards []card) (int, error) {
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
		winningTotal := card.winningTotal()

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
	file, err := os.Open("part2.txt")
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

	total, err := processCards(cards)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Result: %d", total)
}
