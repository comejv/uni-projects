from sys import argv
from os.path import isfile
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from classes import Bridge, Bridges
from vision import create_nodes_from_image, create_nodes_from_text, fatal
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
        return -vpool.id(-bridge.id)


def bridges_to_clauses(vpool: IDPool, cases: list[Bridges]) -> list[list[int]]:
    """Convert a Bridges object to a list of clauses.

    Args:
        bridges (Bridges): Bridges object to convert.

    Returns:
        list[list[int]]: List of clauses.
    """
    clauses = []
    # Add a clause for each bridge
    for case in cases:
        clauses.append([bridge_to_id(vpool, bridge) for bridge in case])

    return clauses


def cnf_to_bridges(vpool: IDPool, cnf: CNF) -> list[str]:
    """Convert a CNF formula to a list of bridge ids.

    Args:
        cnf (CNF): CNF object representing the formula.

    Returns:
        Bridges: list of bridge ids.
    """
    if cnf is None:
        return []
    bid = []
    for var in solver.get_model():
        if var > 0:
            bid.append(vpool.obj(var))
        else:
            bid.append(-vpool.obj(-var))
    return bid


def dnf_to_cnf(dnf: list[list]) -> list[list]:
    """Convert a dnf to a cnf.

    Args:
        dnf (list[list]): dnf to convert.

    Returns:
        list[list]: cnf.
    """
    cnf = []
    if dnf == []:
        return [[]]
    else:
        list = dnf[0]
        suite = dnf[1:]
        for lit in list:
            for lit2 in dnf_to_cnf(suite):
                lit2.append(lit)
                cnf.append(lit2)
        return cnf


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
    cnf = CNF()

    # Nodes must have {node.value} bridges exactly
    for node in nodes:
        dnf = bridges_to_clauses(vpool, rules.connect_node(node))
        cnf.extend(dnf_to_cnf(dnf))

    # Bridges can't cross each other
    cnf.extend(bridges_to_clauses(vpool, rules.no_crossing(bridges)))

    # Create dimacs output file
    write_dimacs("output/test.cnf", cnf)

    # Create a SAT solver instance for this formula:
    with Solver(bootstrap_with=cnf) as solver:
        # Print number of variables and clauses
        print("Number of variables :", solver.nof_vars())
        print("Number of clauses :", solver.nof_clauses())

        # Add phases (assumptions):
        # solver.set_phases([vpool.id(bridges[0].id)]) # Bridge 0 must be used

        # Call the solver for this formula:
        if solver.solve():
            print("This game is solvable. One possible solution is:")
            print("Var names :", solver.get_model())
            print("Bridge ids :", cnf_to_bridges(vpool, cnf))
        else:
            print("This game is not solvable.")
