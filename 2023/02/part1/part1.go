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

type roll struct {
	blue  int
	red   int
	green int
}

type game struct {
	number int
	rolls  []roll
}

func processLine(line string) (game, error) {
	gameSeparators := strings.Split(line, ":")
	gameRegexp := regexp.MustCompile(`Game (\d+)`)
	gameMatch := gameRegexp.FindStringSubmatch(gameSeparators[0])

	gameNumInt, err := strconv.Atoi(gameMatch[1])
	if err != nil {
		return game{}, err
	}

	rollSeparators := strings.Split(gameSeparators[1], ";")
	resultRegexp := regexp.MustCompile(`(\d+) (blue|red|green)`)
	gameRolls := []roll{}
	for _, rollStr := range rollSeparators {
		gameRoll := roll{}
		resultSeparators := strings.Split(rollStr, ",")
		for _, result := range resultSeparators {
			resultMatch := resultRegexp.FindStringSubmatch(result)
			resultNumInt, err := strconv.Atoi(resultMatch[1])
			if err != nil {
				return game{}, err
			}
			switch color := resultMatch[2]; color {
			case "blue":
				gameRoll.blue = resultNumInt
			case "red":
				gameRoll.red = resultNumInt
			case "green":
				gameRoll.green = resultNumInt
			default:
				return game{}, fmt.Errorf("unexpected color: %s", color)
			}
		}
		gameRolls = append(gameRolls, gameRoll)
	}

	return game{number: gameNumInt, rolls: gameRolls}, nil
}

func isGamePossible(gameTest game, desiredRoll roll) bool {
	for _, roll := range gameTest.rolls {
		if roll.blue > desiredRoll.blue || roll.green > desiredRoll.green || roll.red > desiredRoll.red {
			return false
		}
	}
	return true
}

func main() {
	file, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	games := []game{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		game, err := processLine(scanner.Text())
		if err != nil {
			log.Fatal(err)
		}
		games = append(games, game)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	possibleGames := []game{}
	for _, game := range games {
		if isGamePossible(
			game,
			roll{
				red:   12,
				green: 13,
				blue:  14,
			}) {
			possibleGames = append(possibleGames, game)
		}
	}

	total := 0
	for _, game := range possibleGames {
		total += game.number
	}

	fmt.Printf("Result: %d", total)
}
