package aoc

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Day14 struct{}

type PosVel struct {
	pos    Pos
	vx, vy int
}

func (p PosVel) Move(g GridDim) PosVel {
	pos := Pos{
		x: (p.pos.x + p.vx + g.x) % g.x,
		y: (p.pos.y + p.vy + g.y) % g.y,
	}
	return PosVel{pos: pos, vx: p.vx, vy: p.vy}
}

type GridDim struct {
	x int
	y int
}

func ParseLine(l string) PosVel {
	parts := strings.Split(l, " ")
	pos := strings.SplitN(parts[0][2:], ",", 2)
	x, err := strconv.Atoi(pos[1])
	check(err)
	y, err := strconv.Atoi(pos[0])
	check(err)
	vel := strings.SplitN(parts[1][2:], ",", 2)
	vx, err := strconv.Atoi(vel[1])
	check(err)
	vy, err := strconv.Atoi(vel[0])
	check(err)
	return PosVel{pos: Pos{x: x, y: y}, vx: vx, vy: vy}
}

func ParsePos(path string) []PosVel {
	f, err := os.Open(path)
	check(err)
	posVel := make([]PosVel, 0)
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()
		posVel = append(posVel, ParseLine(line))
	}
	return posVel
}

func Move(p PosVel, g GridDim, n int) PosVel {
	for i := 0; i < n; i++ {
		p = p.Move(g)
	}
	return p
}

func CalcScore(p Pos, g GridDim, scores map[int]int) {
	left := false
	top := false
	if g.x%2 == 1 && p.x == g.x/2 {
		return
	}
	if g.y%2 == 1 && p.y == g.y/2 {
		return
	}
	if (p.x - (g.x / 2)) < 0 {
		left = true
	}
	if (p.y - (g.y / 2)) < 0 {
		top = true
	}

	if left && top {
		scores[0] += 1
	} else if !left && top {
		scores[1] += 1
	} else if left && !top {
		scores[2] += 1
	} else {
		scores[3] += 1
	}
}

func (d Day14) Part1(path string) {
	posVel := ParsePos(path)
	g := GridDim{x: 103, y: 101}
	fmt.Println("Grid:", g)
	n := 100
	scores := make(map[int]int)
	positions := make([]Pos, 0)
	for _, pv := range posVel {
		pos := Move(pv, g, n).pos
		positions = append(positions, pos)
		CalcScore(pos, g, scores)
	}
	PrintMap(g, positions)
	fmt.Println(scores[0] * scores[1] * scores[2] * scores[3])
}

func PrintMap(g GridDim, pos []Pos) {
	m := make([][]int, g.x)
	for i := range m {
		m[i] = make([]int, g.y)
	}
	for _, p := range pos {
		m[p.x][p.y] = 1
	}

	// nasty heuristic for part2
	found := false
	for i := 0; i < g.x; i++ {
		res := 0
		for j := 0; j < g.y; j++ {
			if res >= 10 {
				found = true
				break
			}
			if m[i][j] == 1 {
				res += 1
			} else {
				res = 0
			}
		}
		if found {
			break
		}
	}
	if !found {
		return
	}

	for _, line := range m {
		for _, el := range line {
			if el == 0 {
				fmt.Printf(".")
			} else {
				fmt.Printf("%d", el)
			}
		}
		fmt.Printf("\n")
	}
	fmt.Println()
}

func (d Day14) Part2(path string) {
	posVel := ParsePos(path)
	g := GridDim{x: 103, y: 101}
	fmt.Println("Grid:", g)
	n := 100000
	positions := make([]Pos, len(posVel))
	for i := 0; i < n; i++ {
		for j, pv := range posVel {
			posVelEl := Move(pv, g, 1)
			positions[j] = posVelEl.pos
			posVel[j] = posVelEl
		}
		fmt.Println(i)
		PrintMap(g, positions)
	}
}
