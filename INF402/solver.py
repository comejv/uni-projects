from sys import argv
from os.path import isfile
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from vision import Node, create_nodes_from_image, create_nodes_from_text, draw_bridge, fatal


class Bridge:
    def __init__(self, lvl: int, n1: Node, n2: Node) -> None:
        self.lvl = lvl
        self.n1 = n1
        self.n2 = n2

    def __repr__(self) -> str:
        return f"({self.n1} -> {self.n2}, lvl {self.lvl})"


class Bridges:
    def __init__(self) -> None:
        self.dict = dict()
        self._len = 0

    def __len__(self) -> int:
        return self._len

    def __getitem__(self, key: str) -> Bridge:
        return self.dict[key]

    def __iter__(self):
        return iter(self.dict.items())

    def __repr__(self) -> str:
        return f"Bridges({self.dict})"

    def bridge_id(self, lvl: int, n1: Node, n2: Node) -> int:
        """ Return a unique id for a bridge. n1 and n2 are not ordered.

        Args:
            lvl (int): level of the bridge.
            n1 (Node): first node of the bridge.
            n2 (Node): second node of the bridge.

        Returns:
            int: unique integer id for the bridge.
        """
        nl = sorted([n1, n2], key=lambda n: n.id)

        # On assume que les node.id < 100
        if lvl > 0:
            id = lvl * 10000 + nl[0].id * 100 + nl[1].id
        else:
            id = lvl * 10000 - nl[0].id * 100 - nl[1].id
        return id

    def add_from_nodes(self, lvl: int, n1: Node, n2: Node) -> None:

        bid = self.bridge_id(lvl, n1, n2)

        if bid not in self.dict:
            self.dict[bid] = Bridge(lvl, n1, n2)
            self._len += 1

    # TODO: trouver la pos de l'ile à partir de l'id
    # def add_from_id(self, bid: int) -> None:
    #     if bid not in self.dict:
    #         abid = abs(bid)
    #         lvl = abid // 10000
    #         n1id = (abid % 10000) // 100
    #         n2id = abid % 100
    #         if bid < 0:
    #             lvl = -lvl
    #         self.dict[bid] = Bridge(lvl, Node(n1id), Node(n2id))
    #         self._len += 1

    def from_node(self, n: Node) -> list:
        """ Return the list of bridges connected to the node n.

        Args:
            n (Node): node to check.

        Returns:
            list: list of bridges connected to the node n.
        """
        return [b for b in self.dict.values() if b.n1 == n or b.n2 == n]


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

    print(f"Number of nodes: {len(nodes)}")
    print(f"Number of bridges: {len(bridges)}")
    print(*bridges.dict.items(), sep='\n')

    print("Bridges from node 0:")
    print(*bridges.from_node(nodes[0]), sep='\n')

    # # SAT solver usage example
    # # create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
    # cnf = CNF(from_clauses=[[-1, 2], [-1, -2]])

    # vpool = IDPool()

    # # create a SAT solver for this formula:
    # with Solver(bootstrap_with=cnf) as solver:
    #     # call the solver for this formula:
    #     print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

    #     # the formula is satisfiable and so has a model:
    #     print('and the model is:', solver.get_model())
