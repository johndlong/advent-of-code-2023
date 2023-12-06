package main

import (
	"testing"

	"github.com/johndlong/advent-of-code/2023/06/common"
)

func TestProcessLinesWithWhitespace(t *testing.T) {
	t.Parallel()
	races, err := common.ProcessLines("testdata/data.txt", false)
	if err != nil {
		t.Fatal(err)
	}
	if races[0].Duration != 7 {
		t.Fatalf("expected %d; got %d", 7, races[0].Duration)
	}
	if races[0].Record != 9 {
		t.Fatalf("expected %d; got %d", 9, races[0].Record)
	}
}

func TestDoesChargeBeatRecord(t *testing.T) {
	t.Parallel()
	type testDataInfo struct {
		chargeTime     int
		raceTime       int
		record         int
		expectedResult bool
	}

	testData := []testDataInfo{
		{chargeTime: 0, raceTime: 7, record: 9, expectedResult: false},
		{chargeTime: 1, raceTime: 7, record: 9, expectedResult: false},
		{chargeTime: 2, raceTime: 7, record: 9, expectedResult: true},
		{chargeTime: 3, raceTime: 7, record: 9, expectedResult: true},
		{chargeTime: 4, raceTime: 7, record: 9, expectedResult: true},
		{chargeTime: 5, raceTime: 7, record: 9, expectedResult: true},
		{chargeTime: 6, raceTime: 7, record: 9, expectedResult: false},
		{chargeTime: 7, raceTime: 7, record: 9, expectedResult: false},
	}

	for _, td := range testData {
		result := common.DoesChargeBeatRecord(td.chargeTime, td.raceTime, td.record)
		if result != td.expectedResult {
			t.Errorf("expected %v; got: %v", td.expectedResult, result)
		}
	}
}

func TestNumberWinningOptions(t *testing.T) {
	t.Parallel()
	races, err := common.ProcessLines("testdata/data.txt", false)
	if err != nil {
		t.Fatal(err)
	}

	for i, expectedResult := range []int{4, 8, 9} {
		result := races[i].NumberWinningOptions()
		if result != expectedResult {
			t.Errorf("expected %d; got: %d", expectedResult, result)
		}
	}
}

func TestPart1(t *testing.T) {
	t.Parallel()
	result := part1("testdata/data.txt")
	if result != 288 {
		t.Fatalf("expected %d; got %d", 288, result)
	}
}
