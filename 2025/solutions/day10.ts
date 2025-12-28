import { readInput, sum } from "@utils/helpers.ts";

type System = {
    desiredState: Set<number>
    buttons: Array<Set<number>>
    desiredJoltage: Array<number>
}

function getSystems(): System[]{
    return readInput("day10.txt").split("\n").map(
        (line: string) => {
            const desiredState = new Set(
                line.match(/\[.*\]/g)?.[0]
                .slice(1, -1)
                .split("")
                .map((x, i) => (x === "#" ? i : -1))
                .filter((x) => (x >= 0))
            )
            const desiredJoltage = line.match(/\{.*\}/g)?.[0].slice(1, -1).split(",").map((x) => Number(x))
            if (desiredJoltage === undefined){
                throw Error("bad input")
            }
            const buttons = []
            for (let button of line.matchAll(/\([0-9,]*\)/g)){
                buttons.push(
                    new Set(button[0].slice(1, -1).split(",").map(
                        (x) => Number(x)
                    ))
                )
            }
            return {desiredState, buttons, desiredJoltage}
        }
    )   
}

function solveState(sys: System){
    let curStates: Set<number>[] = [new Set([])]
    let nextStates: Set<number>[] = []
    let depths = 0
    let seeState: Record<string, boolean> = {}
    while (curStates.length > 0){
        for (const curState of curStates){
            if (curState.symmetricDifference(sys.desiredState).size === 0){
                return depths
            }
            sys.buttons.forEach(
                (button) => {
                    const inter = button.intersection(curState)
                    const nextState = curState.union(button).difference(inter)
                    const nextStateStr = JSON.stringify(Array.from(nextState).toSorted())
                    if (seeState[nextStateStr] === undefined){
                        seeState[nextStateStr] = true
                        nextStates.push(nextState)
                    }
                }
            )
        }
        curStates = nextStates
        nextStates = []
        depths += 1
    }
    throw Error("Not solvable")
}

function gcdTwoNumbers(a: number, b: number): number {
    while (b !== 0) {
        const temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

function gcdFinder(...numbers: number[]): number {
    if (numbers.length === 0) {
        throw new Error("At least one number must be provided.");
    }

    const absoluteNumbers = numbers.map(num => Math.abs(num));
    let result = absoluteNumbers[0] as number;

    for (let i = 1; i < absoluteNumbers.length; i++) {
        result = gcdTwoNumbers(result, absoluteNumbers[i] as number);

        if (result === 1) {
            break;
        }
    }

    return result;
}

type Step = {
    state: number[]
    depth: number
}

function solveJoltage(
    sys: System,
    seenStep: Record<string, number>
): number{
    let curSteps: Step[] = [
        {state: sys.desiredJoltage, depth: 0}
    ]
    let nextSteps: Step[] = []
    seenStep[JSON.stringify(sys.desiredJoltage)] = 0
    while (curSteps.length > 0){
        for (const curStep of curSteps){
            const gcd = gcdFinder(...curStep.state)
            if (gcd > 1){
                const reducedState = curStep.state.map((x) => x / gcd)
                // console.log("FOUND GCD", curStep.state, reducedState)
                try{
                    const res = curStep.depth + gcd * solveJoltage(
                        {
                            ...sys,
                            desiredJoltage: reducedState
                        },
                        seenStep,
                    )
                    console.log(res)
                    return res
                } catch (e){
                    continue
                }
            }

            if (sum(curStep.state) === 0){
                console.log(curStep.depth)
                return curStep.depth
            }

            sys.buttons.forEach(
                (button) => {
                    const nextStep = {
                        state: [...curStep.state], depth: curStep.depth + 1
                    }
                    button.forEach((b) => {
                        (nextStep.state[b] as number) -= 1
                    })
                    const nextStateStr = JSON.stringify(nextStep.state)
                    if (
                        seenStep[nextStateStr] === undefined &&
                        nextStep.state.filter((x) => x < 0).length === 0
                    ){
                        seenStep[nextStateStr] = nextStep.depth
                        nextSteps.push(nextStep)
                    }
                }
            )
        }
        curSteps = nextSteps
        nextSteps = []
    }
    throw Error("Not solvable")
}


// function solveJoltage(
//     sys: System,
//     depth: number,
//     memo: Record<string, number>
// ): number{
//     if (sys.desiredJoltage.filter((x) => x < 0).length > 0){
//         return Infinity
//     }
//     if (sum(sys.desiredJoltage) === 0){
//         console.log("done", depth)
//         return depth
//     }
//     const memoised = memo[JSON.stringify(sys.desiredJoltage)]
//     if (memoised !== undefined){
//         return memoised
//     }
//     const res: number[] = []
//     console.log(sys.desiredJoltage, depth)
//     sys.buttons.forEach(
//         (button) => {
//             const nextState = [...sys.desiredJoltage]
//             button.forEach((b) => {nextState[b] -= 1})
//             const tmp = solveJoltage(
//                 {
//                     ...sys,
//                     desiredJoltage: nextState
//                 },
//                 depth + 1,
//                 memo,
//             )
//             const nextStateStr = JSON.stringify(nextState)
//             memo[nextStateStr] = tmp
//             res.push(tmp)
//         }
//     )
//     return res.toSorted()[0] || Infinity
// }

function part1(){
    const systems = getSystems()
    let res = 0
    systems.forEach(
        (sys) => {
            res += solveState(sys)
        }
    )
    console.log(res)
}

function part2(){
    const systems = getSystems()
    let res = 0
    systems.forEach(
        (sys) => {
            const tmp = solveJoltage(sys, {})
            console.log(tmp)
            res += tmp
        }
    )
    console.log(res)
}

function main(){
    part2()
}

main()