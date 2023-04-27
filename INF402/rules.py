from classes import Bridge, Bridges, Node, Arc, Way


def n_choose_k(list: list[Bridge], n: int) -> list[list]:
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
    return [([list[0].get_neg()] + x) for x in n_choose_k(list[1:], n - 1)] + n_choose_k(list[1:], n)


def lvl2_impl_lvl1(cases: list[list]) -> list[list]:
    """Clean the cases where a lvl 2 bridge is alone.

    Args:
        cases (list[list]): list of cases.

    Returns:
        list[list]: list of cases where a lvl 2 bridge is not alone.
    """
    clean_cases = []

    # For each case
    for case in cases:
        # Sort bridges by lvl
        lvl1 = []
        lvl2 = []
        for bridge in case:
            if bridge.lvl == -1:
                lvl1.append(bridge)
            elif bridge.lvl == -2:
                lvl2.append(bridge)

        if not lvl1:
            clean_cases.append(case)
        else:
            skip = False
            for bridge in lvl2:
                b1 = Bridge(-1, bridge.n1, bridge.n2)
                if b1 not in lvl1:
                    skip = True
                    break
            if skip:
                clean_cases.append(case)
    return clean_cases


# Rule 1: A node must have its number in bridges connected to it.
def connect_node(node: Node) -> list[Bridges]:
    """Returns all the possible bridge configurations for a node (DNF).

    Args:
        node (Node): node to connect.

    Returns:
        list[Bridges]: DNF list of all the possible bridge configurations for a node.
    """
    # Lister tous les ponts possibles
    bridges = [Bridge(x, node, neigh) for x in [1, 2]
               for neigh in node.neighbours]

    cases = []

    # List all bridges combinations (node.value out of bridges)
    n = len(node.neighbours)*2
    for i in range(1, n+1):
        if i != node.value:
            cases = cases + n_choose_k(bridges, i)
        else:
            cases = cases + lvl2_impl_lvl1(n_choose_k(bridges, i))

    # Add negatives to the cases
    for case in cases:
        for bridge in bridges:
            if bridge.get_neg() not in case:
                case.append(bridge)

    # If node.value is 0, add all bridges as negatives
    case_0 = []
    for i in bridges:
        if i.lvl == 1:
            case_0.append(i)
    cases.append(case_0)

    # Delete cases where a lvl 2 bridge is alone
    # clean_cases = lvl2_impl_lvl1(cases)

    return cases


def no_crossing(bridges: list[Bridges]) -> list[list[Bridges]]:
    """Returns CNF stating that bridges can't cross.

    Args:
        bridges (list[Bridges]): list of possible bridges.

    Returns:
        list[list[Bridges]]: CNF stating that bridges can't cross.
    """
    cnf = []
    horizontal = []
    vertical = []
    for bridge in bridges.dict.values():
        if bridge.horizontal():
            horizontal.append(bridge)
        else:
            vertical.append(bridge)

    for bridge in horizontal:
        for bridge2 in vertical:
            # If bridge is between bridge2 nodes and bridge2 is between bridge nodes
            if bridge.n1.x > bridge2.n1.x and bridge.n1.x < bridge2.n2.x \
                    and bridge2.n1.y > bridge.n1.y and bridge2.n1.y < bridge.n2.y:
                cnf.append([bridge.get_neg(), bridge2.get_neg()])
    return cnf


def fp(n1:Node,n2:Node,deja:list[Node]):
    if n1 == n2:
        return True
    b=False
    for e in n1.neighbours:
        if e not in deja:
            b = b or fp(e,n2,deja + [n1])
    return b

def find_paths(n1: Node, n2: Node, deja_vu: list[Node] = []) -> list[list]:
    """Returns all the paths between n1 and n2.

    Args:
        n1 (Node): First node.
        n2 (Node): Second node.
        deja_vu (list[Node], optional): List of nodes already visited. Defaults to [].

    Returns:
        list: List of all the paths between n1 and n2.
    """
    if n1.id == n2.id:
        return [[Way(n1, n2, True)]]
    paths = [[Way(n1, n2, False)]]
    temp_list = []
    for neigh in n1.neighbours:
        outgoings = []
        arriving = []
        if neigh not in deja_vu:
            neigh_paths = find_paths(neigh, n2, deja_vu + [n1])
            if neigh_paths != []:
                temp_list.append([Arc(n1, neigh, False),
                                  Bridge(1, n1, neigh)])
                temp_list += neigh_paths
        if fp(neigh,n2, deja_vu):
            for path in paths:
                outgoings.append(path + [Arc(n1, neigh, True)])
                arriving.append(path + [Way(neigh, n2, True)])
            paths = outgoings + arriving
    if len(paths) == 1 :
        return []
    return paths + temp_list


def delete_incomplete_clause(clause: list[list]) -> list[list]:
    for i,e in enumerate(clause) :
        pop=False
        for j,f in enumerate(clause) :
            if i != j :
                if f == e :
                    pop=True
                elif f[0] == e[0]:
                    pop=True
                    clause[j]+=e[1:]
        if pop:
            clause.pop(i)
    return clause

def nul(nodes: list[Node]):
    clause = []
    for n in nodes:
        for node in nodes :
            if n != node:
                paths = [[Way(n,node,False)]]
                for neigh in node.neighbours:
                    outgoings = []
                    arriving = []    
                    for path in paths:
                        outgoings.append(path + [Arc(node, neigh, True)])
                        arriving.append(path + [Way(neigh, node, True)])
                    paths = outgoings + arriving
                    clause.append([Arc(node, neigh, False),
                                    Bridge(1, node, neigh)])
            else:
                paths = [[Way(n,node,True)]]
            clause += paths


    node_init = nodes[0]
    for node in nodes[1:]:
        clause.append([Way(node_init, node, True)])

    for node_x in nodes:
        for neigh in node_x.neighbours:
            clause.append([Arc(node_x,neigh,False), Arc(neigh,node_x,False)])

    return clause

def connexite(nodes: list[Node]):
    node_init = nodes[0]
    clause = []
    for node in nodes[1:]:
        clause.append([Way(node_init, node, True)])
        clause = clause + find_paths(node_init, node)
    for node_x in nodes:
        for neigh in node_x.neighbours:
            clause.append([Arc(node_x,neigh,False), Arc(neigh,node_x,False)])
    return clause
