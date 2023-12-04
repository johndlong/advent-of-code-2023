package common

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Card struct {
	Number         int
	WinningNumbers []int
	ActualNumbers  []int
}

func (c *Card) WinningTotal() int {
	retval := 0
	winningNumbers := map[int]bool{}
	for _, winningNumber := range c.WinningNumbers {
		winningNumbers[winningNumber] = true
	}
	for _, number := range c.ActualNumbers {
		if _, ok := winningNumbers[number]; ok {
			retval++
		}
	}

	return retval
}

func getNumbers(sequence string) ([]int, error) {
	retval := []int{}
	resultRegexp := regexp.MustCompile(`(\d+)`)
	resultMatch := resultRegexp.FindAllStringSubmatch(sequence, -1)
	for _, results := range resultMatch {
		number, err := strconv.Atoi(results[0])
		if err != nil {
			return []int{}, fmt.Errorf("%w number to int: %s", err, results[0])
		}
		retval = append(retval, number)
	}

	return retval, nil
}

func ProcessLines(path string) ([]Card, error) {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	lines := []string{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	cards := []Card{}
	for _, line := range lines {
		card, err := processLine(line)
		if err != nil {
			return []Card{}, err
		}
		cards = append(cards, card)
	}

	return cards, nil
}

func processLine(line string) (Card, error) {
	gameSeparators := strings.Split(line, ":")
	gameRegexp := regexp.MustCompile(`Card\s+(\d+)`)
	gameMatch := gameRegexp.FindStringSubmatch(gameSeparators[0])

	gameNumInt, err := strconv.Atoi(gameMatch[1])
	if err != nil {
		return Card{}, fmt.Errorf("%w: card ID to int: %s", err, gameMatch[1])
	}

	separators := strings.Split(gameSeparators[1], "|")

	winningNumbers, err := getNumbers(separators[0])
	if err != nil {
		return Card{}, err
	}
	numbers, err := getNumbers(separators[1])
	if err != nil {
		return Card{}, err
	}

	return Card{Number: gameNumInt, WinningNumbers: winningNumbers, ActualNumbers: numbers}, nil
}
