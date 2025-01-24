import os
import copy
import cv2
import numpy as np
import json


# hardcoded labels for face parsing model labels
FACE_PARSING_LABELS = [
    "background",
    "skin",
    "nose",
    "eye_g",
    "l_eye",
    "r_eye",
    "l_brow",
    "r_brow",
    "l_ear",
    "r_ear",
    "mouth",
    "u_lip",
    "l_lip",
    "hair",
    "hat",
    "ear_r",
    "neck_l",
    "neck",
    "cloth",
]


class BlobDetector:
    def __init__(self):
        self.params = cv2.SimpleBlobDetector_Params()
        self.params.filterByArea = True
        self.params.minArea = 100
        self.params.maxArea = 10000000
        self.params.minDistBetweenBlobs = 10

        self.params.filterByCircularity = True
        self.params.minCircularity = 0.2

        self.params.filterByColor = True
        self.params.blobColor = 0
        self.params.minThreshold = 50
        self.params.maxThreshold = 220
        self.params.thresholdStep = 10

        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.2

        self.params.filterByConvexity = True
        self.params.minConvexity = 0.1

        self.params.minRepeatability = 2

        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def set_params(self, params):
        self.params = copy.deepcopy(params)
        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def detect_blobs(self, image_path, gaussian_blur_kernel_size=3):
        image = cv2.imread(image_path)
        blur_image = cv2.GaussianBlur(
            image, (gaussian_blur_kernel_size, gaussian_blur_kernel_size), 0
        )
        keypoints = self.detector.detect(blur_image)

        return keypoints

    def draw_blobs(
        self, image_path, mask_path, keypoints, output_path, output_keypoints_path
    ):
        image = cv2.imread(image_path)

        skin_idx = FACE_PARSING_LABELS.index("skin")
        nose_idx = FACE_PARSING_LABELS.index("nose")

        mask = np.load(mask_path)

        keypoints_json = []

        for keypoint in keypoints:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            size = keypoint.size
            radius = int(size / 2)

            idx = mask[y, x]
            keypoints_json.append(
                {"x": x, "y": y, "size": size, "label": FACE_PARSING_LABELS[idx]}
            )

            if idx == skin_idx:
                color = (0, 255, 0)
            elif idx == nose_idx:
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)

            cv2.circle(image, (x, y), radius + 1, color, 2)

        # draw a legend for the colors
        cv2.putText(
            image,
            "Skin",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            "Nose",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            "Other",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )
        cv2.imwrite(output_path, image)

        with open(output_keypoints_path, "w") as f:
            json.dump(keypoints_json, f)


if __name__ == "__main__":

    image_path = (
        "/home/zwhy/QT_project/labeling_tool/test_data/face_001_ISIC_0029290.png"
    )
    mask_path = "/home/zwhy/QT_project/labeling_tool/test_data/segmented_images/masks/face_001_ISIC_0029290_mask.npy"
    output_path = "/home/zwhy/QT_project/labeling_tool/test_data/blob_images/face_001_ISIC_0029290_blobs.png"
    output_keypoints_path = "/home/zwhy/QT_project/labeling_tool/test_data/blob_images/keypoints/face_001_ISIC_0029290_keypoints.json"

    blob_detector = BlobDetector()
    keypoints = blob_detector.detect_blobs(image_path)
    blob_detector.draw_blobs(
        image_path, mask_path, keypoints, output_path, output_keypoints_path
    )
