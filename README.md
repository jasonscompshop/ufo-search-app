# UFO Search App

A Flask web application for searching and browsing declassified UFO documents with full-text search, OCR, and image extraction.

## What's Included

- **115 original PDF documents** - all government declassified files
- **Pre-indexed database** - instant search, no setup needed
- **4000+ extracted images** - with OCR text (see Mega download below)
- **Full-text search** - across all documents and images

## Quick Setup

### 1. Clone the repo
```bash
git clone https://github.com/jasonscompshop/ufo-search-app.git
cd ufo-search-app
```

### 2. Download images (Mega.nz)
Download the extracted images folder from:
**https://mega.nz/folder/fOxmiSyB#UubvIy6_ncbz1YleY33jvA**

After download, place the `static/extracted_images/` folder in the project directory so it looks like:
```
ufo-search-app/static/extracted_images/
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR
- **Mac:** `brew install tesseract`
- **Windows:** https://github.com/UB-Mannheim/tesseract/wiki
- **Linux:** `sudo apt install tesseract-ocr`

### 5. Run the app
```bash
python app.py
```

Open **http://localhost:5000** in your browser.

## Features

- Full-text search across all 115 documents
- OCR text extraction from scanned pages and images
- Click images to view full-size version
- Browse by document or search by keyword
- Modern dark theme interface
- Works on local network (for other devices)

## Network Access

To access from other devices:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```
Then connect to `http://YOUR_IP:5000`

## Adding More PDFs

Place new PDFs in `~/UFO_Files/` and run:
```bash
python index_pdfs.py
```

## Project Structure

```
ufo-search-app/
├── PDFs/              # 115 original PDF documents
├── app.py             # Flask web application
├── index_pdfs.py      # PDF indexing script with OCR
├── requirements.txt   # Python dependencies
├── ufo_index.db       # Pre-indexed database
├── static/
│   └── extracted_images/  # Extracted images (download from Mega)
└── templates/         # HTML templates
```

## Requirements

- Python 3.8+
- Tesseract OCR
- Flask, pymupdf, pytesseract, Pillow, pandas

## License

Declassified government documents - public domain records.