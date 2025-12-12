"""
Dataset Split Tab - UI for splitting datasets into train/val/test sets
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                              QLineEdit, QTextEdit, QGroupBox, QSpinBox, QComboBox,
                              QCheckBox, QProgressBar, QGridLayout)


class DatasetSplitTab(QWidget):
    """Tab for dataset splitting functionality"""

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

        # Split Options
        split_group = QGroupBox("Split Options")
        split_layout = QVBoxLayout()

        # Split ratios
        ratio_layout = QGridLayout()
        ratio_layout.addWidget(QLabel("Train %:"), 0, 0)
        self.train_ratio = QSpinBox()
        self.train_ratio.setRange(0, 100)
        self.train_ratio.setValue(70)
        ratio_layout.addWidget(self.train_ratio, 0, 1)

        ratio_layout.addWidget(QLabel("Validation %:"), 1, 0)
        self.val_ratio = QSpinBox()
        self.val_ratio.setRange(0, 100)
        self.val_ratio.setValue(20)
        ratio_layout.addWidget(self.val_ratio, 1, 1)

        ratio_layout.addWidget(QLabel("Test %:"), 2, 0)
        self.test_ratio = QSpinBox()
        self.test_ratio.setRange(0, 100)
        self.test_ratio.setValue(10)
        ratio_layout.addWidget(self.test_ratio, 2, 1)

        # Total percentage label
        self.total_label = QLabel("Total: 100%")
        ratio_layout.addWidget(self.total_label, 3, 0, 1, 2)

        split_layout.addLayout(ratio_layout)

        # Split method
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Split Method:"))
        self.split_method = QComboBox()
        self.split_method.addItems(["Random", "Stratified", "Sequential", "Group-based"])
        method_layout.addWidget(self.split_method)
        method_layout.addStretch()
        split_layout.addLayout(method_layout)

        # Shuffle option
        self.shuffle_check = QCheckBox("Shuffle before splitting")
        self.shuffle_check.setChecked(True)
        split_layout.addWidget(self.shuffle_check)

        # Random seed
        seed_layout = QHBoxLayout()
        seed_layout.addWidget(QLabel("Random Seed:"))
        self.random_seed = QSpinBox()
        self.random_seed.setRange(0, 999999)
        self.random_seed.setValue(42)
        seed_layout.addWidget(self.random_seed)
        seed_layout.addStretch()
        split_layout.addLayout(seed_layout)

        split_group.setLayout(split_layout)
        layout.addWidget(split_group)

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

        # Create separate folders option
        self.separate_folders_check = QCheckBox("Create separate folders for train/val/test")
        self.separate_folders_check.setChecked(True)
        output_layout.addWidget(self.separate_folders_check)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Progress and buttons
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Splitting")
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
