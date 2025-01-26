import sys
import os
import sqlite3
import glob
from natsort import natsort
from dataclasses import dataclass
import json

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QListWidgetItem,
    QTableWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

# Import the class from the generated ui_labeling_tool.py
from ui_labeling_tool_main import Ui_MainWindow
from init_db import init_db
from modules.face_segementation import FaceSegmentation
from modules.blob_detector import BlobDetector, BlobSettings


@dataclass
class Settings:
    """Dataclass to store settings."""

    db_path: str
    workspace_path: str
    seg_image_folder: str
    seg_mask_folder: str
    blob_image_folder: str
    blob_keypoints_folder: str


class LabelingTool(QMainWindow, Ui_MainWindow):
    def __init__(self, segmenter):
        super().__init__()
        self.setupUi(self)  # This initializes all widgets from the UI

        # Store database path
        self.dbStatus.setText("Waiting for directory selection...")

        # A list to keep track of images in the selected directory
        self.init_settings()
        self.init_blob_settings()

        self.image_paths = []
        self.seg_image_paths = []
        self.blob_image_paths = []

        self.current_index = 0
        self.focus_mode_enabled = False

        # Connect buttons (matching the object names from Qt Designer)
        self.actionOpen_Workspace.triggered.connect(self.open_directory)
        self.actionCreate_New_Database.triggered.connect(
            lambda: self.init_database(self.settings.workspace_path)
        )
        self.actionUpdate_Database.triggered.connect(
            lambda: self.update_database(self.settings.workspace_path)
        )
        self.actionParse_Current_Image.triggered.connect(
            self.face_segmentation_current_image
        )
        self.actionBlob_Detector_With_Face_Parsing.triggered.connect(
            self.blob_detector_current_image
        )

        self.addLabelButton.clicked.connect(self.add_label)
        self.removeLabelButton.clicked.connect(self.remove_label)
        self.prevImageButton.clicked.connect(self.prev_image)
        self.nextImageButton.clicked.connect(self.next_image)
        self.focusModeButton.clicked.connect(self.set_focus_mode)

        self.seg_tool = segmenter
        self.blob_detector = BlobDetector()

        # (Optional) Connect other signals/slots or do other setup...

    def init_settings(self):
        self.settings = Settings(
            db_path="",
            workspace_path="",
            seg_image_folder="",
            seg_mask_folder="",
            blob_image_folder="",
            blob_keypoints_folder="",
        )

    def update_settings_to_json(self, workspace_path):
        """Save current settings to directory"""
        settings_path = os.path.join(workspace_path, "settings.json")
        with open(settings_path, "w") as f:
            # dump regular settings
            json.dump(self.settings.__dict__, f)
            # dump blob settings

    def init_blob_settings(self):
        self.blob_settings = BlobSettings()

    def update_blob_settings(self, blob_settings):
        self.blob_settings = blob_settings
        self.blob_detector.set_blob_settings(self.blob_settings)

    def update_blob_settings_to_json(self, workspace_path):
        """Save current settings to directory"""
        blob_settings_path = os.path.join(workspace_path, "blob_settings.json")
        with open(blob_settings_path, "w") as f:
            json.dump(self.blob_settings.__dict__, f)

    def write_settings_to_json(self, workspace_path):
        """Save current settings to directory"""
        self.update_settings_to_json(workspace_path)
        self.update_blob_settings_to_json(workspace_path)

    def read_settings_from_json(self, workspace_path):

        reg_settings_detected = False
        blob_settings_detected = False

        """Read settings from directory"""
        settings_path = os.path.join(workspace_path, "settings.json")
        if os.path.exists(settings_path):
            reg_settings_detected = True
            with open(settings_path, "r") as f:
                settings = json.load(f)
                self.settings = Settings(**settings)

        blob_settings_path = os.path.join(workspace_path, "blob_settings.json")
        if os.path.exists(blob_settings_path):
            blob_settings_detected = True
            with open(blob_settings_path, "r") as f:
                blob_settings = json.load(f)
                self.blob_settings = BlobSettings(**blob_settings)
                self.blob_detector.set_blob_settings(self.blob_settings)

        return reg_settings_detected, blob_settings_detected

    def open_directory(self):
        """Open a directory and set up the workspace environment."""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if not directory:
            return

        self.settings.workspace_path = directory
        self._setup_workspace(directory)
        self._load_workspace_images()
        self._verify_database()
        self.write_settings_to_json(directory)

    def _setup_workspace(self, directory):
        """Set up workspace folders and load settings."""
        reg_settings_detected, blob_settings_detected = self.read_settings_from_json(
            directory
        )

        if not reg_settings_detected:
            self.settings.seg_image_folder, self.seg_mask_folder = (
                self.find_segmentation_folder(directory)
            )

        if not blob_settings_detected:
            self.settings.blob_image_folder, self.blob_keypoints_folder = (
                self.find_blob_folder(directory)
            )

    def _load_workspace_images(self):
        """Load all image paths from workspace directories."""
        self.image_paths = natsort.natsorted(
            glob.glob(os.path.join(self.settings.workspace_path, "*.jpg"))
            + glob.glob(os.path.join(self.settings.workspace_path, "*.png"))
        )

        self.seg_image_paths = natsort.natsorted(
            glob.glob(os.path.join(self.settings.seg_image_folder, "*.jpg"))
            + glob.glob(os.path.join(self.settings.seg_image_folder, "*.png"))
        )

        self.blob_image_paths = natsort.natsorted(
            glob.glob(os.path.join(self.settings.blob_image_folder, "*.jpg"))
            + glob.glob(os.path.join(self.settings.blob_image_folder, "*.png"))
        )

    def _verify_database(self):
        """Verify database existence and status."""
        self.settings.db_path = self.find_database(self.settings.workspace_path)

        if not os.path.exists(self.settings.db_path):
            QMessageBox.warning(
                self,
                "Warning",
                "Database not found. Please initialize the database first.",
            )
            self.dbStatus.setText("Database not found.")
            return

        self.dbStatus.setText("Database found.")
        self.load_labels()
        self.current_index = 0

        self._check_database_consistency()
        self.update_image_display()

    def _check_database_consistency(self):
        """Check if database image count matches directory image count."""
        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM images")
        db_image_count = c.fetchone()[0]
        conn.close()

        if db_image_count != len(self.image_paths):
            QMessageBox.warning(
                self,
                "Warning",
                f"Number of images in database ({db_image_count}) does not match directory ({len(self.image_paths)}), suggested update database.",
            )

    def create_segmentation_folder(self, workspace_path):
        """Create a folder for the segmented images."""
        if workspace_path:
            seg_folder = os.path.join(workspace_path, "segmented_images")
            os.makedirs(seg_folder, exist_ok=True)
            mask_folder = os.path.join(seg_folder, "masks")
            os.makedirs(mask_folder, exist_ok=True)
            return seg_folder, mask_folder
        return None

    def find_segmentation_folder(self, workspace_path):
        """Find the folder for the segmented images."""
        if workspace_path:
            seg_folder = os.path.join(workspace_path, "segmented_images")
            mask_folder = os.path.join(seg_folder, "masks")
            if os.path.exists(seg_folder) and os.path.exists(mask_folder):
                return seg_folder, mask_folder
        return self.create_segmentation_folder(workspace_path)

    def find_blob_folder(self, workspace_path):
        """Find the folder for the blobed images."""
        if workspace_path:
            blob_folder = os.path.join(workspace_path, "blob_images")
            keypoints_folder = os.path.join(blob_folder, "keypoints")
            if os.path.exists(blob_folder) and os.path.exists(keypoints_folder):
                return blob_folder, keypoints_folder
        return self.create_blob_folder(workspace_path)

    def create_blob_folder(self, workspace_path):
        """Create a folder for the blobed images."""
        if workspace_path:
            blob_folder = os.path.join(workspace_path, "blob_images")
            os.makedirs(blob_folder, exist_ok=True)
            keypoints_folder = os.path.join(blob_folder, "keypoints")
            os.makedirs(keypoints_folder, exist_ok=True)
            return blob_folder, keypoints_folder
        return None

    def find_database(self, workspace_path):
        return os.path.join(workspace_path, "labels.db")

    def init_database(self, workspace_path):
        if not workspace_path:
            QMessageBox.warning(
                self, "Warning", "Please select a directory containing images first."
            )
            return
        # if found database exists, warn the user that it will be overwritten
        if os.path.exists(self.find_database(workspace_path)):
            reply = QMessageBox.question(
                self,
                "Warning",
                "Database already exists. Do you want to overwrite it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return
            else:
                os.remove(self.settings.db_path)
        init_db(workspace_path)
        self.settings.db_path = self.find_database(workspace_path)
        self.dbStatus.setText(f"Database found.")
        self.load_labels()
        self.current_index = 0
        self.update_image_display()

    def update_database(self, workspace_path):
        if not workspace_path:
            QMessageBox.warning(
                self, "Warning", "Please select a directory containing images first."
            )
            return

        if not os.path.exists(self.settings.db_path):
            QMessageBox.warning(
                self,
                "Warning",
                "Database not found. Please initialize the database first.",
            )
            return
        # find the images that is new and add them to the database
        db_image_paths = []
        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("SELECT image_path FROM images")
        rows = c.fetchall()
        conn.close()
        for (image_path,) in rows:
            db_image_paths.append(image_path)

        new_images = list(set(self.image_paths) - set(db_image_paths))
        if new_images:
            conn = sqlite3.connect(self.settings.db_path)
            c = conn.cursor()
            for image_path in new_images:
                c.execute("INSERT INTO images (image_path) VALUES (?)", (image_path,))
            conn.commit()
            conn.close()

        # check if there are images in the database that are not in the directory

        images_remove = list(set(db_image_paths) - set(self.image_paths))
        if images_remove:
            conn = sqlite3.connect(self.settings.db_path)
            c = conn.cursor()
            for image_path in images_remove:
                c.execute("DELETE FROM images WHERE image_path=?", (image_path,))
            conn.commit()
            conn.close()

        self.update_image_display()

    def load_labels(self):
        """Load label definitions from the SQLite database into the labelList."""
        self.labelList.clear()

        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("SELECT id, label_name, key_binding FROM labels")
        rows = c.fetchall()
        conn.close()

        for label_id, label_name, key_binding in rows:
            item = QListWidgetItem(f"{label_name} ({key_binding})")
            item.setData(Qt.ItemDataRole.UserRole, label_id)
            self.labelList.addItem(item)

    def add_label(self):
        """Add a new label to the database and reload the list."""
        label_name = self.labelNameEdit.text().strip()
        key_binding = self.keyBindEdit.text().strip()

        if not label_name or not key_binding:
            QMessageBox.warning(
                self, "Warning", "Label name or key binding cannot be empty."
            )
            return

        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()

        # Example check for duplicate key binding
        c.execute("SELECT count(*) FROM labels WHERE key_binding=?", (key_binding,))
        if c.fetchone()[0] > 0:
            QMessageBox.warning(
                self, "Warning", f"Key '{key_binding}' is already bound."
            )
            conn.close()
            return

        # Insert label
        c.execute(
            "INSERT INTO labels (label_name, key_binding) VALUES (?, ?)",
            (label_name, key_binding),
        )
        conn.commit()
        conn.close()

        # Reload labels
        self.load_labels()

        # Clear input
        self.labelNameEdit.clear()
        self.keyBindEdit.clear()

    def remove_label(self):
        """Remove the selected label from the database and reload the list."""
        selected_item = self.labelList.currentItem()
        if not selected_item:
            return

        label_id = selected_item.data(Qt.ItemDataRole.UserRole)

        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()

        # Remove label from labels table
        c.execute("DELETE FROM labels WHERE id=?", (label_id,))

        # Remove label from image_labels junction table
        c.execute("DELETE FROM image_labels WHERE label_id=?", (label_id,))

        conn.commit()
        conn.close()

        # Reload labels
        self.load_labels()
        self.update_cur_image_labels_display()

    def switch_widget_focus(self, switch):
        if switch:
            self.curImageLabelsList.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.labelList.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

            # enable focus on line edits
            self.labelNameEdit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.keyBindEdit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        else:
            self.curImageLabelsList.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.labelList.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # disable focus on line edits
            self.labelNameEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.keyBindEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_focus_mode(self):
        """Toggle focus mode."""
        self.focus_mode_enabled = not self.focus_mode_enabled
        if self.focus_mode_enabled:
            self.focusStatus.setText("ON")
            self.switch_widget_focus(False)

        else:
            self.focusStatus.setText("OFF")
            self.switch_widget_focus(True)

    def update_image_display(self):
        if not self.image_paths:
            self.imageLabelTabRaw.clear()
            self.imageLabelTabSeg.clear()
            return
        pixmap = QPixmap(self.image_paths[self.current_index])
        pixmap = pixmap.scaled(
            self.imageLabelTabRaw.width(),
            self.imageLabelTabRaw.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
        )
        self.imageLabelTabRaw.setPixmap(pixmap)
        raw_image_name = os.path.basename(self.image_paths[self.current_index])
        self.imageIDCount.setText(
            f"{self.current_index+1}/{len(self.image_paths)}, {raw_image_name}"
        )
        self.update_cur_image_labels_display()

        if self.seg_image_paths:
            # match the segmented image with the raw image based on the name
            seg_image_name = raw_image_name.split(".")[0] + "_segmented.png"
            seg_image_path = os.path.join(
                self.settings.seg_image_folder, seg_image_name
            )
            if os.path.exists(seg_image_path):
                seg_pixmap = QPixmap(seg_image_path)
                seg_pixmap = seg_pixmap.scaled(
                    self.imageLabelTabSeg.width(),
                    self.imageLabelTabSeg.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                )
                self.imageLabelTabSeg.setPixmap(seg_pixmap)
            else:
                self.imageLabelTabSeg.clear()

        if self.blob_image_paths:
            # match the segmented image with the raw image based on the name
            blob_image_name = raw_image_name.split(".")[0] + "_blobs.png"
            blob_image_path = os.path.join(
                self.settings.blob_image_folder, blob_image_name
            )
            if os.path.exists(blob_image_path):
                blob_pixmap = QPixmap(blob_image_path)
                blob_pixmap = blob_pixmap.scaled(
                    self.imageLabelTabBlob.width(),
                    self.imageLabelTabBlob.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                )
                self.imageLabelTabBlob.setPixmap(blob_pixmap)
            else:
                self.imageLabelTabBlob.clear()

    def keyPressEvent(self, event):
        # Example: if user typed "A", label the current image with label that has key_binding='A'
        if event.text():
            if event.text().upper() == ",":
                self.prev_image()
            elif event.text().upper() == ".":
                self.next_image()
            else:

                pressed_key = event.text().upper()
                # print(f"Pressed key: {pressed_key}")
                self.label_current_image(pressed_key)

    def prev_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.update_image_display()

    def next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.update_image_display()

    def label_current_image(self, pressed_key):
        if not self.image_paths:
            return

        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()

        # Find label by pressed key
        c.execute("SELECT id FROM labels WHERE UPPER(key_binding)=?", (pressed_key,))
        result = c.fetchone()
        # if result is None:
        #     QMessageBox.warning(
        #         self, "Warning", f"No label found for key '{pressed_key}'."
        #     )
        #     conn.close()
        #     return

        # print(f"Labeling image {self.current_index+1} with label {label_id}")
        # we find the image id from the image path
        if result is None:
            return

        label_id = result[0]
        c.execute(
            "SELECT id FROM images WHERE image_path=?",
            (self.image_paths[self.current_index],),
        )
        image_id = c.fetchone()[0]

        # print(f"Current image id: {image_id}")
        # check if the label is already associated with the image
        c.execute(
            "SELECT count(*) FROM image_labels WHERE image_id=? AND label_id=?",
            (image_id, label_id),
        )

        if c.fetchone()[0] > 0:
            # remove the label from the image
            c.execute(
                "DELETE FROM image_labels WHERE image_id=? AND label_id=?",
                (image_id, label_id),
            )
        else:
            c.execute(
                "INSERT INTO image_labels (image_id, label_id) VALUES (?, ?)",
                (image_id, label_id),
            )

        conn.commit()
        conn.close()

        self.update_cur_image_labels_display()

    def update_cur_image_labels_display(self):
        """Update the list of labels for the current image."""
        if not self.image_paths:
            self.curImageLabelsList.clear()
            return

        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()

        # given the image path, find the labels associated with it in the junction table
        # Create a junction table for image-label relationships
        # """
        # CREATE TABLE IF NOT EXISTS image_labels (
        #     image_id INTEGER,
        #     label_id INTEGER,
        #     PRIMARY KEY (image_id, label_id),
        #     FOREIGN KEY (image_id) REFERENCES images(id),
        #     FOREIGN KEY (label_id) REFERENCES labels(id)
        # )
        # """

        # find the image_id from the image path
        c.execute(
            "SELECT id FROM images WHERE image_path=?",
            (self.image_paths[self.current_index],),
        )
        image_id = c.fetchone()[0]

        # print(f"Current image id: {image_id}")

        c.execute(
            """
            SELECT label_name
            FROM labels
            JOIN image_labels ON labels.id = image_labels.label_id
            WHERE image_labels.image_id = ?
            """,
            (image_id,),
        )
        image_labels = c.fetchall()
        conn.close()

        self.curImageLabelsList.clear()
        for (label_name,) in image_labels:
            self.curImageLabelsList.addItem(label_name)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # move the right groupbox to the right side of the window
        self.rightGroupBox.setGeometry(
            self.width() - self.rightGroupBox.width(),
            0,
            self.rightGroupBox.width(),
            self.rightGroupBox.height(),
        )

        # change the upper groupbox width to match the window width minus the right groupbox width
        self.upperGroupBox.setGeometry(
            0,
            0,
            self.width() - self.rightGroupBox.width(),
            self.upperGroupBox.height(),
        )
        self.imageTab.setGeometry(
            0,
            self.upperGroupBox.height(),
            self.upperGroupBox.width(),
            self.height() - self.upperGroupBox.height() - self.statusBar().height(),
        )

        self.imageLabelTabRaw.setGeometry(
            0, 0, self.imageTab.width(), self.imageTab.height()
        )
        self.imageLabelTabSeg.setGeometry(
            0, 0, self.imageTab.width(), self.imageTab.height()
        )
        self.imageLabelTabBlob.setGeometry(
            0, 0, self.imageTab.width(), self.imageTab.height()
        )

        self.update_image_display()  # re-scale image to the label size

    def face_segmentation_current_image(self):
        if not self.image_paths:
            QMessageBox.warning(
                self, "Warning", "Please select a directory containing images first."
            )
            return
        if not self.settings.seg_image_folder:
            QMessageBox.warning(
                self, "Warning", "Please select a directory for segmented images first."
            )
            return
        if not self.seg_mask_folder:
            QMessageBox.warning(
                self, "Warning", "Please select a directory for mask images first."
            )
            return
        image_path = self.image_paths[self.current_index]
        seg_image_name = os.path.basename(image_path).split(".")[0] + "_segmented.png"
        seg_image_path = os.path.join(self.settings.seg_image_folder, seg_image_name)
        seg_mask_name = os.path.basename(image_path).split(".")[0] + "_mask.npy"
        seg_mask_path = os.path.join(self.seg_mask_folder, seg_mask_name)

        # print(f"Segmenting face in {image_path}")
        # print(f"Saving segmented image to {seg_image_path}")
        # print(f"Saving mask to {seg_mask_path}")
        self.seg_tool.segment_face(image_path, seg_image_path, seg_mask_path)
        # update self.seg_image_paths
        self.seg_image_paths = natsort.natsorted(
            glob.glob(os.path.join(self.settings.seg_image_folder, "*.jpg"))
            + glob.glob(os.path.join(self.settings.seg_image_folder, "*.png"))
        )
        self.update_image_display()

    def blob_detector_current_image(self):
        if not self.image_paths:
            QMessageBox.warning(
                self, "Warning", "Please select a directory containing images first."
            )
            return
        if not self.settings.seg_image_folder:
            QMessageBox.warning(
                self, "Warning", "Please select a directory for segmented images first."
            )
            return
        if not self.seg_mask_folder:
            QMessageBox.warning(
                self, "Warning", "Please select a directory for mask images first."
            )
            return

        # check if a face_paring image exists
        base_name = os.path.basename(self.image_paths[self.current_index]).split(".")[0]
        seg_image_name = base_name + "_segmented.png"
        seg_image_path = os.path.join(self.settings.seg_image_folder, seg_image_name)
        if not os.path.exists(seg_image_path):
            # segment the face first
            self.face_segmentation_current_image()

        image_path = self.image_paths[self.current_index]
        mask_path = os.path.join(
            self.seg_mask_folder,
            os.path.basename(image_path).split(".")[0] + "_mask.npy",
        )
        output_image_name = base_name + "_blobs.png"
        output_image_path = os.path.join(
            self.settings.blob_image_folder, output_image_name
        )

        output_keypoints_name = base_name + "_keypoints.json"
        output_keypoints_path = os.path.join(
            self.blob_keypoints_folder, output_keypoints_name
        )
        keypoints = self.blob_detector.detect_blobs(image_path)
        self.blob_detector.draw_blobs(
            image_path, mask_path, keypoints, output_image_path, output_keypoints_path
        )

        # update self.blob_image_paths
        self.blob_image_paths = natsort.natsorted(
            glob.glob(os.path.join(self.settings.blob_image_folder, "*.jpg"))
            + glob.glob(os.path.join(self.settings.blob_image_folder, "*.png"))
        )
        self.update_image_display()


def main():
    app = QApplication(sys.argv)
    segmentor = FaceSegmentation()
    window = LabelingTool(segmentor)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
