import cv2
import mediapipe as mp

# Import necessary libraries for computer vision (cv2) and hand/face detection (mediapipe)

# Initialize MediaPipe face and hand detection models
mp_face_detection = mp.solutions.face_detection  # Create a FaceDetection object
mp_drawing = mp.solutions.drawing_utils           # Create a DrawingUtils object for annotations

mp_hands = mp.solutions.hands                     # Create a Hands object for hand detection

# Start capturing video from the default camera (usually webcam)
cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(  # Create a FaceDetection context manager
     model_selection=1,                   # Select a fast face detection model (optional)
     min_detection_confidence=0.5) as face_detection, \
     mp_hands.Hands(                      # Create a Hands context manager
         min_detection_confidence=0.7,      # Set minimum confidence for hand detection
         min_tracking_confidence=0.5) as hands:  # Set minimum confidence for hand tracking

    while cap.isOpened():  # Loop as long as the video capture is open
        success, image = cap.read()  # Read a frame from the video capture

        if not success:  # Handle cases where no frame is read
            print("Ignoring empty camera frame.")
            # If working with a video, you might want to break the loop here
            break

        # Flip the image horizontally for a natural selfie-view display
        image = cv2.flip(image, 1)

        # Convert the BGR image (OpenCV color format) to RGB for MediaPipe processing
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with Face Detection
        results_face = face_detection.process(image_rgb)  # Detect faces in the image

        # Process the image with Hand Detection
        results_hands = hands.process(image_rgb)  # Detect hands in the image

        # Draw face detection annotations on the image
        if results_face.detections:  # Check if faces were detected
            for detection in results_face.detections:
                mp_drawing.draw_detection(image, detection)  # Draw rectangles around faces

        # Draw hand annotations on the image
        if results_hands.multi_hand_landmarks:  # Check if hands were detected
            for hand_landmarks in results_hands.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # Draw lines and dots for detected hand landmarks and connections

        # Display the processed image with annotations on the screen
        cv2.imshow('MediaPipe Face and Hand Detection', image)

        # Check for 'Esc' key press to exit the program
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
