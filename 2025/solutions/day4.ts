import { readInput, getGridString, getAdjacent, type Grid, type Pos, getAdjacentPos } from "@utils/file.ts"

function removeDFS(pos: Pos, grid: Grid<string>, withRecursion: boolean): number{
    const row = grid[pos.row]
    if (
        row !== undefined && 
        row[pos.col] === "@" &&
        (getAdjacent(pos, grid)
        .map((x) => x === "@" ? 1 : 0)
        .reduce((a: number, b: number) => a + b, 0) < 4)
    ){
        row[pos.col] = "."
        if (withRecursion){
            return (
                1 + getAdjacentPos(pos, grid).map(
                    (pos) => removeDFS(pos, grid, withRecursion)).reduce((a, b) => a + b, 0
                )
            )
        } else{
            return 1
        }
    }
    return 0
}

function _part(withRecursion: boolean){
    const grid = getGridString(readInput("day4.txt"))
    let res = 0
    grid.forEach(
        (rowVal, row) => {
            rowVal.forEach(
                (_, col) => {
                    const pos = {row, col}
                    res += removeDFS(pos, grid, withRecursion)
                }
            )
        }
    )
    console.log(res)
}

function part1(){
    _part(false)
}

function part2(){
    _part(true)
}

function main(){
    part1()
    part2()
}

main()