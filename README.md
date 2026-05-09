# 🔍 UFO Document Search Engine

> **Search 115 declassified UFO documents instantly** - FBI files, military reports, government correspondence, and more.

![UFO](https://img.shields.io/badge/UFO-Search-blue) ![Python](https://img.shields.io/badge/Python-Flask-green) ![License](https://img.shields.io/badge/License-Public%20Domain-red)

## 🚀 Download Everything

This repo contains **everything you need** - just two downloads:

| File | Size | Download |
|------|------|----------|
| **All Files (code + PDFs + database)** | ~2.5 GB | `git clone` this repo |
| **Extracted Images (4000+)** | ~19 GB | [Download from Mega](https://mega.nz/folder/fOxmiSyB#UubvIy6_ncbz1YleY33jvA) |

### Quick Setup (5 minutes)

```bash
# 1. Clone this repo
git clone https://github.com/jasonscompshop/ufo-search-app.git
cd ufo-search-app

# 2. Download images from Mega
#    Go to: https://mega.nz/folder/fOxmiSyB#UubvIy6_ncbz1YleY33jvA
#    Download the extracted_images folder
#    Place it in: static/extracted_images/

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Tesseract OCR (required for text extraction)
#    Mac:     brew install tesseract
#    Windows: https://github.com/UB-Mannheim/tesseract/wiki
#    Linux:   sudo apt install tesseract-ocr

# 5. Run!
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## 📁 What's Included

### Documents (115 PDFs - 2.2 GB)
- FBI case files and memos
- Air Force incident reports
- Military radar observations
- Congressional correspondence
- NASA astronaut debriefings
- Declassified CIA/FBI documents

### Search Features
- ✅ Full-text search across ALL documents
- ✅ OCR text from scanned pages
- ✅ Image search with extracted text
- ✅ Highlighted search results
- ✅ Click images to view full-size

### Technical
- **Flask** web application
- **SQLite** database (pre-indexed)
- **pytesseract** for OCR
- **pymupdf** for PDF processing

---

## 🛠️ Setup Requirements

| Requirement | Installation |
|-------------|--------------|
| Python 3.8+ | [python.org](https://python.org) |
| Tesseract OCR | [Install Guide](https://github.com/tesseract-ocr/tesseract) |
| pip packages | `pip install -r requirements.txt` |

---

## 🌐 Network Access

Access from other devices on your network:

```bash
# Find your IP
ifconfig | grep "inet " | grep -v 127.0.0.1

# Connect from other devices
http://YOUR_IP:5000
```

---

## 📊 Stats

- **115** documents
- **3,960** pages indexed
- **4,000+** images extracted
- **1.5M+** words searchable

---

## 📂 Project Structure

```
ufo-search-app/
├── PDFs/                    # All 115 original PDFs
├── app.py                  # Flask web app
├── index_pdfs.py           # PDF indexing script
├── requirements.txt        # Python dependencies
├── ufo_index.db            # Pre-indexed database
├── static/
│   └── extracted_images/    # Download separately from Mega
└── templates/               # HTML interface
```

---

## 🔐 Source

All documents are **official declassified government records** obtained through FOIA requests and public disclosure programs.

---

*Built with Flask, OCR, and ♥ for the UFO research community*