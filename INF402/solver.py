from sys import argv
from os.path import isfile
from cv2 import imread
from pysat.formula import CNF
from pysat.solvers import Solver

from vision import create_nodes, draw_bridge, fatal


if __name__ == '__name__':
    if len(argv) != 2:
        impath = input(
            "Please enter the path to the image you want to process:\n")
        while not isfile(impath):
            impath = input(
                "Path is not a file or doesn't exist. Please enter a valid path:\n")
    else:
        impath = argv[1]
        if not isfile(impath):
            fatal("Path is not a file or doesn't exist. Please enter a valid path.")

    # Read original image
    im = imread(impath)

    nodes = create_nodes(im)

    ### SAT solver usage example ###
    # create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
    cnf = CNF(from_clauses=[[-1, 2], [-1, -2]])

    # create a SAT solver for this formula:
    with Solver(bootstrap_with=cnf) as solver:
        # call the solver for this formula:
        print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

        # the formula is satisfiable and so has a model:
        print('and the model is:', solver.get_model())
