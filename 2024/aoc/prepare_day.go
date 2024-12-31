package aoc

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path"
)

func CreateNotExistingFile(path string) {
	var file *os.File
	var err error
	if _, err := os.Stat(path); os.IsNotExist(err) {
		file, err = os.Create(path)
		check(err)
	} else {
		file, err = os.Open(path)
		check(err)
	}
	defer file.Close()
	if err != nil {
		log.Fatalf("Failed to create / open file: %v", err)
	}
}

func FetchInput(path string, day int) {
	headerValue := os.Getenv("AOC_SESSION")
	url := fmt.Sprintf("https://adventofcode.com/2024/day/%d/input", day)

	client := &http.Client{}

	req, err := http.NewRequest("GET", url, nil)
	check(err)
	req.Header.Add("Cookie", fmt.Sprintf("session=%s", headerValue))
	resp, err := client.Do(req)
	check(err)
	defer resp.Body.Close()

	file, err := os.OpenFile(path, os.O_WRONLY, 0644)
	check(err)
	defer file.Close()

	_, err = io.Copy(file, resp.Body)
	check(err)
}

func PrepareDay(day int) {
	codeDir := path.Dir("aoc/.")
	runFile := (path.Join(codeDir, fmt.Sprintf("day%d.go", day)))
	inputFile := GetInputFile(day)
	CreateNotExistingFile(runFile)
	CreateNotExistingFile(inputFile)
	FetchInput(inputFile, day)
}

func GetInputFile(day int) string {
	inputDir := path.Dir("inputs/.")
	return (path.Join(inputDir, fmt.Sprintf("day%d-input.txt", day)))
}
