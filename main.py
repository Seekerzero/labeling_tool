import sys
import os
import sqlite3
import glob
from natsort import natsort

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
from ui_labeling_tool import Ui_MainWindow
from init_db import init_db
from modules.face_segementation import FaceSegmentation


class LabelingTool(QMainWindow, Ui_MainWindow):
    def __init__(self, segmenter):
        super().__init__()
        self.setupUi(self)  # This initializes all widgets from the UI

        # Store database path
        self.dbStatus.setText("Waiting for directory selection...")
        self.db_path = ""
        self.workspace_path = ""

        # A list to keep track of images in the selected directory
        self.image_paths = []
        self.seg_image_folder = ""
        self.seg_mask_folder = ""
        self.seg_image_paths = []
        self.current_index = 0
        self.focus_mode_enabled = False
        # Connect buttons (matching the object names from Qt Designer)
        self.actionOpen_Workspace.triggered.connect(self.open_directory)
        self.actionCreate_New_Database.triggered.connect(
            lambda: self.init_database(self.workspace_path)
        )
        self.actionParse_Current_Image.triggered.connect(
            self.face_segmentation_current_image
        )

        self.addLabelButton.clicked.connect(self.add_label)
        self.removeLabelButton.clicked.connect(self.remove_label)
        self.prevImageButton.clicked.connect(self.prev_image)
        self.nextImageButton.clicked.connect(self.next_image)
        self.focusModeButton.clicked.connect(self.set_focus_mode)

        self.seg_tool = segmenter

        # (Optional) Connect other signals/slots or do other setup...

    def open_directory(self):
        """Open a file dialog to select a directory containing images."""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.image_paths = natsort.natsorted(
                glob.glob(os.path.join(directory, "*.jpg"))
                + glob.glob(os.path.join(directory, "*.png"))
            )
            self.workspace_path = directory

            self.seg_image_folder, self.seg_mask_folder = self.find_segmentation_folder(
                self.workspace_path
            )

            if not os.path.exists(self.seg_image_folder):
                self.seg_image_folder, self.seg_mask_folder = (
                    self.create_segmentation_folder(self.workspace_path)
                )

            self.seg_image_paths = natsort.natsorted(
                glob.glob(os.path.join(self.seg_image_folder, "*.jpg"))
                + glob.glob(os.path.join(self.seg_image_folder, "*.png"))
            )

            self.db_path = self.find_database(self.workspace_path)
            if not os.path.exists(self.db_path):
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Database not found. Please initialize the database first.",
                )
                self.dbStatus.setText(f"Database not found.")
            else:
                self.dbStatus.setText(f"Database found.")
                self.load_labels()
                self.current_index = 0
                self.update_image_display()

    def create_segmentation_folder(self, workspace_path):
        """Create a folder for the segmented images."""
        if self.workspace_path:
            seg_folder = os.path.join(workspace_path, "segmented_images")
            os.makedirs(seg_folder, exist_ok=True)
            mask_folder = os.path.join(seg_folder, "masks")
            os.makedirs(mask_folder, exist_ok=True)
            return seg_folder, mask_folder
        return None

    def find_segmentation_folder(self, workspace_path):
        """Find the folder for the segmented images."""
        if self.workspace_path:
            seg_folder = os.path.join(workspace_path, "segmented_images")
            mask_folder = os.path.join(seg_folder, "masks")
            if os.path.exists(seg_folder) and os.path.exists(mask_folder):
                return seg_folder, mask_folder
        return self.create_segmentation_folder(workspace_path)

    def find_database(self, workspace_path):
        return os.path.join(workspace_path, "labels.db")

    def init_database(self, workspace_path):

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
                os.remove(self.db_path)
        init_db(workspace_path)
        self.db_path = self.find_database(workspace_path)
        self.dbStatus.setText(f"Database found.")
        self.load_labels()
        self.current_index = 0
        self.update_image_display()

    def load_labels(self):
        """Load label definitions from the SQLite database into the labelList."""
        self.labelList.clear()

        conn = sqlite3.connect(self.db_path)
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

        conn = sqlite3.connect(self.db_path)
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

        conn = sqlite3.connect(self.db_path)
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

        # check if the image is larger than the label
        overSize = (
            pixmap.width() > self.imageLabelTabRaw.width()
            or pixmap.height() > self.imageLabelTabRaw.height()
        )
        height_width_ratio = pixmap.height() / pixmap.width()
        new_height = pixmap.height()
        new_width = pixmap.width()
        if overSize:
            if height_width_ratio > 1:
                ratio = self.imageLabelTabRaw.height() / pixmap.height()
                new_height = pixmap.height() * ratio
                new_width = pixmap.width() * ratio
                if new_width > self.imageLabelTabRaw.width():
                    ratio = self.imageLabelTabRaw.width() / new_width
                    new_height = new_height * ratio
                    new_width = new_width * ratio

                pixmap = pixmap.scaled(
                    new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio
                )

            else:
                ratio = self.imageLabelTabRaw.width() / pixmap.width()
                new_height = pixmap.height() * ratio
                new_width = pixmap.width() * ratio
                if new_height > self.imageLabelTabRaw.height():
                    ratio = self.imageLabelTabRaw.height() / new_height
                    new_height = new_height * ratio
                    new_width = new_width * ratio
                pixmap = pixmap.scaled(
                    new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio
                )
        else:
            pixmap = pixmap.scaled(
                self.imageLabelTabRaw.width(),
                self.imageLabelTabRaw.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
            )

        print(f"New width: {pixmap.width()}, New height: {pixmap.height()}")
        # self.imageLabel.setPicture(image)

        scaled = pixmap.scaled(
            self.imageLabelTabRaw.size(), Qt.AspectRatioMode.KeepAspectRatio
        )
        self.imageLabelTabRaw.setPixmap(scaled)
        self.imageIDCount.setText(
            f"{self.current_index+1}/{len(self.image_paths)}  {os.path.basename(self.image_paths[self.current_index])}"
        )
        self.update_cur_image_labels_display()

        if self.seg_image_paths:
            # match the segmented image with the raw image based on the name
            raw_image_name = os.path.basename(self.image_paths[self.current_index])
            seg_image_name = raw_image_name.split(".")[0] + "_segmented.png"
            seg_image_path = os.path.join(self.seg_image_folder, seg_image_name)
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

        conn = sqlite3.connect(self.db_path)
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

        conn = sqlite3.connect(self.db_path)
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
        self.rightUpperGroupBox.setGeometry(
            self.width() - self.rightUpperGroupBox.width(),
            0,
            self.rightUpperGroupBox.width(),
            self.rightUpperGroupBox.height(),
        )
        self.rightBelowGroupBox.setGeometry(
            self.width() - self.rightBelowGroupBox.width(),
            self.rightUpperGroupBox.height(),
            self.rightBelowGroupBox.width(),
            self.rightBelowGroupBox.height(),
        )
        # change the upper groupbox width to match the window width minus the right groupbox width
        self.upperGroupBox.setGeometry(
            0,
            0,
            self.width() - self.rightUpperGroupBox.width(),
            self.upperGroupBox.height(),
        )
        self.imageTab.setGeometry(
            0,
            self.upperGroupBox.height(),
            self.upperGroupBox.width(),
            self.height() - self.upperGroupBox.height(),
        )

        self.imageLabelTabRaw.setGeometry(
            0, 0, self.imageTab.width(), self.imageTab.height()
        )
        self.imageLabelTabSeg.setGeometry(
            0, 0, self.imageTab.width(), self.imageTab.height()
        )
        self.update_image_display()  # re-scale image to the label size

    def face_segmentation_current_image(self):
        if not self.image_paths:
            QMessageBox.warning(
                self, "Warning", "Please select a directory containing images first."
            )
            return
        if not self.seg_image_folder:
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
        seg_image_path = os.path.join(self.seg_image_folder, seg_image_name)
        seg_mask_name = os.path.basename(image_path).split(".")[0] + "_mask.npy"
        seg_mask_path = os.path.join(self.seg_mask_folder, seg_mask_name)

        # print(f"Segmenting face in {image_path}")
        # print(f"Saving segmented image to {seg_image_path}")
        # print(f"Saving mask to {seg_mask_path}")
        self.seg_tool.segment_face(image_path, seg_image_path, seg_mask_path)
        # update self.seg_image_paths
        self.seg_image_paths = natsort.natsorted(
            glob.glob(os.path.join(self.seg_image_folder, "*.jpg"))
            + glob.glob(os.path.join(self.seg_image_folder, "*.png"))
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
