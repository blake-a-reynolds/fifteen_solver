# Fifteen Solver
A 15 puzzle consists of a 4x4 grid of 15 numbered tiles and a blank space, where the goal is to rearrange the tiles by sliding them into the adjacent empty space until they are in ascending order from top left to bottom right (with the space last).

| | | | |
| :-: | :-: | :-: | :-: |
|  1 | 2  | 3  | 4  |
|  5 | 6  | 7  | 8  |
|  9 | 10  | 11  |   |
| 13 | 14 | 15 | 12 |

=> slide 12 up

| | | | |
| :-: | :-: | :-: | :-: |
|  1 | 2  | 3  | 4  |
|  5 | 6  | 7  | 8  |
|  9 | 10  | 11  | 12 |
| 13 | 14 | 15 |  |

### Usage
`python3 fifteen.py N1 N2 N3 N4 N5 N6 N7 N8 N9 N10 N11 N12 N13 N14 N15 N16`

where N1-N16 are the tile numbers from top-left to bottom-right, and 0 is used for the empty space

#### Example
| | | | |
| :-: | :-: | :-: | :-: |
|   6 |   3 | 10 |   9 |
|   5 | 15 |   8 |   2 |
|      | 11 |   7 | 14 |
| 13 |   1 |  4  | 12 |

##### Input

`python3 fifteen.py 6 3 10 9 5 15 8 2 0 11 7 14 13 1 4 12`

##### Output
```
Nodes generated: 18039 (8913 open, 9126 closed)
Solution(58):
0.	start
         6  3 10  9
	 5 15  8  2
	[] 11  7 14
	13  1  4 12

1.	up
	 6  3 10  9
	[] 15  8  2
	 5 11  7 14
	13  1  4 12

2.	up
	[]  3 10  9
	 6 15  8  2
	 5 11  7 14
	13  1  4 12
```
...
```
57.	down
	 1  2  3  4
	 5  6  7  8
	 9 10 11 12
	13 14 [] 15

58.	right
	 1  2  3  4
	 5  6  7  8
	 9 10 11 12
	13 14 15 []
```
