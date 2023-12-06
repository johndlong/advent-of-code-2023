package common

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

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

func ProcessLines(path string) ([]Race, error) {
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
	if len(lines) != 2 {
		return races, fmt.Errorf("incorrect datafile")
	}

	times := []int{}
	records := []int{}

	valueRegexp := regexp.MustCompile(`(\d+)`)
	timesMatch := valueRegexp.FindAllStringSubmatch(lines[0], -1)
	for _, timeStr := range timesMatch {
		time, err := strconv.Atoi(timeStr[0])
		if err != nil {
			return races, err
		}
		times = append(times, time)
	}

	recordsMatch := valueRegexp.FindAllStringSubmatch(lines[1], -1)
	for _, recordStr := range recordsMatch {
		record, err := strconv.Atoi(recordStr[0])
		if err != nil {
			return races, err
		}
		records = append(records, record)
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
