# UFO Search App

A Flask web application for searching and browsing declassified UFO documents with full-text search, OCR, and image extraction.

**Includes pre-indexed database with 115 documents, 3960 pages, and 4000+ extracted images.**

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Tesseract OCR
# Mac: brew install tesseract
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Linux: sudo apt install tesseract-ocr

# 3. Run the app
python app.py
```

Open **http://localhost:5000** in your browser.

## What's Included

- **Pre-indexed database** (`ufo_index.db`) - 115 UFO documents ready to search
- **Extracted images** (`static/extracted_images/`) - 4000+ images with OCR text
- **Flask web app** - dark theme UI with search, browse, and image viewer

## Features

- Full-text search across all documents
- OCR text extraction from scanned pages and images
- Click images to open full-size version
- Browse by document or search by keyword
- Modern dark theme interface

## Adding More PDFs

Want to add your own PDFs? Add them to `~/UFO_Files/` and run:
```bash
python index_pdfs.py
```

## Network Access

To access from other devices on your network, find your IP:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```
Then connect to `http://YOUR_IP:5000`.

## Project Structure

```
ufo-search-app/
├── app.py              # Flask web application
├── index_pdfs.py       # PDF indexing script with OCR
├── requirements.txt    # Python dependencies
├── ufo_index.db        # Pre-indexed database (115 docs)
├── static/
│   └── extracted_images/  # 4000+ extracted images
└── templates/          # HTML templates
```

## Requirements

- Python 3.8+
- Tesseract OCR
- Flask, pymupdf, pytesseract, Pillow, pandas