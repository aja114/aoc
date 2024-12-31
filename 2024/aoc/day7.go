package aoc

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Day7 struct{}

type Ops int

const (
	MUL Ops = iota
	ADD
)

func getOperations(path string) [][]int64 {
	f, err := os.Open(path)
	check(err)
	defer f.Close()
	scanner := bufio.NewScanner(f)
	ops := make([][]int64, 0)
	for scanner.Scan() {
		l := scanner.Text()
		values := strings.Split(l, " ")
		targetStr := values[0]
		target, err := strconv.ParseInt(targetStr[:len(targetStr)-1], 10, 64)
		check(err)
		operands := make([]int64, len(values))
		operands[0] = target
		for i, val := range values[1:] {
			operands[i+1], err = strconv.ParseInt(val, 10, 64)
			check(err)
		}
		ops = append(ops, operands)
	}
	return ops
}

func checkOps(target int64, curr int64, remaings []int64, concat bool) bool {
	if curr > target {
		return false
	}
	if len(remaings) == 0 {
		return curr == target
	}
	head, tail := remaings[0], remaings[1:]
	res := checkOps(target, curr*head, tail, concat) || checkOps(target, curr+head, tail, concat)
	if concat {
		conc, err := strconv.Atoi(strconv.Itoa(int(curr)) + strconv.Itoa(int(head)))
		check(err)
		res = res || checkOps(target, int64(conc), tail, concat)
	}
	return res
}

func (d Day7) Part1(path string) {
	ops := getOperations(path)
	res := int64(0)
	for _, values := range ops {
		target, operands := values[0], values[1:]
		if checkOps(target, operands[0], operands[1:], false) {
			res += int64(target)
		}
	}
	fmt.Println(res)
}

func (d Day7) Part2(path string) {
	ops := getOperations(path)
	res := int64(0)
	for _, values := range ops {
		target, operands := values[0], values[1:]
		if checkOps(target, operands[0], operands[1:], true) {
			res += int64(target)
		}
	}
	fmt.Println(res)
}
