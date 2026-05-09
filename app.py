import os
import sqlite3
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import urllib.parse

app = Flask(__name__)
PDF_DIR = os.path.expanduser("~/UFO_Files/")
DB_PATH = "ufo_index.db"
IMAGE_DIR = "static/extracted_images"
STATIC_DIR = "static"

app = Flask(__name__, static_folder=STATIC_DIR)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db()
    dates = conn.execute("SELECT DISTINCT date FROM documents WHERE date != '' ORDER BY date DESC").fetchall()
    
    doc_count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    page_count = conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
    img_count = conn.execute("SELECT COUNT(*) FROM images").fetchone()[0]
    
    conn.close()
    return render_template("home.html", dates=dates, 
                           doc_count=doc_count, page_count=page_count, img_count=img_count)

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    
    conn = get_db()
    
    try:
        all_results = []
        
        if query:
            safe_query = query.replace('"', ' ').replace("'", " ").replace("*", " ")
            
            # Search pages
            sql_pages = """
                SELECT 
                    d.filename, d.title, d.agency, d.date, d.description,
                    p.page_number, COALESCE(p.text_combined, p.text_direct, '') as page_text, p.id as page_id,
                    NULL as image_path, 'page' as result_type,
                    CASE WHEN COALESCE(p.text_combined, p.text_direct, '') LIKE '%' || ? || '%' THEN 1 ELSE 0 END as relevance
                FROM pages p
                JOIN documents d ON p.doc_id = d.id
                WHERE (p.text_combined LIKE '%' || ? || '%' OR p.text_direct LIKE '%' || ? || '%')
                ORDER BY relevance DESC, d.filename, p.page_number
            """
            pages_results = conn.execute(sql_pages, [safe_query, safe_query, safe_query]).fetchall()
            all_results.extend(pages_results)
            
            # Search images OCR text
            sql_images = """
                SELECT 
                    d.filename, d.title, d.agency, d.date, d.description,
                    i.page_number, COALESCE(i.text_ocr, '') as page_text, i.id as page_id,
                    i.image_path, 'image' as result_type,
                    CASE WHEN COALESCE(i.text_ocr, '') LIKE '%' || ? || '%' THEN 1 ELSE 0 END as relevance
                FROM images i
                JOIN documents d ON i.doc_id = d.id
                WHERE i.text_ocr LIKE '%' || ? || '%' AND i.text_ocr IS NOT NULL AND i.text_ocr != ''
                ORDER BY relevance DESC, d.filename, i.page_number
            """
            img_results = conn.execute(sql_images, [safe_query, safe_query]).fetchall()
            all_results.extend(img_results)
            
            all_results.sort(key=lambda x: (-x["relevance"], x["filename"], x["page_number"]))
        else:
            # No query - show pages alphabetically
            sql_all = """
                SELECT 
                    d.filename, d.title, d.agency, d.date, d.description,
                    p.page_number, COALESCE(p.text_combined, p.text_direct, '') as page_text, p.id as page_id,
                    NULL as image_path, 'page' as result_type, 0 as relevance
                FROM pages p
                JOIN documents d ON p.doc_id = d.id
                ORDER BY d.filename, p.page_number
            """
            all_results = conn.execute(sql_all).fetchall()
            
            # Also include images in the default browse
            sql_images_all = """
                SELECT 
                    d.filename, d.title, d.agency, d.date, d.description,
                    i.page_number, COALESCE(i.text_ocr, '') as page_text, i.id as page_id,
                    i.image_path, 'image' as result_type, 0 as relevance
                FROM images i
                JOIN documents d ON i.doc_id = d.id
                ORDER BY d.filename, i.page_number
            """
            img_results = conn.execute(sql_images_all).fetchall()
            all_results.extend(img_results)
        
        conn.close()
        
        output = []
        seen = set()
        for row in all_results:
            key = f"{row['filename']}_{row['page_number']}"
            if key in seen:
                continue
            seen.add(key)
                
            page_text = row["page_text"] or ""
            
            if query and page_text:
                lower_text = page_text.lower()
                lower_query = safe_query.lower()
                pos = lower_text.find(lower_query)
                if pos >= 0:
                    start = max(0, pos - 80)
                    end = min(len(page_text), pos + len(query) + 80)
                    preview = ("..." if start > 0 else "") + page_text[start:end] + ("..." if end < len(page_text) else "")
                else:
                    preview = page_text[:200] + "..." if len(page_text) > 200 else page_text
            else:
                preview = page_text[:200] + "..." if len(page_text) > 200 else page_text
            
            if query:
                for word in safe_query.split():
                    if word:
                        preview = preview.replace(word, f"<mark>{word}</mark>")
                        preview = preview.replace(word.lower(), f"<mark>{word.lower()}</mark>")
                        preview = preview.replace(word.upper(), f"<mark>{word.upper()}</mark>")
            
            item = {
                "filename": row["filename"],
                "title": row["title"],
                "agency": row["agency"],
                "date": row["date"],
                "page_number": row["page_number"],
                "preview": preview,
                "pdf_url": f"/pdf/{row['filename']}",
                "result_type": row["result_type"]
            }
            
            if row["image_path"]:
                item["image_path"] = row["image_path"]
            
            output.append(item)
        
        return jsonify(output)
        
    except Exception as e:
        print(f"Search error: {e}")
        conn.close()
        return jsonify([])

