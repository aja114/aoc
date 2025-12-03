import { readInput } from "../utils/file.ts"

const START_DIAL = 50
const factor = {
  L: -1,
  R: 1
}

function countPosZero(rotations: string[], countIntermediate: boolean){
  let pos = START_DIAL
  let res = 0
  rotations.forEach(
    (x: string) => {
      if (x.length == 0){
        return
      }
      const dir: "L" | "R" = x[0]
      const val: number = Number(x.slice(1))
      const f = factor[dir]
      let newPos = pos + f * val % 100
      if (newPos < 0){
        newPos += 100
      } else if (newPos > 99){
        newPos -= 100
      }

      if (countIntermediate){
        if (dir == "R"){
          res += ((pos + val) / 100 | 0)
        } else{
          res += ((100 - pos + val) / 100 | 0)
          if (pos === 0){
            res -= 1
          }
        }
      } else if (newPos === 0){
        res += 1
      }
      pos = newPos
    }
  )
  return res
}

function part1() {
  const input = readInput("day1.txt")
  const rotations = input.split("\n")
  const res = countPosZero(rotations, false)
  console.log("Part 1 solution: ", res)
}

function part2(){
  const input = readInput("day1.txt")
  const rotations = input.split("\n")
  const res = countPosZero(rotations, true)
  console.log("Part 2 solution: ", res)
}

function main(){
  part1()
  part2()
}

main()