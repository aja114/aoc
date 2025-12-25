import { readInput } from "@utils/helpers.ts"

function part1(){
    const inp = readInput("day3.txt")
    let res = 0
    inp.split("\n").forEach(
        (line: string) => {
            let maxL = 0
            let pos = 0
            let maxR = 0
            for (let i = 0; i < line.length - 1; i+=1){
                const el = line[i]
                if (Number(el) > maxL){
                    maxL = Number(el)
                    pos = i
                }
            }
            for (let j = pos+1; j < line.length; j+=1){
                const el = line[j]
                if (Number(el) > maxR){
                    maxR = Number(el)
                }
            }
            res += maxL * 10 + maxR
        }
    )
    console.log(res)
}

const SEQ_LEN = 12


function argMax(arr: number[]): number {
    return (
        arr
        .map((x, i) => [x, i] as [number, number])
        .reduce((r, a) => (a[0] > r[0] ? a : r))[1]
    );
}

function largestSubSeq(line: string): number{
    let res = ""
    let currLine = line
    while (true){
        if (res.length == SEQ_LEN){
            return Number(res)
        }
        const candidates = (
            currLine
            .slice(0, currLine.length - (SEQ_LEN - res.length - 1))
            .split("")
            .map((x) => Number(x))
        )
        const i = argMax(candidates)
        res += currLine[i]
        currLine = currLine.slice(i + 1)
    }
}

function part2(){
    const inp = readInput("day3.txt")
    let res = 0
    inp.split("\n").forEach(
        (line) => {
            res += largestSubSeq(line)
        }
    )
    console.log(res)
}

function main(){
    part1()
    part2()
}

main()