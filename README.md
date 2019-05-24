# Detect and Decode barcode in an image file

This utility will load an image and try to find if any barcode exists. Then decode them with Zbar library.

## Prerequisites

The code were written in python. Please make sure you have correspond environment.

- Python 3
- OpenCV
- ZBar library

```bash
# Install required packages
sudo apt update
sudo apt install libzbar-dev
pip install opencv-python
pip install pyzbar
```

## Usage

```bash
python detect_barcode.py -i "<your image path here>"
```

## Contact

Kuang-Cheng, Chien - me@kcchien.com
