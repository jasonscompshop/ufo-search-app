import os
import sqlite3
import fitz  # pymupdf
import pytesseract
from PIL import Image
import re
import hashlib

# Configuration
PDF_DIR = os.path.expanduser("~/UFO_Files/")
DB_PATH = "ufo_index.db"
IMAGE_DIR = "static/extracted_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Ensure SQLite FTS5 is available
import sqlite3
sqlite3.enable_callback_tracebacks(True)

def init_database():
    """Initialize SQLite database with FTS5 support"""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    c = conn.cursor()
    
    # Drop existing tables to start fresh
    c.execute("DROP TABLE IF EXISTS images")
    c.execute("DROP TABLE IF EXISTS pages")
    c.execute("DROP TABLE IF EXISTS documents")
    
    # Create fresh tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            title TEXT,
            agency TEXT,
            date TEXT,
            doc_id TEXT,
            description TEXT,
            file_path TEXT,
            pages_total INTEGER DEFAULT 0,
            images_total INTEGER DEFAULT 0
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            page_number INTEGER,
            text_direct TEXT,
            text_ocr TEXT,
            text_combined TEXT,
            word_count INTEGER DEFAULT 0,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            page_number INTEGER,
            image_path TEXT,
            text_ocr TEXT,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        )
    """)
    
    # FTS5 virtual table - index both direct and OCR text
    c.execute("DROP TABLE IF EXISTS page_fts")
    c.execute("""
        CREATE VIRTUAL TABLE page_fts USING fts5(
            page_id UNINDEXED,
            text,
            content='pages',
            content_rowid='id'
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized (fresh start)")

def get_text_hash(text):
    """Create a quick hash to detect if text changed"""
    return hashlib.md5(text.encode()).hexdigest()[:8]

def extract_all_text_from_page(page, pdf_filename, page_num, doc_id_db, conn):
    """
    Extract text using BOTH methods:
    1. Direct text extraction (PyMuPDF)
    2. OCR of page render
    Then combine both for complete coverage
    """
    text_direct = ""
    text_ocr = ""
    
    # Method 1: Direct extraction
    try:
        text_direct = page.get_text("text").strip()
    except Exception as e:
        print(f"  ⚠️ Direct extraction failed page {page_num}: {e}")
    
    # Method 2: Always OCR every page (guarantees nothing is missed)
    try:
        # Render page at high DPI for best OCR
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save page image for reference
        safe_name = "".join(c for c in pdf_filename if c.isalnum() or c in "._- ").replace(" ", "_")
        page_img_path = os.path.join(IMAGE_DIR, f"{safe_name}_page{page_num}.png")
        img.save(page_img_path)
        
        # Run OCR
        text_ocr = pytesseract.image_to_string(img).strip()
        
    except Exception as e:
        print(f"  ⚠️ OCR failed page {page_num}: {e}")
    
    # Combine both texts (deduplicate)
    combined = text_direct
    if text_ocr:
        # If OCR found text not in direct extraction, add it
        if text_ocr not in text_direct:
            combined = text_direct + "\n\n" + text_ocr
    
    word_count = len(combined.split()) if combined else 0
    
    return text_direct, text_ocr, combined, word_count

def extract_embedded_images(page, pdf_filename, page_num, doc_id_db, conn):
    """Extract and OCR all embedded images from a page"""
    extracted_texts = []
    image_list = page.get_images(full=True)
    
    if not image_list:
        return []
    
    try:
        doc = fitz.open(os.path.join(PDF_DIR, pdf_filename))
    except Exception as e:
        print(f"  ⚠️ Could not open PDF for image extraction: {e}")
        return []
    
    for img_index, img in enumerate(image_list):
        try:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save image
            safe_filename = "".join(c for c in pdf_filename if c.isalnum() or c in "._- ").replace(" ", "_")
            img_filename = f"{safe_filename}_p{page_num}_img{img_index}.{image_ext}"
            img_path = os.path.join(IMAGE_DIR, img_filename)
            
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            
            # OCR the image
            img_ocr_text = ""
            try:
                img_obj = Image.open(io.BytesIO(image_bytes))
                img_ocr_text = pytesseract.image_to_string(img_obj).strip()
            except Exception as e:
                print(f"  ⚠️ Image OCR failed: {e}")
            
            # Save to database
            c = conn.cursor()
            c.execute("""
                INSERT INTO images (doc_id, page_number, image_path, text_ocr)
                VALUES (?, ?, ?, ?)
            """, (doc_id_db, page_num, img_path, img_ocr_text))
            
            if img_ocr_text:
                extracted_texts.append(img_ocr_text)
                
        except Exception as e:
            print(f"  ⚠️ Image extraction failed: {e}")
    
    doc.close()
    return extracted_texts

def parse_filename_for_metadata(filename):
    """Extract metadata from filename patterns"""
    name = filename.replace('.pdf', '')
    parts = name.split('_')
    
    doc_id = ""
    agency = "Unknown"
    case_number = ""
    section = ""
    
    for part in parts:
        if part.startswith('hs1-'):
            doc_id = part.replace('hs1-', '')
            agency = "HS-1"
        elif part.startswith('hq-'):
            case_number = part.replace('hq-', '')
            agency = "FBI"
        elif part.startswith('section-'):
            section = part.replace('section-', '')
        elif part.startswith('65_'):
            doc_id = part.replace('65_', '')
    
    title = name.replace('_', ' ').replace('-', ' ').title()
    return {"doc_id": doc_id, "agency": agency, "case_number": case_number, "section": section, "title": title}

def extract_pdf_metadata(pdf_path):
    """Extract metadata from PDF document properties"""
    try:
        doc = fitz.open(pdf_path)
        meta = doc.metadata
        page_count = len(doc)
        doc.close()
        return {
            "title": meta.get('title', '') or '',
            "author": meta.get('author', '') or '',
            "subject": meta.get('subject', '') or '',
            "creator": meta.get('creator', '') or '',
            "pages": page_count
        }
    except:
        return {"title": "", "author": "", "subject": "", "creator": "", "pages": 0}

def process_all_pdfs():
    """Main function to process all PDFs with complete text extraction"""
    init_database()
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    c = conn.cursor()
    
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF files\n")
    
    total_pages = 0
    total_words = 0
    
    for filename in pdf_files:
        pdf_path = os.path.join(PDF_DIR, filename)
        print(f"📄 {filename}")
        
        # Parse metadata
        filename_meta = parse_filename_for_metadata(filename)
        pdf_meta = extract_pdf_metadata(pdf_path)
        
        title = pdf_meta["title"] or filename_meta["title"]
        agency = filename_meta["agency"]
        doc_id_str = filename_meta["doc_id"]
        description = f"ID: {doc_id_str} | Case: {filename_meta['case_number']} | Section: {filename_meta['section']} | From: {pdf_meta['creator']}"
        
        # Insert document
        c.execute("""
            INSERT INTO documents (filename, title, agency, date, doc_id, description, file_path, pages_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (filename, title, agency, "", doc_id_str, description, pdf_path, pdf_meta["pages"]))
        conn.commit()
        
        # Get doc ID
        c.execute("SELECT id FROM documents WHERE filename = ?", (filename,))
        doc_id_db = c.fetchone()[0]
        
        # Open PDF
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"  ❌ Failed to open: {e}")
            continue
        
        print(f"  Pages: {len(doc)}")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_number = page_num + 1
            
            # Extract text using BOTH methods
            text_direct, text_ocr, text_combined, word_count = extract_all_text_from_page(
                page, filename, page_number, doc_id_db, conn
            )
            
            # Extract embedded images and OCR them
            img_texts = extract_embedded_images(page, filename, page_number, doc_id_db, conn)
            
            # Add image OCR text to combined
            if img_texts:
                img_combined = " ".join(img_texts)
                if img_combined not in text_combined:
                    text_combined = text_combined + "\n" + img_combined
                word_count += len(img_combined.split())
            
            # Save page to database
            c.execute("""
                INSERT INTO pages (doc_id, page_number, text_direct, text_ocr, text_combined, word_count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (doc_id_db, page_number, text_direct, text_ocr, text_combined, word_count))
            
            # Get page ID and add to FTS
            c.execute("SELECT id FROM pages WHERE doc_id = ? AND page_number = ?", (doc_id_db, page_number))
            page_id = c.fetchone()[0]
            
            c.execute("INSERT INTO page_fts (page_id, text) VALUES (?, ?)", (page_id, text_combined))
            
            total_words += word_count
        
        page_count = len(doc)
        doc.close()
        conn.commit()
        
        total_pages += page_count
        print(f"  ✅ {page_count} pages | {total_words} words | Images: {c.execute('SELECT COUNT(*) FROM images WHERE doc_id = ?', (doc_id_db,)).fetchone()[0]}\n")
    
    conn.close()
    
    print("\n" + "="*50)
    print("✅ INDEXING COMPLETE")
    print("="*50)
    print(f"📄 Documents: {len(pdf_files)}")
    print(f"📑 Total Pages: {total_pages}")
    print(f"📝 Total Words Indexed: {total_words:,}")
    
    # Verify search works
    print("\n🔍 Testing search index...")
    verify_search()

def verify_search():
    """Verify the FTS index is working"""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    c = conn.cursor()
    
    # Test 1: Simple word search
    test_words = ["the", "and", "report", "document"]
    
    for word in test_words:
        c.execute("""
            SELECT COUNT(*) as cnt FROM page_fts WHERE text MATCH ?
        """, (word,))
        count = c.fetchone()[0]
        print(f"  '{word}' found in {count:,} pages")
    
    # Test 2: Multi-word search
    c.execute("""
        SELECT COUNT(*) FROM page_fts WHERE text MATCH 'unidentified aerial'
    """)
    multi_count = c.fetchone()[0]
    print(f"  'unidentified aerial' found in {multi_count:,} pages")
    
    # Test 3: Sample results
    c.execute("""
        SELECT p.text_combined, d.filename, p.page_number
        FROM page_fts f
        JOIN pages p ON f.page_id = p.id
        JOIN documents d ON p.doc_id = d.id
        WHERE page_fts MATCH 'ufo'
        LIMIT 3
    """)
    results = c.fetchall()
    
    if results:
        print(f"\n  🔎 Sample 'ufo' search results:")
        for i, (text, fname, pnum) in enumerate(results, 1):
            preview = text[:150] + "..." if text and len(text) > 150 else (text or "No text")
            print(f"    {i}. {fname} (page {pnum}): {preview[:80]}...")
    
    conn.close()
    print("\n✅ Search index is ready!")

if __name__ == "__main__":
    import io  # Added for image handling
    process_all_pdfs()