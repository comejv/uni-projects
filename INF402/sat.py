# Author: Côme VINCENT & Emile GUILLAUME
# Date: 2023-04-13

from random import choice, random
from classes import CNF, IDPool


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


def cnf_to_3sat(cnf: CNF) -> CNF:
    """Convert a CNF formula to a 3SAT formula.

    Args:
        cnf (CNF): A list of clauses.

    Returns:
        CNF: A list of clauses where each clause has at most 3.
    """
    v_max_3sat = cnf.nvars()
    t_sat = CNF()
    for clause in cnf.clauses():
        if len(clause) == 1:
            t_sat.add_clause([clause[0], v_max_3sat + 1, v_max_3sat + 2])
            t_sat.add_clause([clause[0], -(v_max_3sat + 1), v_max_3sat + 2])
            t_sat.add_clause([clause[0], v_max_3sat + 1, -(v_max_3sat + 2)])
            t_sat.add_clause([clause[0], -(v_max_3sat + 1), -(v_max_3sat + 2)])
            v_max_3sat += 2
        elif len(clause) == 2:
            t_sat.add_clause([clause[0], clause[1], v_max_3sat + 1])
            t_sat.add_clause([clause[0], clause[1], -(v_max_3sat + 1)])
            v_max_3sat += 1
        elif len(clause) == 3:
            t_sat.add_clause(clause)
        else:
            c_len = len(clause)
            for i in range(c_len):
                if 1 <= i <= c_len - 4:
                    t_sat.add_clause(
                        [clause[i + 1], -(v_max_3sat + i), v_max_3sat + i + 1])
                elif i == 0:
                    t_sat.add_clause([clause[0], clause[1], v_max_3sat + 1])
                else:
                    t_sat.add_clause(
                        [clause[-2], clause[-1], -(v_max_3sat + i)])
                    v_max_3sat = v_max_3sat + i
                    break
    return t_sat


def jw_heuristic(cnf: CNF) -> list[float]:
    """JW heuristic algorithm.

    Args:
        cnf (CNF): A list of clauses.

    Returns:
        list[int]: List of assignments. The index of the list corresponds to
            the variable number, and the value to the inverse probability.

    """
    # Initialize the score, add one because there's no var 0
    scores = [0] * (cnf.nvars() + 1)
    total = 0
    for clause in cnf.clauses():
        for var in clause:
            scores[abs(var)] += len(clause)
            total += len(clause)

    # Normalize and inverse scores
    scores = [total - x for x in scores]
    total = sum(scores)
    scores = [x / total for x in scores]

    return [sum(scores[:i+1]) for i in range(len(scores))]


def moms_heuristic(cnf: CNF) -> list[float]:
    """MOMS heuristic algorithm. (maximum occurences in clauses of
    minimum size)

    Args:
        cnf (CNF): A list of clauses.

    Returns:
        list[int]: List of assignments. The index of the list corresponds to
            the variable number, and the value to the probability.
    """
    # Initialize the score, add one because there's no var 0
    scores = [0] * (cnf.nvars() + 1)
    total = 0

    clauses_copy = cnf.clauses()

    while clauses_copy:
        min_size = min(len(clause) for clause in clauses_copy)
        for clause in clauses_copy:
            if len(clause) == min_size:
                for var in clause:
                    scores[abs(var)] += 1
                    total += 1
        clauses_copy = [
            clause for clause in clauses_copy if len(clause) != min_size]

    # Normalize and inverse scores
    scores = [total - x for x in scores]
    total = sum(scores)
    scores = [x / total for x in scores]

    return [sum(scores[:i+1]) for i in range(len(scores))]


def custom_random_choice(scores: list[float]):
    rand_num = random()

    for i, cum_prob in enumerate(scores):
        if rand_num <= cum_prob:
            return i


def walk_sat(cnf: CNF, heuristic: str = None) -> list[int]:
    """WalkSAT algorithm.

    Args:
        cnf (CNF): A list of clauses.

    Returns:
        list[int]: List of assignments. The index of the list corresponds to
            the variable number, and the value to the assignment.
    """
    # Clean the CNF formula
    # Commented because slower than possible gains
    # delete_valid_clauses(cnf)

    # Initialize the model
    model = []
    for i in range(1, cnf.nvars()+1):
        model.append(i)

    # Run heuristic algorithm
    if heuristic:
        heuristic = heuristic.lower()
        if heuristic == 'jw':
            score = jw_heuristic(cnf)
        elif heuristic == 'moms':
            score = moms_heuristic(cnf)

    MAX_ITERATION = 100000
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
        if x <= 0.6:
            # Random choice
            y = abs(choice(clause))
        else:
            if heuristic:
                # Deterministic choice (probability inverse of score)
                y = custom_random_choice(score)
            else:
                y = abs(clause[0])

        # Flip the variable
        model[y-1] = model[y-1] * (-1)
        n_iter += 1

    print("Itération maximale atteinte")

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
