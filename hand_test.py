import cv2
import mediapipe as mp


# --------------------------------
# MediaPipe Hand Landmarker
# --------------------------------

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1
)


# --------------------------------
# Camera
# --------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not access camera")
    exit()


# --------------------------------
# Hand Detection
# --------------------------------

with HandLandmarker.create_from_options(options) as landmarker:

    while True:

        success, frame = camera.read()

        if not success:
            print("Could not read camera frame")
            break

        # Mirror the camera
        frame = cv2.flip(frame, 1)

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hand
        result = landmarker.detect(mp_image)


        # --------------------------------
        # Index Finger Detection
        # --------------------------------

        if result.hand_landmarks:

            for hand in result.hand_landmarks:

                height, width, _ = frame.shape

                # Landmark 8 = index finger tip
                index_tip = hand[8]

                x = int(index_tip.x * width)
                y = int(index_tip.y * height)


                # Draw large green dot
                cv2.circle(
                    frame,
                    (x, y),
                    12,
                    (0, 255, 0),
                    -1
                )


                # Display coordinates
                cv2.putText(
                    frame,
                    f"Index: ({x}, {y})",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2
                )


        # --------------------------------
        # Display Camera
        # --------------------------------

        cv2.imshow(
            "Gesture Hand Test",
            frame
        )


        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


# --------------------------------
# Cleanup
# --------------------------------

camera.release()
cv2.destroyAllWindows()