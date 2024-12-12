package aoc

import (
	"fmt"
)

type Day6 struct{}

var NextPos = map[Dir]Dir{
	Up:    Right,
	Right: Down,
	Down:  Left,
	Left:  Up,
}

func nextPos(pos PosDir, arr []string, fakObstPos Pos) PosDir {
	var npos Pos
	switch pos.d {
	case Up:
		npos = Pos{
			x: pos.x - 1,
			y: pos.y,
		}
	case Right:
		npos = Pos{
			x: pos.x,
			y: pos.y + 1,
		}
	case Down:
		npos = Pos{
			x: pos.x + 1,
			y: pos.y,
		}
	case Left:
		npos = Pos{
			x: pos.x,
			y: pos.y - 1,
		}
	}
	if npos.isValid(arr) {
		if arr[npos.x][npos.y] == '#' || npos == fakObstPos {
			return PosDir{
				x: pos.x,
				y: pos.y,
				d: NextPos[pos.d],
			}
		}
	}
	return PosDir{
		x: npos.x,
		y: npos.y,
		d: pos.d,
	}
}

func getStartPos(arr []string) PosDir {
	for i, l := range arr {
		for j, el := range l {
			if el == '^' {
				return PosDir{
					x: i,
					y: j,
					d: Up,
				}
			}
		}
	}
	return PosDir{}
}

func (d Day6) Part1(path string) {
	arr := getMap(path)
	posDir := getStartPos(arr)
	positions := make(map[Pos]bool)
	for posDir.isValid(arr) {
		positions[posDir.toPos()] = true
		posDir = nextPos(posDir, arr, Pos{x: -10, y: -10})
	}
	fmt.Println(len(positions))
}

func hasCycle(posDir PosDir, arr []string, newBlocker map[Pos]bool) {
	positions := make(map[PosDir]bool)
	newBlock := nextPos(posDir, arr, Pos{x: -1, y: -1}).toPos()
	if !newBlock.isValid(arr) || (newBlock == posDir.toPos()) || arr[newBlock.x][newBlock.y] == '#' {
		return
	}
	posDir = getStartPos(arr)
	for posDir.isValid(arr) {
		_, exist := positions[posDir]
		if exist {
			newBlocker[newBlock] = true
			return
		}
		positions[posDir] = true
		posDir = nextPos(posDir, arr, newBlock)
	}
}

func (d Day6) Part2(path string) {
	arr := getMap(path)
	posDir := getStartPos(arr)
	newBlocker := make(map[Pos]bool)
	for posDir.isValid(arr) {
		hasCycle(posDir, arr, newBlocker)
		posDir = nextPos(posDir, arr, Pos{x: -10, y: -10})
	}
	fmt.Println(len(newBlocker))
}
