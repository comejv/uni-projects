import json
from sys import argv
import cv2 as cv
from numpy import array, argmax, resize
import onnxruntime


class Ile:
    def __init__(self, x, y, w):
        self.x: int = x
        self.y: int = y
        self.weight: int = w
        self.neighbours: list[Ile] = []

    def __repr__(self) -> str:
        return f"Ile([{self.x}, {self.y}] : {self.weight})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def add_neighbour(self, neighbour):
        if neighbour not in self.neighbours and neighbour != self and type(neighbour) == Ile:
            self.neighbours.append(neighbour)
        else:
            print("Error: Neighbour not added")


def preprocess_image(img: cv.Mat) -> cv.Mat:
    # Convert to grayscale then to binary
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binary_img = cv.threshold(gray_img, 127, 255, cv.THRESH_BINARY_INV)

    return binary_img


def get_enclosing_circles(img: cv.Mat) -> list[tuple[tuple[int, int], int]]:
    """For every external contour, find the enclosing circle.

    Args:
        img (cv.Mat): OpenCV matrice of an image. Image is not altered.

    Returns:
        list[tuple(int, int), int]: list of (x, y) position of each circle's center
        and its radius.
    """
    # Find contours
    contours, hierarchy = cv.findContours(
        img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    clean_contours = [cnt for cnt in contours if cv.contourArea(cnt) > 50]
    polygons = [cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
                for cnt in clean_contours]

    # Get islands center position
    return [cv.minEnclosingCircle(polygon) for polygon in polygons]


def get_inscribed_rectangle(img: cv.Mat,
                            islands: list[tuple[tuple[int, int], int]]) -> list[cv.Mat]:
    """Get a rectangle inscribed in the enclosing circle of each island.

    Args:
        img (cv.Mat): OpenCV matrice of an image. Image is not altered.
        islands (list[tuple[int, int], int]): list of (x, y) position of each circle's center
        and its radius.

    Returns:
        list[cv.Mat]: list of OpenCV image matrice of each rectangle.
    """
    patches = []
    for island in islands:
        x, y = int(island[0][0]), int(island[0][1])
        length = int(1.1 * island[1])
        rect = cv.getRectSubPix(img, (length, length), (x, y))
        patches.append(rect)

    return patches


def digit_ocr(source_img: cv.Mat,
              model="data/mnist_model/mnist-8.onnx") -> int:
    """Perform digit OCR on a single image.

    Args:
        source_img (cv.Mat): OpenCV matrice of an image. Image is not altered.
        model (str, optional): Path to an onnx model. Model must have input of (1x1x28x28)
        and output of (1x10). Defaults to "data/mnist_model/mnist-8.onnx".

    Returns:
        int: The digit recognized by the model.
    """
    # Resize image
    img = cv.resize(source_img, dsize=(28, 28),
                    interpolation=cv.INTER_AREA)
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


def draw_bridges(img: cv.Mat,
                 ile1: Ile,
                 ile2: Ile,
                 col=(0, 0, 255)) -> cv.Mat:
    """Draw bridges on an image.

    Args:
        img (cv.Mat): OpenCV matrice of an image. Image is not altered.
        bridges (list[tuple[int, int]]): list of (n, m) index of each bridge's
        start and end island.

    Returns:
        cv.Mat: OpenCV matrice of the image with bridges drawn.
    """
    start = (int(ile1.x), int(ile1.y))
    end = (int(ile2.x), int(ile2.y))
    cv.line(img, start, end, col, 2)

    return img


def create_islands(img: cv.Mat) -> list[Ile]:
    """Create a list of Ile objects from an image.

    Args:
        img (cv.Mat): OpenCV matrice of an image. Image is not altered.

    Returns:
        list[Ile]: list of Ile objects.
    """
    iles = []

    # Preprocess image and get islands contours
    imbinary = preprocess_image(img)
    islands = get_enclosing_circles(imbinary)

    # Get patches of numbers inside islands
    patches = get_inscribed_rectangle(imbinary, islands)

    # Find edge width
    edge_width = min(min([island[0][1] for island in islands]),
                     min([island[0][0] for island in islands])) - islands[0][1]

    # Find average column width
    y_pos = [island[0][1] for island in islands]
    spacing = int(min([abs(y1-y2) for y1 in y_pos for y2 in y_pos if abs(y1 - y2) > .5]))

    # Create Ile objects
    for i, patch in enumerate(patches):
        x = int((islands[i][0][1] - edge_width)/spacing)
        y = int((islands[i][0][0] - edge_width)/spacing)
        iles.append(Ile(x, y, digit_ocr(patch)))

    # Sort islands by position (top to bottom, left to right)
    iles.sort(key=lambda x: (x.x, x.y))

    return iles


if __name__ == '__main__':
    if len(argv) != 2:
        impath = print(
            'Please enter the path to the image you want to process:')
    else:
        impath = argv[1]

    # Read original image
    img = cv.imread(impath)

    iles = create_islands(img)

    print(*iles, sep='\n')
