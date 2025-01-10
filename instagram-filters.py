# Import modules
import cv2

import numpy as np


imagePath = "vaibhav.jpg"
image = cv2.imread(imagePath)

def pencilSketch(image, arguments=0):
    """
    Converts a given image into a pencil sketch-like representation using
    a combination of grayscale conversion, Gaussian Blur, Laplacian edge
    detection, and thresholding. This function processes a colored image
    to extract its edges and renders these edges in a binary format that
    resembles a pencil sketch.

    :param image: The source image to be converted to a pencil sketch.
    :type image: numpy.ndarray
    :param arguments: Placeholder for additional arguments, default is 0.
    :type arguments: int
    :return: An image that represents the pencil sketch of the source image.
    :rtype: numpy.ndarray
    """
    grayImage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gaussianBlurredImage=cv2.GaussianBlur(grayImage,(3,3),0,0)
    laplacianImage=cv2.Laplacian(gaussianBlurredImage,cv2.CV_32F,ksize=3,scale=1,delta=0)
    _,edges=cv2.threshold(laplacianImage,10,255,cv2.THRESH_BINARY_INV)
    pencilSketchImage=np.uint8(edges)
    pencilSketchImage=cv2.merge((pencilSketchImage,pencilSketchImage,pencilSketchImage))

    return pencilSketchImage


def cartoonify(image):
    """
    Converts an input image into a cartoonized version by applying multiple image
    processing techniques including edge detection, smoothing, and color manipulation.

    :param image: The input image that needs to be cartoonified.
                  The image should be in BGR color space and can be represented
                  as a NumPy array.
    :type image: numpy.ndarray
    :return: A cartoon-styled image obtained by blending edge detection results
             with enhanced and smoothed colors from the original image.
    :rtype: numpy.ndarray
    """
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_blurred = cv2.medianBlur(gray, 7)
    gaussianBlurredImage = cv2.GaussianBlur(grayImage, (3, 3), 0, 0)

    edges = cv2.Laplacian(gaussianBlurredImage, cv2.CV_8U, ksize=5)

    _, edges_inv = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)

    # reduce noise and smooth the image while keeping the edges sharp
    color_smoothed = cv2.bilateralFilter(image, 9, 300, 300)

    hsv = cv2.cvtColor(color_smoothed, cv2.COLOR_BGR2HSV)

    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)

    vibrant_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    cartoonImage = cv2.bitwise_and(vibrant_image, vibrant_image, mask=edges_inv)

    return cartoonImage




# Apply cartoonification
cartoon_image = cartoonify(image)

# Apply pencil sketching
pencil_sketch_image = pencilSketch(image)

# Display results
cv2.imshow("Original Image", image)
cv2.imshow("Cartoonified Image", cartoon_image)
cv2.imshow("Pencil Sketch", pencil_sketch_image)


c = cv2.waitKey(0)
cv2.destroyAllWindows()
