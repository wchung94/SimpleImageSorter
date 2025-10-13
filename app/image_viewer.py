from PyQt6.QtWidgets import (QLabel, QMainWindow, QFileDialog, QListWidget, 
                             QListWidgetItem, QSplitter, QPushButton)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
import os
from image_loader import load_image, load_folder_images
from thumbnail_creator import create_thumbnail
from file_operations import copy_current_image_to_new_folder

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize variables
        self.current_folder = None
        self.image_files = []
        self.current_image_index = -1
        self.new_folder_path = ""
        
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
        self.file_list.setMovement(QListWidget.Movement.Static)
        self.file_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Create splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.file_list)
        self.splitter.addWidget(self.image_label)
        self.splitter.setStretchFactor(1, 1)
        self.setCentralWidget(self.splitter)
        
        # Create button to select a new folder
        self.select_folder_button = QPushButton("Select Folder", self)
        self.select_folder_button.setGeometry(10, 500, 120, 30)
        self.select_folder_button.clicked.connect(self.select_new_folder)

        # Create status bar
        self.statusBar().show()

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            load_image(file_name, self.image_label)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Open Folder",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder_path:
            self.current_folder = folder_path
            self.load_folder_images()

    def load_folder_images(self):
        """Load all image files from the current folder."""
        if not self.current_folder:
            return
            
        self.image_files = load_folder_images(self.current_folder, self.file_list)
        
        if self.image_files:
            self.current_image_index = 0
            self.load_image(self.image_files[0])
            self.file_list.setCurrentRow(0)
        else:
            self.current_image_index = -1
            self.image_label.clear()
            self.image_label.setText("No images found in the selected folder")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_Down:
            self.next_image()
        elif event.key() == Qt.Key.Key_Left or event.key() == Qt.Key.Key_Up:
            self.previous_image()
        elif event.key() in [Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3, Qt.Key.Key_4, 
                             Qt.Key.Key_5, Qt.Key.Key_6, Qt.Key.Key_7, Qt.Key.Key_8, 
                             Qt.Key.Key_9, Qt.Key.Key_0]:
            copy_current_image_to_new_folder(self.new_folder_path, self.image_files, self.current_image_index)

    def on_file_selected(self, item):
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.current_image_index = self.image_files.index(file_path)
        load_image(file_path, self.image_label)

    def next_image(self):
        if not self.image_files or self.current_image_index == -1:
            return
            
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        load_image(self.image_files[self.current_image_index], self.image_label)
        self.file_list.setCurrentRow(self.current_image_index)

    def previous_image(self):
        if not self.image_files or self.current_image_index == -1:
            return
            
        self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
        load_image(self.image_files[self.current_image_index], self.image_label)
        self.file_list.setCurrentRow(self.current_image_index)

    def select_new_folder(self):
        self.new_folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.new_folder_path:
            print(f"New folder selected: {self.new_folder_path}")