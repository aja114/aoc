package aoc

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Day13 struct{}

type Game struct {
	target  Pos
	buttonA Pos
	buttonB Pos
}

type Score struct {
	a int
	b int
}

var PointsA int = 3
var PointsB int = 1

func getButton(line string) Pos {
	arr := strings.Split(line, " ")
	x, err := strconv.Atoi(arr[2][2 : len(arr[2])-1])
	check(err)
	y, err := strconv.Atoi(arr[3][2:])
	check(err)
	return Pos{x: x, y: y}
}

func getTarget(line string) Pos {
	arr := strings.Split(line, " ")
	x, err := strconv.Atoi(arr[1][2 : len(arr[1])-1])
	check(err)
	y, err := strconv.Atoi(arr[2][2:])
	check(err)
	return Pos{x: x, y: y}
}

func getGames(path string) []Game {
	f, err := os.Open(path)
	check(err)
	scanner := bufio.NewScanner(f)
	i := 0
	var game Game
	games := make([]Game, 0)
	for scanner.Scan() {
		line := scanner.Text()
		if i%4 == 0 {
			game = Game{
				buttonA: getButton(line),
			}
		}
		if i%4 == 1 {
			game.buttonB = getButton(line)
		}
		if i%4 == 2 {
			game.target = getTarget(line)
		}
		if i%4 == 3 {
			games = append(games, game)
		}
		i += 1
	}
	return games
}

func compScore1(s Score) int {
	if s.a > 100 || s.b > 100 {
		return int(math.Inf(1))
	}
	return s.a*PointsA + s.b*PointsB
}

func compScore2(s Score) int {
	if s == infScore(-1) {
		return int(math.Inf(1))
	}
	return s.a*PointsA + s.b*PointsB
}

func infScore(val int) Score {
	return Score{val, val}
}

func getBestScore(game Game, infVal int) Score {
	num := game.buttonA.y*game.target.x - game.buttonA.x*game.target.y
	denom := game.buttonB.x*game.buttonA.y - game.buttonA.x*game.buttonB.y
	remainder := num % denom
	if remainder != 0 {
		return infScore(infVal)
	}
	b := num / denom
	num = (game.target.x - b*game.buttonB.x)
	denom = game.buttonA.x
	if remainder := num % denom; remainder != 0 {
		return infScore(infVal)
	}
	a := num / denom
	return Score{a, b}
}

func (d Day13) Part2(path string) {
	games := getGames(path)
	res := 0
	for _, game := range games {
		game.target.x += 10000000000000
		game.target.y += 10000000000000
		s := getBestScore(game, 101)
		score := compScore2(s)
		if score < int(math.Inf(1)) {
			res += score
		}
	}
	fmt.Println(res)
}

func (d Day13) Part1(path string) {
	games := getGames(path)
	res := 0
	for _, game := range games {
		s := getBestScore(game, -1)
		score := compScore2(s)
		if score < int(math.Inf(1)) {
			res += score
		}
	}
	fmt.Println(res)
}
