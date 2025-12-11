"""
AI Data Processing Tool
A PySide6 application for processing images and labels with sampling,
augmentation, dataset splitting, and prefix/postfix functionality.

GitHub: https://github.com/davidvct/AI_data_processing_tool
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                              QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                              QLineEdit, QTextEdit, QGroupBox, QSpinBox,
                              QDoubleSpinBox, QComboBox, QCheckBox, QListWidget,
                              QTableWidget, QSplitter, QFileDialog, QSlider,
                              QProgressBar, QRadioButton, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SamplingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()

        # Dataset path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Dataset Path:"))
        self.dataset_path = QLineEdit()
        path_layout.addWidget(self.dataset_path)
        self.browse_btn = QPushButton("Browse")
        path_layout.addWidget(self.browse_btn)
        input_layout.addLayout(path_layout)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Sampling Options
        sampling_group = QGroupBox("Sampling Options")
        sampling_layout = QGridLayout()

        # Sample size
        sampling_layout.addWidget(QLabel("Sample Size:"), 0, 0)
        self.sample_size = QSpinBox()
        self.sample_size.setRange(1, 100000)
        self.sample_size.setValue(100)
        sampling_layout.addWidget(self.sample_size, 0, 1)

        # Sampling method
        sampling_layout.addWidget(QLabel("Sampling Method:"), 1, 0)
        self.sampling_method = QComboBox()
        self.sampling_method.addItems(["Random", "Stratified", "Systematic", "Cluster"])
        sampling_layout.addWidget(self.sampling_method, 1, 1)

        # Random seed
        sampling_layout.addWidget(QLabel("Random Seed:"), 2, 0)
        self.random_seed = QSpinBox()
        self.random_seed.setRange(0, 999999)
        self.random_seed.setValue(42)
        sampling_layout.addWidget(self.random_seed, 2, 1)

        sampling_group.setLayout(sampling_layout)
        layout.addWidget(sampling_group)

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
        self.start_btn = QPushButton("Start Sampling")
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


class AugmentationTab(QWidget):
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


class DatasetSplitTab(QWidget):
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


class PrefixPostfixTab(QWidget):
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

        # File type filter
        file_type_layout = QHBoxLayout()
        file_type_layout.addWidget(QLabel("File Type:"))
        self.file_type = QComboBox()
        self.file_type.addItems(["All", "Images (*.jpg, *.png, *.bmp)", "Labels (*.txt)", "Custom"])
        file_type_layout.addWidget(self.file_type)
        file_type_layout.addStretch()
        input_layout.addLayout(file_type_layout)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Naming Options
        naming_group = QGroupBox("Naming Options")
        naming_layout = QVBoxLayout()

        # Operation type
        operation_layout = QHBoxLayout()
        self.add_prefix_radio = QRadioButton("Add Prefix")
        self.add_postfix_radio = QRadioButton("Add Postfix")
        self.add_both_radio = QRadioButton("Add Both")
        self.replace_radio = QRadioButton("Replace Pattern")
        self.add_prefix_radio.setChecked(True)

        operation_layout.addWidget(self.add_prefix_radio)
        operation_layout.addWidget(self.add_postfix_radio)
        operation_layout.addWidget(self.add_both_radio)
        operation_layout.addWidget(self.replace_radio)
        operation_layout.addStretch()
        naming_layout.addLayout(operation_layout)

        # Prefix input
        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(QLabel("Prefix:"))
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("e.g., train_")
        prefix_layout.addWidget(self.prefix_input)
        naming_layout.addLayout(prefix_layout)

        # Postfix input
        postfix_layout = QHBoxLayout()
        postfix_layout.addWidget(QLabel("Postfix:"))
        self.postfix_input = QLineEdit()
        self.postfix_input.setPlaceholderText("e.g., _v2")
        postfix_layout.addWidget(self.postfix_input)
        naming_layout.addLayout(postfix_layout)

        # Replace pattern
        replace_layout = QGridLayout()
        replace_layout.addWidget(QLabel("Find:"), 0, 0)
        self.find_pattern = QLineEdit()
        replace_layout.addWidget(self.find_pattern, 0, 1)
        replace_layout.addWidget(QLabel("Replace with:"), 1, 0)
        self.replace_pattern = QLineEdit()
        replace_layout.addWidget(self.replace_pattern, 1, 1)
        naming_layout.addLayout(replace_layout)

        # Additional options
        self.preserve_extension = QCheckBox("Preserve file extension")
        self.preserve_extension.setChecked(True)
        naming_layout.addWidget(self.preserve_extension)

        self.sequential_numbering = QCheckBox("Add sequential numbering")
        naming_layout.addWidget(self.sequential_numbering)

        # Numbering options
        number_layout = QHBoxLayout()
        number_layout.addWidget(QLabel("Start from:"))
        self.start_number = QSpinBox()
        self.start_number.setRange(0, 999999)
        self.start_number.setValue(1)
        number_layout.addWidget(self.start_number)
        number_layout.addWidget(QLabel("Padding:"))
        self.padding = QSpinBox()
        self.padding.setRange(1, 10)
        self.padding.setValue(4)
        number_layout.addWidget(self.padding)
        number_layout.addStretch()
        naming_layout.addLayout(number_layout)

        naming_group.setLayout(naming_layout)
        layout.addWidget(naming_group)

        # Preview section
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout()

        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(2)
        self.preview_table.setHorizontalHeaderLabels(["Original Name", "New Name"])
        self.preview_table.setMaximumHeight(150)
        preview_layout.addWidget(self.preview_table)

        preview_btn_layout = QHBoxLayout()
        self.preview_btn = QPushButton("Generate Preview")
        preview_btn_layout.addWidget(self.preview_btn)
        preview_btn_layout.addStretch()
        preview_layout.addLayout(preview_btn_layout)

        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        # Output section
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()

        self.copy_files = QRadioButton("Copy files with new names")
        self.rename_files = QRadioButton("Rename files in place")
        self.copy_files.setChecked(True)
        output_layout.addWidget(self.copy_files)
        output_layout.addWidget(self.rename_files)

        output_path_layout = QHBoxLayout()
        output_path_layout.addWidget(QLabel("Output Path (for copy):"))
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
        self.start_btn = QPushButton("Start Renaming")
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


class ImageLabelProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Data Processing Tool")
        self.setGeometry(100, 100, 1000, 800)

        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #4CAF50;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                padding: 5px 15px;
                border-radius: 3px;
                border: 1px solid #cccccc;
                background-color: #f8f8f8;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
            }
            QPushButton:pressed {
                background-color: #d8d8d8;
            }
        """)

        self.init_ui()

    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create title label
        title_label = QLabel("AI Data Processing Tool")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Add tabs
        self.sampling_tab = SamplingTab()
        self.augmentation_tab = AugmentationTab()
        self.dataset_split_tab = DatasetSplitTab()
        self.prefix_postfix_tab = PrefixPostfixTab()

        self.tab_widget.addTab(self.sampling_tab, "Sampling")
        self.tab_widget.addTab(self.augmentation_tab, "Augmentation")
        self.tab_widget.addTab(self.dataset_split_tab, "Dataset Split")
        self.tab_widget.addTab(self.prefix_postfix_tab, "Prefix/Postfix")

        main_layout.addWidget(self.tab_widget)

        # Create status bar
        self.statusBar().showMessage("Ready")


def main():
    app = QApplication(sys.argv)
    window = ImageLabelProcessor()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()