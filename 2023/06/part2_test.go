package main

import (
	"testing"

	"github.com/johndlong/advent-of-code/2023/06/common"
)

func TestProcessLinesIgnoreWhitespace(t *testing.T) {
	t.Parallel()
	races, err := common.ProcessLines("testdata/data.txt", true)
	if err != nil {
		t.Fatal(err)
	}
	if races[0].Duration != 71530 {
		t.Fatalf("expected %d; got %d", 71530, races[0].Duration)
	}
	if races[0].Record != 940200 {
		t.Fatalf("expected %d; got %d", 940200, races[0].Record)
	}
}

func TestNumberWinningOptionsPart2(t *testing.T) {
	t.Parallel()
	races, err := common.ProcessLines("testdata/data.txt", true)
	if err != nil {
		t.Fatal(err)
	}

	result := races[0].NumberWinningOptions()
	if result != 71503 {
		t.Errorf("expected %d; got: %d", 71503, result)
	}
}

func TestPart2(t *testing.T) {
	t.Parallel()
	result := part2("testdata/data.txt")
	if result != 71503 {
		t.Fatalf("expected %d; got %d", 71503, result)
	}
}
