"""Should be run like `python prepare_day.py 4`."""
import sys
import os
import requests
import pathlib


def create_files(day: int, day_input: str | None = None):
    p = pathlib.Path()
    input_file = p / f"day{day}-input.txt"
    input_file.touch(exist_ok=True)
    if day_input:
        input_file.write_text(day_input)
    test_input_file = p / f"day{day}-input.txt.test"
    test_input_file.touch(exist_ok=True)
    code_file = p / f"day{day}.py"
    code_file.touch(exist_ok=True)


def fetch_input(day: int) -> str:
    session_cookie = os.getenv("AOC_SESSION")
    headers = {
        "Cookie": f"session={session_cookie}"
    }
    day_input = requests.get(
        f"https://adventofcode.com/2023/day/{day}/input",
        headers=headers
    ).text
    return day_input


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Missing day input.")
    day = int(sys.argv[1])
    print(day)
    create_files(day, day_input=fetch_input(day))
    
    