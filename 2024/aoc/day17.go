package aoc

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Day17 struct{}

type Inst int

const (
	ADV Inst = iota // rA / 2**CombOp -> rA
	BXL             // rB xor LitOp -> rB
	BST             // CombOp % 8 -> rB
	JNZ             // rA == 0 -> pass || rA != 0 -> Inst = LitOp
	BXC             // rB XOR rC -> rC
	OUT             // CombOp % 8 -> print
	BDV             // rA / 2**CombOp -> rB
	CDV             // rA / 2**CombOp -> rC
)

type Registers struct {
	A int
	B int
	C int
}

type State17 struct {
	reg     Registers
	instPtr int
}

func (s State17) isDone(inst []InstOp) bool {
	return s.instPtr >= len(inst)
}

type InstOp struct {
	inst Inst
	op   int
}

func GetComboOp(op int, registers Registers) int {
	if op <= 3 {
		return op
	}
	if op == 4 {
		return registers.A
	}
	if op == 5 {
		return registers.B
	}
	if op == 6 {
		return registers.C
	}
	panic("Bad operand")
}

func RunOp(inst InstOp, s State17, stdout []string) (State17, []string) {
	switch inst.inst {
	case ADV:
		s.reg.A = s.reg.A / IntPow(2, GetComboOp(inst.op, s.reg))
	case BXL:
		s.reg.B = s.reg.B ^ inst.op
	case BST:
		s.reg.B = GetComboOp(inst.op, s.reg) % 8
	case JNZ:
		if s.reg.A == 0 {
			s.instPtr += 1
			return s, stdout
		}
		s.instPtr = inst.op / 2
		return s, stdout
	case BXC:
		s.reg.B = s.reg.B ^ s.reg.C
	case OUT:
		// fmt.Println(GetComboOp(inst.op, s.reg) % 8)
		res := strconv.Itoa(GetComboOp(inst.op, s.reg) % 8)
		stdout = append(stdout, res)
	case BDV:
		s.reg.B = s.reg.A / IntPow(2, GetComboOp(inst.op, s.reg))
	case CDV:
		s.reg.C = s.reg.A / IntPow(2, GetComboOp(inst.op, s.reg))
	}
	s.instPtr += 1
	return s, stdout
}

func GetStateInst(path string) (State17, []InstOp) {
	s := State17{
		reg:     Registers{},
		instPtr: 0,
	}
	f, err := os.Open(path)
	check(err)
	defer f.Close()
	scanner := bufio.NewScanner(f)

	scanner.Scan()
	t := scanner.Text()
	regStr := strings.Split(t, " ")
	regInt, err := strconv.Atoi(regStr[2])
	check(err)
	s.reg.A = regInt

	scanner.Scan()
	t = scanner.Text()
	regStr = strings.Split(t, " ")
	regInt, err = strconv.Atoi(regStr[2])
	check(err)
	s.reg.B = regInt

	scanner.Scan()
	t = scanner.Text()
	regStr = strings.Split(t, " ")
	regInt, err = strconv.Atoi(regStr[2])
	check(err)
	s.reg.C = regInt

	scanner.Scan()
	scanner.Scan()
	instOp := make([]InstOp, 0)
	t = scanner.Text()
	instStr := strings.Split(t[9:], ",")
	i := 0
	for i < len(instStr) {
		inst, err := strconv.Atoi(instStr[i])
		check(err)
		i += 1
		op, err := strconv.Atoi(instStr[i])
		check(err)
		i += 1
		instOp = append(instOp, InstOp{inst: Inst(inst), op: op})
	}
	return s, instOp
}

func (d Day17) Part1(path string) {
	s, inst := GetStateInst(path)
	fmt.Println(inst)
	stdout := make([]string, 0)
	for !s.isDone(inst) {
		fmt.Println(s, inst[s.instPtr])
		s, stdout = RunOp(inst[s.instPtr], s, stdout)
	}
	fmt.Println(s)
	fmt.Println(strings.Join(stdout, ","))
}

type State17WithPref struct {
	s    State17
	pref string
}

func (d Day17) Part2(path string) {
	startS, inst := GetStateInst(path)

	s := startS
	valA := 1
	s.reg.A = valA

	seenStates := make(map[State17WithPref]bool)

	expectedStdoutArr := make([]string, len(inst)*2)
	for j := 0; j < len(inst); j += 1 {
		expectedStdoutArr[2*j] = strconv.Itoa(int(inst[j].inst))
		expectedStdoutArr[2*j+1] = strconv.Itoa(inst[j].op)
	}
	expectedStdoutStr := strings.Join(expectedStdoutArr, "")
	fmt.Println("expected out", expectedStdoutArr, expectedStdoutStr)

	stdout := make([]string, 0)
	for true {
		stdoutStr := strings.Join(stdout, "")
		_, seen := seenStates[State17WithPref{s, stdoutStr}]
		seenStates[State17WithPref{s, stdoutStr}] = true
		if stdoutStr == expectedStdoutStr {
			fmt.Println(valA)
			return
		}
		if s.isDone(inst) || seen {
			fmt.Println(stdoutStr)
			s = startS
			stdout = make([]string, 0)
			valA = valA + 1
			s.reg.A = valA
			fmt.Println("restarting with", valA)
			if valA > 400 {
				return
			}
			continue
		}
		s, stdout = RunOp(inst[s.instPtr], s, stdout)
	}
}
