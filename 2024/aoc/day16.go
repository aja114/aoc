package aoc

import (
	"fmt"
	"math"
	"sync"
)

type Day16 struct{}

type Path struct {
	pos   Pos
	score int
	step  int
	dir   Dir
	hist  []Pos
}

func (p Path) getNextPaths(m []string, seen map[Pos]int, results chan<- []Path) {
	directions := []Dir{Up, Right, Down, Left}
	score, s := seen[p.pos]
	if s && score < p.score {
		results <- []Path{}
		return
	}
	nextPaths := make([]Path, 0)
	for _, dir := range directions {
		nextPos := p.pos.WithDir(dir).getNext()
		if !nextPos.isValid(m) || m[nextPos.x][nextPos.y] == '#' {
			continue
		}
		// Costly to copy the array every time
		newHist := make([]Pos, len(p.hist))
		copy(newHist, p.hist)
		nextPath := Path{
			pos:   nextPos,
			score: p.score + 1 + ternary((dir+p.dir)%2 == 1, 1000, 0),
			step:  p.step + 1,
			dir:   dir,
			hist:  append(newHist, nextPos),
		}
		nextPaths = append(nextPaths, nextPath)
	}
	results <- nextPaths
}

func (p Path) isSuccessful(m []string) bool {
	if m[p.pos.x][p.pos.y] == 'E' {
		fmt.Println("Succesful path", p.score, p.step)
		return true
	}
	return false
}

func (d Day16) GetSuccessfulPaths(m []string) []Path {
	startPath := Path{
		pos:   GetPos(m, 'S'),
		dir:   Right,
		score: 0,
		step:  0,
		hist:  []Pos{GetPos(m, 'S')},
	}
	paths := []Path{startPath}
	successfulPaths := make([]Path, 0)
	seen := make(map[Pos]int)
	for len(paths) > 0 {
		nexPaths := []Path{}
		results := make(chan []Path)
		var wg sync.WaitGroup
		for _, path := range paths {
			wg.Add(1)
			go func(p Path) {
				defer wg.Done()
				if p.isSuccessful(m) {
					successfulPaths = append(successfulPaths, p)
				} else {
					p.getNextPaths(m, seen, results)
				}
			}(path)
		}
		go func() {
			wg.Wait()
			close(results)
		}()
		for result := range results {
			nexPaths = append(nexPaths, result...)
		}
		// Update the cache
		for _, path := range paths {
			val, s := seen[path.pos]
			if s {
				seen[path.pos] = min(path.score, val)
			} else {
				seen[path.pos] = path.score
			}
		}
		paths = nexPaths
	}
	return successfulPaths
}

func (d Day16) Part1(path string) {
	m := getMap(path)
	successfulPaths := d.GetSuccessfulPaths(m)
	res := int(math.Inf(1))
	for _, sp := range successfulPaths {
		if sp.score < res {
			res = sp.score
		}
	}
	fmt.Println(res)
}

func (d Day16) Part2(path string) {
	m := getMap(path)
	successfulPaths := d.GetSuccessfulPaths(m)
	min := int(math.Inf(1))
	for _, sp := range successfulPaths {
		if sp.score < min {
			min = sp.score
		}
	}
	res := make(map[Pos]bool)
	for _, sp := range successfulPaths {
		if sp.score != min {
			continue
		}
		for _, pos := range sp.hist {
			res[pos] = true
		}
	}
	fmt.Println(len(res))
}
