# Hashiwokakero puzzle solver
> Python program that solves a Hashiwokakero (Bridges) puzzle.

This program can solve a Hashiwokakero puzzle. It uses [computer vision](vision.py) to read the puzzle from an image or a text file and a [SAT solver](solver.py) to solve it according to the [rules](rules.py).

## Usage
```
usage: main.py [-h] [-i INPUT] [-d DIMACS] [-c CNF] [-p] [-t] [-w WRITE_FILE] [--branching BRANCHING] [--use-c-walk] [-q] [-b]

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
  --branching BRANCHING
                        what branching heuristic walksat should use. If none provided, always chooses the same variable.
  --use-c-walk          use the C implementation of our Walksat
  -q, --quiet           do not print the solution
  -b, --bridge-help     show how the bridges are numbered
```
> If you want to use the --use-c-walk flag, you need to have the library compiled. You can do so using this command :
> 
> `cd data/c_lib/ && py setup.py build_ext --inplace && cd ../..`

## Example
- Solve example 3x3_1, write clauses in a file and show graphical solution on stdout : `py main.py -i data/examples/3x3_1.txt -c clauses.dimacs -w stdout`
- Solve example 3x3_1, show nothing on stdout and use moms branching heuristic : `python3.9 main.py -qi data/examples/3x3_1.txt --branching moms`