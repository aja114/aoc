import { mult, readInput, sum } from "@utils/helpers.ts";

function part1(){
    const inp = readInput("day6.txt")
    const nums = inp.split("\n").map(
        (x) => x.trim().split(" ").filter((x) => x != "")
    )
    const ops = nums.pop() as string[]
    const numsT: string[][] = []
    for (let i = 0; i < nums.length; i+=1){
        for (let j = 0; j < (nums[0] as string[]).length; j+=1){
            const el = (nums[i] as string[])[j] as string
            if (i == 0){
                numsT.push([el])
            } else{
                (numsT[j] as string[]).push(el)
            }
        }
    }
    let res = 0
    numsT.forEach(
        (seq, i) => {
            if (ops[i] === "+"){
                res += seq.reduce((a, b) => Number(a) + Number(b), 0)
            } else{
                res += seq.reduce((a, b) => Number(a) * Number(b), 1)
            }
        }
    )
    console.log(res)
}

function computeColNums(arr: string[]){
    const nums: number[] = []
    let i = (arr[0] as string).length - 1
    while (i >= 0){
        let num = ""
        arr.forEach(
            (x) => {
                if (x !== " "){
                    num += x[i]
                }
            }
        )
        nums.push(Number(num))
        i -= 1
    }
    return nums
}

function part2(){
    const inp = readInput("day6.txt")
    const nums = inp.split("\n")
    const ops = (nums.pop() as string).split("").map((x) => x.trim()).filter((x) => x != "")
    const cols: string[][] = []
    let i = 0
    let col: string[] = []
    while (i < (nums[0] as string).length){
        const newEls: string[] = [] 
        nums.forEach(
            (num) => {
                newEls.push(num[i] as string)
            }
        )
        if (newEls.every((x) => x === " ")){
            cols.push(col)
            col = []
        } else {
            if (col.length === 0){
                newEls.forEach(
                    (el) => col.push(el)
                )
            } else {
                newEls.forEach(
                    (el, i) => col[i] += el
                )
            }
        }
        i += 1
    }
    cols.push(col)
    let res = 0
    cols.forEach(
        (col, i) => {
            const nums = computeColNums(col)
            if (ops[i] === "+"){
                res += sum(nums)
            } else{
                res += mult(nums)
            }
        }
    )
    console.log(res)
}

function main(){
    part1()
    part2()
}

main()