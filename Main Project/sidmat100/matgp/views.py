from django.shortcuts import render
from matrimony.models import PersonalDetails
from django.shortcuts import get_object_or_404
from django.utils import timezone
import os

# Create your views here.


# matgp/views.py
from django.shortcuts import render
from django.http import HttpResponse
import cv2
import numpy as np
from gplearn.genetic import SymbolicRegressor

# Step 1: Define Feature Extraction Functions
def extract_laplacian_variance(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return np.var(laplacian)

def extract_edge_intensity(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return np.mean(edges)

# Step 2: Prepare Training Data
def prepare_training_data(image_paths, label):
    X_train = []
    y_train = []

    for path in image_paths:
        image = cv2.imread(path)
        features = [extract_laplacian_variance(image), extract_edge_intensity(image)]
        X_train.append(features)
        y_train.append(label)

    return np.array(X_train), np.array(y_train)

# Function to get image paths from a folder
def get_image_paths(folder_path):
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_paths.append(os.path.join(folder_path, filename))
    return image_paths

# Step 3: Define GP Model
gp_model = SymbolicRegressor(population_size=100, generations=50)

# Step 4: Train GP Model
def train_gp_model(X_train, y_train):
    gp_model.fit(X_train, y_train)

# Step 5: Prediction
def predict_image_blur(image):
    features = [extract_laplacian_variance(image), extract_edge_intensity(image)]
    prediction = gp_model.predict(np.array(features).reshape(1, -1))

    if prediction == 1:
        return True  # Return True if image is blurred
    else:
        return False  # Return False if image is sharp

# Example usage:
blurred_folder_path = "D:\\sidpy\\GP\\blurimages"
sharp_folder_path = "D:\\sidpy\\GP\\sharpimg"

blurred_image_paths = get_image_paths(blurred_folder_path)
sharp_image_paths = get_image_paths(sharp_folder_path)

X_train_blurred, y_train_blurred = prepare_training_data(blurred_image_paths, 1) # Label for blurred image
X_train_sharp, y_train_sharp = prepare_training_data(sharp_image_paths, 0) # Label for sharp image

X_train = np.concatenate((X_train_blurred, X_train_sharp))
y_train = np.concatenate((y_train_blurred, y_train_sharp))

train_gp_model(X_train, y_train)

def detect_faces(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        is_blurred = predict_image_blur(image)

        if is_blurred:
            result = "The image is blurred.Please Upload a clear Image."
        else:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) == 0:
                result = "Sorry No faces detected  Please Upload an Image with Clear Face."
            elif len(faces) == 1:
                user = request.user
                try:
                    personal_details = PersonalDetails.objects.get(user=user)
                except PersonalDetails.DoesNotExist:
                    # Create a new PersonalDetails object for the user
                    personal_details = PersonalDetails(user=user, date_of_birth=timezone.now())
                    personal_details.save()

                personal_details.profile_image.save('profile_image.jpg', image_file)
                personal_details.save()
                request.session['profile_image_url'] = personal_details.profile_image.url
                result = "The uploaded picture is verified and valid. This has been placed as your Final Profile Picture."
            else:
                result = " Multiple faces detected Please Upload an Image with a clear Face."

        return render(request, 'matgp/result.html', {'result': result})

    return render(request, 'matgp/upload.html')









