import cv2
import mediapipe as mp
import requests

LAPTOP_IP = "192.168.46.202"  # Change this to your laptop's IP
FILE_URL = f"http://{LAPTOP_IP}:5000/download"

# Initialize hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect open hand (palm facing forward)
            palm_base = landmarks.landmark[mp_hands.HandLandmark.WRIST].y
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

            if index_tip < palm_base - 0.2:
                print("[INFO] Open hand detected! Downloading file...")
                response = requests.get(FILE_URL)
                with open("received_file", "wb") as file:
                    file.write(response.content)
                print("[SUCCESS] File received!")

    cv2.imshow("Hand Gesture Receiver", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
