#!/usr/bin/env bash

if [[ $1 -lt 10 ]]
then
  day="0${1}"
elif [[ $1 -le 25 ]]
then
  day=$1
else
  echo "Error: day can not be larger than 25"
  exit 1
fi

day_directory="./day$day"
day_pyfile="$day_directory/day$day.py"
day_test_file="$day_directory/test_day$day.txt"
day_input_file="$day_directory/input_day$day.txt"

if [[ -d $day_directory ]]
then
  echo "Error: directory $day_directory already exists!"
  exit 1
fi

echo "generate directory $day_directory"
mkdir "$day_directory"
echo "writing file $day_pyfile"
touch "$day_pyfile"
echo "writing file $day_test_file"
touch "$day_test_file"
echo "writing file $day_input_file"
touch "$day_input_file"

{
echo "###############################################################"
echo "# Advent of Code 2022                                         #"
echo "# Day $day https://adventofcode.com/2021/day/$day                 #"
echo "# Puzzle input at https://adventofcode.com/2022/day/$day/input  #"
echo "###############################################################"
echo ""
echo ""
echo "#import ..."
echo ""
echo ""
echo "def read_input(filename: str) -> []:"
echo "    with open(filename, \"r\") as fs:"
echo "        pass"
echo "    return input"
echo ""
echo ""
echo "def solve_part_i(input):"
echo "    pass"
echo ""
echo ""
echo "def solve_part_ii(input):"
echo "    pass"
echo ""
echo ""
echo "if __name__ == \"__main__\":"
echo "    filename = \"test_day$day.txt\""
echo "    print(\"--- Part One ---\")"
echo "    print(solve_part_i(read_input(filename)))"
echo "    print(\"--- Part Two ---\")"
echo "    print(solve_part_ii(read_input(filename)))"
echo "    "
} >> "$day_pyfile"

