from sys import argv
from os.path import isfile
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from classes import Bridge, Bridges, Node
from vision import create_nodes_from_image, create_nodes_from_text, draw_bridge, fatal
import rules


def read_dimacs(filename: str) -> CNF:
    """Read a CNF formula from a DIMACS file.

    Args:
        filename (str): Path to the DIMACS file.

    Returns:
        CNF: CNF object representing the formula.
    """
    return CNF(from_file=filename)


def write_dimacs(filename: str, cnf: CNF) -> None:
    """Write a CNF formula to a DIMACS file.

    Args:
        filename (str): Path to the DIMACS file.
        cnf (CNF): CNF object representing the formula.
    """
    cnf.to_file(filename)


if __name__ == '__main__':
    if len(argv) != 2:
        fpath = input(
            "Please enter the path to the image you want to process:\n")
        while not isfile(fpath):
            fpath = input(
                "Path is not a file or doesn't exist. Please enter a valid path:\n")
    else:
        fpath = argv[1]
        if not isfile(fpath):
            fatal("Path is not a file or doesn't exist. Please enter a valid path.")

    # Check file extension
    if fpath.endswith(".txt"):
        nodes = create_nodes_from_text(fpath)
    elif fpath.endswith(".jpg") or fpath.endswith(".png"):
        nodes = create_nodes_from_image(fpath)

    # Create every possible bridge
    bridges = Bridges()
    for i, node in enumerate(nodes):
        for neighbor in nodes[i].neighbours:
            bridges.add_from_nodes(1, node, neighbor)
            bridges.add_from_nodes(2, node, neighbor)

    rules.rule1(nodes[0])

    # # SAT solver usage example
    # # create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
    # cnf = CNF(from_clauses=[[-1, 2], [-1, -2]])

    # vpool = IDPool()
    # id = lambda x: vpool.id(x.id)

    # # create a SAT solver for this formula:
    # with Solver(bootstrap_with=cnf) as solver:
    #     # call the solver for this formula:
    #     print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

    #     # the formula is satisfiable and so has a model:
    #     print('and the model is:', solver.get_model())
