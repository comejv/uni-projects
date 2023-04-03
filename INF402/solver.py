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


def bridge_to_id(vpool: IDPool, bridge: Bridge) -> int:
    """Convert a bridge to an ID.

    Args:
        bridge (Bridge): Bridge to convert.

    Returns:
        int: ID of the bridge. Negative if the bridge is not used.
    """
    if bridge.lvl > 0:
        return vpool.id(bridge.id)
    else:
        return -vpool.id(bridge.id)


def bridges_to_cnf(vpool: IDPool, cases: list[Bridges]) -> CNF:
    """Convert a Bridges object to a CNF formula.

    Args:
        bridges (Bridges): Bridges object to convert.

    Returns:
        CNF: CNF object representing the formula.
    """
    cnf = CNF()

    # Add a clause for each bridge
    for case in cases:
        cnf.append([bridge_to_id(vpool, bridge) for bridge in case])

    return cnf


def cnf_to_bridges(vpool: IDPool, cnf: CNF) -> list[str]:
    """Convert a CNF formula to a list of bridge ids.

    Args:
        cnf (CNF): CNF object representing the formula.

    Returns:
        Bridges: list of bridge ids.
    """
    bid = []
    for var in solver.get_model():
        if var > 0:
            bid.append(vpool.obj(var))
        else:
            bid.append(-vpool.obj(-var))
    return bid


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

    # Create a variable pool for the bridges
    vpool = IDPool()
    fnc = bridges_to_cnf(vpool, rules.connect_node(nodes[0]))
    write_dimacs("output/test.cnf", fnc)

    # create a SAT solver for this formula:
    with Solver(bootstrap_with=fnc) as solver:
        # call the solver for this formula:
        print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

        # the formula is satisfiable and so has a model:
        print('and the model is:', solver.get_model())

        # print the model using initial variable name
        print('and the model is:', cnf_to_bridges(vpool, fnc))
