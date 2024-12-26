# Battleship Solitaire

## Overview

This program solves the [Battleship Solitaire game](<https://en.wikipedia.org/wiki/Battleship_(game)>) as a Constraint Satisfaction Problem (CSP). The goal of the game is to place ships on a grid such that the number of ship segments in each row and column matches the given constraints, and no two ships are adjacent to each other.

## How It Works

The program reads an input file containing the puzzle configuration, including row and column constraints and initial board setup. It then uses a backtracking algorithm to find a valid placement of ships that satisfies all constraints. The solution is written to an output file.

## Input File Format

The input file should contain the following:

1. The first line contains the row constraints.
2. The second line contains the column constraints.
3. The third line contains the ship constraints.
4. The remaining lines contain the initial board setup.

Example:

```
211222
140212
3210
000000
0000S0
000000
000000
00000.
000000
```

## Output File Format

The output file will contain the solved board with ships placed according to the constraints.

Example:

```
<>....
....S.
.^....
.M...S
.v.^..
...v.S
```

## How to Use

1. Ensure you have Python installed on your system.
2. Save your puzzle configuration in an input file (e.g., `input_easy1.txt`).
3. Run the program with the following command:
   ```
   python battle.py --inputfile <path_to_input_file> --outputfile <path_to_output_file>
   ```
   Replace `<path_to_input_file>` with the path to your input file and `<path_to_output_file>` with the desired path for the output file.

Example:

```
python battle.py --inputfile tests/input_easy1.txt --outputfile tests/input_easy_out.txt
```

## Dependencies

- Python 3.x
