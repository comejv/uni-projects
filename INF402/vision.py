import json
from os.path import isfile
from sys import argv

import cv2
import onnxruntime
from numpy import argmax, array, resize


def fatal(msg: str):
    print("\x1b[31m" + msg + "\x1b[0m")
    exit(1)


class Node:
    def __init__(self, x, y, v):
        self.x: int = int(x)
        self.y: int = int(y)
        self.value: int = int(v)
        self.neighbours: list[Node] = []

    def __repr__(self) -> str:
        return f"Node([{self.x}, {self.y}] : {self.value})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def add_neighbour(self, neighbour):
        if neighbour not in self.neighbours and neighbour != self and type(neighbour) == Node:
            self.neighbours.append(neighbour)
        else:
            raise ValueError("Neighbour not added")


def find_node(x: int, y: int, nodes: list[Node]) -> Node or None:
    for node in nodes:
        if node.x == x and node.y == y:
            return node

    return None


def preprocess_image(img: cv2.Mat) -> cv2.Mat:
    # Convert to grayscale then to binary
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV)

    return binary_img


def get_enclosing_circles(img: cv2.Mat) -> list[tuple[tuple[int, int], int]]:
    """For every external contour, find the enclosing circle.

    Args:
        img (cv2.Mat): OpenCV matrice of an image. Image is not altered.

    Returns:
        list[tuple(int, int), int]: list of (x, y) position of each circle's center
        and its radius.
    """
    # Find contours
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    clean_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 50]
    polygons = [cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
                for cnt in clean_contours]

    # Get circles center position
    return [cv2.minEnclosingCircle(polygon) for polygon in polygons]


def get_inscribed_rectangles(img: cv2.Mat,
                             circles: list[tuple[tuple[int, int], int]]) -> list[cv2.Mat]:
    """Get a rectangle inscribed in each circle.

    Args:
        img (cv2.Mat): OpenCV matrice of an image. Image is not altered.
        circles (list[tuple[int, int], int]): list of (x, y) position of each circle's center
        and its radius.

    Returns:
        list[cv2.Mat]: list of OpenCV image matrice of each rectangle.
    """
    patches = []
    for c in circles:
        x, y = int(c[0][0]), int(c[0][1])
        length = int(1.1 * c[1])
        rect = cv2.getRectSubPix(img, (length, length), (x, y))
        patches.append(rect)

    return patches


def digit_ocr(source_img: cv2.Mat,
              model="data/mnist_model/mnist-8.onnx") -> int:
    """Perform digit OCR on a single image.

    Args:
        source_img (cv2.Mat): OpenCV matrice of an image. Image is not altered.
        model (str, optional): Path to an onnx model. Model must have input of (1x1x28x28)
        and output of (1x10). Defaults to "data/mnist_model/mnist-8.onnx".

    Returns:
        int: The digit recognized by the model.
    """
    # Resize image
    img = cv2.resize(source_img, dsize=(28, 28),
                     interpolation=cv2.INTER_AREA)
    img = resize(img, (1, 1, 28, 28))

    # Image to readable input
    data = json.dumps({'data': img.tolist()})
    data = array(json.loads(data)['data']).astype('float32')

    # Inference
    session = onnxruntime.InferenceSession(model, None)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    result = session.run([output_name], {input_name: data})

    return int(argmax(array(result).squeeze(), axis=0))


def find_neighbours(nodes: list[Node], n_col: int):
    """Find the neighbours of each node.

    Args:
        nodes (list[Node]): list of node objects.
    """
    for node in nodes:
        x1, x2, y1, y2 = node.x, node.x, node.y, node.y

        while any([x1 > 0, x2 < n_col, y1 > 0, y2 < n_col]):
            x1, x2, y1, y2 = x1-1, x2+1, y1-1, y2+1
            up = find_node(x1, node.y, nodes) if x1 >= 0 else None
            down = find_node(x2, node.y, nodes) if x2 <= n_col else None
            left = find_node(node.x, y1, nodes) if y1 >= 0 else None
            right = find_node(node.x, y2, nodes) if y2 <= n_col else None

            if up:
                node.add_neighbour(up)
                x1 = -1
            if down:
                node.add_neighbour(down)
                x2 = n_col + 1
            if left:
                node.add_neighbour(left)
                y1 = -1
            if right:
                node.add_neighbour(right)
                y2 = n_col + 1

    return nodes


def create_nodes(img: cv2.Mat) -> list[Node]:
    """Create a list of node objects from an image.

    Args:
        img (cv2.Mat): OpenCV matrice of an image. Image is not altered.

    Returns:
        list[Node]: list of node objects.
    """
    nodes_list = []

    # Preprocess image and get nodes contours
    imbinary = preprocess_image(img)
    circles = get_enclosing_circles(imbinary)

    # Get patches of numbers inside circles
    patches = get_inscribed_rectangles(imbinary, circles)

    # Find img's minimum edge width (smallest circle coordinates - circle radius)
    edge_width = min([min(c[0]) for c in circles]) - circles[0][1]

    # Find minimum column width (smallest distance between two nodes)
    y_pos = [c[0][1] for c in circles]
    spacing = int(min([abs(y1-y2)
                  for y1 in y_pos for y2 in y_pos if abs(y1 - y2) > .5]))

    # Create node objects, find their relative position in the grid and value
    for i, patch in enumerate(patches):
        x = int((circles[i][0][1] - edge_width)/spacing)
        y = int((circles[i][0][0] - edge_width)/spacing)
        nodes_list.append(Node(x, y, digit_ocr(patch)))

    # Find neighbours
    find_neighbours(nodes_list, int((img.shape[0] - 2*edge_width)/spacing))

    # Sort nodes by position (top to bottom, left to right)
    nodes_list.sort(key=lambda x: (x.x, x.y))

    return nodes_list


def draw_bridge(img: cv2.Mat,
                node1: Node,
                node2: Node,
                col=(0, 0, 255)) -> cv2.Mat:
    """Draw bridges on an image.

    Args:
        img (cv2.Mat): OpenCV matrice of an image. Image is not altered.
        bridges (list[tuple[int, int]]): list of (n, m) index of each bridge's
        start and end node.

    Returns:
        cv2.Mat: OpenCV matrice of the image with bridges drawn.
    """
    if node1 not in node2.neighbours:
        return img
    start = (node1.x, node1.y)
    end = (node2.x, node2.y)
    cv2.line(img, start, end, col, 2)

    return img


if __name__ == '__main__':
    if len(argv) != 2:
        impath = input(
            "Please enter the path to the image you want to process:\n")
        while not isfile(impath):
            impath = input(
                "Path is not a file or doesn't exist. Please enter a valid path:\n")
    else:
        impath = argv[1]
        if not isfile(impath):
            fatal("Path is not a file or doesn't exist. Please enter a valid path.")

    # Read original image
    img = cv2.imread(impath)

    nodes = create_nodes(img)

    for node in nodes:
        print(node, node.neighbours)
