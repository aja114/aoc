package aoc

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type Day interface {
	Part1(path string)
	Part2(path string)
}
