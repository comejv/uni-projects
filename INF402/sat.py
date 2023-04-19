# Author: Côme VINCENT & Emile GUILLAUME
# Date: 2023-04-13

from random import choice, random


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
        self.__nvars = max(max(abs(var) for var in var)
                           for var in self.clauses())

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

    def obj(self, id: int) -> int:
        """Get the object name corresponding to the given integer ID.
        If name was a string, its hash is returned.

        Args:
            id (int): Integer ID.

        Returns:
            int: Name or hash of the name.
        """
        # Invert the map and return the name
        return list(self.id_map.keys())[list(self.id_map.values()).index(id)]


def delete_valid_clauses(cnf: CNF, assignments: list[int] = []) -> None:
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

def unsat_clauses(assignation: list[int], cnf: CNF) -> list[list[int]]:
    """Return the list of unsatisfied clauses.

    Args:
        assignation (list[int]): List of assignments. The index of the list
            corresponds to the variable number, and the value to the assignment.
        cnf (CNF): A list of clauses.

    Returns:
        list[list[int]]: List of unsatisfied clauses. If the list is empty,
            the assignation satisfies the CNF formula.
    """
    unsat = []
    for clause in cnf.clauses():
        clause_1 = False
        for var in clause:
            if var in assignation:
                clause_1 = True
                break
        if not clause_1:
            unsat.append(clause)

    return unsat


def walk_sat(cnf: CNF) -> list[int]:
    """WalkSAT algorithm.

    Args:
        cnf (CNF): A list of clauses.

    Returns:
        list[int]: List of assignments. The index of the list corresponds to
            the variable number, and the value to the assignment.
    """
    # Clean the CNF formula
    # delete_valid_clauses(cnf)

    # Initialize the model
    model = []
    for i in range(1,cnf.nvars()+1):
        model.append(i)

    MAX_ITERATION = 10000
    n_iter = 0
    while n_iter < MAX_ITERATION:
        # Get the list of unsatisfied clauses
        clauses = unsat_clauses(model, cnf)
        
        # If there are no unsatisfied clauses, return the model
        if clauses == []:
            return model

        # Get a random unsatisfied clause
        clause = choice(clauses)

        # Get a variable from the clause
        x = random()
        if x <= 0.4:
            y = choice(clause)
        else:
            y = clause[0]

        # Flip the variable
        model[abs(y)-1] = model[abs(y)-1] * (-1)
        n_iter += 1

    return None


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
    print("Name of 1:", pool.obj(1))

    # Solve the formula
    model = walk_sat(cnf)
    print("Satisfiable:", model is not None)
    print("Model:", model)
