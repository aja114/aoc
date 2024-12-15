package aoc

import (
	"fmt"
	"os"
	"strconv"
)

type Day9 struct{}

func getID(i int) int {
	return (i + 1) / 2
}

func isFreeBlocks(i int) bool {
	return i%2 != 0
}

func getVal(b byte) int {
	v, err := strconv.Atoi(string(b))
	check(err)
	return v
}

func (d Day9) Part1(path string) {
	str := ""
	line, err := os.ReadFile(path)
	check(err)
	checksum := 0
	startPtr := 0
	endPtr := len(line) - 1
	idx := 0
	var availableFreeBlocks int
	var endBlocks int
	for startPtr < endPtr {
		if isFreeBlocks(endPtr) {
			endPtr -= 1
		} else if !isFreeBlocks(endPtr) && endBlocks == 0 {
			endBlocks = getVal(line[endPtr])
		} else if !isFreeBlocks(startPtr) {
			for i := 0; i < getVal(line[startPtr]); i++ {
				checksum += getID(startPtr) * idx
				idx += 1
				str = fmt.Sprintf("%s%d", str, getID(startPtr))
			}
			startPtr += 1
		} else if isFreeBlocks(startPtr) && availableFreeBlocks == 0 {
			availableFreeBlocks = getVal(line[startPtr])
			if availableFreeBlocks == 0 {
				startPtr += 1
			}
		} else {
			checksum += getID(endPtr) * idx
			availableFreeBlocks -= 1
			endBlocks -= 1
			idx += 1
			str = fmt.Sprintf("%s%d", str, getID(endPtr))
			if availableFreeBlocks == 0 {
				startPtr += 1
			}
			if endBlocks == 0 {
				endPtr -= 1
			}
		}
	}
	if endBlocks > 0 {
		for i := 0; i < endBlocks; i++ {
			checksum += getID(endPtr) * idx
			idx += 1
			str = fmt.Sprintf("%s%d", str, getID(endPtr))
		}
	}
	fmt.Println(checksum)
}

type Block struct {
	full   bool
	size   int
	fileId int
}

func CalcChecksum(arr []Block) int {
	idx := 0
	checksum := 0
	for _, el := range arr {
		for i := 0; i < el.size; i++ {
			checksum += idx * el.fileId
			idx += 1
		}
	}
	return checksum
}

func (d Day9) Part2(path string) {
	line, err := os.ReadFile(path)
	arr := make([]Block, 0)
	check(err)
	idx := 0
	// Build array of blocks
	for i, el := range line {
		var block Block
		size, err := strconv.Atoi(string(el))
		check(err)
		if isFreeBlocks(i) {
			block = Block{full: false, size: size, fileId: 0}
		} else {
			block = Block{full: true, size: size, fileId: idx}
			idx += 1
		}
		arr = append(arr, block)
	}
	// Create a new array of blocks
	startPtr := 0
	endPtr := len(line) - 1
	newArr := make([]Block, 0)
	for startPtr < endPtr {
		if !arr[endPtr].full {
			endPtr -= 1
		} else if arr[startPtr].full {
			newArr = append(newArr, arr[startPtr])
			startPtr += 1
		} else {
			emptyBlock := arr[startPtr]
			i := endPtr
			for i > startPtr {
				if emptyBlock.size == 0 {
					newArr = append(newArr, emptyBlock)
					startPtr += 1
					break
				} else if arr[i].full && arr[i].size <= emptyBlock.size {
					newArr = append(newArr, arr[i])
					arr[i].full = false
					arr[i].fileId = 0
					emptyBlock.size -= arr[i].size
					i = endPtr - 1
				} else if !arr[i].full || arr[i].size > emptyBlock.size {
					i -= 1
				}
			}
			if emptyBlock.size != 0 {
				newArr = append(newArr, emptyBlock)
				startPtr += 1
			}
		}
	}
	// Add a final block if it is full
	if arr[startPtr].full {
		newArr = append(newArr, arr[startPtr])
	}
	fmt.Println(CalcChecksum(newArr))
}
