# Author: Côme VINCENT
# Date: 2023-04-13

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
        self.__nvars = max(self.nvars(), max(abs(var) for var in clause))

    def remove_clause(self, clause: list[int]) -> None:
        """Remove a clause from the CNF formula.

        Args:
            clause (list[int]): List of integer variables.
        """
        self.__clauses.remove(clause)
        self.__nclauses -= 1
        self.__nvars = max([abs(lit) for lit in var] for var in self.clauses())

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
        with open(filename, "w") as f:
            # Write the header
            f.write(f"p cnf {self.nvars()} {self.nclauses()}")

            # Write the clauses
            for clause in self.clauses():
                f.write(" ".join(map(str, clause)) + " 0")


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

    def name(self, id: int) -> int:
        """Get the name corresponding to the given integer ID.
        If name was a string, its hash is returned.

        Args:
            id (int): Integer ID.

        Returns:
            int: Name.
        """
        # Invert the map and return the name
        return list(self.id_map.keys())[list(self.id_map.values()).index(id)]


def delete_valid_clauses(cnf: CNF, assignments: list[int]) -> None:
    """Delete all valid clauses from the CNF formula.

    Args:
        cnf (CNF): A list of clauses.
        assignments (list[int]): List of assignments.
    """
    # Delete valid clauses
    for clause in cnf.clauses():
        # Check if the clause contains a variable that is assigned to True
        if any(var in assignments for var in clause if var > 0):
            cnf.remove_clause(clause)
            continue
        # Check if the clause contains both a variable and its negation
        for n, var in enumerate(clause):
            if -var in clause[n:]:
                cnf.remove_clause(clause)
                break


def dpll_rec(cnf: CNF, assignments: set[int]) -> tuple[bool, list[int]]:
    cnf_is_modified = True
    while cnf_is_modified:
        cnf_is_modified = False

        # 1. Check if the formula is empty (True)
        if cnf.nclauses() == 0:
            return True, assignments
        # or if assignments are contradictory (False)
        if any(-var in assignments for var in assignments):
            return False, []

        # 2. Reduction : remove clauses containing another one
        for clause in cnf.clauses():
            for other_clause in cnf.clauses():
                if clause != other_clause and set(clause).issubset(set(other_clause)):
                    cnf.remove_clause(other_clause)
                    break

        # 3. Pure literal elimination : remove clauses containing an isolated literals
        # Find all isolated literals
        isolated_literals = set()
        skip = []
        for clause in cnf.clauses():
            for lit in clause:
                if abs(lit) in skip:
                    continue
                if -lit in isolated_literals:
                    isolated_literals.remove(-lit)
                    skip += [abs(lit)]
                else:
                    isolated_literals.add(lit)

        # Deal with them
        for clause in cnf.clauses():
            for lit in clause:
                if lit in isolated_literals:
                    # Remove all clauses containing an isolated literal
                    # and add the assignment
                    cnf.remove_clause(clause)
                    cnf_is_modified = True
                    break

        # If the CNF formula has been modified, restart the loop
        if cnf_is_modified:
            continue

        # 4. Unit propagation : remove clauses containing a unit literal
        for clause in cnf.clauses():
            if len(clause) == 1:
                # Remove all clauses containing a unit literal
                # and add the assignment
                cnf.remove_clause(clause)
                assignments.append(clause[0])
                cnf_is_modified = True
                break
        if cnf_is_modified:
            continue

        # 5. Choose a literal and recurse
        return dpll_rec(cnf, assignments + [cnf.clauses()[0][0]]) or dpll_rec(cnf, assignments + [-cnf.clauses()[0][0]])


def dpll(cnf: CNF, assignments: set[int] = set()) -> tuple[bool, list[int]]:
    """Checks the satisfability of a list of clauses using the DPLL algorithm.

    Args:
        cnf (CNF): A list of clauses.
        assignments (list[int]): List of assignments.

    Returns:
        tuple[bool, list[int]]: A tuple containing a boolean indicating if the formula is satisfiable
        and a list of assignments if the formula is satisfiable.
    """
    # Delete valid clauses
    delete_valid_clauses(cnf, assignments)

    # Check if the formula has empty clauses
    if any(len(clause) == 0 for clause in cnf.clauses()):
        return False, []

    return dpll_rec(cnf, assignments)


if __name__ == '__main__':
    # CNF + IDPool example
    cnf = CNF()
    pool = IDPool()

    obj = [1, 2, 3, 4, 5]
    print(obj)

    obj_id = [pool.id(obj) for obj in obj]
    print(obj_id)

    # (1 + 2) * (1 + 3) * (1 + -4) * (2 + 4) * (3 + 4) * (-3 + 5) * (4 + 5) * (-1 + 1)
    # Should be satisfiable
    cnf.add_clause([pool.id(obj[0]), pool.id(obj[1])])
    cnf.add_clause([pool.id(obj[0]), pool.id(obj[2])])
    cnf.add_clause([pool.id(obj[0]), -pool.id(obj[3])])
    cnf.add_clause([pool.id(obj[1]), pool.id(obj[3])])
    cnf.add_clause([pool.id(obj[2]), pool.id(obj[3])])
    cnf.add_clause([-pool.id(obj[2]), pool.id(obj[4])])
    cnf.add_clause([pool.id(obj[3]), pool.id(obj[4])])
    cnf.add_clause([-pool.id(obj[0]), pool.id(obj[0])])

    print(cnf)
    cnf.print_clauses()

    print("ID of 'a':", pool.id('a'))
    print("Name of 1:", pool.name(1))

    # Solve the formula
    sat, model = dpll(cnf)
    print("Satisfiable:", sat)
    print("Model:", model)
    print(cnf.clauses())
