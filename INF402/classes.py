class Node:
    def __init__(self, id, x, y, v):
        self.id: int = id
        self.x: int = int(x)
        self.y: int = int(y)
        self.value: int = int(v)
        self.neighbours: list[Node] = []

    def __repr__(self) -> str:
        return f"Node({self.id} : [{self.x}, {self.y}], {self.value})"

    def __eq__(self, __other) -> bool:
        if not isinstance(__other, self.__class__):
            return NotImplemented
        return self.x == __other.x and self.y == __other.y and self.id == __other.id

    def add_neighbour(self, neighbour):
        if neighbour not in self.neighbours and neighbour != self and type(neighbour) == Node:
            self.neighbours.append(neighbour)
        else:
            raise ValueError("Neighbour not added")


class Bridge:
    def __init__(self, lvl: int, n1: Node, n2: Node) -> None:
        self.lvl = lvl
        self.n1 = n1
        self.n2 = n2
        assert self.n1.x == self.n2.x or self.n1.y == self.n2.y
        self.id = None
        self.get_id()

    def __repr__(self) -> str:
        return f"({self.n1} -> {self.n2}, lvl {self.lvl})"

    def __eq__(self, __other: object) -> bool:
        if not isinstance(__other, self.__class__):
            return NotImplemented
        return self.id == __other.id

    def get_id(self) -> None:
        if self.id:
            return self.id

        nl = sorted([self.n1, self.n2], key=lambda n: n.id)

        # On assume que les node.id < 100
        if self.lvl > 0:
            self.id = self.lvl * 10000 + nl[0].id * 100 + nl[1].id
        else:
            self.id = self.lvl * 10000 - nl[0].id * 100 - nl[1].id

    def get_neg(self) -> 'Bridge':
        return Bridge(-self.lvl, self.n1, self.n2)

    def horizontal(self) -> bool:
        return self.n1.x == self.n2.x


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

    def add_from_nodes(self, lvl: int, n1: Node, n2: Node) -> None:
        # Sort nodes by id
        # nl = sorted([n1, n2], key=lambda n: n.id)
        bridge = Bridge(lvl, n1, n2)

        if bridge.id not in self.dict:
            self.dict[bridge.id] = bridge
            self._len += 1

    def connected_to_node(self, n: Node) -> list:
        """ Return the list of bridges connected to the node n.

        Args:
            n (Node): node to check.

        Returns:
            list: list of bridges connected to the node n.
        """
        return [b for b in self.dict.values() if b.n1 == n or b.n2 == n]


class Arc:
    def __init__(self, n1: Node, n2: Node, value: bool) -> None:
        self.n1: Node = n1
        self.n2: Node = n2
        self.value: bool = value
        self.id: int = self.get_id(n1.id, n2.id)

    def __repr__(self) -> str:
        if self.value:
            return f"A->{self.n1.id}to{self.n2.id}"
        return f"-A->{self.n1.id}to{self.n2.id}"

    def __eq__(self, __other) -> bool:
        if not isinstance(__other, self.__class__):
            return NotImplemented
        return self.n2 == self.n2 and self.n1 == self.n1

    def get_id(self, n1: int, n2: int):
        return 30000 + n1 * 100 + n2


class Way:
    def __init__(self, n1: Node, n2: Node, value: bool) -> None:
        self.n1: Node = n1
        self.n2: Node = n2
        self.value: bool = value
        self.id: int = self.get_id(n1.id, n2.id)

    def __repr__(self) -> str:
        if self.value:
            return f"W->{self.n1.id}to{self.n2.id}"
        return f"-W->{self.n1.id}to{self.n2.id}"

    def __eq__(self, __other) -> bool:
        if not isinstance(__other, self.__class__):
            return NotImplemented
        return self.n2 == self.n2 and self.n1 == self.n1

    def get_id(self, n1: int, n2: int) -> int:
        return 40000 + n1 * 100 + n2


