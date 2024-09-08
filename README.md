Here’s a **detailed README** for your Flask-based fingerprint classification project. You can use it in your GitHub repository.

---

# Fingerprint Classification with Flask

This project is a Flask-based web application that allows users to upload fingerprint images, which are then processed and classified using pre-trained models. The application detects whether the uploaded image is a fingerprint, identifies the subject ID, and classifies the finger used in the fingerprint image (e.g., left thumb, right index).

## Table of Contents

1. [Installation](#installation)
2. [How It Works](#how-it-works)
3. [Folder Structure](#folder-structure)
4. [Usage](#usage)
5. [Models Used](#models-used)
6. [Detecting Fingerprints](#detecting-fingerprints)
7. [Routes and Endpoints](#routes-and-endpoints)
8. [Example](#example)
9. [Credits](#credits)

---

## Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtual environment (optional, but recommended)

### Libraries

Before starting, you need to install the following dependencies:

```bash
pip install flask keras opencv-python numpy
```

If you're using a virtual environment (recommended), activate it before installing dependencies.

### Cloning the Repository

```bash
git clone https://github.com/AnuragLandge/Fingerprint_Classification.git
cd Fingerprint_Classification
```

### Downloading Pre-trained Models

Ensure you have the following pre-trained models in the root directory:
- `subject_id_model.h5`
- `finger_number_model.h5`

You can either train these models or acquire pre-trained versions. Place them in the same directory as the app.

---

## How It Works

The application works as follows:

1. **Image Upload**: A user uploads a fingerprint image via the web interface.
2. **Pre-processing**: The image is processed (converted to grayscale, resized, and normalized).
3. **Fingerprint Detection**: The app checks if the uploaded image is a valid fingerprint by calculating ridge patterns using Canny or Sobel edge detection.
4. **Prediction**: Two pre-trained models are used:
   - **Subject ID Model**: Predicts the ID of the person based on the fingerprint.
   - **Finger Number Model**: Classifies the fingerprint as a specific finger (e.g., left thumb, right index, etc.).
5. **Result Display**: The predicted subject ID and finger name are shown on the web interface.

---

## Folder Structure

```bash
Fingerprint_Classification/
│
├── app.py  # Main Flask app
├── subject_id_model.h5  # Pre-trained model for subject ID prediction
├── finger_number_model.h5  # Pre-trained model for finger classification
├── templates/
│   └── index.html  # HTML template for the homepage
├── static/  # Static files (CSS, JS, images)
├── uploads/  # Folder for storing uploaded fingerprint images
└── README.md  # This README file
```

---

## Usage

### 1. Running the Application

After installing the dependencies, you can start the Flask application by running the following command:

```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000/`.

### 2. Upload a Fingerprint

- Go to the homepage.
- Upload an image in `.jpg`, `.png`, or `.jpeg` format.
- The app will process the image and return the predicted subject ID and finger name (e.g., "Right Thumb Finger").

### 3. Detecting Fingerprints

The app uses edge detection (Canny/Sobel) to determine if the uploaded image is a valid fingerprint. If less than 20% of the image is composed of edges, the app will reject the image as "Not a fingerprint."

---

## Models Used

1. **Subject ID Model**: This model is responsible for identifying the individual based on their fingerprint.
   - The model takes in a grayscale image of size 96x96 and outputs a predicted class (subject ID).
   - Example: If there are 10 subjects, it will predict a number from 1 to 10.

2. **Finger Number Model**: This model identifies which finger was used to capture the fingerprint (e.g., left thumb, right index).
   - It also takes in a grayscale image of size 96x96 and outputs a number from 0 to 9 (where 0 corresponds to the left little finger, and 9 corresponds to the right thumb).

---

## Detecting Fingerprints

To detect whether an uploaded image is a valid fingerprint, the application first applies Gaussian blur to reduce noise and then performs **Canny edge detection** or **Sobel edge detection**. 

- **Canny Edge Detection**: Used to identify strong edges in the image. The percentage of edge pixels (ridges) is calculated to determine if it's likely to be a fingerprint.
- If the detected edge percentage is below 20%, the image is considered "Not a fingerprint."

### Edge Detection Code Example

Here is the function that detects fingerprints based on edge detection:

```python
def detect_fingerprint(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(img, 50, 150)
    total_pixels = img.shape[0] * img.shape[1]
    edge_pixels = cv2.countNonZero(edges)
    edge_percentage = (edge_pixels / total_pixels) * 100
    return edge_percentage
```

---

## Routes and Endpoints

### `/`

- **Method**: `GET`
- **Description**: Displays the home page with the upload form.

### `/upload`

- **Method**: `POST`
- **Description**: Handles image upload, fingerprint detection, and model prediction.
- **Input**: A file upload (image).
- **Output**: Predicted subject ID and finger classification, or a rejection message if the image is not a fingerprint.

---

## Example

Once you upload an image, the app will predict the **subject ID** and **finger name** based on the fingerprint.

For example:
- Uploaded Image: Fingerprint image of a right thumb.
- Output: `Predicted Id: 3, Finger Names: Right Thumb Finger`

---

## Credits

- **Flask**: Python web framework.
- **OpenCV**: For image processing and edge detection.
- **Keras**: For loading and using the pre-trained models.

---


