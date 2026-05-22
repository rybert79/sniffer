import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import time
import re
from urllib.parse import urlparse
from ddgs import DDGS
from concurrent.futures import ThreadPoolExecutor, as_completed

# kata kunci situs slot
SIGNATURES = {
    "gacor": 30,
    "slot": 25,
    "deposit pulsa": 20,
    "wd instan": 20,
    "maxwin": 30,
    "bandar online": 15
}

TOTAL_MAX_SCORE = sum(SIGNATURES.values())

def save_to_db(url, title, score):
    """Fungsi menyimpan data ke DB (SQLite aman digunakan dengan banyak thread)"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'judol_archive.db')
    
    # 1. Penerapan Sensor (Defanging) URL sebelum masuk ke database publik
    defanged_url = url.replace("http://", "hxxp://").replace("https://", "hxxps://")
    parts = defanged_url.split('/')
    if len(parts) > 2:
        domain = parts[2]
        if len(domain) > 5:
            # Sensor bagian tengah domain (misal: websitegacor.com -> web****cor.com)
            censored_domain = domain[:3] + "****" + domain[-4:]
            defanged_url = defanged_url.replace(domain, censored_domain)
            
    # 2. Penerapan Sensor Judul Situs (Title Scrubbing) berdasarkan kata kunci SIGNATURES
    censored_title = title
    for keyword in SIGNATURES.keys():
        if keyword in censored_title.lower():
            # Cari kata sensitif tanpa pandang huruf besar/kecil lalu samarkan menjadi ****
            insens_keyword = re.compile(re.escape(keyword), re.IGNORECASE)
            censored_title = insens_keyword.sub("****", censored_title)
            
    # timeout=20 dipasang agar jika banyak thread mengantre menulis ke DB, tidak terjadi error 'database is locked'
    conn = sqlite3.connect(db_path, timeout=20)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO suspects (url, site_title, confidence_score) VALUES (?, ?, ?)",
            (defanged_url, censored_title, score)
        )
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

def scan_single_url(index, total, url):
    """Fungsi yang akan dieksekusi oleh setiap thread untuk mengecek satu website"""
    parsed_domain = urlparse(url).netloc

    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        # Timeout ketat (4 detik) wajib dipasang agar bot tidak macet menunggu website yang lemot
        response = requests.get(url, headers=headers, timeout=4)
        
        if 'text/html' not in response.headers.get('Content-Type', ''):
            return

        html_content = response.text.lower()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
        
        current_score = 0
        for keyword, weight in SIGNATURES.items():
            if keyword in html_content:
                current_score += weight
                
        match_percentage = round((current_score / TOTAL_MAX_SCORE) * 100)
        
        if match_percentage >= 25:
            save_to_db(url, title, match_percentage)
            # ubah line dibawah menjadi print(f"    [!] POSITIF [{match_percentage}%] -> {parsed_domain}") untuk mereveal link 
            print(f"    [!] POSITIF [{match_percentage}%] -> ********")
        # hapus comment line 97 untuk pemberitahuan yang lebih detail dn hapus line 96 secara menyeluruh
        else:
            pass

    except Exception:
        a = 1
        #print(f"    [x] OFFLINE -> {parsed_domain}")

if __name__ == "__main__":
    print("[*] ====================================================== [*]")
    print("[*]              SNIFFER rybert edition                    [*]")
    print("[*] ====================================================== [*]")
    
    # Kita kumpulkan target dalam jumlah banyak dari beberapa kata kunci sekaligus
    kata_kunci_list = [
        "slot gacor deposit pulsa",
        "link alternatif slot resmi",
        "bandar slot maxwin terbaru",
        "togel online",
        "agen judi bola",
        "judi slot",
        "olympus",
        "zeus",
        "taruhan"
    ]
    
    targets = []
    print("Mengumpulkan target dari DuckDuckGo")
    
    try:
        with DDGS() as ddgs:
            for kw in kata_kunci_list:
                # Ambil 40 hasil per kata kunci agar total target mendekati atau lebih dari 100
                results = ddgs.text(kw, max_results=40)
                for r in results:
                    url_asli = r.get('href')
                    if url_asli:
                        parsed_url = urlparse(url_asli)
                        index_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
                        
                        domain_name = parsed_url.netloc.lower()
                        # banned website yang sudah jelas bukan situs slot
                        banned_domains = ["google", "facebook", "duckduckgo", "instagram", "twitter", "linkedin", "youtube", "wikipedia", "github", "quora", "reddit", "scribd", "x", "pixabay", "wikihow", "bing"]
                        if not any(x in domain_name for x in banned_domains):
                            if index_url not in targets:
                                targets.append(index_url)
    except Exception as e:
        print(f"[-] Kendala pengumpulan target: {e}")

    total_urls = len(targets)
    print(f"\nBerhasil mengamankan total {total_urls} target unik.")
    
    # menentukan jumlh worker. aku pilih 50 soalnya laptopku low end
    max_workers = min(50, total_urls) 
    print(f"Meluncurkan {max_workers} Thread Worker Sekaligus...\n")

    # Proses eksekusi massal menggunakan ThreadPool
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Daftarkan semua tugas scan ke dalam antrean executor
        futures = [
            executor.submit(scan_single_url, i, total_urls, url) 
            for i, url in enumerate(targets, 1)
        ]
        
        # Tunggu sampai semua pekerja selesai bekerja
        for future in as_completed(futures):
            pass

    end_time = time.time()
    print("\nPemindaian Selesai!")
    print(f"Total Waktu Eksekusi: {round(end_time - start_time, 2)} detik untuk {total_urls} website.")
    print("Silakan periksa dashboard. jalankan app.py dan 'localhost:5000' di browser ")