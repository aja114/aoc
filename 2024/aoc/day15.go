package aoc

import (
	"bufio"
	"fmt"
	"os"
)

type Day15 struct{}

func GetDir(r rune) Dir {
	switch r {
	case '^':
		return Up
	case '>':
		return Right
	case 'v':
		return Down
	case '<':
		return Left
	default:
		panic("Bad value for direction")
	}
}

func (d Day15) GetMapDir(path string) ([][]rune, []Dir) {
	f, err := os.Open(path)
	check(err)
	scanner := bufio.NewScanner(f)
	directions := make([]Dir, 0)
	m := make([][]rune, 0)
	parseDir := false
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			parseDir = true
			continue
		}
		if !parseDir {
			m = append(m, []rune(line))
		} else {
			for _, el := range line {
				directions = append(directions, GetDir(el))
			}
		}
	}
	return m, directions
}

func (d Day15) Move(m [][]rune, pos PosDir) Pos {
	nextPos := pos.getNext()
	if m[nextPos.x][nextPos.y] == '.' {
		return nextPos
	}
	if m[nextPos.x][nextPos.y] == '#' {
		return pos.toPos()
	}
	if m[nextPos.x][nextPos.y] == 'O' {
		runningPos := pos
		for {
			runningPos = runningPos.getNext().WithDir(pos.d)
			if m[runningPos.x][runningPos.y] == '.' {
				m[runningPos.x][runningPos.y] = 'O'
				m[nextPos.x][nextPos.y] = '.'
				return nextPos
			}
			if m[runningPos.x][runningPos.y] == '#' {
				return pos.toPos()
			}
			if m[runningPos.x][runningPos.y] == 'O' {
				continue
			}
		}
	}
	panic("Unkown element met")
}

func (d Day15) PrintMap(m [][]rune, pos Pos) {
	for i, line := range m {
		for j, el := range line {
			curPos := Pos{x: i, y: j}
			if curPos == pos {
				fmt.Printf("@")
			} else {
				fmt.Printf("%c", el)
			}
		}
		fmt.Printf("\n")
	}
	fmt.Println()
}

func (d Day15) CalcScore(m [][]rune, el rune) int {
	res := 0
	for i, line := range m {
		for j := range line {
			if m[i][j] == el {
				res += i*100 + j
			}
		}
	}
	return res
}

func (d Day15) GetStartPos(m [][]rune) Pos {
	var pos Pos
	for i, line := range m {
		for j := range line {
			if m[i][j] == '@' {
				pos = Pos{x: i, y: j}
				m[i][j] = '.'
			}
		}
	}
	return pos
}

func (d Day15) Part1(path string) {
	m, dirs := d.GetMapDir(path)
	pos := d.GetStartPos(m)
	for _, dir := range dirs {
		pos = d.Move(m, PosDir{x: pos.x, y: pos.y, d: dir})
	}
	fmt.Println(d.CalcScore(m, 'O'))
}

func (d Day15) UpdateMap(m [][]rune) [][]rune {
	upMap := make([][]rune, len(m))
	for i := range m {
		upMap[i] = make([]rune, 2*len(m[0]))
		for j := range m[i] {
			switch m[i][j] {
			case '.':
				upMap[i][2*j] = '.'
				upMap[i][2*j+1] = '.'
			case '#':
				upMap[i][2*j] = '#'
				upMap[i][2*j+1] = '#'
			case 'O':
				upMap[i][2*j] = '['
				upMap[i][2*j+1] = ']'
			case '@':
				upMap[i][2*j] = '@'
				upMap[i][2*j+1] = '.'
			}
		}
	}
	return upMap
}

type Box struct {
	left  Pos
	right Pos
}

func (b Box) FromRight(right Pos) Box {
	return Box{
		left:  right.WithDir(Left).getNext(),
		right: right,
	}
}

func (b Box) FromLeft(left Pos) Box {
	return Box{
		left:  left,
		right: left.WithDir(Right).getNext(),
	}
}

