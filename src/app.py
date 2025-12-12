"""
AI Data Processing Tool - Main Application Window
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.modules.sampling.sampling_tab import SamplingTab
from src.modules.augmentation.augmentation_tab import AugmentationTab
from src.modules.dataset_split.dataset_split_tab import DatasetSplitTab
from src.modules.prefix_postfix.prefix_postfix_tab import PrefixPostfixTab


class ImageLabelProcessor(QMainWindow):
    """Main application window"""

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
        """Initialize the user interface"""
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
