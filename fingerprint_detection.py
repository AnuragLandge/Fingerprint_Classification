import cv2
import numpy as np

def detect_fingerprint(image_data):
    # Convert the image data to a NumPy array
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Apply Gaussian blur to the image to reduce noise
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Apply ridge detection using the Sobel fter
    gradient_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    gradient_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
    gradient_magnitude = cv2.magnitude(gradient_x, gradient_y)

    # Threshold the gradient magnitude to detect ridges
    threshold = 50
    ridge_mask = gradient_magnitude > threshold

    # Calculate the percentage of ridge pixels in the image
    ridge_pixel_count = np.count_nonzero(ridge_mask)
    total_pixel_count = img.shape[0] * img.shape[1]
    ridge_percentage = (ridge_pixel_count / total_pixel_count) * 100

    return ridge_percentage


