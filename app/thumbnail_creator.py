from PyQt6.QtGui import QPixmap

def create_thumbnail(image_path):
    """Create a thumbnail for the image."""
    pixmap = QPixmap(image_path)
    scaled_pixmap = pixmap.scaled(
        64, 64,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )
    return scaled_pixmap