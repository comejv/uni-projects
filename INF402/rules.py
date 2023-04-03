from classes import Bridge, Bridges, Node


def n_choose_k(list: list, n: int) -> list[list]:
    """ Return all the combinations of n elements in the list l.

    Args:
        l (list): list to take elements from.
        n (int): number of elements to take.

    Returns:
        list: list of all the combinations of n elements in the list l.
    """
    if n == 0:
        return [[]]
    if len(list) == 0:
        return []
    return [([list[0]] + x) for x in n_choose_k(list[1:], n - 1)] + n_choose_k(list[1:], n)


def lvl2_impl_lvl1(cases: list[list]) -> list[list]:
    """Clean the cases where a lvl 2 bridge is alone.

    Args:
        cases (list[list]): list of cases.

    Returns:
        list[list]: list of cases where a lvl 2 bridge is not alone.
    """
    clean_cases = []
    for case in cases:
        lvl1 = [b.n2 for b in case if b.lvl == 1]
        lvl2 = [b.n2 for b in case if b.lvl == 2]
        if not lvl2:
            clean_cases.append(case)
        else:
            for node in lvl2:
                if node not in lvl1:
                    break
                clean_cases.append(case)
    return clean_cases


# Rule 1: A node must have its number in bridges connected to it.
def connect_node(node: Node) -> list[Bridges]:
    """Return all the possible bridge configurations for a node.

    Args:
        node (Node): node to connect.

    Returns:
        list[Bridges]: list of all the possible bridge configurations for a node.
    """
    # Lister tous les ponts possibles
    bridges = [Bridge(x, node, neigh) for x in [1, 2]
               for neigh in node.neighbours]

    # List all bridges combinations (node.value out of bridges)
    cases = n_choose_k(bridges, node.value)

    # Supprimer les ponts de niveau 2 qui sont sans pont de niveau 1
    clean_cases = lvl2_impl_lvl1(cases)

    return clean_cases
