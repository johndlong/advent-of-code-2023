package common

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

const expectedLines = 2

var errIncorrectDataFile = errors.New("incorrect datafile")

type Race struct {
	Duration int
	Record   int
}

func (r *Race) NumberWinningOptions() int {
	total := 0
	for i := 0; i < r.Duration; i++ {
		if DoesChargeBeatRecord(i, r.Duration, r.Record) {
			total++
		}
	}

	return total
}

func DoesChargeBeatRecord(chargeTime int, duration int, record int) bool {
	runTime := duration - chargeTime
	distance := chargeTime * runTime

	return distance > record
}

func ProcessLines(path string, ignoreWhitespace bool) ([]Race, error) {
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

	races := []Race{}
	if len(lines) != expectedLines {
		return races, fmt.Errorf("%w", errIncorrectDataFile)
	}

	valueRegexp := regexp.MustCompile(`(\d+)`)
	timesMatch := valueRegexp.FindAllStringSubmatch(lines[0], -1)
	times, err := processValues(timesMatch, ignoreWhitespace)
	if err != nil {
		return races, fmt.Errorf("failed convert: %w", err)
	}
	recordsMatch := valueRegexp.FindAllStringSubmatch(lines[1], -1)
	records, err := processValues(recordsMatch, ignoreWhitespace)
	if err != nil {
		return races, fmt.Errorf("failed convert: %w", err)
	}

	for i := range times {
		race := Race{
			Duration: times[i],
			Record:   records[i],
		}
		races = append(races, race)
	}

	return races, nil
}

func processValues(valuesMatch [][]string, ignoreWhitespace bool) ([]int, error) {
	retval := []int{}
	valueStr := []string{}
	if ignoreWhitespace {
		valueStr = append(valueStr, "")
	}
	for _, value := range valuesMatch {
		if ignoreWhitespace {
			valueStr[0] += value[0]
		} else {
			valueStr = append(valueStr, value[0])
		}
	}

	for _, value := range valueStr {
		result, err := strconv.Atoi(value)
		if err != nil {
			return retval, fmt.Errorf("failed convert: %w", err)
		}
		retval = append(retval, result)
	}

	return retval, nil
}
