import dataclasses
import os
import glob

import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
from torch import nn
from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor


@dataclasses.dataclass
class Face_Image:
    name: str
    path: str
    label: np.ndarray


class FaceSegmentation:
    def __init__(self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.image_processor = SegformerImageProcessor.from_pretrained(
            "jonathandinu/face-parsing"
        )
        self.model = SegformerForSemanticSegmentation.from_pretrained(
            "jonathandinu/face-parsing"
        )
        self.model.to(self.device)

    def segment_face(self, image_input_path, output_path, output_mask_path):
        print(f"Segmenting face in {image_input_path}")

        image = Image.open(image_input_path)
        inputs = self.image_processor(images=image, return_tensors="pt").to(self.device)
        outputs = self.model(**inputs)
        logits = outputs.logits

        # resize output to match input image dimensions

        upsampled_logits = nn.functional.interpolate(
            logits,
            size=image.size[::-1],
            mode="bilinear",
            align_corners=False,  # H x W
        )
        labels = upsampled_logits.argmax(dim=1)[0]

        labels_viz = labels.cpu().numpy()

        if output_path:
            ##save the segmented image with the same name + _segmented in the output directory

            plt.imsave(output_path, labels_viz)

        if output_mask_path:
            ##save the mask npy file with the same name + _mask in the output directory

            np.save(output_mask_path, labels_viz)


if __name__ == "__main__":
    face_raw_dir = "/home/zwhy/skin_cancer_scanner/data/faces/raw"
    face_output_dir = "/home/zwhy/skin_cancer_scanner/data/faces/segmented"
    face_mask_dir = "/home/zwhy/skin_cancer_scanner/data/faces/mask"

    input_images = glob.glob(os.path.join(face_raw_dir, "*.png"))
    input_image = input_images[0]
    output_image_name = os.path.basename(input_image).split(".")[0] + "_segmented.png"
    output_image_path = os.path.join(face_output_dir, output_image_name)
    output_mask_output_name = os.path.basename(input_image).split(".")[0] + "_mask.npy"
    output_mask_path = os.path.join(face_mask_dir, output_mask_output_name)

    print(f"Segmenting face in {input_image}")
    print(f"Saving segmented image to {output_image_path}")
    print(f"Saving mask to {output_mask_path}")
    face_segmentation = FaceSegmentation()

    face_segmentation.segment_face(
        input_image,
        output_image_path,
        output_mask_path,
    )
