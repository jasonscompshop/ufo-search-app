# 🔍 UFO Document Search Engine

> **Search 115 declassified UFO documents instantly** - FBI files, military reports, government correspondence, and more.

**Source:** [war.gov/ufo](https://war.gov/ufo) | **License:** Public Domain

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Download Everything

**1A. Get the code (from GitHub)**
```bash
git clone https://github.com/jasonscompshop/ufo-search-app.git
cd ufo-search-app
```

**1B. Get the images (from Mega)**
- Go to: **https://mega.nz/folder/fOxmiSyB#UubvIy6_ncbz1YleY33jvA**
- Download the `extracted_images` folder
- Place it inside: `ufo-search-app/static/extracted_images/`

Your folder should look like:
```
ufo-search-app/static/extracted_images/0001.jpg
                                         0002.jpg
                                         ...
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Tesseract OCR

| Your Computer | Command to Run |
|---------------|----------------|
| **Mac** | `brew install tesseract` |
| **Windows** | [Download installer](https://github.com/UB-Mannheim/tesseract/wiki) then run it |
| **Linux** | `sudo apt install tesseract-ocr` |

### Step 4: Run the App

```bash
python app.py
```

### Step 5: Open Your Browser

Go to: **http://localhost:5000**

That's it! 🎉

---

## 📱 Access From Other Devices

Want to view it on your phone or other computer?

**1. Find your IP address:**
```bash
# Mac/Linux:
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows:
ipconfig
```

**2. On the other device, go to:**
```
http://YOUR_IP:5000
```

Example: If your IP is `192.168.1.100`, then go to `http://192.168.1.100:5000`

---

## 🔧 Troubleshooting

### "pip: command not found"
```bash
python3 -m pip install -r requirements.txt
```

### "Tesseract not found"
Make sure you installed Tesseract and restarted your terminal.

### "Port 5000 is already in use"
```bash
python app.py --port 5001
```
Then go to `http://localhost:5001`

### Images not showing
Make sure the `extracted_images` folder is in:
```
ufo-search-app/static/extracted_images/
```

---

## 📂 What You Get

| Item | Description |
|------|-------------|
| **115 PDFs** | Original declassified documents |
| **4000+ Images** | Extracted from all pages |
| **Pre-indexed Search** | Instant full-text search |
| **OCR Text** | Searchable text from images |

---

## 🛠️ Adding Your Own PDFs

1. Put new PDF files in `~/UFO_Files/`
2. Run:
```bash
python index_pdfs.py
```
3. Restart the app:
```bash
python app.py
```

---

## 📊 Search Features

- ✅ Search all 115 documents
- ✅ Highlighted results (see where your search terms appear)
- ✅ Click images to view full-size
- ✅ Browse by document
- ✅ Image OCR search

---

## 🔐 Source

All documents from [war.gov/ufo](https://war.gov/ufo) - Official declassified UFO records.

---

**Questions?** Open an issue on GitHub.

*Built with Flask + OCR + ♥*