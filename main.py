import os
import sys
import json
import glob
import sqlite3
from dataclasses import dataclass

from natsort import natsorted
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QListWidgetItem,
)

from ui_labeling_tool_main import Ui_MainWindow
from init_db import init_db
from modules.face_segementation import FaceSegmentation
from modules.blob_detector import BlobDetector, BlobSettings


@dataclass
class Settings:
    """Holds main configuration."""

    db_path: str
    workspace_path: str
    seg_image_folder: str
    seg_mask_folder: str
    blob_image_folder: str
    blob_keypoints_folder: str


class LabelingTool(QMainWindow, Ui_MainWindow):
    """Main application window for labeling images."""

    def __init__(self, segmenter: FaceSegmentation):
        super().__init__()
        self.setupUi(self)
        self.seg_tool = segmenter
        self.blob_detector = BlobDetector()

        self.settings = Settings("", "", "", "", "", "")
        self.blob_settings = BlobSettings()

        self.image_paths = []
        self.seg_image_paths = []
        self.blob_image_paths = []
        self.current_index = 0
        self.focus_mode_enabled = False

        self.dbStatus.setText("Waiting for directory selection...")

        self._connect_actions()

    def _connect_actions(self):
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

        # set the default imageTab to raw image
        self.imageTab.setCurrentIndex(0)

    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if not directory:
            return
        self.settings.workspace_path = directory
        self._setup_workspace(directory)
        self._load_workspace_images()
        self._verify_database()
        self.write_settings_to_json(directory)

    def _setup_workspace(self, directory: str):
        reg_settings, blob_settings = self.read_settings_from_json(directory)
        if not reg_settings:
            seg_folders = self.find_segmentation_folder(directory)
            self.settings.seg_image_folder, self.seg_mask_folder = seg_folders
        if not blob_settings:
            blob_folders = self.find_blob_folder(directory)
            self.settings.blob_image_folder, self.blob_keypoints_folder = blob_folders

    def _load_workspace_images(self):
        self.image_paths = natsorted(
            glob.glob(os.path.join(self.settings.workspace_path, "*.jpg"))
            + glob.glob(os.path.join(self.settings.workspace_path, "*.png"))
        )
        self.seg_image_paths = natsorted(
            glob.glob(os.path.join(self.settings.seg_image_folder, "*.jpg"))
            + glob.glob(os.path.join(self.settings.seg_image_folder, "*.png"))
        )
        self.blob_image_paths = natsorted(
            glob.glob(os.path.join(self.settings.blob_image_folder, "*.jpg"))
            + glob.glob(os.path.join(self.settings.blob_image_folder, "*.png"))
        )

    def _verify_database(self):
        self.settings.db_path = self.find_database(self.settings.workspace_path)
        if not os.path.exists(self.settings.db_path):
            QMessageBox.warning(self, "Warning", "Database not found.")
            self.dbStatus.setText("Database not found.")
            return
        self.dbStatus.setText("Database found.")
        self.load_labels()
        self.current_index = 0
        self._check_database_consistency()
        self.update_image_display()

    def _check_database_consistency(self):
        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM images")
        db_image_count = c.fetchone()[0]
        conn.close()
        if db_image_count != len(self.image_paths):
            QMessageBox.warning(
                self,
                "Warning",
                f"DB images ({db_image_count}) != folder images ({len(self.image_paths)})",
            )

    def write_settings_to_json(self, workspace_path: str):
        self._save_regular_settings(workspace_path)
        self._save_blob_settings(workspace_path)

    def _save_regular_settings(self, workspace_path: str):
        settings_path = os.path.join(workspace_path, "settings.json")
        with open(settings_path, "w") as f:
            json.dump(self.settings.__dict__, f)

    def _save_blob_settings(self, workspace_path: str):
        blob_settings_path = os.path.join(workspace_path, "blob_settings.json")
        with open(blob_settings_path, "w") as f:
            json.dump(self.blob_settings.__dict__, f)

    def read_settings_from_json(self, workspace_path: str):
        reg_settings_detected = False
        blob_settings_detected = False

        settings_path = os.path.join(workspace_path, "settings.json")
        if os.path.exists(settings_path):
            reg_settings_detected = True
            with open(settings_path, "r") as f:
                data = json.load(f)
                self.settings = Settings(**data)

        blob_settings_path = os.path.join(workspace_path, "blob_settings.json")
        if os.path.exists(blob_settings_path):
            blob_settings_detected = True
            with open(blob_settings_path, "r") as f:
                data = json.load(f)
                self.blob_settings = BlobSettings(**data)
                self.blob_detector.set_blob_settings(self.blob_settings)

        return reg_settings_detected, blob_settings_detected

    def find_segmentation_folder(self, workspace_path: str):
        seg_folder = os.path.join(workspace_path, "segmented_images")
        mask_folder = os.path.join(seg_folder, "masks")
        if os.path.exists(seg_folder) and os.path.exists(mask_folder):
            return seg_folder, mask_folder
        return self._create_segmentation_folder(workspace_path)

    def _create_segmentation_folder(self, workspace_path: str):
        seg_folder = os.path.join(workspace_path, "segmented_images")
        os.makedirs(seg_folder, exist_ok=True)
        mask_folder = os.path.join(seg_folder, "masks")
        os.makedirs(mask_folder, exist_ok=True)
        return seg_folder, mask_folder

    def find_blob_folder(self, workspace_path: str):
        blob_folder = os.path.join(workspace_path, "blob_images")
        keypoints_folder = os.path.join(blob_folder, "keypoints")
        if os.path.exists(blob_folder) and os.path.exists(keypoints_folder):
            return blob_folder, keypoints_folder
        return self._create_blob_folder(workspace_path)

    def _create_blob_folder(self, workspace_path: str):
        blob_folder = os.path.join(workspace_path, "blob_images")
        os.makedirs(blob_folder, exist_ok=True)
        keypoints_folder = os.path.join(blob_folder, "keypoints")
        os.makedirs(keypoints_folder, exist_ok=True)
        return blob_folder, keypoints_folder

    def find_database(self, workspace_path: str):
        return os.path.join(workspace_path, "labels.db")

    def init_database(self, workspace_path: str):
        if not workspace_path:
            QMessageBox.warning(self, "Warning", "Select an image directory first.")
            return
        db_path = self.find_database(workspace_path)
        if os.path.exists(db_path):
            reply = QMessageBox.question(
                self,
                "Warning",
                "DB exists. Overwrite?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return
            os.remove(db_path)
        init_db(workspace_path)
        self.settings.db_path = self.find_database(workspace_path)
        self.dbStatus.setText("Database found.")
        self.load_labels()
        self.current_index = 0
        self.update_image_display()

    def update_database(self, workspace_path: str):
        if not workspace_path:
            QMessageBox.warning(self, "Warning", "Select an image directory first.")
            return
        if not os.path.exists(self.settings.db_path):
            QMessageBox.warning(self, "Warning", "DB not found. Please initialize.")
            return
        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("SELECT image_path FROM images")
        db_image_paths = [row[0] for row in c.fetchall()]
        conn.close()

        new_images = list(set(self.image_paths) - set(db_image_paths))
        if new_images:
            conn = sqlite3.connect(self.settings.db_path)
            c = conn.cursor()
            for path in new_images:
                c.execute("INSERT INTO images (image_path) VALUES (?)", (path,))
            conn.commit()
            conn.close()

        removed_images = list(set(db_image_paths) - set(self.image_paths))
        if removed_images:
            conn = sqlite3.connect(self.settings.db_path)
            c = conn.cursor()
            for path in removed_images:
                c.execute("DELETE FROM images WHERE image_path=?", (path,))
            conn.commit()
            conn.close()

        self.update_image_display()

    def load_labels(self):
        self.labelList.clear()
        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("SELECT id, label_name, key_binding FROM labels")
        for label_id, label_name, key_binding in c.fetchall():
            item = QListWidgetItem(f"{label_name} ({key_binding})")
            item.setData(Qt.ItemDataRole.UserRole, label_id)
            self.labelList.addItem(item)
        conn.close()

    def add_label(self):
        label_name = self.labelNameEdit.text().strip()
        key_binding = self.keyBindEdit.text().strip()
        if not label_name or not key_binding:
            QMessageBox.warning(self, "Warning", "Label or key cannot be empty.")
            return
        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM labels WHERE key_binding=?", (key_binding,))
        if c.fetchone()[0] > 0:
            QMessageBox.warning(self, "Warning", f"Key '{key_binding}' taken.")
            conn.close()
            return
        c.execute(
            "INSERT INTO labels (label_name, key_binding) VALUES (?, ?)",
            (label_name, key_binding),
        )
        conn.commit()
        conn.close()
        self.labelNameEdit.clear()
        self.keyBindEdit.clear()
        self.load_labels()

    def remove_label(self):
        item = self.labelList.currentItem()
        if not item:
            return
        label_id = item.data(Qt.ItemDataRole.UserRole)
        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM labels WHERE id=?", (label_id,))
        c.execute("DELETE FROM image_labels WHERE label_id=?", (label_id,))
        conn.commit()
        conn.close()
        self.load_labels()
        self.update_cur_image_labels_display()

    def set_focus_mode(self):
        self.focus_mode_enabled = not self.focus_mode_enabled
        self.focusStatus.setText("ON" if self.focus_mode_enabled else "OFF")
        if self.focus_mode_enabled:
            self._switch_widget_focus(False)
        else:
            self._switch_widget_focus(True)

    def _switch_widget_focus(self, enable: bool):
        focus = Qt.FocusPolicy.StrongFocus if enable else Qt.FocusPolicy.NoFocus
        self.curImageLabelsList.setFocusPolicy(focus)
        self.labelList.setFocusPolicy(focus)
        self.labelNameEdit.setFocusPolicy(focus)
        self.keyBindEdit.setFocusPolicy(focus)

    def update_image_display(self):
        if not self.image_paths:
            self.imageLabelTabRaw.clear()
            self.imageLabelTabSeg.clear()
            return
        raw_path = self.image_paths[self.current_index]
        self._set_pixmap(raw_path, self.imageLabelTabRaw)
        name = os.path.basename(raw_path)
        self.imageIDCount.setText(
            f"{self.current_index + 1}/{len(self.image_paths)}, {name}"
        )
        self._set_segmentation_pixmap(name)
        self._set_blob_pixmap(name)
        self.update_cur_image_labels_display()

    def _set_pixmap(self, path: str, label_widget):
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(
            label_widget.width(), label_widget.height(), Qt.KeepAspectRatio
        )
        label_widget.setPixmap(pixmap)

    def _set_segmentation_pixmap(self, file_name: str):
        seg_name = os.path.splitext(file_name)[0] + "_segmented.png"
        seg_path = os.path.join(self.settings.seg_image_folder, seg_name)
        if os.path.exists(seg_path):
            self._set_pixmap(seg_path, self.imageLabelTabSeg)
        else:
            self.imageLabelTabSeg.clear()

    def _set_blob_pixmap(self, file_name: str):
        blob_name = os.path.splitext(file_name)[0] + "_blobs.png"
        blob_path = os.path.join(self.settings.blob_image_folder, blob_name)
        if os.path.exists(blob_path):
            self._set_pixmap(blob_path, self.imageLabelTabBlob)
        else:
            self.imageLabelTabBlob.clear()

    def update_cur_image_labels_display(self):
        self.curImageLabelsList.clear()
        if not self.image_paths:
            return
        path = self.image_paths[self.current_index]
        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("SELECT id FROM images WHERE image_path=?", (path,))
        image_id = c.fetchone()
        if not image_id:
            conn.close()
            return
        c.execute(
            """SELECT label_name
               FROM labels JOIN image_labels
               ON labels.id = image_labels.label_id
               WHERE image_id=?""",
            (image_id[0],),
        )
        for (label,) in c.fetchall():
            self.curImageLabelsList.addItem(label)
        conn.close()

    def keyPressEvent(self, event):
        if not event.text():
            return
        key = event.text().upper()
        if key == ",":
            self.prev_image()
        elif key == ".":
            self.next_image()
        else:
            self.label_current_image(key)

    def label_current_image(self, pressed_key: str):
        if not self.image_paths:
            return
        conn = sqlite3.connect(self.settings.db_path)
        c = conn.cursor()
        c.execute("SELECT id FROM labels WHERE UPPER(key_binding)=?", (pressed_key,))
        label_row = c.fetchone()
        if not label_row:
            conn.close()
            return
        label_id = label_row[0]
        img_path = self.image_paths[self.current_index]
        c.execute("SELECT id FROM images WHERE image_path=?", (img_path,))
        image_id = c.fetchone()[0]
        c.execute(
            "SELECT count(*) FROM image_labels WHERE image_id=? AND label_id=?",
            (image_id, label_id),
        )
        if c.fetchone()[0] > 0:
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

    def prev_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.update_image_display()

    def next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.update_image_display()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.rightGroupBox.setGeometry(
            self.width() - self.rightGroupBox.width(),
            0,
            self.rightGroupBox.width(),
            self.rightGroupBox.height(),
        )
        self.upperGroupBox.setGeometry(
            0, 0, self.width() - self.rightGroupBox.width(), self.upperGroupBox.height()
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
        self.update_image_display()

    def face_segmentation_current_image(self):
        if not self._validate_folders():
            return
        img_path = self.image_paths[self.current_index]
        base = os.path.splitext(os.path.basename(img_path))[0]
        seg_image_path = os.path.join(
            self.settings.seg_image_folder, f"{base}_segmented.png"
        )
        seg_mask_path = os.path.join(self.seg_mask_folder, f"{base}_mask.npy")
        self.seg_tool.segment_face(img_path, seg_image_path, seg_mask_path)
        self.seg_image_paths = natsorted(
            glob.glob(os.path.join(self.settings.seg_image_folder, "*.jpg"))
            + glob.glob(os.path.join(self.settings.seg_image_folder, "*.png"))
        )
        self.update_image_display()

    def _validate_folders(self):
        if not self.image_paths:
            QMessageBox.warning(self, "Warning", "Select a directory first.")
            return False
        if not self.settings.seg_image_folder:
            QMessageBox.warning(self, "Warning", "No segmentation folder selected.")
            return False
        if not self.seg_mask_folder:
            QMessageBox.warning(self, "Warning", "No mask folder selected.")
            return False
        return True

    def blob_detector_current_image(self):
        if not self._validate_folders():
            return
        base = os.path.splitext(os.path.basename(self.image_paths[self.current_index]))[
            0
        ]
        seg_image_name = f"{base}_segmented.png"
        seg_image_path = os.path.join(self.settings.seg_image_folder, seg_image_name)
        if not os.path.exists(seg_image_path):
            self.face_segmentation_current_image()

        image_path = self.image_paths[self.current_index]
        mask_path = os.path.join(self.seg_mask_folder, f"{base}_mask.npy")
        out_img_path = os.path.join(
            self.settings.blob_image_folder, f"{base}_blobs.png"
        )
        out_kp_path = os.path.join(self.blob_keypoints_folder, f"{base}_keypoints.json")

        keypoints = self.blob_detector.detect_blobs(image_path)
        self.blob_detector.draw_blobs(
            image_path, mask_path, keypoints, out_img_path, out_kp_path
        )
        self.blob_image_paths = natsorted(
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
