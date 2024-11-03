import cv2
import mediapipe as mp

# Initialize the models
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

mp_hands = mp.solutions.hands

# Start the video capture
cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection, \
     mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, you might want to break the loop
      break

    # Flip the image horizontally for a selfie-view display
    image = cv2.flip(image, 1)

    # Convert the BGR image to RGB for MediaPipe processing
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image with Face Detection
    results_face = face_detection.process(image_rgb)

    # Process the image with Hand Detection
    results_hands = hands.process(image_rgb)

    # Draw the face detection annotations on the image.
    if results_face.detections:
      for detection in results_face.detections:
        mp_drawing.draw_detection(image, detection)

    # Draw the hand annotations on the image.
    if results_hands.multi_hand_landmarks:
      for hand_landmarks in results_hands.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('MediaPipe Face and Hand Detection', image)

    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()