class CNF:
    def __init__(self, from_clauses=None, from_file=None) -> None:
        # List of clauses
        self.__clauses = []
        # Number of variables
        self.__nvars = 0
        # Number of clauses
        self.__nclauses = 0

        if from_clauses is not None:
            for clause in from_clauses:
                self.add_clause(clause)

        if from_file is not None:
            self.from_file(from_file)

    def __repr__(self) -> str:
        return f"CNF(nvars={self.nvars()}, nclauses={self.nclauses()})"

    def print_clauses(self) -> None:
        """Print the clauses in the CNF formula."""
        for clause in self.clauses():
            print(clause)

    def clauses(self) -> list[list[int]]:
        """Return the clauses in the CNF formula.

        Returns:
            list[list[int]]: List of clauses.
        """
        return self.__clauses

    def nvars(self) -> int:
        """Return the number of variables in the CNF formula.

        Returns:
            int: Number of variables.
        """
        return self.__nvars

    def nclauses(self) -> int:
        """Return the number of clauses in the CNF formula.

        Returns:
            int: Number of clauses.
        """
        return self.__nclauses

    def add_clause(self, clause: list[int]) -> None:
        """Add a clause to the CNF formula.

        Args:
            clause (list[int]): List of integer variables.
        """
        self.__clauses.append(clause)
        self.__nclauses += 1
        # Update the number of variables
        # Assume that the variables are numbered consecutively
        if not clause:
            print("Aucun pont possible, jeu insatisfaisable")
            exit(1)
        self.__nvars = max(self.nvars(), max(abs(var) for var in clause))

    def remove_clause(self, clause: list[int]) -> None:
        """Remove a clause from the CNF formula.

        Args:
            clause (list[int]): List of integer variables.
        """
        self.__clauses.remove(clause)
        self.__nclauses -= 1
        self.__nvars = max(max(abs(var) for var in clause)
                           for clause in self.clauses())

    def extend(self, clauses: list[list[int]]) -> None:
        """Add a list of clauses to the CNF formula.

        Args:
            clauses (list[list[int]]): List of clauses.
        """
        for clause in clauses:
            self.add_clause(clause)

    def from_file(self, filename: str) -> None:
        """Read a dimacs file and store the clauses in the object.

        Args:
            filename (str): Name of the file to read.
        """
        with open(filename, "r") as f:
            # Read the header
            while not f.readline().startswith("p"):
                pass
            # Read the number of variables and clauses
            self.__nvars, self.__nclauses = map(int, f.readline().split()[2:])

            # Read the clauses
            for line in f:
                # Skip comments and empty lines
                if line.startswith("c") or line.strip() == "":
                    continue
                # Read the clause and ignore ending 0
                split_line = line.split()
                assert split_line.pop() == "0", "Clause not terminated by 0"
                self.add_clause(list(map(int, split_line)))

    def to_file(self, filename: str) -> None:
        """Write the CNF formula to a dimacs file.

        Args:
            filename (str): Name of the file to write.
        """
        filename.rstrip()
        with open(filename, "w") as f:
            # Write the header
            f.write(f"p cnf {self.nvars()} {self.nclauses()}\n")

            # Write the clauses
            for clause in self.clauses():
                f.write(" ".join(map(str, clause)) + " 0\n")


class IDPool:
    def __init__(self, start_from=1) -> None:
        # Next ID to assign
        self.next_id = start_from
        # Map from IDs to integers
        self.id_map = {}

    def id(self, name) -> int:
        """Get the integer ID corresponding to the given name (int or str).
        If name is a string, it is hashed.

        Args:
            id (int): ID to convert.

        Returns:
            int: Integer ID.
        """
        # Hash the name if it is not an integer
        if not isinstance(name, int):
            name = hash(name)
        # Add the name to the map if it is not already there
        if name not in self.id_map:
            self.id_map[name] = self.next_id
            self.next_id += 1
        # Return the ID
        return self.id_map[name]

    def obj(self, id: int) -> int:
        """Get the object name corresponding to the given integer ID.
        If name was a string, its hash is returned. If object was not
        found, returns None.

        Args:
            id (int): Integer ID.

        Returns:
            int: Name or hash of the name.
        """
        try:
            # Invert the map and return the name
            return list(self.id_map.keys())[list(self.id_map.values()).index(id)]
        except ValueError:
            # Return None if object was not found
            return None


if __name__ == "__main__":
    vpool = IDPool()
    ia = vpool.id(1)
    print(vpool.obj(1))
    print(vpool.obj(2))
