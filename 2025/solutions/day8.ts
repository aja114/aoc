import { readInput } from "@utils/helpers.ts"
import { Heap } from 'heap-js';

type Point = { 
    x: number
    y: number
    z: number
}

type Dist = {
    p1: Point
    p2: Point
    d: number
}

function dist(p1: Point, p2: Point): Dist{
    return {
        p1,
        p2,
        d: Math.sqrt(
            Math.pow(p1.x-p2.x, 2) +
            Math.pow(p1.y-p2.y, 2) +
            Math.pow(p1.z-p2.z, 2)
        )
    }
}

function appendToCircuits(
    circuits: Record<string, Set<Point>>, points: Set<Point>, 
){
    for (let i of Object.keys(circuits)){
        const c = circuits[i] as Set<Point>
        if (c && (c.intersection(points)).size > 0){
            delete circuits[i]
            return appendToCircuits(circuits, points.union(c))
        }
    }
    circuits[crypto.randomUUID()] = points
}

function getDistHeap(points: Point[]){
    const customPriorityComparator = (a: Dist, b: Dist) => a.d - b.d;
    const distHeap = new Heap(customPriorityComparator);
    points.forEach(
        (p1, i) => {
            for (let j=i+1; j<points.length; j+=1){
                const p2 = points[j] as Point
                distHeap.push(dist(p1, p2))
            }
        }
    )
    return distHeap
}

function getPoints(): Point[]{
    const points: Point[] = []
    const inp = readInput("day8.txt")
    inp.split("\n").forEach(
        (line: string, i: number) => {
            const [x, y, z] = line.split(",")
            points.push({
                x: Number(x), y: Number(y), z: Number(z)
            })
        }
    )
    return points
}

function part1(){
    const points = getPoints()
    const distHeap = getDistHeap(points)
    const circuits: Record<string, Set<Point>> = {}
    const N = 1000
    for (let _=0; _<N; _+=1){
        const d = distHeap.pop() as Dist;
        appendToCircuits(
            circuits, new Set([d.p1, d.p2])
        )
    }
    const circuitLength = Object.values(circuits).map((v) => v.size).toSorted((a, b) => b - a)
    const first = circuitLength[0]
    const second = circuitLength[1]
    const third = circuitLength[2]
    if (
        !(first && second && third)
    ){
        throw Error("Im done")
    }
    console.log(first * second * third)
}

function part2(){
    const points = getPoints()
    const distHeap = getDistHeap(points)
    const circuits: Record<string, Set<Point>> = {}
    let d = undefined;
    // Keep going until we've reached a single circuit
    while ((Object.keys(circuits).length != 1) || (Object.values(circuits)[0]?.size != points.length)){
        d = distHeap.pop() as Dist;
        appendToCircuits(circuits, new Set([d.p1, d.p2]))
    }
    if (d !== undefined){
        console.log(d.p1, d.p2)
        console.log(d.p1.x * d.p2.x)
    }
}

function main(){
    part1()
    part2()
}

main()