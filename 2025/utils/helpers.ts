import fs from "fs";
import path from "path";
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export type Pos = {
    row: number
    col: number
}

export type Grid<T> = T[][]

const UP_LEFT: [number, number] = [-1, -1]
const UP: [number, number] = [-1, 0]
const UP_RIGHT: [number, number] = [-1, 1]
const DOWN_LEFT: [number, number] = [1, -1]
const DOWN: [number, number] = [1, 0]
const DOWN_RIGHT: [number, number] = [1, 1]
const LEFT: [number, number] = [0, -1]
const RIGHT: [number, number] = [0, 1]

const ALL_ADJ: [number, number][] = [
    UP_LEFT,
    UP,
    UP_RIGHT,
    DOWN_LEFT,
    DOWN,
    DOWN_RIGHT,
    LEFT,
    RIGHT,   
]

export function readInput(inputFile: string): string{
    const filePath = path.join(__dirname, "../inputs", inputFile);
    const data = fs.readFileSync(filePath).toString()
    return data
}


export function getGridString(s: string): Grid<string>{
    return s.split("\n").map(
        (line) => Array(...line)
    )
}


export function getAdjacent<T>(pos: Pos, grid: Grid<T>): T[]{
    const rowLen = grid.length
    const colLen = (grid[0] as T[]).length
    const res: T[] = []
    ALL_ADJ.forEach(
        ([deltaRow, deltaCol]) => {
            const newRow = (pos.row + deltaRow)
            const newCol = (pos.col + deltaCol)
            if (
                newRow >= 0 && 
                newRow < rowLen && 
                newCol >= 0 && 
                newCol < colLen && 
                grid[newRow] !== undefined && 
                grid[newRow][newCol] !== undefined
            ){
                res.push(grid[newRow][newCol])
            }
        }
    )
    return res
}

export function getAdjacentPos<T>(pos: Pos, grid: Grid<T>): Pos[]{
    const rowLen = grid.length
    const colLen = (grid[0] as T[]).length
    const res: Pos[] = []
    ALL_ADJ.forEach(
        ([deltaRow, deltaCol]) => {
            const newRow = (pos.row + deltaRow)
            const newCol = (pos.col + deltaCol)
            if (
                newRow >= 0 && 
                newRow < rowLen && 
                newCol >= 0 && 
                newCol < colLen
            ){
                res.push({row: newRow, col: newCol})
            }
        }
    )
    return res
}

export function mult(arr: number[]){
    return arr.reduce((a, b) => a * b, 1)
}

export function sum(arr: number[]): number{
    return arr.reduce((a, b) => a + b, 0)
}