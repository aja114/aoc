digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def replace_digits(s: str) -> str:
    for i in range(len(s)-1):
        if s[i] in digits.values():
            break
        for digit_str, digit in digits.items():
            l = len(digit_str)
            if s[i:i+l] == digit_str:
                s = s[:i] + digit + s[i+l:]
                break
        else:
            continue
        break
    for i in range(len(s)-1, -1, -1):
        if s[i] in digits.values():
            break
        for digit_str, digit in digits.items():
            l = len(digit_str)
            if s[i-l:i] == digit_str:
                s = s[:i-l] + digit + s[i:]
                break
        else:
            continue
        break
    return s


def get_calib(s: str) -> int:
    for i in s:
        try:
            return int(i)
        except:
            pass
    return 0


with open("day1-input.txt", "r") as f:
   inp = f.readlines()

s = 0
for line in inp:
    line = replace_digits(line)
    print(line)
    s += 10 * get_calib(line)
    s += get_calib(line[::-1])

print(s)


