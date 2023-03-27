import json
from sys import argv
import cv2 as cv
from numpy import array, argmax, resize
import onnxruntime


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
                 islands: list[tuple[tuple[int, int], int]],
                 bridges: list[tuple[int, int]]) -> cv.Mat:
    """Draw bridges on an image.

    Args:
        img (cv.Mat): OpenCV matrice of an image. Image is not altered.
        bridges (list[tuple[int, int]]): list of (n, m) index of each bridge's
        start and end island.

    Returns:
        cv.Mat: OpenCV matrice of the image with bridges drawn.
    """
    for bridge in bridges:
        start = tuple(map(int, islands[bridge[0]][0]))
        end = tuple(map(int, islands[bridge[1]][0]))
        cv.line(img, start, end, (0, 0, 255), 2)

    return img


if __name__ == '__main__':
    if len(argv) != 2:
        im_path = print(
            'Please enter the path to the image you want to process:')
    else:
        im_path = argv[1]

    # Read and show original image
    img = cv.imread(im_path)

    cv.imshow("Original", img)
    cv.waitKey(2000)

    # Preprocess image and get islands contours
    imbinary = preprocess_image(img)
    islands = get_enclosing_circles(imbinary)

    # Get patches of numbers inside islands
    patches = get_inscribed_rectangle(imbinary, islands)

    for i, patch in enumerate(patches):
        cv.imshow("Number", patch)
        print(digit_ocr(patch), islands[i][0])
        cv.waitKey(10000)

    bridges = [(0, 1), (2, 3), (4, 5)]
    imbridges = draw_bridges(img, islands, bridges)

    cv.imshow("Bridges", imbridges)
    cv.waitKey(10000)
