# GACOR-SNIFFER
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white) 
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white) 
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38BDF8?style=for-the-badge&logo=tailwind-css&logoColor=white) 
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

GACOR-SNIFFER adalah sistem otomatisasi berbasis Python yang dirancang untuk mendeteksi, menganalisis, dan mengarsipkan replikasi template situs web mencurigakan (khususnya indikasi judi online) di internet secara *real-time*. Sistem ini mengintegrasikan mesin pencari publik untuk pengumpulan target secara dinamis dan memproses pemindaian massal menggunakan arsitektur *Multi-Threading*.

Proyek ini dikembangkan sebagai inovasi teknologi dalam mendukung Keamanan Siber pada **Hackathon vinco(2026)**.

---

## 🎯 Tujuan Pengembangan Proyek

Proyek ini diinisialisasi dan dikembangkan dengan tujuan strategis sebagai berikut:
1. **Inovasi cyber-security:** Menjadi solusi teknologi preventif dalam membantu pihak berwenang melakukan pemetaan (*mapping*) dan pengawasan dini terhadap penyebaran situs web ilegal yang merugikan masyarakat.
2. **Skalabilitas Pemantauan:** Membuktikan bahwa pemindaian open-source berbasis intelijen (OSINT) dapat dilakukan secara cepat, efisien, dan ramah sumber daya tanpa ketergantungan pada API berbayar yang kaku.
3. **Riset & Edukasi Keamanan Siber:** Sebagai media pembelajaran arsitektur pemrograman pararel (*multi-threading*), analisis heuristik konten web, serta integrasi sistem pangkalan data relasional terdistribusi.

---

## ⚠️ PERINGATAN PENGGUNAAN & DISCLAIMER

> **PENTING untuk Diperhatikan:**
> 
> 1. **Keperluan Akademis:** Alat ini dibuat murni untuk keperluan riset, partisipasi perlombaan Hackathon, dan analisis forensik digital defensif.
> 2. **Kepatuhan Hukum:** Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini untuk aktivitas pemindaian agresif atau tanpa izin (*unauthorized scanning*) yang melanggar hukum siber setempat atau apapun itu yang melanggar hukum (seperti UU ITE di Indonesia).
> 3. **Etika Jaringan:** Sistem ini telah dilengkapi pembatas kecepatan (*rate-limiting*) internal guna menghormati performa server target serta mematuhi batas wajar penggunaan jaringan (*fair use*).

---

## 💻 Informasi Dependensi Library

Proyek ini dibangun menggunakan beberapa pustaka (library) eksternal Python dengan fungsionalitas spesifik sebagai berikut:

| Library | Fungsi Utama dalam Sistem |
| :--- | :--- |
| **`duckduckgo_search` (DDGS)** | Bertindak sebagai radar penjelajah otomatis (*OSINT crawler*) untuk mengumpulkan tautan URL live terupdate dari mesin pencari tanpa hambatan proteksi Captcha. |
| **`requests`** | Mengalirkan permintaan HTTP/HTTPS ke server target untuk mengunduh kode sumber (source code) halaman web secara asinkron. |
| **`beautifulsoup4` (bs4)** | Membedah struktur dokumen HTML target guna mengekstrak elemen penting seperti judul halaman (*site title*). |
| **`Flask`** | Berperan sebagai micro-framework backend untuk membangun server lokal dan menyajikan antarmuka visual dashboard pemantauan. |
| **`sqlite3`** *(Bawaan Python)* | Mengelola pangkalan data relasional lokal secara efisien dan mendukung isolasi transaksi saat terjadi penulisan data massal (*Thread-Safe Lock*). |
| **`concurrent.futures`** *(Bawaan Python)* | Menyediakan modul `ThreadPoolExecutor` untuk mengelola worker pararel (*multi-threading*) agar pemindaian berjalan berlipat-lipat lebih cepat. |

---

## 🛠️ Panduan Instalasi & Prasyarat

Pastikan sistem operasi Anda sudah terpasang Python 3.x. Jalankan perintah berikut untuk memasang seluruh dependensi secara massal:

```bash
pip install requests beautifulsoup4 flask ddgs
```

jalankah perintah untuk membuat database

```bash
python database.py
```
lakukan pengambilan website

```bash
python collector.py
```
