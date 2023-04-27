# Hashiwokakero puzzle solver
> Python program that solves a Hashiwokakero (Bridges) puzzle.

This program can solve a Hashiwokakero puzzle. It uses [computer vision](vision.py) to read the puzzle from an image or a text file and a [SAT solver](solver.py) to solve it according to the [rules](rules.py).

## Usage
```
usage: main.py [-h] [-i INPUT] [-d DIMACS] [-c CNF] [-p] [-t] [-w WRITE_FILE] [-q QUIET] [-b]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to the input file
  -d DIMACS, --dimacs DIMACS
                        path to the already generated DIMACS file
  -c CNF, --cnf CNF     path to the file where the CNF will be written
  -p, --pysat           use PySAT instead of our own WalkSAT
  -t, --sat3            convert CNF to 3 sat before using
  -w WRITE_FILE, --write_file WRITE_FILE
                        Write the graphical solution to the given file
  -q QUIET, --quiet QUIET
                        do not print the solution
  -b, --bridge-help     show how the bridges are numbered
```

## Example
`py main.py -i data/examples/3x3_1.txt -c clauses.dimacs -w stdout`
