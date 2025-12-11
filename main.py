"""
AI Data Processing Tool
A PySide6 application for processing images and labels with sampling,
augmentation, dataset splitting, and prefix/postfix functionality.

GitHub: https://github.com/davidvct/AI_data_processing_tool
"""

import sys
import os
import random
import shutil
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                              QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                              QLineEdit, QTextEdit, QGroupBox, QSpinBox,
                              QDoubleSpinBox, QComboBox, QCheckBox, QListWidget,
                              QTableWidget, QSplitter, QFileDialog, QSlider,
                              QProgressBar, QRadioButton, QGridLayout, QListWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor


class SamplingTab(QWidget):
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
        self.progress_bar = QProgressBar()
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
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        layout.addStretch()
        self.setLayout(layout)

    def create_video_frame_yolo_ui(self):
        """Create UI for Video Frame - Yolo mode"""
        self.video_frame_widget = QWidget()
        main_layout = QVBoxLayout()

        # Input folder path
        input_group = QGroupBox("Input Folder")
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Folder Path:"))
        self.vf_input_path = QLineEdit()
        self.vf_input_path.setPlaceholderText("Select folder containing video subfolders...")
        input_layout.addWidget(self.vf_input_path)
        self.vf_browse_btn = QPushButton("Browse")
        self.vf_browse_btn.clicked.connect(self.browse_input_folder)
        input_layout.addWidget(self.vf_browse_btn)
        self.vf_analyze_btn = QPushButton("Analyze")
        self.vf_analyze_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")
        self.vf_analyze_btn.clicked.connect(self.analyze_dataset)
        input_layout.addWidget(self.vf_analyze_btn)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # Create horizontal splitter for left panel (video folders) and right panel (controls)
        splitter = QSplitter(Qt.Horizontal)

        # Left Panel - Video Folders List
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        folders_label = QLabel("Video Folders")
        folders_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        left_layout.addWidget(folders_label)

        # Toolbar for folder list
        folder_toolbar = QHBoxLayout()
        self.vf_select_all_btn = QPushButton("Select All")
        self.vf_select_all_btn.clicked.connect(self.select_all_folders)
        self.vf_deselect_all_btn = QPushButton("Deselect All")
        self.vf_deselect_all_btn.clicked.connect(self.deselect_all_folders)
        folder_toolbar.addWidget(self.vf_select_all_btn)
        folder_toolbar.addWidget(self.vf_deselect_all_btn)
        folder_toolbar.addStretch()
        left_layout.addLayout(folder_toolbar)

        # Video folders list with checkboxes
        self.vf_folders_list = QListWidget()
        self.vf_folders_list.setMinimumWidth(250)
        left_layout.addWidget(self.vf_folders_list)

        left_panel.setLayout(left_layout)

        # Right Panel - Controls and Statistics
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        # Statistics Section
        stats_group = QGroupBox("Dataset Statistics")
        stats_layout = QGridLayout()

        # Create labels for statistics
        stats_layout.addWidget(QLabel("Total Images:"), 0, 0)
        self.vf_total_images_label = QLabel("N/A")
        stats_layout.addWidget(self.vf_total_images_label, 0, 1)

        stats_layout.addWidget(QLabel("Total Labels:"), 1, 0)
        self.vf_total_labels_label = QLabel("N/A")
        stats_layout.addWidget(self.vf_total_labels_label, 1, 1)

        stats_layout.addWidget(QLabel("Video Folders:"), 2, 0)
        self.vf_video_folders_label = QLabel("N/A")
        stats_layout.addWidget(self.vf_video_folders_label, 2, 1)

        stats_layout.addWidget(QLabel("Images per Folder:"), 3, 0)
        self.vf_images_per_folder_label = QLabel("N/A")
        stats_layout.addWidget(self.vf_images_per_folder_label, 3, 1)

        stats_layout.addWidget(QLabel("Image Resolutions:"), 4, 0)
        self.vf_resolutions_label = QLabel("N/A")
        self.vf_resolutions_label.setWordWrap(True)
        stats_layout.addWidget(self.vf_resolutions_label, 4, 1)

        stats_layout.addWidget(QLabel("Image File Size:"), 5, 0)
        self.vf_file_size_label = QLabel("N/A")
        stats_layout.addWidget(self.vf_file_size_label, 5, 1)

        stats_layout.addWidget(QLabel("Annotations per File:"), 6, 0)
        self.vf_annotations_label = QLabel("N/A")
        stats_layout.addWidget(self.vf_annotations_label, 6, 1)

        stats_layout.addWidget(QLabel("Classes Found:"), 7, 0)
        self.vf_classes_label = QLabel("N/A")
        stats_layout.addWidget(self.vf_classes_label, 7, 1)

        stats_group.setLayout(stats_layout)
        right_layout.addWidget(stats_group)

        # Sampling Options
        sampling_group = QGroupBox("Sampling Options")
        sampling_layout = QGridLayout()

        # Sample size
        sampling_layout.addWidget(QLabel("Sample Size:"), 0, 0)
        self.vf_sample_size = QSpinBox()
        self.vf_sample_size.setRange(1, 100000)
        self.vf_sample_size.setValue(50)
        sampling_layout.addWidget(self.vf_sample_size, 0, 1)

        # Random seed
        sampling_layout.addWidget(QLabel("Random Seed:"), 1, 0)
        self.vf_random_seed = QSpinBox()
        self.vf_random_seed.setRange(0, 999999)
        self.vf_random_seed.setValue(42)
        sampling_layout.addWidget(self.vf_random_seed, 1, 1)

        sampling_group.setLayout(sampling_layout)
        right_layout.addWidget(sampling_group)

        # Output section
        output_group = QGroupBox("Output Folder")
        output_layout = QVBoxLayout()

        output_path_layout = QHBoxLayout()
        output_path_layout.addWidget(QLabel("Output Path:"))
        self.vf_output_path = QLineEdit()
        self.vf_output_path.setPlaceholderText("Will create 'images' and 'labels' folders here...")
        output_path_layout.addWidget(self.vf_output_path)
        self.vf_output_browse_btn = QPushButton("Browse")
        self.vf_output_browse_btn.clicked.connect(self.browse_output_folder)
        output_path_layout.addWidget(self.vf_output_browse_btn)
        output_layout.addLayout(output_path_layout)

        output_group.setLayout(output_layout)
        right_layout.addWidget(output_group)

        right_layout.addStretch()
        right_panel.setLayout(right_layout)

        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)  # Left panel
        splitter.setStretchFactor(1, 2)  # Right panel gets more space

        main_layout.addWidget(splitter)
        self.video_frame_widget.setLayout(main_layout)

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

    # Video Frame - Yolo mode handlers
    def browse_input_folder(self):
        """Browse for input folder containing video subfolders"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Input Folder",
            self.vf_input_path.text() if self.vf_input_path.text() else ""
        )
        if folder:
            self.vf_input_path.setText(folder)
            self.log_text.append(f"Input folder selected: {folder}")
            self.scan_video_folders()

    def browse_output_folder(self):
        """Browse for output folder"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            self.vf_output_path.text() if self.vf_output_path.text() else ""
        )
        if folder:
            self.vf_output_path.setText(folder)
            self.log_text.append(f"Output folder selected: {folder}")

    def analyze_dataset(self):
        """Analyze the dataset and display statistics"""
        input_path = self.vf_input_path.text()
        if not input_path:
            self.log_text.append("Error: Please select an input folder first")
            return

        self.log_text.append(f"Analyzing dataset at: {input_path}")
        # TODO: Implement dataset analysis
        self.log_text.append("Analysis complete (not yet implemented)")

    def select_all_folders(self):
        """Select all video folders"""
        for i in range(self.vf_folders_list.count()):
            item = self.vf_folders_list.item(i)
            item.setCheckState(Qt.Checked)

    def deselect_all_folders(self):
        """Deselect all video folders"""
        for i in range(self.vf_folders_list.count()):
            item = self.vf_folders_list.item(i)
            item.setCheckState(Qt.Unchecked)

    def scan_video_folders(self):
        """Scan input folder for video subfolders and populate the list"""
        input_path = self.vf_input_path.text()
        if not input_path or not os.path.exists(input_path):
            self.log_text.append("Error: Invalid input folder path")
            return

        # Clear existing list
        self.vf_folders_list.clear()

        # Scan for subfolders
        try:
            subfolders = [f for f in os.listdir(input_path)
                         if os.path.isdir(os.path.join(input_path, f))]

            if not subfolders:
                self.log_text.append("No subfolders found in the selected directory")
                return

            # Add each subfolder to the list with a checkbox
            for folder_name in sorted(subfolders):
                item = QListWidgetItem(folder_name)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked)  # Default to checked
                self.vf_folders_list.addItem(item)

            self.log_text.append(f"Found {len(subfolders)} video folder(s)")

        except Exception as e:
            self.log_text.append(f"Error scanning folders: {str(e)}")

    def start_sampling(self):
        """Start the sampling process based on current mode"""
        current_mode = self.mode_selector.currentIndex()

        if current_mode == 0:  # Video Frame - Yolo
            self.start_video_frame_sampling()
        else:
            self.log_text.append(f"Error: {self.mode_selector.currentText()} mode is not yet implemented")

    def start_video_frame_sampling(self):
        """Start sampling for Video Frame - Yolo mode"""
        # Validate inputs
        input_path = self.vf_input_path.text()
        output_path = self.vf_output_path.text()

        if not input_path:
            self.log_text.append("Error: Please select an input folder")
            return

        if not output_path:
            self.log_text.append("Error: Please select an output folder")
            return

        if not os.path.exists(input_path):
            self.log_text.append("Error: Input folder does not exist")
            return

        # Get selected video folders
        selected_folders = []
        for i in range(self.vf_folders_list.count()):
            item = self.vf_folders_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_folders.append(item.text())

        if not selected_folders:
            self.log_text.append("Error: No video folders selected")
            return

        sample_size = self.vf_sample_size.value()
        random_seed = self.vf_random_seed.value()

        self.log_text.append("=" * 50)
        self.log_text.append("Starting sampling process...")
        self.log_text.append(f"Input folder: {input_path}")
        self.log_text.append(f"Output folder: {output_path}")
        self.log_text.append(f"Selected folders: {len(selected_folders)}")
        self.log_text.append(f"Sample size: {sample_size}")
        self.log_text.append(f"Random seed: {random_seed}")
        self.log_text.append("=" * 50)

        try:
            # Step 1: Collect all image/label pairs from selected folders
            self.log_text.append("Step 1: Collecting image/label pairs...")
            image_label_pairs = []
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

            for folder_name in selected_folders:
                video_folder_path = os.path.join(input_path, folder_name)
                frames_folder = os.path.join(video_folder_path, 'frames')
                labels_folder = os.path.join(video_folder_path, 'labels')

                # Check if frames and labels folders exist
                if not os.path.exists(frames_folder):
                    self.log_text.append(f"Warning: 'frames' folder not found in {folder_name}, skipping...")
                    continue

                if not os.path.exists(labels_folder):
                    self.log_text.append(f"Warning: 'labels' folder not found in {folder_name}, skipping...")
                    continue

                # Get all image files from frames folder
                for image_file in os.listdir(frames_folder):
                    if Path(image_file).suffix.lower() in image_extensions:
                        # Get corresponding label file (same name but .txt extension)
                        label_file = Path(image_file).stem + '.txt'
                        image_path = os.path.join(frames_folder, image_file)
                        label_path = os.path.join(labels_folder, label_file)

                        # Only add if both image and label exist
                        if os.path.exists(label_path):
                            image_label_pairs.append({
                                'image': image_path,
                                'label': label_path,
                                'folder': folder_name,
                                'filename': image_file
                            })

            self.log_text.append(f"Found {len(image_label_pairs)} valid image/label pairs")

            if len(image_label_pairs) == 0:
                self.log_text.append("Error: No valid image/label pairs found")
                return

            # Step 2: Randomly sample specified number
            self.log_text.append(f"Step 2: Randomly sampling {sample_size} pairs...")
            random.seed(random_seed)

            if sample_size > len(image_label_pairs):
                self.log_text.append(f"Warning: Sample size ({sample_size}) is larger than available pairs ({len(image_label_pairs)})")
                self.log_text.append("Using all available pairs instead")
                sampled_pairs = image_label_pairs
            else:
                sampled_pairs = random.sample(image_label_pairs, sample_size)

            self.log_text.append(f"Sampled {len(sampled_pairs)} pairs")

            # Step 3: Create output folders
            self.log_text.append("Step 3: Creating output folders...")
            output_images_folder = os.path.join(output_path, 'images')
            output_labels_folder = os.path.join(output_path, 'labels')

            os.makedirs(output_images_folder, exist_ok=True)
            os.makedirs(output_labels_folder, exist_ok=True)
            self.log_text.append(f"Created: {output_images_folder}")
            self.log_text.append(f"Created: {output_labels_folder}")

            # Step 4: Copy sampled files to output folders
            self.log_text.append("Step 4: Copying files...")
            self.progress_bar.setMaximum(len(sampled_pairs))
            self.progress_bar.setValue(0)

            for idx, pair in enumerate(sampled_pairs):
                # Copy image
                dest_image = os.path.join(output_images_folder, pair['filename'])
                shutil.copy2(pair['image'], dest_image)

                # Copy label
                label_filename = Path(pair['filename']).stem + '.txt'
                dest_label = os.path.join(output_labels_folder, label_filename)
                shutil.copy2(pair['label'], dest_label)

                self.progress_bar.setValue(idx + 1)

            self.log_text.append("=" * 50)
            self.log_text.append("✓ Sampling completed successfully!")
            self.log_text.append(f"✓ {len(sampled_pairs)} image/label pairs copied to output folder")
            self.log_text.append("=" * 50)

        except Exception as e:
            self.log_text.append(f"Error during sampling: {str(e)}")
            import traceback
            self.log_text.append(traceback.format_exc())


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