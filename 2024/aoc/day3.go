package aoc

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Day3 struct{}

func getStr(path string) string {
	f, err := os.Open(path)
	check(err)
	defer f.Close()
	reader := io.Reader(f)
	p, err := io.ReadAll(reader)
	check(err)
	return string(p)
}

func calcMul(s string) int {
	num := strings.Split(s[4:len(s)-1], ",")
	res := 1
	for _, el := range num {
		val, err := strconv.Atoi(el)
		check(err)
		res *= val
	}
	return res
}

func findAndCalc(s string) int {
	r, err := regexp.Compile("mul\\([0-9]{1,3},[0-9]{1,3}\\)")
	check(err)
	res := 0
	for _, el := range r.FindAllString(s, -1) {
		res += calcMul(el)
	}
	return res
}

func (d Day3) Part1(path string) {
	inp := getStr(path)
	fmt.Println(findAndCalc(inp))
}

func (d Day3) Part2(path string) {
	inp := getStr(path)
	inp += "do()"
	// Doing some trickery because golang does not support negative lookahead
	inp = strings.ReplaceAll(inp, "[", "{")
	inp = strings.ReplaceAll(inp, "]", "}")
	inp = strings.ReplaceAll(inp, "don't", "[")
	inp = strings.ReplaceAll(inp, "do", "]")
	do := "\\]"
	dont := "\\["
	pat := fmt.Sprintf("%s(([^%s]*?))%s", dont, do, do)
	r, err := regexp.Compile(pat)
	check(err)
	inp = r.ReplaceAllString(inp, "")
	fmt.Println(findAndCalc(inp))
}
