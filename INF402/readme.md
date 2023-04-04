# Hashiwokakero puzzle solver
> Python program that solves a Hashiwokakero (Bridges) puzzle.

This program can solve a Hashiwokakero puzzle. It uses [computer vision](vision.py) to read the puzzle from an image or a text file and a [SAT solver](solver.py) to solve it according to the [rules](rules.py).

## Usage
```
usage: main.py [-h] [-i IMAGE] [-t TEXT] [-d DIMACS] [-c CNF] [-q QUIET]

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        Path to the image file
  -t TEXT, --text TEXT  Path to the text file
  -d DIMACS, --dimacs DIMACS
                        Path to the already generated DIMACS file
  -c CNF, --cnf CNF     Path to the file where the CNF will be written
  -q QUIET, --quiet QUIET
                        Do not print the solution
```
