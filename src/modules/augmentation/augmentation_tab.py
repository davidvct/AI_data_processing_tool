"""
Augmentation Tab - UI for image augmentation operations
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                              QLineEdit, QTextEdit, QGroupBox, QSpinBox, QCheckBox,
                              QProgressBar)


class AugmentationTab(QWidget):
    """Tab for image augmentation functionality"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()

        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Dataset Path:"))
        self.dataset_path = QLineEdit()
        path_layout.addWidget(self.dataset_path)
        self.browse_btn = QPushButton("Browse")
        path_layout.addWidget(self.browse_btn)
        input_layout.addLayout(path_layout)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Augmentation Options
        aug_group = QGroupBox("Augmentation Options")
        aug_layout = QVBoxLayout()

        # Create two columns for augmentation options
        options_layout = QHBoxLayout()

        # Left column
        left_column = QVBoxLayout()
        self.rotate_check = QCheckBox("Rotation")
        self.flip_horizontal_check = QCheckBox("Horizontal Flip")
        self.flip_vertical_check = QCheckBox("Vertical Flip")
        self.brightness_check = QCheckBox("Brightness Adjustment")
        self.contrast_check = QCheckBox("Contrast Adjustment")

        left_column.addWidget(self.rotate_check)
        left_column.addWidget(self.flip_horizontal_check)
        left_column.addWidget(self.flip_vertical_check)
        left_column.addWidget(self.brightness_check)
        left_column.addWidget(self.contrast_check)

        # Right column
        right_column = QVBoxLayout()
        self.noise_check = QCheckBox("Add Noise")
        self.blur_check = QCheckBox("Blur")
        self.crop_check = QCheckBox("Random Crop")
        self.scale_check = QCheckBox("Scale/Zoom")
        self.color_jitter_check = QCheckBox("Color Jitter")

        right_column.addWidget(self.noise_check)
        right_column.addWidget(self.blur_check)
        right_column.addWidget(self.crop_check)
        right_column.addWidget(self.scale_check)
        right_column.addWidget(self.color_jitter_check)

        options_layout.addLayout(left_column)
        options_layout.addLayout(right_column)
        aug_layout.addLayout(options_layout)

        # Augmentation multiplier
        multiplier_layout = QHBoxLayout()
        multiplier_layout.addWidget(QLabel("Augmentation Multiplier:"))
        self.aug_multiplier = QSpinBox()
        self.aug_multiplier.setRange(1, 10)
        self.aug_multiplier.setValue(2)
        multiplier_layout.addWidget(self.aug_multiplier)
        multiplier_layout.addStretch()
        aug_layout.addLayout(multiplier_layout)

        aug_group.setLayout(aug_layout)
        layout.addWidget(aug_group)

        # Output section
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()

        output_path_layout = QHBoxLayout()
        output_path_layout.addWidget(QLabel("Output Path:"))
        self.output_path = QLineEdit()
        output_path_layout.addWidget(self.output_path)
        self.output_browse_btn = QPushButton("Browse")
        output_path_layout.addWidget(self.output_browse_btn)
        output_layout.addLayout(output_path_layout)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Progress and buttons
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Augmentation")
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        layout.addLayout(button_layout)

        # Log area
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        layout.addStretch()
        self.setLayout(layout)
