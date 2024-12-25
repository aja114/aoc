package aoc

import (
	"bufio"
	"os"
	"slices"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type Day interface {
	Part1(path string)
	Part2(path string)
}

func getMap(path string) []string {
	f, err := os.Open(path)
	check(err)
	arr := make([]string, 0)
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		arr = append(arr, scanner.Text())
	}
	return arr
}

type Dir int

type Pos struct {
	x, y int
}

func (p Pos) Sub(p1 Pos) Pos {
	return Pos{x: p.x - p1.x, y: p.y - p1.y}
}

func (p Pos) Add(p1 Pos) Pos {
	return Pos{x: p.x + p1.x, y: p.y + p1.y}
}

func (p Pos) Invert() Pos {
	return Pos{x: -p.x, y: -p.y}
}

type PosDir struct {
	x, y int
	d    Dir
}

const (
	Up Dir = iota
	Right
	Down
	Left
)

var DirDelta = map[Dir]Pos{
	Up:    {x: -1, y: 0},
	Right: {x: 0, y: 1},
	Down:  {x: 1, y: 0},
	Left:  {x: 0, y: -1},
}

func (p Pos) isValid(arr []string) bool {
	return p.x >= 0 && p.x < len(arr) && p.y >= 0 && p.y < len(arr[0])
}

func (p PosDir) isValid(arr []string) bool {
	return p.toPos().isValid(arr)
}

func (p PosDir) toPos() Pos {
	return Pos{
		x: p.x,
		y: p.y,
	}
}

func (p Pos) WithDir(dir Dir) PosDir {
	return PosDir{
		x: p.x,
		y: p.y,
		d: dir,
	}
}

func (p PosDir) getNext() Pos {
	return p.toPos().Add(DirDelta[p.d])
}

func GetEl(m [][]rune, pos Pos) rune {
	return m[pos.x][pos.y]
}

func ternary[T any](condition bool, trueVal, falseVal T) T {
	if condition {
		return trueVal
	}
	return falseVal
}

func (pos Pos) GetAdjacent(arr []string) []Pos {
	up := Pos{
		x: pos.x - 1,
		y: pos.y,
	}
	right := Pos{
		x: pos.x,
		y: pos.y + 1,
	}
	down := Pos{
		x: pos.x + 1,
		y: pos.y,
	}
	left := Pos{
		x: pos.x,
		y: pos.y - 1,
	}
	adj := []Pos{up, right, down, left}
	return slices.DeleteFunc(adj, func(x Pos) bool { return !x.isValid(arr) })
}

func getPos(arr []string, target rune) Pos {
	for i, l := range arr {
		for j, el := range l {
			if el == target {
				return Pos{
					x: i,
					y: j,
				}
			}
		}
	}
	return Pos{}
}

func getAllPos(arr []string, target rune) []Pos {
	positions := []Pos{}
	for i, l := range arr {
		for j, el := range l {
			if el == target {
				positions = append(positions, Pos{
					x: i,
					y: j,
				})
			}
		}
	}
	return positions
}
