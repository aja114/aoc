package aoc

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Day5 struct{}

type DepMap map[string]map[string]bool

func getDepMap(dependecies []string) DepMap {
	depMap := make(DepMap)
	for _, d := range dependecies {
		pre := strings.Split(d, "|")[0]
		post := strings.Split(d, "|")[1]
		_, exists := depMap[post]
		if exists {
			depMap[post][pre] = true
		} else {
			depMap[post] = make(map[string]bool)
			depMap[post][pre] = true
		}
	}
	return depMap
}

func updatePossible(pages []string, depMap DepMap) bool {
	for i, page := range pages {
		for _, nextPage := range pages[i:] {
			_, exist := depMap[page][nextPage]
			if exist {
				return false
			}
		}
	}
	return true
}

func possibleUpdateScore(update string, depMap DepMap) int {
	pages := strings.Split(update, ",")
	upPossible := updatePossible(pages, depMap)
	if !upPossible {
		return 0
	}
	n, err := strconv.Atoi(string(pages[len(pages)/2]))
	check(err)
	return n
}

func impossibleUpdateScore(update string, depMap DepMap) int {
	pages := strings.Split(update, ",")
	upPossible := updatePossible(pages, depMap)
	if upPossible {
		return 0
	}
	i := 0
	newPages := make([]string, 0)
	for len(pages) > 0 {
		if i >= len(pages) {
			i = 0
			continue
		}
		el := pages[i]

		canInsert := true
		for j, remainPage := range pages {
			if i == j {
				continue
			}
			_, exist := depMap[pages[i]][remainPage]
			if exist {
				canInsert = false
				break
			}
		}
		if canInsert {
			newPages = append(newPages, el)
			pages = slices.Delete(pages, i, i+1)
		} else {
			i += 1
		}
	}
	n, err := strconv.Atoi(string(newPages[len(newPages)/2]))
	check(err)
	return n
}

func (d Day5) getUpdDep(path string) ([]string, DepMap) {
	f, err := os.Open(path)
	check(err)
	defer f.Close()
	scanner := bufio.NewScanner(f)
	dependecies := make([]string, 0)
	updates := make([]string, 0)
	depSection := true
	for scanner.Scan() {
		t := scanner.Text()
		if t == "" {
			depSection = false
			continue
		}
		if depSection {
			dependecies = append(dependecies, t)
		} else {
			updates = append(updates, t)
		}
	}
	depMap := getDepMap(dependecies)
	return updates, depMap
}

func (d Day5) Part1(path string) {
	updates, depMap := d.getUpdDep(path)
	res := 0
	for _, up := range updates {
		res += possibleUpdateScore(up, depMap)
	}
	fmt.Println(res)
}

func (d Day5) Part2(path string) {
	updates, depMap := d.getUpdDep(path)
	res := 0
	for _, up := range updates {
		res += impossibleUpdateScore(up, depMap)
	}
	fmt.Println(res)
}
