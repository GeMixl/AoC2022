# --- Day 15: Beacon Exclusion Zone ---

Came up with the following idea to solve the first puzzle: 
 
- Put all sensors including their position, their Manhattan distance D and an activation flag (default false) into a data structure.
- For the row in question: Look for all sensors which have a orthogonal distance (along the y-axis) less or equal D. Activate those sensors. 

```commandline
Identify active sensors for row 50:
sensor_1 with y=30 and D=25 --> D >  abs(row - y) --> activate with Y=5
sensor_2 with y=40 and D=5  --> D <  abs(row - y) --> do not activate
sensor_3 with y=50 and D=10 --> D == abs(row - y) --> activate with Y=10
sensor_4 with y=60 and D=15 --> D >  abs(row - y) --> activate with Y=5
sensor_5 with y=70 and D=10 --> D <  abs(row - y) --> do not activate
```

- Loop over all active sensors:
  - Remember the distance between row and sensor Y this is the difference of y-coordinates. 
  - From the cell closest to the sensor (the one with the x-coordinate of the sensor) jump D - Y steps to each side and remember those points.
    These are the edges of the range that is 'covered' by the sensor. 
  - Store this tupel for the sensor.

````commandline
Get ranges for the active sensors
sensor_1 with x=20 and Y=5  --> range_1 is (15, 25)
sensor_3 with x=30 and Y=10 --> range_3 is (20, 40)
sensor_4 with x=10 and Y=5  --> range_5 is (5, 15)
````

- Once I have all the ranges from all relevant sensors, I can look for the gaps, i.e. cells that are not covered by any range:

```commandline
Possible relations between two sorted ranges: 
range_1 covers range_2  -->  (0, 5), (1, 4)
range_1 is covered by range_2  -->  (0, 5), (0, 7)
range_1 and range_2 are overlaping --> (0, 5), (3, 7)
range_1 and range_2 are touching --> (0, 5), (6, 7)
range_1 and range_2 are not touching --> (0, 5), (7, 9)
```

- Sort the different ranges ascending by their starting position and if those are similar descending by their end position.
  With this sorting rules I make sure that the second range never covers the first range. I can therefore simplify the range aggregation above:
```commandline
Sorting rules: 
Sort (2, 3) and (1, 2) to (1, 2), (2, 3)
Sort (1, 3) and (1, 2) to (1, 3), (1, 2)
Sort (1, 2) and (1, 2) to (1, 2), (1, 2)
```
## For counting the occupied cells (Part 1)

- Create a covered_cells variable and initiate to 0.
- Iterate over all ranges.
  - Calculate the difference between end and start of the current range.
  - Add this difference to the covered_cells variable.
  - Store the end position of the current range.

```commandline
covered_cells = 0
for range in list_of_ranges:
  if (end_of_range < range[0]):
    covered_range = range[1] - range[0] + 1
  if (end_of_range > range[0]) & (end_of_range < range[1]):
    covered_ranges += range[1] - end_of_range + 1
  end_of_range = range[1]
```

For part 1 I need the number of cells at which NO beacon can be for a certain line.
With the steps above I can easily calculate this.
Only that I need to subtract all cells from the result, where there already is a beacon.

## For finding the empty cells in a search region (Part 2)

- Take the starting position of the first range. All cells smaller than this position are not covered. They will be stored in a result vector. 
```commandline
Empty position search pseudocode
empty_cells = [0 : first_range[0]-1]
for range_1, range_2 in ((p1, p2), (q1, q2)), ((q1, q2), (r1, r2))
  if range_1 and range_2 not touching: 
    add [range_1[1]+1 : range_2[0]-1] to empty_cells
```
- Take the end position of the first range. No cells go to the result vector. 
- Take the starting position of the second range. If this is larger than the end position of the previous range the cells in between go into the result vector. 
- Take the end positon of the second range. If this is larger than the end position of the firs array, take the end position of the first array
(in this case the second array is fully within the first array).
- Keep going like this until all ranges are treated.  

To extend this to an entire search region it is  not necessary to do the full calculation for each row of the regtion.
Since the occupied range from a sensor becomes 2 cells smaller/larger when we jump to new line (depending if the sensor comes closer or less close to the new line).

```commandline
```