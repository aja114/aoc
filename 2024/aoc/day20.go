package aoc

import (
	"fmt"
)

type Day20 struct{}

type Path20 struct {
	pos        Pos
	hasCheated bool
	inCheat    bool
	numCheat   int
	startCheat Pos
	endCheat   Pos
	time       int
}

type CheatPath struct {
	start Pos
	end   Pos
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

func GetCheatedPath(
	m []string, path Path20, seen map[Pos]bool, end Pos, time int, maxTime int, seenCheat map[CheatPath]Path20,
) int {
	if time > maxTime {
		return 0
	}
	if path.pos == end {
		path.time = time
		if cheatPath, s := seenCheat[CheatPath{path.startCheat, path.endCheat}]; s {
			if path.time < cheatPath.time {
				seenCheat[CheatPath{path.startCheat, path.endCheat}] = path
			}
		} else {
			seenCheat[CheatPath{path.startCheat, path.endCheat}] = path
		}
		return 1
	}
	adjacents := path.pos.GetAdjacent(m)
	count := 0
	seen[path.pos] = true
	for _, adj := range adjacents {
		if s, e := seen[adj]; s && e {
			continue
		}
		if m[adj.x][adj.y] == '#' && (!path.hasCheated || (path.inCheat && path.numCheat > 0)) {
			count += GetCheatedPath(
				m, Path20{
					pos:        adj,
					hasCheated: true,
					inCheat:    true,
					numCheat:   path.numCheat - 1,
					startCheat: ternary(path.inCheat, path.startCheat, path.pos),
				}, seen, end, time+1, maxTime, seenCheat,
			)
		}
		if m[adj.x][adj.y] != '#' {
			if path.inCheat {
				if _, s := seenCheat[CheatPath{path.startCheat, adj}]; s {
					continue
				}
				count += GetCheatedPath(
					m, Path20{
						pos:        adj,
						hasCheated: path.hasCheated,
						inCheat:    false,
						numCheat:   path.numCheat,
						startCheat: path.startCheat,
						endCheat:   adj,
					},
					seen, end, time+1, maxTime, seenCheat,
				)
			} else {
				count += GetCheatedPath(
					m, Path20{
						pos:        adj,
						hasCheated: path.hasCheated,
						inCheat:    path.inCheat,
						numCheat:   path.numCheat,
						startCheat: path.startCheat,
						endCheat:   path.endCheat,
					}, seen, end, time+1, maxTime, seenCheat,
				)
			}
		}
	}
	seen[path.pos] = false
	return count
}

func (d Day20) Part1(path string) {
	m := getMap(path)
	start := GetPos(m, 'S')
	end := GetPos(m, 'E')
	fmt.Println(start, end)
	bestTime := GetBestTime(m, start, end)
	fmt.Println("bestTime", bestTime)
	startPath := Path20{pos: start, numCheat: 20}
	cheatPath := map[CheatPath]Path20{}
	fmt.Println(GetCheatedPath(m, startPath, make(map[Pos]bool), end, 0, bestTime-50, cheatPath))
	fmt.Println(len(cheatPath))

	countByImp := make(map[int]int)
	for _, p := range cheatPath {
		countByImp[bestTime-p.time] += 1
		fmt.Println(p)
	}

	fmt.Println(countByImp)
}

func (d Day20) Part2(path string) {

}