func (b Box) GetUpDown(m [][]rune, dir Dir) []Box {
	boxes := make([]Box, 0)
	if GetEl(m, b.left.WithDir(dir).getNext()) == '[' {
		return []Box{Box{}.FromLeft(b.left.WithDir(dir).getNext())}
	}
	if GetEl(m, b.left.WithDir(dir).getNext()) == ']' {
		boxes = append(boxes, Box{}.FromRight(b.left.WithDir(dir).getNext()))
	}
	if GetEl(m, b.right.WithDir(dir).getNext()) == ']' {
		return []Box{Box{}.FromRight(b.right.WithDir(dir).getNext())}
	}
	if GetEl(m, b.right.WithDir(dir).getNext()) == '[' {
		boxes = append(boxes, Box{}.FromLeft(b.right.WithDir(dir).getNext()))
	}
	return boxes
}

func (b Box) Move(m [][]rune, dir Dir) {
	m[b.left.x][b.left.y] = '.'
	m[b.right.x][b.right.y] = '.'
	nextLeft := b.left.WithDir(dir).getNext()
	nextRight := b.right.WithDir(dir).getNext()
	m[nextLeft.x][nextLeft.y] = '['
	m[nextRight.x][nextRight.y] = ']'
}

func (d Day15) MoveHor(m [][]rune, b Box, dir Dir) bool {
	if dir == Left {
		nextPos := b.left.WithDir(dir).getNext()
		if GetEl(m, nextPos) == ']' {
			if d.MoveHor(m, Box{}.FromRight(nextPos), dir) {
				b.Move(m, dir)
				return true
			}
		} else if GetEl(m, nextPos) == '.' {
			b.Move(m, dir)
			return true
		}
	}
	if dir == Right {
		nextPos := b.right.WithDir(dir).getNext()
		if GetEl(m, nextPos) == '[' {
			if d.MoveHor(m, Box{}.FromLeft(nextPos), dir) {
				b.Move(m, dir)
				return true
			}
		} else if GetEl(m, nextPos) == '.' {
			b.Move(m, dir)
			return true
		}
	}
	return false
}

func (d Day15) MoveVert(m [][]rune, boxes []Box, dir Dir) bool {
	nextBoxes := make([]Box, 0)
	for _, b := range boxes {
		leftNext := b.left.WithDir(dir).getNext()
		rightNext := b.right.WithDir(dir).getNext()
		if m[leftNext.x][leftNext.y] == '#' || m[rightNext.x][rightNext.y] == '#' {
			return false
		}
		nextBoxes = append(nextBoxes, b.GetUpDown(m, dir)...)
	}
	if len(nextBoxes) == 0 || d.MoveVert(m, nextBoxes, dir) {
		for _, b := range boxes {
			b.Move(m, dir)
		}
		return true
	}
	return false
}

func (d Day15) Move2(m [][]rune, pos PosDir) Pos {
	nextPos := pos.getNext()
	if m[nextPos.x][nextPos.y] == '.' {
		return nextPos
	}
	if m[nextPos.x][nextPos.y] == '#' {
		return pos.toPos()
	}
	// Push to the right && left
	if pos.d == Right && GetEl(m, nextPos) == '[' {
		return ternary(d.MoveHor(m, Box{}.FromLeft(nextPos), pos.d), nextPos, pos.toPos())
	}
	if pos.d == Left && GetEl(m, nextPos) == ']' {
		return ternary(d.MoveHor(m, Box{}.FromRight(nextPos), pos.d), nextPos, pos.toPos())
	}
	// Push to the up && down
	if (pos.d == Up || pos.d == Down) && m[nextPos.x][nextPos.y] == '[' {
		return ternary(d.MoveVert(m, []Box{Box{}.FromLeft(nextPos)}, pos.d), nextPos, pos.toPos())
	}
	if (pos.d == Up || pos.d == Down) && m[nextPos.x][nextPos.y] == ']' {
		return ternary(d.MoveVert(m, []Box{Box{}.FromRight(nextPos)}, pos.d), nextPos, pos.toPos())
	}
	panic(fmt.Sprintf("Unkown combination met: %v, %c", pos, m[nextPos.x][nextPos.y]))
}

func (d Day15) Part2(path string) {
	m, dirs := d.GetMapDir(path)
	m = d.UpdateMap(m)
	pos := d.GetStartPos(m)
	for _, dir := range dirs {
		pos = d.Move2(m, PosDir{x: pos.x, y: pos.y, d: dir})
	}
	fmt.Println(d.CalcScore(m, '['))
}
