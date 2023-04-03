class Node:
    def __init__(self, id, x, y, v):
        self.id: int = id
        self.x: int = int(x)
        self.y: int = int(y)
        self.value: int = int(v)
        self.neighbours: list[Node] = []

    def __repr__(self) -> str:
        return f"Node({self.id} : [{self.x}, {self.y}], {self.value})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.id == other.id

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
        self.id = None
        self.get_id()

    def __repr__(self) -> str:
        return f"({self.n1} -> {self.n2}, lvl {self.lvl})"

    def get_id(self):
        if self.id:
            return self.id

        nl = sorted([self.n1, self.n2], key=lambda n: n.id)

        # On assume que les node.id < 100
        if self.lvl > 0:
            self.id = self.lvl * 10000 + nl[0].id * 100 + nl[1].id
        else:
            self.id = self.lvl * 10000 - nl[0].id * 100 - nl[1].id


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
        bridge = Bridge(lvl, n1, n2)

        if bridge.id not in self.dict:
            self.dict[bridge.id] = bridge
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
