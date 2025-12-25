import { readInput, sum } from "@utils/helpers.ts"

function getRanges(r: string): [number, number][]{
    return r?.split("\n").map(
        (x: string) => {
            const [s, e] = x.split("-") as [string, string]
            return [Number(s), Number(e)] as [number, number]
        }
    ).toSorted(
        (a, b) => (a[0] - b[0])
    )

}

function inRanges(id: number, ranges: [number, number][]): boolean{
    let found = false
    ranges.forEach(
        ([s, e]) => {
            if (id >= s && id <= e){
                found = true
                return 
            }
        }
    )
    return found
}

function removeOverlappingRanges(ranges: [number, number][]): [number, number][]{
    const newRanges: [number, number][] = []
    ranges.forEach(
        (range) => {
            if (newRanges.length === 0){
                newRanges.push(range)
                return
            }
            const [s, e] = range
            const [prevS, prevE] = newRanges.pop() as [number, number]
            if (s > prevE){
                newRanges.push([prevS, prevE])
                newRanges.push([s, e])
                return
            } else {
                newRanges.push([prevS, Math.max(prevE, e)])
                return
            }
        }
    )
    return newRanges
}

function part1(){
    const inp = readInput("day5.txt")
    const [rangesStr, idsStr] = inp.split("\n\n")
    const ids = (idsStr as string).split("\n")
    const ranges = getRanges(rangesStr as string)
    console.log(
        sum(ids.map((id) => inRanges(Number(id), ranges) ? 1 : 0))
    )
}

function part2(){
    const inp = readInput("day5.txt")
    const [rangesStr, _] = inp.split("\n\n")
    const ranges = getRanges(rangesStr as string)
    const newRanges = removeOverlappingRanges(ranges)
    console.log(
        sum(newRanges.map(([s, e]) => e - s + 1))
    )
}

function main(){
    part1()
    part2()
}

main()