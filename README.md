# AI Data Processing Tool

A comprehensive PySide6 application for processing images and labels with various data manipulation functionalities.

**GitHub Repository:** [https://github.com/davidvct/AI_data_processing_tool](https://github.com/davidvct/AI_data_processing_tool)

## Features

The application provides four main functionalities through a tabbed interface:

### 1. Sampling
- Random, stratified, systematic, and cluster sampling methods
- Configurable sample size and random seed
- Progress tracking and logging

### 2. Augmentation
- Multiple augmentation techniques:
  - Rotation
  - Horizontal/Vertical Flip
  - Brightness/Contrast adjustment
  - Noise addition
  - Blur effects
  - Random cropping
  - Scale/Zoom
  - Color jitter
- Augmentation multiplier for creating multiple variations

### 3. Dataset Split
- Train/Validation/Test splitting with customizable ratios
- Multiple split methods: Random, Stratified, Sequential, Group-based
- Option to create separate folders for each split
- Shuffle and random seed options

### 4. Prefix/Postfix
- Add prefix, postfix, or both to filenames
- Pattern replacement functionality
- Sequential numbering with padding
- Preview before applying changes
- Copy or rename in place options

## Installation

1. Clone the repository:
```bash
git clone https://github.com/davidvct/AI_data_processing_tool.git
cd AI_data_processing_tool
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.8+
- PySide6 >= 6.5.0
- Pillow >= 10.0.0
- numpy >= 1.24.0
- opencv-python >= 4.8.0

## Usage

Run the application:
```bash
python main.py
```

## GUI Structure

The application features:
- Clean, modern tabbed interface
- Organized sections with grouped controls
- Progress bars for long-running operations
- Log areas for operation feedback
- Input validation with appropriate controls (spinboxes, checkboxes, radio buttons)
- Browse buttons for file/folder selection
- Preview functionality where applicable

## Development Status

Currently, the GUI structure is complete and ready for backend functionality implementation. The interface includes all necessary UI elements that can be connected to processing functions.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

[To be added]

## Author

David VCT

## Repository

[https://github.com/davidvct/AI_data_processing_tool](https://github.com/davidvct/AI_data_processing_tool)