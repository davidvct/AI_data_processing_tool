"""
Sampling Tab - Main tab for various sampling modes
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QGroupBox, QComboBox, QLabel, QTextEdit,
                              QProgressBar, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from src.modules.sampling.video_frame_yolo import VideoFrameYoloWidget


class SamplingTab(QWidget):
    """Main sampling tab with mode selector"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Sampling Mode Selection at the top
        mode_group = QGroupBox("Sampling Mode")
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Select Mode:"))
        self.mode_selector = QComboBox()
        self.mode_selector.addItem("Video Frame - Yolo")
        self.mode_selector.addItem("String folder")
        self.mode_selector.addItem("Tile")
        self.mode_selector.addItem("Standard")

        # Style placeholder items in gray
        for i in range(1, 4):  # Items 1, 2, 3 are placeholders
            self.mode_selector.setItemData(i, QColor(150, 150, 150), Qt.ForegroundRole)

        self.mode_selector.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_selector)
        mode_layout.addStretch()
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Progress and log (shared across all modes)
        self.progress_bar = QProgressBar()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)

        # Container for mode-specific UIs
        self.mode_container = QWidget()
        self.mode_layout = QVBoxLayout()
        self.mode_container.setLayout(self.mode_layout)
        layout.addWidget(self.mode_container)

        # Create all mode UIs
        self.create_video_frame_yolo_ui()
        self.create_placeholder_ui("String folder")
        self.create_placeholder_ui("Tile")
        self.create_placeholder_ui("Standard")

        # Show default mode
        self.on_mode_changed(0)

        # Progress and buttons (common for all modes)
        layout.addWidget(self.progress_bar)

        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Sampling")
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.start_btn.clicked.connect(self.start_sampling)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        layout.addLayout(button_layout)

        # Log area (common for all modes)
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        layout.addStretch()
        self.setLayout(layout)

    def create_video_frame_yolo_ui(self):
        """Create UI for Video Frame - Yolo mode"""
        self.video_frame_widget = VideoFrameYoloWidget(self.log_text, self.progress_bar)

    def create_placeholder_ui(self, mode_name):
        """Create placeholder UI for modes not yet implemented"""
        placeholder_widget = QWidget()
        placeholder_layout = QVBoxLayout()

        # Add spacer to center the message
        placeholder_layout.addStretch()

        # Placeholder message
        placeholder_label = QLabel(f"{mode_name} mode")
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_font = QFont()
        placeholder_font.setPointSize(14)
        placeholder_font.setBold(True)
        placeholder_label.setFont(placeholder_font)
        placeholder_label.setStyleSheet("color: #999999;")
        placeholder_layout.addWidget(placeholder_label)

        coming_soon_label = QLabel("Coming Soon")
        coming_soon_label.setAlignment(Qt.AlignCenter)
        coming_soon_font = QFont()
        coming_soon_font.setPointSize(12)
        coming_soon_label.setFont(coming_soon_font)
        coming_soon_label.setStyleSheet("color: #bbbbbb;")
        placeholder_layout.addWidget(coming_soon_label)

        placeholder_layout.addStretch()

        placeholder_widget.setLayout(placeholder_layout)

        # Store widget reference with mode name
        if mode_name == "String folder":
            self.string_folder_widget = placeholder_widget
        elif mode_name == "Tile":
            self.tile_widget = placeholder_widget
        elif mode_name == "Standard":
            self.standard_widget = placeholder_widget

    def on_mode_changed(self, index):
        """Handle mode selection change"""
        # Clear current layout
        while self.mode_layout.count():
            child = self.mode_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

        # Show selected mode UI
        if index == 0:  # Video Frame - Yolo
            self.mode_layout.addWidget(self.video_frame_widget)
        elif index == 1:  # String folder
            self.mode_layout.addWidget(self.string_folder_widget)
        elif index == 2:  # Tile
            self.mode_layout.addWidget(self.tile_widget)
        elif index == 3:  # Standard
            self.mode_layout.addWidget(self.standard_widget)

    def start_sampling(self):
        """Start the sampling process based on current mode"""
        # Change button state immediately
        self.start_btn.setEnabled(False)
        self.start_btn.setText("Sampling in progress...")
        self.start_btn.setStyleSheet("QPushButton { background-color: #FFC107; color: white; }")
        self.stop_btn.setEnabled(True)

        # Process events to update UI immediately
        QApplication.processEvents()

        current_mode = self.mode_selector.currentIndex()

        if current_mode == 0:  # Video Frame - Yolo
            self.video_frame_widget.start_sampling()
        else:
            self.log_text.append(f"Error: {self.mode_selector.currentText()} mode is not yet implemented")

        # Reset button state after completion
        self.reset_sampling_button()

    def reset_sampling_button(self):
        """Reset the sampling button to its original state"""
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Start Sampling")
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.stop_btn.setEnabled(False)
