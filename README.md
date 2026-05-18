# 🔍 UFO Document Search

war.gov/ufo

Includes a pre-indexed database (`ufo_index.db`) with all 115 documents searchable out of the box!

---

### Step 1: Download Everything

**1A. Get the code
```bash
git clone https://github.com/jasonscompshop/ufo-search-app.git
cd ufo-search-app
```

**1B. Get the files
- Go to: **https://war.gov/ufo
- Click "Download All" to get all PDF files
- Extract the ZIP and copy all PDF files to: `~/UFO_Files/`

Your folder should look like:
```
~/UFO_Files/65_hs1-834228961_62-hq-83894_section_9.pdf
                       dow-uap-d10-mission-report-middle-east-may-2022.pdf
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
