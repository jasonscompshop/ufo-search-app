# 🔍 UFO Document Search Engine

> **Search 115 declassified UFO documents instantly** - FBI files, military reports, government correspondence, and more.

![UFO](https://img.shields.io/badge/UFO-Search-blue) ![Python](https://img.shields.io/badge/Python-Flask-green) ![Source](https://img.shields.io/badge/Source-war.gov/ufo-orange)

## 📦 Data Source

All documents sourced from [war.gov/ufo](https://war.gov/ufo) - Official declassified UFO records.

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

All documents sourced from **[war.gov/ufo](https://war.gov/ufo)** - Official declassified UFO records obtained through FOIA requests and public disclosure programs.

---

*Built with Flask, OCR, and ♥ for the UFO research community*