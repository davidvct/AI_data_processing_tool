"""
AI Data Processing Tool
A PySide6 application for processing images and labels with sampling,
augmentation, dataset splitting, and prefix/postfix functionality.

GitHub: https://github.com/davidvct/AI_data_processing_tool
"""

import sys
from PySide6.QtWidgets import QApplication

from src.app import ImageLabelProcessor


def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = ImageLabelProcessor()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()