# 🔍 UFO Document Search Engine

> **Search 115 declassified UFO documents instantly** - from the latest government release at archive.war.gov/ufo

**Source:** [archive.war.gov/ufo](https://archive.war.gov/ufo) | **115+ PDFs • Full-text Search**

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Download Everything

**1A. Get the code (from GitHub)**
```bash
git clone https://github.com/jasonscompshop/ufo-search-app.git
cd ufo-search-app
```

**1B. Get the files**
- Go to: **https://archive.war.gov/ufo**
- Click "Download All" to get all PDF files
- Extract the ZIP and copy all PDF files to: `~/UFO_Files/`

Your folder should look like:
```
~/UFO_Files/65_hs1-834228961_62-hq-83894_section_9.pdf
                       dow-uap-d10-mission-report-middle-east-may-2022.pdf
                       ...
```

The repo already includes a pre-indexed database (`ufo_index.db`) with all 115 documents searchable out of the box! Skip to Step 2.

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

### No results showing
Make sure your PDFs are in `~/UFO_Files/` - the database uses filenames to link to the files.

---

## 📂 What You Get

| Item | Description |
|------|-------------|
| **115+ PDFs** | Original declassified documents |
| **Pre-indexed Search** | Database included - search immediately |
| **4,000+ Images** | Extracted & OCR'd from all pages |

---

## 🛠️ Adding Your Own PDFs

1. Put new PDF files in `~/UFO_Files/`
2. Run the indexer:
```bash
python index_pdfs.py
```
3. Restart the app:
```bash
python app.py
```

This extracts text and embedded images from all PDFs.

---

## 📊 Search Features

- ✅ Search all 115 documents instantly
- ✅ Highlighted results (see where your search terms appear)
- ✅ Browse by document
- ✅ 4,000+ images with OCR text searchable

---

## 🔐 Source

All documents from **[archive.war.gov/ufo](https://archive.war.gov/ufo)** - Latest government UFO disclosure release containing FBI files, military reports, Air Force documents, and more.

---

**Questions?** Open an issue on GitHub.

*Built with Flask + OCR + ♥*