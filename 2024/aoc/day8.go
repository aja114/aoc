package aoc

import "fmt"

type Day8 struct{}

func getAntinodes(positions []Pos, m []string) []Pos {
	antinodes := make([]Pos, 0)
	for i := range positions {
		for j := i + 1; j < len(positions); j++ {
			ant1, ant2 := getAntinode(positions[i], positions[j])
			if ant1.isValid(m) {
				antinodes = append(antinodes, ant1)
			}
			if ant2.isValid(m) {
				antinodes = append(antinodes, ant2)
			}
		}
	}
	return antinodes
}

func getAntinode(p1 Pos, p2 Pos) (Pos, Pos) {
	diff := p2.Sub(p1)
	return p2.Add(diff), p1.Add(diff.Invert())
}

func getAntenas(m []string) map[string][]Pos {
	antenas := make(map[string][]Pos)
	for i := range m {
		for j := range m[i] {
			a := string(m[i][j])
			if a != "." {
				if _, exists := antenas[a]; exists {
					antenas[a] = append(antenas[a], Pos{x: i, y: j})
				} else {
					antenas[a] = []Pos{{x: i, y: j}}
				}
			}
		}
	}
	return antenas
}

func (d Day8) Part1(path string) {
	m := getMap(path)
	antenas := getAntenas(m)
	allAntenas := make(map[Pos]bool)
	for _, v := range antenas {
		for _, ant := range getAntinodes(v, m) {
			allAntenas[ant] = true
		}
	}

	fmt.Println(len(allAntenas))
}

func getAntinodes2(positions []Pos, m []string) []Pos {
	antinodes := make([]Pos, 0)
	for i := range positions {
		for j := i + 1; j < len(positions); j++ {
			ants := getAntinode2(positions[i], positions[j], m)
			antinodes = append(antinodes, ants...)
		}
	}
	return antinodes
}

func getAntinode2(p1 Pos, p2 Pos, m []string) []Pos {
	diff := p2.Sub(p1)
	res := make([]Pos, 0)
	ant1 := p2
	for ant1.isValid(m) {
		res = append(res, ant1)
		ant1 = ant1.Add(diff)
	}
	ant2 := p1
	for ant2.isValid(m) {
		res = append(res, ant2)
		ant2 = ant2.Add(diff.Invert())
	}
	return res
}

func (d Day8) Part2(path string) {
	m := getMap(path)
	antenas := getAntenas(m)
	allAntenas := make(map[Pos]bool)
	for _, v := range antenas {
		for _, ant := range getAntinodes2(v, m) {
			allAntenas[ant] = true
		}
	}
	fmt.Println(len(allAntenas))
}
