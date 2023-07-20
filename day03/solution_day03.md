# Advent of Code 2021                                         #

Day 03 https://adventofcode.com/2021/day/03                 #

Puzzle input at https://adventofcode.com/2022/day/03/input  #

It took me two attempts to understand this puzzle (first I did not understand that the groups of elfs are already in subsequent order).
Finally I adapted my code slightly to get it right: 

* push all elfs into a queue
* initialize the sticker-attachment_effort with 1
* continue while there are still elfs in the queue
* pop the first three elf of the queue the first one is the current elf, the remaining two are the other elfs
* iterate over the characters of the current elf (duplicates are removed)
* see if the chaacter is in any of the other elfs
* if there are 2 elfs found: translate the character into its value
* add the values
* continue the while loop