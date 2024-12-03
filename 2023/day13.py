import itertools

matrix = list[list[str]]


def get_input(file: str) -> list[matrix]:
    with open(file, "r") as f:
        inp = f.read()
    matrices = [
        [
            list(x.strip()) for x in l.strip().split("\n")
        ]
        for l in inp.strip().split("\n\n")
    ]
    return matrices


def find_row_sim(mat: matrix) -> int | None:
    for i in range(1, len(mat)):
        mirror_length = min(i, len(mat)-i)
        left_side = mat[max(i-mirror_length, 0):i]
        right_side = mat[i:min(len(mat), i+mirror_length)]
        if left_side == right_side[::-1]:
            return i
    return None


def find_col_sim(mat: matrix) -> int | None:
    transpose_mat = list(zip(*mat))
    return find_row_sim(transpose_mat)


def find_row_sim_with_smudge(mat: matrix) -> int | None:
    for i in range(1, len(mat)):
        mirror_length = min(i, len(mat)-i)
        left_side = mat[max(i-mirror_length, 0):i]
        right_side = mat[i:min(len(mat), i+mirror_length)]
        left_side_flat = itertools.chain.from_iterable(left_side)
        right_side_flat = itertools.chain.from_iterable(right_side[::-1])
        if sum(x!=y for x, y in zip(left_side_flat, right_side_flat)) == 1:
            return i
    return None


def find_col_sim_with_smudge(mat: matrix) -> int | None:
    transpose_mat = list(zip(*mat))
    return find_row_sim_with_smudge(transpose_mat)


def part1(file: str) -> int:
    matrices = get_input(file)
    s = 0    
    for i, mat in enumerate(matrices):
        if (r_mir := find_row_sim(mat)) is not None:
            s += r_mir * 100
        if (c_mir := find_col_sim(mat)) is not None:
            s += c_mir
    return s


def part2(file: str) -> int:
    matrices = get_input(file)
    s = 0    
    for i, mat in enumerate(matrices):
        if (r_mir := find_row_sim_with_smudge(mat)) is not None:
            s += r_mir * 100
        if (c_mir := find_col_sim_with_smudge(mat)) is not None:
            s += c_mir
    return s


if __name__ == "__main__":
    print(part1("day13-input.txt"))
    print(part2("day13-input.txt"))
