package aoc

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Day19 struct{}

func GetPatterns(path string) ([]string, []string) {
	f, err := os.Open(path)
	check(err)
	defer f.Close()
	scanner := bufio.NewScanner(f)
	scanner.Scan()
	patterns := strings.Split(scanner.Text(), ", ")
	targets := make([]string, 0)
	scanner.Scan()
	for scanner.Scan() {
		targets = append(targets, scanner.Text())
	}
	return patterns, targets
}

func isPossible(target string, patterns []string, seen map[string]int) int {
	if len(target) == 0 {
		return 1
	}
	fmt.Println(target)
	if b, s := seen[target]; s {
		return b
	}
	for _, pattern := range patterns {
		if strings.HasPrefix(target, pattern) {
			res := isPossible(target[len(pattern):], patterns, seen)
			seen[target] += res
		}
	}
	if _, s := seen[target]; !s {
		seen[target] = 0
	}
	return seen[target]
}

func (d Day19) Part1(path string) {
	patterns, targets := GetPatterns(path)
	seen := make(map[string]int)
	res := 0
	for _, target := range targets {
		fmt.Println(isPossible(target, patterns, seen))
		if isPossible(target, patterns, seen) > 0 {
			fmt.Println(target, "is possible")
			res += 1
		}
	}
	fmt.Println(res)
}

func (d Day19) Part2(path string) {
	patterns, targets := GetPatterns(path)
	seen := make(map[string]int)
	res := 0
	for _, target := range targets {
		fmt.Println(target, "is possible")
		res += isPossible(target, patterns, seen)
	}
	fmt.Println(res)
}
