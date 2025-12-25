import { readInput, getGridString, type Pos, type Grid } from "@utils/helpers.ts";


const splitterRe = new RegExp(/\^/g);

function part1(){
    const inp = readInput("day7.txt").split("\n")
    const beams: Set<number> = new Set()
    let res = 0
    beams.add(inp[0]?.indexOf("S") as number)
    for (let i=1; i<inp.length; i+=1){
        console.log(inp[i])
        console.log(beams)
        const matches = inp[i]?.matchAll(splitterRe)
        if (matches === undefined){
            continue
        }
        const splitters = new Set()
        for (const match of matches) {
            splitters.add(match.index)
        }
        const toSplit = beams.intersection(splitters)
        toSplit.forEach(
            (s) => {
                res += 1
                beams.add(s + 1)
                beams.add(s - 1)
                beams.delete(s)
            }
        )
    }
    console.log(res)
}

function posKey(pos: Pos): string{
    return `${pos.row}-${pos.col}`
}

function countPath(grid: Grid<string>, pos: Pos, memo: Record<string,number>): number{
    const key = posKey(pos)
    let res: number
    if (memo[key] !== undefined){
        return memo[key]
    }
    if (pos.row >= grid.length){
        return 1
    }
    if ((grid[pos.row] as string[])[pos.col] === "^"){
        res = (
            countPath(grid, {row: pos.row + 1, col: pos.col - 1}, memo) + 
            countPath(grid, {row: pos.row + 1, col: pos.col + 1}, memo)
        )
    } else {
        res = countPath(grid, {row: pos.row + 1, col: pos.col}, memo)
    }
    memo[key] = res
    return res
}

function part2(){
    const inp = readInput("day7.txt")
    const start = inp.indexOf("S") as number
    const grid = getGridString(inp)
    console.log(
        countPath(grid, {row: 0, col: start}, {})
    )
}

function main(){
    part1()
    part2()
}

main()