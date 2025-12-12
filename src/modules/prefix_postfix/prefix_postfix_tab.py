"""
Prefix/Postfix Tab - UI for file renaming operations
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                              QLineEdit, QTextEdit, QGroupBox, QSpinBox, QComboBox,
                              QCheckBox, QRadioButton, QProgressBar, QTableWidget,
                              QGridLayout)


class PrefixPostfixTab(QWidget):
    """Tab for prefix/postfix file renaming functionality"""

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
