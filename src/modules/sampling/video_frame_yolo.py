"""
Video Frame - Yolo sampling implementation
Handles sampling of image/label pairs from video frame datasets
"""

import os
import random
import shutil
from pathlib import Path
from PIL import Image

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                              QLineEdit, QGroupBox, QSpinBox, QListWidget, QSplitter,
                              QGridLayout, QListWidgetItem, QMessageBox, QFileDialog,
                              QApplication)
from PySide6.QtCore import Qt

from src.utils.file_utils import format_file_size


class VideoFrameYoloWidget(QWidget):
    """UI and logic for Video Frame - Yolo sampling mode"""

    def __init__(self, log_text, progress_bar):
        super().__init__()
        self.log_text = log_text
        self.progress_bar = progress_bar
        self.init_ui()

    def init_ui(self):
        """Initialize the UI for Video Frame - Yolo mode"""
        main_layout = QVBoxLayout()

        # Input folder path
        input_group = QGroupBox("Input Folder")
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Folder Path:"))
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Select folder containing video subfolders...")
        input_layout.addWidget(self.input_path)
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_input_folder)
        input_layout.addWidget(self.browse_btn)
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")
        self.analyze_btn.clicked.connect(self.analyze_dataset)
        input_layout.addWidget(self.analyze_btn)
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
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all_folders)
        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all_folders)
        folder_toolbar.addWidget(self.select_all_btn)
        folder_toolbar.addWidget(self.deselect_all_btn)
        folder_toolbar.addStretch()
        left_layout.addLayout(folder_toolbar)

        # Video folders list with checkboxes
        self.folders_list = QListWidget()
        self.folders_list.setMinimumWidth(250)
        left_layout.addWidget(self.folders_list)

        left_panel.setLayout(left_layout)

        # Right Panel - Controls and Statistics
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        # Statistics Section
        stats_group = QGroupBox("Dataset Statistics")
        stats_layout = QGridLayout()

        # Create labels for statistics
        stats_layout.addWidget(QLabel("Total Images:"), 0, 0)
        self.total_images_label = QLabel("N/A")
        stats_layout.addWidget(self.total_images_label, 0, 1)

        stats_layout.addWidget(QLabel("Total Labels:"), 1, 0)
        self.total_labels_label = QLabel("N/A")
        stats_layout.addWidget(self.total_labels_label, 1, 1)

        stats_layout.addWidget(QLabel("Video Folders:"), 2, 0)
        self.video_folders_label = QLabel("N/A")
        stats_layout.addWidget(self.video_folders_label, 2, 1)

        stats_layout.addWidget(QLabel("Images per Folder:"), 3, 0)
        self.images_per_folder_label = QLabel("N/A")
        stats_layout.addWidget(self.images_per_folder_label, 3, 1)

        stats_layout.addWidget(QLabel("Image Resolutions:"), 4, 0)
        self.resolutions_label = QLabel("N/A")
        self.resolutions_label.setWordWrap(True)
        stats_layout.addWidget(self.resolutions_label, 4, 1)

        stats_layout.addWidget(QLabel("Image File Size:"), 5, 0)
        self.file_size_label = QLabel("N/A")
        stats_layout.addWidget(self.file_size_label, 5, 1)

        stats_layout.addWidget(QLabel("Annotations per File:"), 6, 0)
        self.annotations_label = QLabel("N/A")
        stats_layout.addWidget(self.annotations_label, 6, 1)

        stats_layout.addWidget(QLabel("Classes Found:"), 7, 0)
        self.classes_label = QLabel("N/A")
        stats_layout.addWidget(self.classes_label, 7, 1)

        stats_group.setLayout(stats_layout)
        right_layout.addWidget(stats_group)

        # Sampling Options
        sampling_group = QGroupBox("Sampling Options")
        sampling_layout = QGridLayout()

        # Sample size
        sampling_layout.addWidget(QLabel("Sample Size:"), 0, 0)
        self.sample_size = QSpinBox()
        self.sample_size.setRange(1, 100000)
        self.sample_size.setValue(50)
        sampling_layout.addWidget(self.sample_size, 0, 1)

        # Random seed
        sampling_layout.addWidget(QLabel("Random Seed:"), 1, 0)
        self.random_seed = QSpinBox()
        self.random_seed.setRange(0, 999999)
        self.random_seed.setValue(42)
        sampling_layout.addWidget(self.random_seed, 1, 1)

        sampling_group.setLayout(sampling_layout)
        right_layout.addWidget(sampling_group)

        # Output section
        output_group = QGroupBox("Output Folder")
        output_layout = QVBoxLayout()

        output_path_layout = QHBoxLayout()
        output_path_layout.addWidget(QLabel("Output Path:"))
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Will create 'images' and 'labels' folders here...")
        output_path_layout.addWidget(self.output_path)
        self.output_browse_btn = QPushButton("Browse")
        self.output_browse_btn.clicked.connect(self.browse_output_folder)
        output_path_layout.addWidget(self.output_browse_btn)
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
        self.setLayout(main_layout)

    def browse_input_folder(self):
        """Browse for input folder containing video subfolders"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Input Folder",
            self.input_path.text() if self.input_path.text() else ""
        )
        if folder:
            self.input_path.setText(folder)
            self.log_text.append(f"Input folder selected: {folder}")
            self.scan_video_folders()

    def browse_output_folder(self):
        """Browse for output folder"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            self.output_path.text() if self.output_path.text() else ""
        )
        if folder:
            self.output_path.setText(folder)
            self.log_text.append(f"Output folder selected: {folder}")

    def analyze_dataset(self):
        """Analyze the dataset and display statistics"""
        input_path = self.input_path.text()
        if not input_path:
            self.log_text.append("Error: Please select an input folder first")
            return

        if not os.path.exists(input_path):
            self.log_text.append("Error: Input folder does not exist")
            return

        self.log_text.append("=" * 50)
        self.log_text.append(f"Analyzing dataset at: {input_path}")
        QApplication.processEvents()

        try:
            # Get all video folders
            video_folders = [f for f in os.listdir(input_path)
                           if os.path.isdir(os.path.join(input_path, f))]

            if not video_folders:
                self.log_text.append("Error: No subfolders found")
                return

            # Initialize statistics
            total_images = 0
            total_labels = 0
            folder_image_counts = []
            resolutions = {}
            file_sizes = []
            annotation_counts = []
            all_classes = set()
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

            # Analyze each video folder
            for folder_name in video_folders:
                video_folder_path = os.path.join(input_path, folder_name)
                frames_folder = os.path.join(video_folder_path, 'frames')
                labels_folder = os.path.join(video_folder_path, 'labels')

                # Check if folders exist
                if not os.path.exists(frames_folder) or not os.path.exists(labels_folder):
                    continue

                # Count images in this folder
                folder_images = 0

                # Analyze frames folder
                for image_file in os.listdir(frames_folder):
                    if Path(image_file).suffix.lower() in image_extensions:
                        folder_images += 1
                        total_images += 1
                        image_path = os.path.join(frames_folder, image_file)

                        # Get file size
                        file_size = os.path.getsize(image_path)
                        file_sizes.append(file_size)

                        # Get image resolution (only sample some to save time)
                        if total_images % 10 == 0 or total_images <= 10:
                            try:
                                with Image.open(image_path) as img:
                                    resolution = f"{img.width}x{img.height}"
                                    resolutions[resolution] = resolutions.get(resolution, 0) + 1
                            except Exception:
                                pass  # Skip if image can't be opened

                folder_image_counts.append(folder_images)

                # Analyze labels folder
                for label_file in os.listdir(labels_folder):
                    if label_file.endswith('.txt'):
                        total_labels += 1
                        label_path = os.path.join(labels_folder, label_file)

                        # Count annotations and classes in this label file
                        try:
                            with open(label_path, 'r') as f:
                                lines = f.readlines()
                                annotation_counts.append(len(lines))

                                # Extract class IDs (first number in each line)
                                for line in lines:
                                    parts = line.strip().split()
                                    if parts:
                                        all_classes.add(int(parts[0]))
                        except Exception:
                            pass  # Skip if file can't be read

            # Calculate statistics
            num_folders = len([c for c in folder_image_counts if c > 0])
            min_images = min(folder_image_counts) if folder_image_counts else 0
            max_images = max(folder_image_counts) if folder_image_counts else 0
            avg_images = sum(folder_image_counts) / len(folder_image_counts) if folder_image_counts else 0

            min_file_size = min(file_sizes) if file_sizes else 0
            max_file_size = max(file_sizes) if file_sizes else 0

            min_annotations = min(annotation_counts) if annotation_counts else 0
            max_annotations = max(annotation_counts) if annotation_counts else 0

            num_classes = len(all_classes)

            # Update UI labels
            self.total_images_label.setText(str(total_images))
            self.total_labels_label.setText(str(total_labels))
            self.video_folders_label.setText(str(num_folders))
            self.images_per_folder_label.setText(f"Min: {min_images}, Max: {max_images}, Avg: {avg_images:.1f}")

            # Format resolutions
            if resolutions:
                # Get top 5 most common resolutions
                sorted_res = sorted(resolutions.items(), key=lambda x: x[1], reverse=True)[:5]
                res_text = ", ".join([f"{res} ({count})" for res, count in sorted_res])
                self.resolutions_label.setText(res_text)
            else:
                self.resolutions_label.setText("N/A")

            # Format file sizes
            min_size_str = format_file_size(min_file_size)
            max_size_str = format_file_size(max_file_size)
            self.file_size_label.setText(f"Min: {min_size_str}, Max: {max_size_str}")

            self.annotations_label.setText(f"Min: {min_annotations}, Max: {max_annotations}")
            self.classes_label.setText(str(num_classes))

            # Log results
            self.log_text.append(f"✓ Analysis complete!")
            self.log_text.append(f"  Total images: {total_images}")
            self.log_text.append(f"  Total labels: {total_labels}")
            self.log_text.append(f"  Video folders: {num_folders}")
            self.log_text.append(f"  Classes found: {num_classes}")
            self.log_text.append("=" * 50)

        except Exception as e:
            self.log_text.append(f"Error during analysis: {str(e)}")
            import traceback
            self.log_text.append(traceback.format_exc())

    def select_all_folders(self):
        """Select all video folders"""
        for i in range(self.folders_list.count()):
            item = self.folders_list.item(i)
            item.setCheckState(Qt.Checked)

    def deselect_all_folders(self):
        """Deselect all video folders"""
        for i in range(self.folders_list.count()):
            item = self.folders_list.item(i)
            item.setCheckState(Qt.Unchecked)

    def scan_video_folders(self):
        """Scan input folder for video subfolders and populate the list"""
        input_path = self.input_path.text()
        if not input_path or not os.path.exists(input_path):
            self.log_text.append("Error: Invalid input folder path")
            return

        # Clear existing list
        self.folders_list.clear()

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
                self.folders_list.addItem(item)

            self.log_text.append(f"Found {len(subfolders)} video folder(s)")

        except Exception as e:
            self.log_text.append(f"Error scanning folders: {str(e)}")

    def start_sampling(self):
        """Start sampling for Video Frame - Yolo mode"""
        # Validate inputs
        input_path = self.input_path.text()
        output_path = self.output_path.text()

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
        for i in range(self.folders_list.count()):
            item = self.folders_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_folders.append(item.text())

        if not selected_folders:
            self.log_text.append("Error: No video folders selected")
            return

        sample_size = self.sample_size.value()
        random_seed = self.random_seed.value()

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
            QApplication.processEvents()  # Update UI immediately

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

                # Get all label files once (much faster than checking existence for each image)
                label_files = {Path(f).stem for f in os.listdir(labels_folder) if f.endswith('.txt')}

                # Get all image files from frames folder
                for image_file in os.listdir(frames_folder):
                    if Path(image_file).suffix.lower() in image_extensions:
                        image_stem = Path(image_file).stem

                        # Check if corresponding label exists in the set (O(1) lookup)
                        if image_stem in label_files:
                            image_path = os.path.join(frames_folder, image_file)
                            label_path = os.path.join(labels_folder, image_stem + '.txt')

                            image_label_pairs.append({
                                'image': image_path,
                                'label': label_path,
                                'folder': folder_name,
                                'filename': image_file
                            })

            self.log_text.append(f"Found {len(image_label_pairs)} valid image/label pairs")
            QApplication.processEvents()  # Update UI after collection

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
            self.log_text.append("Step 3: Preparing output folders...")
            output_images_folder = os.path.join(output_path, 'images')
            output_labels_folder = os.path.join(output_path, 'labels')

            os.makedirs(output_images_folder, exist_ok=True)
            os.makedirs(output_labels_folder, exist_ok=True)

            # Check if output folders already contain files
            existing_images = [f for f in os.listdir(output_images_folder) if os.path.isfile(os.path.join(output_images_folder, f))]
            existing_labels = [f for f in os.listdir(output_labels_folder) if os.path.isfile(os.path.join(output_labels_folder, f))]

            if existing_images or existing_labels:
                # Ask user what to do with existing files
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Existing Files Found")
                msg_box.setText(f"The output folders already contain files:\n"
                               f"- {len(existing_images)} image(s)\n"
                               f"- {len(existing_labels)} label(s)\n\n"
                               f"Do you want to delete all existing files before sampling?")
                msg_box.setInformativeText("Yes: Delete all existing files and start fresh\n"
                                          "No: Keep existing files (may overwrite files with same names)\n"
                                          "Cancel: Abort sampling operation")

                yes_btn = msg_box.addButton("Yes", QMessageBox.YesRole)
                no_btn = msg_box.addButton("No", QMessageBox.NoRole)
                cancel_btn = msg_box.addButton("Cancel", QMessageBox.RejectRole)

                msg_box.exec()
                clicked_button = msg_box.clickedButton()

                if clicked_button == cancel_btn:
                    self.log_text.append("Sampling cancelled by user")
                    return
                elif clicked_button == yes_btn:
                    # Delete all existing files
                    self.log_text.append("Deleting existing files...")
                    for img_file in existing_images:
                        os.remove(os.path.join(output_images_folder, img_file))
                    for lbl_file in existing_labels:
                        os.remove(os.path.join(output_labels_folder, lbl_file))
                    self.log_text.append(f"Deleted {len(existing_images)} image(s) and {len(existing_labels)} label(s)")
                else:  # No button
                    self.log_text.append("Keeping existing files (may overwrite files with same names)")

            self.log_text.append(f"Output folder ready: {output_images_folder}")
            self.log_text.append(f"Output folder ready: {output_labels_folder}")

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

                # Update UI every 10 files to show progress
                if (idx + 1) % 10 == 0:
                    QApplication.processEvents()

            self.log_text.append("=" * 50)
            self.log_text.append("✓ Sampling completed successfully!")
            self.log_text.append(f"✓ {len(sampled_pairs)} image/label pairs copied to output folder")
            self.log_text.append("=" * 50)

        except Exception as e:
            self.log_text.append(f"Error during sampling: {str(e)}")
            import traceback
            self.log_text.append(traceback.format_exc())
