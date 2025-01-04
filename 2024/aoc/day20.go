package aoc

import (
	"fmt"
)

type Day20 struct{}

type Path20 struct {
	hasCheated bool
	pos        Pos
	savedTime  int
	parent     *Path20
}

func (p Path20) String() string {
	return fmt.Sprintf("{cheated: %v, pos: %v, savedTime: %d}", p.hasCheated, p.pos, p.savedTime)
}

func (p *Path20) seen(pos Pos) bool {
	curPath := p
	i := 0
	for curPath != nil && i < 3 {
		if curPath.pos == pos {
			return true
		}
		curPath = curPath.parent
		i += 1
	}
	return false
}

func GetBestTime(m []string, start Pos, end Pos) int {
	totalTime := 0
	curPos := []Pos{start}
	seen := make(map[Pos]bool)
	for len(curPos) > 0 {
		nextPos := make([]Pos, 0)
		for _, pos := range curPos {
			if _, s := seen[pos]; s {
				continue
			}
			seen[pos] = true
			if pos == end {
				return totalTime
			}
			adjacents := pos.GetAdjacent(m)
			for _, adj := range adjacents {
				if m[adj.x][adj.y] != '#' {
					nextPos = append(nextPos, adj)
				}
			}
		}
		curPos = nextPos
		totalTime += 1
	}
	return -1
}

func (d Day20) Part1(path string) {
	m := getMap(path)
	start := GetPos(m, 'S')
	end := GetPos(m, 'E')
	fmt.Println(start, end)
	bestTime := GetBestTime(m, start, end)
	fmt.Println("bestTime", bestTime)
	startPath := Path20{false, start, 0, nil}
	curPath := []Path20{startPath}
	totalTime := 0
	successfulPath := make([]Path20, 0)
	for len(curPath) > 0 {
		nextPath := make([]Path20, 0)
		if totalTime > bestTime-100 {
			break
		}
		for _, path := range curPath {
			if path.pos == end {
				path.savedTime = bestTime - totalTime
				successfulPath = append(successfulPath, path)
				continue
			}
			adjacents := path.pos.GetAdjacent(m)
			for _, adj := range adjacents {
				if path.seen(adj) {
					continue
				}
				if m[adj.x][adj.y] == '#' && !path.hasCheated {
					nextPath = append(nextPath, Path20{true, adj, 0, &path})
				}
				if m[adj.x][adj.y] != '#' {
					nextPath = append(nextPath, Path20{path.hasCheated, adj, 0, &path})
				}
			}
		}
		curPath = nextPath
		totalTime += 1
	}
	fmt.Println(len(successfulPath))
}

func (d Day20) Part2(path string) {

}
