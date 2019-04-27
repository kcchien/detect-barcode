# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2
import numpy as np


# decode barcode image
def decode(input_image):
    """Decode barcode image

    :param input_image:
    :return:pyzbar decoded object
    """
    # decode object will look likes below:
    # [
    # Decoded(
    #     data=b'I002-00165498',
    #     type='CODE128',
    #     rect=Rect(
    #               left=1498,
    #               top=869,
    #               width=477,
    #               height=73
    #          ),
    #      polygon=[
    #          Point(x=1498, y=869),
    #          Point(x=1498, y=941),
    #          Point(x=1974, y=942),
    #          Point(x=1975, y=900),
    #          Point(x=1975, y=874)]
    #     )
    # ]

    return pyzbar.decode(input_image)


def draw_bounding_box(input_image, point1: tuple, point2: tuple, color=(0, 0, 255), thickness=5):
    """
    Draw a rectangle bounding box of barcode
    :param input_image:
    :param point1:
    :param point2:
    :param color:
    :param thickness:
    :return:
    """
    cv2.rectangle(input_image, point1, point2, color, thickness)


def draw_poly_bounding_box(input_image, points):
    """
    Draw a polygon bounding box of barcode
    :param input_image:
    :param points:
    :return:
    """
    # If the points do not form a quad, find convex hull
    if len(points) > 4:
        hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
        hull = list(map(tuple, np.squeeze(hull)))
    else:
        hull = points

    # Number of points in the convex hull
    n = len(hull)

    # Draw the convext hull
    for j in range(0, n):
        cv2.line(input_image, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)


def draw_barcode_text(input_image, text, x, y, padding=10, font_scale=1, color=(0, 0, 255), thickness=2):
    """
    Draw barcode information text
    :param input_image:
    :param text:
    :param x:
    :param y:
    :param padding:
    :param font_scale:
    :param color:
    :param thickness:
    :return:
    """
    cv2.putText(input_image, text, (x, y - padding), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)


def display(input_image, decoded_objects):
    """
    Display barcode and QR code location
    :param input_image:
    :param decoded_objects:
    :return:
    """
    # Loop over all decoded objects
    for decoded_object in decoded_objects:
        # extract information from decoded barcode object
        points = decoded_object.polygon
        (x, y, w, h) = decoded_object.rect
        barcode_data = decoded_object.data.decode("utf-8")
        barcode_type = decoded_object.type

        text = "{} ({})".format(barcode_data, barcode_type)

        draw_bounding_box(input_image, (x, y), (x + w, y + h))

        draw_poly_bounding_box(input_image, points)

        # draw the barcode data and barcode type on the image
        draw_barcode_text(input_image, text, x, y)

        print("[INFO] Found {} barcode: {}".format(barcode_type, barcode_data))

    # Display results
    cv2.imshow("Decoded results", input_image)
    cv2.waitKey(0)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")

args = vars(ap.parse_args())

if __name__ == '__main__':

    # load the input image with OpenCV
    image = cv2.imread(args["image"])

    # Decode barcode
    decoded = decode(image)

    # Display image with decoded information
    display(image, decoded)

