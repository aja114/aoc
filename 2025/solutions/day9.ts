import { readInput } from "@utils/helpers.ts";

type Point2D = {
    x: number
    y: number
}

type SparseGrid = {
    points: Record<string, Point2D>,
    maxX: number,
    maxY: number
}


function getPoints(): Point2D[]{
    return readInput("day9.txt").split("\n").map(
        (s) => {
            const [y, x] = s.split(",")
            if (x === undefined || y === undefined){
                throw Error("Invalid Input")
            }
            return {x: Number(x), y: Number(y)}
        }
    )
}

function surface(p1: Point2D, p2: Point2D): number{
    return (Math.abs(p2.x-p1.x)+1) * (Math.abs(p2.y-p1.y)+1)
}


function printSparseGrid(grid: SparseGrid){
    for (let x=0; x<grid.maxX+2; x+=1){
        let row = []
        for (let y=0; y<=grid.maxY+2; y+=1){
            const exists = grid.points[
                JSON.stringify({x, y})
            ] !== undefined
            if (exists){
                row.push("X")
            } else{
                row.push(".")
            }
        }
        row.push("\n")
        console.log(row.join(""))
    }
}

function createSparseGrid(points: Point2D[]): SparseGrid{
    const sparseGrid: SparseGrid = {
        points: {},
        maxX: 0,
        maxY: 0,
    }
    for (let j=0; j<points.length; j+=1){
        const currPoint = points[j]
        const nextPoint = points[(j+1) % points.length]
        if (currPoint && nextPoint){
            sparseGrid.maxX = Math.max(sparseGrid.maxX, currPoint.x)
            sparseGrid.maxY = Math.max(sparseGrid.maxY, currPoint.y)
            if (currPoint.x !== nextPoint.x){
                const diff = Math.abs(nextPoint.x - currPoint.x)
                const op = nextPoint.x > currPoint.x ? 1 : -1
                for (let x=0; x<diff; x+=1){
                    const p = {
                        x: currPoint.x + x * op,
                        y: currPoint.y,
                    }
                    sparseGrid.points[JSON.stringify(p)] = p
                }
            } else{
                const diff = Math.abs(nextPoint.y - currPoint.y)
                const op = nextPoint.y > currPoint.y ? 1 : -1 
                for (let y=0; y<diff; y+=1){
                    const p = {
                        x: currPoint.x,
                        y: currPoint.y + y * op,
                    }
                    sparseGrid.points[JSON.stringify(p)] = p
                }
            }
        }
    }
    return sparseGrid
}

function isPointInGrid(point: Point2D, grid: SparseGrid): boolean{
    let isIn = false
    for (let i=0; i<grid.maxX; i+=1){
        const p = {x:i, y:point.y}
        if (point.x === i){
            return isIn
        }

        if (grid.points[JSON.stringify(p)] !== undefined){
            isIn = !isIn
        }
    }
    return false
}

function part1(){
    const points = getPoints()
    let maxSurface = 0
    points.forEach(
        (p1, i) => {
            for (let j=i+1; j<points.length; j+=1){
                const p2 = points[j] as Point2D
                if (surface(p1, p2) > maxSurface){
                    maxSurface = surface(p1, p2)
                }
            }
        }
    )
    console.log(maxSurface)
}

function part2(){
    const points = getPoints()
    const sparseGrid = createSparseGrid(points)
    let maxSurface = 0
    points.forEach(
        (p1, i) => {
            console.log(i)
            for (let j=i+1; j<points.length; j+=1){
                const p2 = points[j] as Point2D
                if (surface(p1, p2) > maxSurface){
                    maxSurface = surface(p1, p2)
                }
            }
        }
    )
    // console.log(sparseGrid)
    // printSparseGrid(sparseGrid)
    console.log(maxSurface)
}

function main(){
    part2()
}

main()