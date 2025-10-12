from PyQt6.QtWidgets import (QLabel, QMainWindow, QFileDialog, QMenuBar, QMenu, 
                             QApplication, QListWidget, QListWidgetItem, QSplitter)
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import Qt, QSize
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize variables
        self.current_folder = None
        self.image_files = []
        self.current_image_index = -1
        
        # Create image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create file list widget
        self.file_list = QListWidget()
        self.file_list.setIconSize(QSize(64, 64))
        self.file_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.file_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.file_list.setWrapping(True)
        self.file_list.setSpacing(10)
        self.file_list.itemClicked.connect(self.on_file_selected)
        # Disable keyboard navigation in the file list
        self.file_list.setMovement(QListWidget.Movement.Static)
        # Make the file list not accept focus
        self.file_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Create splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.file_list)
        self.splitter.addWidget(self.image_label)
        self.splitter.setStretchFactor(1, 1)  # Make image viewer stretch more than sidebar
        self.setCentralWidget(self.splitter)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar().show()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        # Add Open File action
        open_file_action = file_menu.addAction("Open File")
        open_file_action.triggered.connect(self.open_image)
        
        # Add Open Folder action
        open_folder_action = file_menu.addAction("Open Folder")
        open_folder_action.triggered.connect(self.open_folder)
        
    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            self.load_image(file_name)
            
    def load_image(self, file_path):
        # Load the image
        image = QPixmap(file_path)
        
        # Scale image to fit window while maintaining aspect ratio
        scaled_image = image.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        # Set the image to the label
        self.image_label.setPixmap(scaled_image)
        
        # Update status bar
        if self.current_folder:  # Only update if we're in folder view
            self.update_status_bar()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # If there's an image, rescale it when window is resized
        if self.image_label.pixmap():
            pixmap = QPixmap(self.image_label.pixmap())
            scaled_image = pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_image)
    
    def open_folder(self):
        """Open a folder and list all image files within it."""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Open Folder",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder_path:
            self.current_folder = folder_path
            self.load_folder_images()
    
    def create_thumbnail(self, image_path):
        """Create a thumbnail for the image list."""
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(
            64, 64,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        return scaled_pixmap
        
    def load_folder_images(self):
        """Load all image files from the current folder."""
        if not self.current_folder:
            return
            
        # Supported image formats
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        
        # Clear current list
        self.file_list.clear()
        
        # Get all image files in the folder
        self.image_files = [
            os.path.join(self.current_folder, f)
            for f in os.listdir(self.current_folder)
            if os.path.splitext(f)[1].lower() in image_extensions
        ]
        
        # Sort the files alphabetically
        self.image_files.sort()
        
        # Add images to the list widget with thumbnails
        for image_path in self.image_files:
            item = QListWidgetItem()
            item.setIcon(QIcon(self.create_thumbnail(image_path)))
            item.setText(os.path.basename(image_path))
            item.setData(Qt.ItemDataRole.UserRole, image_path)  # Store full path
            self.file_list.addItem(item)
        
        # Load the first image if available
        if self.image_files:
            self.current_image_index = 0
            self.load_image(self.image_files[0])
            # Select the first item
            self.file_list.setCurrentRow(0)
        else:
            self.current_image_index = -1
            self.image_label.clear()
            self.image_label.setText("No images found in the selected folder")
    
    def keyPressEvent(self, event):
        """Handle keyboard events for image navigation."""
        if event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_Down:
            self.next_image()
        elif event.key() == Qt.Key.Key_Left or event.key() == Qt.Key.Key_Up:
            self.previous_image()
        else:
            super().keyPressEvent(event)
    
    def on_file_selected(self, item):
        """Handle file selection from the list."""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.current_image_index = self.image_files.index(file_path)
        self.load_image(file_path)
        self.update_status_bar()
    
    def next_image(self):
        """Load the next image in the folder."""
        if not self.image_files or self.current_image_index == -1:
            return
            
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        print(self.current_image_index )
        self.load_image(self.image_files[self.current_image_index])
        self.file_list.setCurrentRow(self.current_image_index)
        self.update_status_bar()
    
    def previous_image(self):
        """Load the previous image in the folder."""
        if not self.image_files or self.current_image_index == -1:
            return
            
        self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
        self.load_image(self.image_files[self.current_image_index])
        self.file_list.setCurrentRow(self.current_image_index)
        self.update_status_bar()
    
    def update_status_bar(self):
        """Update the status bar with current image information."""
        if self.image_files and self.current_image_index != -1:
            current_file = os.path.basename(self.image_files[self.current_image_index])
            status_text = f"Image {self.current_image_index + 1} of {len(self.image_files)}: {current_file}"
            self.statusBar().showMessage(status_text)
        else:
            self.statusBar().clearMessage()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())