@app.route("/pdf/<filename>")
def serve_pdf(filename):
    safe_filename = os.path.basename(filename)
    pdf_path = os.path.join(PDF_DIR, safe_filename)
    if not os.path.exists(pdf_path):
        return "PDF not found", 404
    return send_file(pdf_path, mimetype="application/pdf")

@app.route("/file/<filename>")
def view_file(filename):
    conn = get_db()
    doc = conn.execute("SELECT * FROM documents WHERE filename = ?", (filename,)).fetchone()
    if not doc:
        return render_template("file.html", doc=None, pages=[], images=[])
    
    pages = conn.execute("SELECT * FROM pages WHERE doc_id = ? ORDER BY page_number", (doc["id"],)).fetchall()
    images = conn.execute("SELECT * FROM images WHERE doc_id = ? ORDER BY page_number", (doc["id"],)).fetchall()
    conn.close()
    
    return render_template("file.html", doc=doc, pages=pages, images=images)

@app.route("/images")
def browse_images():
    conn = get_db()
    
    # Get stats
    total_docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    total_pages = conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
    total_images = conn.execute("SELECT COUNT(*) FROM images").fetchone()[0]
    
    # Get all images with their OCR text
    images = conn.execute("""
        SELECT i.*, d.filename, d.title 
        FROM images i
        JOIN documents d ON i.doc_id = d.id
        ORDER BY d.filename, i.page_number
    """).fetchall()
    conn.close()
    return render_template("images.html", images=images, 
                           total_docs=total_docs, total_pages=total_pages, total_images=total_images)

@app.route("/search-images")
def search_images():
    """Search specifically in image OCR text"""
    query = request.args.get("q", "").strip()
    
    if not query:
        return jsonify([])
    
    conn = get_db()
    results = conn.execute("""
        SELECT i.*, d.filename, d.title
        FROM images i
        JOIN documents d ON i.doc_id = d.id
        WHERE i.text_ocr LIKE ? AND i.text_ocr IS NOT NULL AND i.text_ocr != ''
        ORDER BY d.filename, i.page_number
    """, (f"%{query}%",)).fetchall()
    conn.close()
    
    output = []
    for row in results:
        preview = (row["text_ocr"] or "")[:200] + "..." if row["text_ocr"] and len(row["text_ocr"]) > 200 else (row["text_ocr"] or "No text")
        for word in query.split():
            preview = preview.replace(word, f"<mark>{word}</mark>")
        
        output.append({
            "image_path": row["image_path"],
            "filename": row["filename"],
            "page_number": row["page_number"],
            "preview": preview,
            "text_ocr": row["text_ocr"]
        })
    
    return jsonify(output)

@app.route("/extracted_images/<path:filename>")
def serve_extracted_image(filename):
    """Serve images from extracted_images directory"""
    return send_from_directory("static/extracted_images", filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)