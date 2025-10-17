from PyQt6.QtWidgets import (QLabel, QMainWindow, QFileDialog, QListWidget, 
                             QListWidgetItem, QSplitter, QPushButton, QTabWidget)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
from .folder_buttonwidget import FolderTab
import os
from .image_loader import load_image, load_folder_images
from .thumbnail_creator import create_thumbnail
from .file_operations import copy_current_image_to_new_folder

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize variables
        self.current_folder = None
        self.image_files = []
        self.current_image_index = -1
        self.new_folder_path = ["folder_1", "folder_2"]

        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar().show()
        
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
        

        # Create main splitter
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        

    

        # Create horizontal splitter for file list and image
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.addWidget(self.file_list)
        content_splitter.addWidget(self.image_label)
        content_splitter.setStretchFactor(1, 1)

        # Create folder tabs
        self.tabs = FolderTab()
        # self.tabs = QTabWidget()

        # self.tabs.setTabPosition(QTabWidget.TabPosition.South)
        # self.tabs.setMovable(True)
        # for folder_name in self.new_folder_path:
        #     self.tabs.addTab(FolderButton(folder_name), folder_name)

        # Add widgets to main splitter
        main_splitter.addWidget(content_splitter)
        main_splitter.addWidget(self.tabs)
        main_splitter.setStretchFactor(0, 4)  # Make the content area larger than the tabs
        
        self.setCentralWidget(main_splitter)


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
            load_image(self.image_files[0], self.image_label)
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
        elif event.key() == Qt.Key.Key_1:
            tab = self.tabs.widget(0)  # Get first tab
            if tab and tab.get_folder_path():
                copy_current_image_to_new_folder(
                    tab.get_folder_path(), 
                    self.image_files, 
                    self.current_image_index
                )
        elif event.key() == Qt.Key.Key_2:
            tab = self.tabs.widget(1)  # Get second tab
            if tab and tab.get_folder_path():
                copy_current_image_to_new_folder(
                    tab.get_folder_path(), 
                    self.image_files, 
                    self.current_image_index
                )
        elif event.key() == Qt.Key.Key_3:
            tab = self.tabs.widget(2)  # Get second tab
            if tab and tab.get_folder_path():
                copy_current_image_to_new_folder(
                    tab.get_folder_path(), 
                    self.image_files, 
                    self.current_image_index
                )

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
