package aoc

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Day18 struct{}

func GetBytesPos(path string) []Pos {
	f, err := os.Open(path)
	check(err)
	defer f.Close()
	scanner := bufio.NewScanner(f)
	positions := make([]Pos, 0)
	for scanner.Scan() {
		t := scanner.Text()
		pos := strings.Split(t, ",")
		x, err := strconv.Atoi(pos[0])
		check(err)
		y, err := strconv.Atoi(pos[1])
		check(err)
		positions = append(positions, Pos{x, y})
	}
	return positions
}

func GetExit(blockers map[Pos]bool) int {
	startPos := Pos{0, 0}
	endPos := Pos{70, 70}
	currPositions := make([]Pos, 0)
	currPositions = append(currPositions, startPos)
	seen := make(map[Pos]bool)
	res := 0
	for len(currPositions) != 0 {
		nextPositions := make([]Pos, 0)
		// fmt.Println(len(currPositions))
		for _, currPos := range currPositions {
			if currPos == endPos {
				return res
			}
			for _, nextPos := range currPos.GetAdjacentGrid(endPos.x+1, endPos.y+1) {
				_, s := seen[nextPos]
				_, b := blockers[nextPos]
				if !s && !b {
					nextPositions = append(nextPositions, nextPos)
					seen[nextPos] = true
				}
			}
		}
		res += 1
		currPositions = nextPositions
	}
	return -1
}

func (d Day18) Part1(path string) {
	positionsArr := GetBytesPos(path)
	blockers := make(map[Pos]bool)
	for i, p := range positionsArr {
		if i > 1023 {
			break
		}
		blockers[p] = true
	}
	fmt.Println(GetExit(blockers))
}

func (d Day18) Part2(path string) {
	positionsArr := GetBytesPos(path)
	blockers := make(map[Pos]bool)
	for i, p := range positionsArr {
		if i > 1023 {
			break
		}
		blockers[p] = true
	}
	for i := 1024; i < len(positionsArr); i++ {
		blockers[positionsArr[i]] = true
		res := GetExit(blockers)
		if res == -1 {
			fmt.Println(positionsArr[i])
			break
		}
	}
}
