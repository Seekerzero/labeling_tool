import sqlite3
import glob
import os
from natsort import natsorted


def init_db(workspace_path):
    db_path = os.path.join(workspace_path, "labels.db")
    conn = sqlite3.connect(database=db_path)
    c = conn.cursor()

    c.execute(
        """
    CREATE TABLE IF NOT EXISTS labels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label_name TEXT NOT NULL,
        key_binding TEXT NOT NULL
    )
    """
    )

    # given the path to a directory, this will return a list of all image files in that directory
    # sorted in natural order
    def get_image_paths(directory):
        return natsorted(
            glob.glob(os.path.join(directory, "*.jpg"))
            + glob.glob(os.path.join(directory, "*.png"))
        )

    images = get_image_paths(workspace_path)

    # c.execute(
    #     """
    # CREATE TABLE IF NOT EXISTS image_labels (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     image_path TEXT NOT NULL,
    #     label_id INTEGER NOT NULL,
    #     FOREIGN KEY(label_id) REFERENCES labels(id)
    # )
    # """
    # )
    # Create a table for images
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT NOT NULL UNIQUE
    )
    """
    )

    # Create a junction table for image-label relationships
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS image_labels (
        image_id INTEGER,
        label_id INTEGER,
        PRIMARY KEY (image_id, label_id),
        FOREIGN KEY (image_id) REFERENCES images(id),
        FOREIGN KEY (label_id) REFERENCES labels(id)
    )
    """
    )

    # Insert all images into the database
    for image in images:
        c.execute("INSERT INTO images (image_path) VALUES (?)", (image,))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
