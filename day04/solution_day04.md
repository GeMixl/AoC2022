# Advent of Code 2022

Day 04 https://adventofcode.com/2021/day/04

Puzzle input at https://adventofcode.com/2022/day/04/input

A relatively straight forward puzzle: using the ternary *between* operator of python I can do the necessary checks.

## Part 1

In part 1 I need to check if in a pair of ranges one range contains the other. 

First see if range 1 is entirely within range 2:
``` python
     (range_2[0] <= range_1[0] <= range_2[1] and
      range_2[0] <= range_1[1] <= range_2[1])
```
Then check of range 2 is within range 1:

``` python
     (range_1[0] <= range_2[0] <= range_1[1] and
      range_1[0] <= range_2[1] <= range_1[1])
```
If any of the two checks gives *True* I will count the range pair

# Part 2

In this part of the puzzle we need to check if there is an overlap of the two ranges. 
For this I can use the same checks as above but just link them with an **OR** condition. 

Here is an example: 

``` python
     range_2[0] <= range_1[0] <= range_2[1] or
     range_2[0] <= range_1[1] <= range_2[1] or
     ...
```
