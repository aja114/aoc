import { readInput } from "../utils/file.ts"

function _isRepeatedChar(s: string, j: number): boolean{
    // console.log("Checking for symbol", s.slice(0, j))
    const char = s.slice(0, j)
    for (let i=0; i<(s.length/j); i+=1){
        if (s.slice(i*j, i*j+j) !== char){
            return false
        }
    }
    return true
}

function isRepeated(id: number, midOnly: boolean): boolean{
    const idStr = String(id)
    // console.log("Checking for repeated", idStr)
    const l = idStr.length
    const mid = l / 2
    if (midOnly){
        return idStr.slice(0, mid) === idStr.slice(mid)
    } else{
        for (let j=1; j<=mid; j+=1){
            if (l % j !== 0){
                continue
            } else{
                if (_isRepeatedChar(idStr, j)){
                    // console.log("FOUND")
                    return true
                }
            }
        }
        return false
    }
}

function partCode(midOnly: boolean){
    const repeatedIds = []
    let repeatedIdsSum = 0
    const inp = readInput("day2.txt")
    const ranges = inp.split(",")
    ranges.forEach(
        (range: string) => {
            const startEnd = range.split("-")
            const s = Number(startEnd[0])
            const e = Number(startEnd[1])
            console.log("RANGES", s, e)
            for (let j=s; j<=e; j+=1){
                if (isRepeated(j, midOnly)){
                    repeatedIds.push(j)
                    repeatedIdsSum += j
                }
            }
        }
    )
    console.log(repeatedIds)
    console.log(repeatedIdsSum)
}

function part1() {
    console.log("Part 1")
    partCode(true)
}

function part2() {
    console.log("Part 1")
    partCode(false)
}

function main(){
  part1()
  part2()
}

main()