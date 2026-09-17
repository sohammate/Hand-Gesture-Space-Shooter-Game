import cv2
import mediapipe as mp


# ==================================================
# HAND TRACKER
# ==================================================

class HandTracker:

    def __init__(
        self,
        model_path="hand_landmarker.task"
    ):

        self.model_path = model_path

        # ==================================================
        # MEDIAPIPE TASKS API
        # ==================================================

        BaseOptions = mp.tasks.BaseOptions

        HandLandmarker = (
            mp.tasks.vision.HandLandmarker
        )

        HandLandmarkerOptions = (
            mp.tasks.vision.HandLandmarkerOptions
        )

        VisionRunningMode = (
            mp.tasks.vision.RunningMode
        )


        # ==================================================
        # HAND LANDMARKER OPTIONS
        # ==================================================

        options = HandLandmarkerOptions(

            base_options=BaseOptions(
                model_asset_path=self.model_path
            ),

            running_mode=(
                VisionRunningMode.IMAGE
            ),

            num_hands=1,

            min_hand_detection_confidence=0.5,

            min_hand_presence_confidence=0.5,

            min_tracking_confidence=0.5
        )


        # ==================================================
        # CREATE HAND LANDMARKER
        # ==================================================

        self.landmarker = (
            HandLandmarker.create_from_options(
                options
            )
        )


        # ==================================================
        # CAMERA
        # ==================================================

        self.camera = cv2.VideoCapture(0)

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )


        # ==================================================
        # GESTURE VARIABLES
        # ==================================================

        self.hand_detected = False

        self.index_x = 0.5

        self.index_folded = False

        self.open_palm = False

        # New three-finger gesture

        self.three_finger = False


    # ==================================================
    # UPDATE HAND
    # ==================================================

    def update(self):

        success, frame = (
            self.camera.read()
        )


        # ==================================================
        # CAMERA FAILURE
        # ==================================================

        if not success:

            self.hand_detected = False

            self.index_folded = False

            self.open_palm = False

            self.three_finger = False

            return None


        # ==================================================
        # FLIP CAMERA
        # ==================================================

        frame = cv2.flip(
            frame,
            1
        )


        # ==================================================
        # CONVERT BGR → RGB
        # ==================================================

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # ==================================================
        # CREATE MEDIAPIPE IMAGE
        # ==================================================

        mp_image = mp.Image(

            image_format=(
                mp.ImageFormat.SRGB
            ),

            data=rgb_frame
        )


        # ==================================================
        # DETECT HAND
        # ==================================================

        results = (
            self.landmarker.detect(
                mp_image
            )
        )


        # ==================================================
        # RESET GESTURES
        # ==================================================

        self.hand_detected = False

        self.index_folded = False

        self.open_palm = False

        self.three_finger = False


        # ==================================================
        # HAND FOUND
        # ==================================================

        if results.hand_landmarks:

            landmarks = (
                results.hand_landmarks[0]
            )

            self.hand_detected = True


            # ==================================================
            # INDEX FINGER POSITION
            # ==================================================

            index_tip = landmarks[8]

            self.index_x = index_tip.x


            # ==================================================
            # CHECK FINGERS
            # ==================================================

            index_extended = (
                self._is_finger_extended(
                    landmarks,
                    8,
                    6
                )
            )

            middle_extended = (
                self._is_finger_extended(
                    landmarks,
                    12,
                    10
                )
            )

            ring_extended = (
                self._is_finger_extended(
                    landmarks,
                    16,
                    14
                )
            )

            pinky_extended = (
                self._is_finger_extended(
                    landmarks,
                    20,
                    18
                )
            )


            # ==================================================
            # INDEX FOLDED
            # ==================================================

            self.index_folded = (
                not index_extended
            )


            # ==================================================
            # OPEN PALM
            # ==================================================

            self.open_palm = (

                index_extended

                and middle_extended

                and ring_extended

                and pinky_extended
            )


            # ==================================================
            # THREE-FINGER GESTURE
            # ==================================================
            #
            # Index  → Extended
            # Middle → Extended
            # Ring   → Extended
            # Pinky  → Folded
            #
            # This creates:
            #
            #       ☝️ + middle + ring
            #
            # Used for the special
            # multi-direction attack.
            #
            # ==================================================

            self.three_finger = (

                index_extended

                and middle_extended

                and ring_extended

                and not pinky_extended
            )


        return frame


    # ==================================================
    # FINGER EXTENSION DETECTION
    # ==================================================

    def _is_finger_extended(
        self,
        landmarks,
        tip_index,
        pip_index
    ):

        tip = landmarks[
            tip_index
        ]

        pip = landmarks[
            pip_index
        ]


        return (
            tip.y < pip.y
        )


    # ==================================================
    # GET INDEX X
    # ==================================================

    def get_index_x(self):

        return self.index_x


    # ==================================================
    # HAND DETECTED
    # ==================================================

    def is_hand_detected(self):

        return self.hand_detected


    # ==================================================
    # INDEX FOLDED
    # ==================================================

    def is_index_folded(self):

        return self.index_folded


    # ==================================================
    # OPEN PALM
    # ==================================================

    def is_open_palm(self):

        return self.open_palm


    # ==================================================
    # THREE-FINGER GESTURE
    # ==================================================

    def is_three_finger(self):

        return self.three_finger


    # ==================================================
    # RELEASE
    # ==================================================

    def release(self):

        self.camera.release()

        self.landmarker.close()