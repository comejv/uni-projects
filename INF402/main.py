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


def get_enclosing_circles(img: cv.Mat) -> list[tuple[int, int], int]:
    """For every external contour, find the enclosing circle.

    Args:
        img (cv.Mat): OpenCV matrice of an image. Image is not altered.

    Returns:
        list[tuple(int, int), int]: list of (x, y) position of each center and its radius.
    """
    # Find contours
    contours, hierarchy = cv.findContours(
        img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    clean_contours = [cnt for cnt in contours if cv.contourArea(cnt) > 50]
    polygons = [cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
                for cnt in clean_contours]

    # Get islands centroids (position)
    return [cv.minEnclosingCircle(polygon) for polygon in polygons]


def get_inscribed_rectangle(img: cv.Mat, islands: list[tuple[int, int], int]) -> list[cv.Mat]:
    patches = []
    for island in islands:
        x, y = int(island[0][0]), int(island[0][1])
        length = int(1.1 * island[1])
        rect = cv.getRectSubPix(img, (length, length), (x, y))
        patches.append(rect)

    return patches


def digit_ocr(source_img: cv.Mat, model="data/mnist_model/mnist-8.onnx") -> int:
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
    img = preprocess_image(img)
    islands = get_enclosing_circles(img)

    # Get patches of numbers inside islands
    patches = get_inscribed_rectangle(img, islands)

    for i, patch in enumerate(patches):
        cv.imshow("Number", patch)
        print(digit_ocr(patch), islands[i][0])
        cv.waitKey(10000)
