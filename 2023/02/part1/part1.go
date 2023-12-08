package main

import (
	"bufio"
	"errors"
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"runtime"
	"strconv"
	"strings"
)

var ErrUnsupportedColor = errors.New("unsupported color")

const (
	expectedRed   = 12
	expectedGreen = 13
	expectedBlue  = 14
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
		return game{}, fmt.Errorf("%w: failed converting game ID to int: %s", err, gameSeparators[0])
	}

	rollSeparators := strings.Split(gameSeparators[1], ";")
	resultRegexp := regexp.MustCompile(`(\d+) (blue|red|green)`)
	gameRolls := []roll{}
	for _, rollStr := range rollSeparators {
		gameRoll := roll{red: 0, green: 0, blue: 0}
		resultSeparators := strings.Split(rollStr, ",")
		for _, result := range resultSeparators {
			resultMatch := resultRegexp.FindStringSubmatch(result)
			resultNumInt, err := strconv.Atoi(resultMatch[1])
			if err != nil {
				return game{}, fmt.Errorf("%w: failed converting roll ID to int: %v", err, resultMatch[1])
			}
			switch color := resultMatch[2]; color {
			case "blue":
				gameRoll.blue = resultNumInt
			case "red":
				gameRoll.red = resultNumInt
			case "green":
				gameRoll.green = resultNumInt
			default:
				return game{}, fmt.Errorf("%w: %s", ErrUnsupportedColor, color)
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
	var inputFlag string
	flag.StringVar(&inputFlag, "filename", "", "input data set")
	flag.Parse()

	if inputFlag == "" {
		panic("file not provided (--filename <path>)")
	}

	file, err := os.Open(inputFlag)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	games := []game{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		game, err := processLine(scanner.Text())
		if err != nil {
			log.Print(err)
			runtime.Goexit()
		}
		games = append(games, game)
	}

	if err := scanner.Err(); err != nil {
		log.Print(err)
		runtime.Goexit()
	}

	possibleGames := []game{}
	for _, game := range games {
		if isGamePossible(
			game,
			roll{
				red:   expectedRed,
				green: expectedGreen,
				blue:  expectedBlue,
			}) {
			possibleGames = append(possibleGames, game)
		}
	}

	total := 0
	for _, game := range possibleGames {
		total += game.number
	}

	log.Printf("Result: %d", total)
}
