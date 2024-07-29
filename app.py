from flask import Flask, render_template, request, redirect, flash
import os
import random
import numpy as np
from keras.models import load_model
import cv2

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with your secret key

# Configure the static URL path and folder
app.static_url_path = '/static'
app.static_folder = 'static'

# Load your trained models
subject_id_model = load_model('subject_id_model.h5')
finger_number_model = load_model('finger_number_model.h5')


def show_fingername(fingernum):
    if fingernum >= 5:
        fingername = "Right "
        fingernum -= 5
    else:
        fingername = "Left "
    if fingernum == 0:
        fingername += "Little"
    elif fingernum == 1:
        fingername += "Ring"
    elif fingernum == 2:
        fingername += "Middle"
    elif fingernum == 3:
        fingername += "Index"
    else:
        fingername += "Thumb"
    return fingername + " Finger"


def detect_fingerprint(image_path):
    try:
        # Load the image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            raise Exception("Image not found")

        # Apply Canny edge detection
        edges = cv2.Canny(img, 50, 150)

        # Calculate the percentage of non-zero pixels (edges)
        total_pixels = img.shape[0] * img.shape[1]
        edge_pixels = cv2.countNonZero(edges)
        edge_percentage = (edge_pixels / total_pixels) * 100

        return edge_percentage

    except Exception as e:
        print(f"Error: {e}")
        return 0  # Return 0 in case of an error


# Define the 'home' route to render the upload form
@app.route('/')
def home():
    return render_template('index.html')

# Define the 'upload' route to handle image uploads and make predictions
@app.route('/upload', methods=['POST'])
def upload():
    # Handle image upload here
    if 'file' not in request.files:
        flash("File Not Selected")
        return redirect('/')

    file = request.files['file']

    if file.filename == '':
        return redirect('/')

    if file:
        image = file.read()  # Get the binary image data

        # Save the uploaded image to the 'uploads' folder
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        image_path = os.path.join(upload_folder, file.filename)
        with open(image_path, 'wb') as img_file:
            img_file.write(image)

        # Call the fingerprint detection function
        ridge_percentage = detect_fingerprint(image_path)

        if ridge_percentage < 20:
            flash("Not a fingerprint")
        else:
            # Convert the image to grayscale
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            img = cv2.resize(img, (96, 96))  # Resize the image to 96x96
            img = img / 255.0  # Normalize to [0, 1]

            # Make predictions

            subject_id_pred = subject_id_model.predict(np.expand_dims(img, axis=0))
            finger_number_pred = finger_number_model.predict(np.expand_dims(img, axis=0))

            # Extract finger names using your show_fingername function
            Id_pred = np.argmax(subject_id_pred)
            finger_pred = np.argmax(finger_number_pred)
            fing_no = show_fingername(finger_pred)
            id = Id_pred + 1
            flash(f"Predicted Id: {id}, Finger Names: {fing_no}")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
