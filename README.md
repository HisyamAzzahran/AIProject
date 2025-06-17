# LuxDraw: Media Belajar Matematika dengan Computer Vision

![Poster Project AI](https://raw.githubusercontent.com/HisyamAzzahran/AIProject/main/Poster%20Project%20AI.jpg)

**Inovasi Teknologi Computer Vision dengan mengintegrasikan Optical Character Recognition (OCR) dan Convolutional Neural Networks (CNN) sebagai teman belajar matematika anak.**

| **Status Proyek** | **Tautan** |
| :--- | :--- |
| **Status** | `Prototype Development` |
| **Repositori** | **[HisyamAzzahran/AIProject](https://github.com/HisyamAzzahran/AIProject)** |

<br>

## 🎯 Latar Belakang & Masalah

Kenyataan di lapangan menunjukkan tantangan besar dalam pendidikan matematika di Indonesia.

* **Skor PISA Rendah**: Skor PISA matematika Indonesia berada di angka **379**, menempatkan kita di **10 besar terbawah** (PISA, 2018).
* **Kompetensi Dasar Kurang**: Hanya **19%** siswa yang memiliki kompetensi matematika dasar (World Bank, 2020).
* **Media Belajar Monoton**: Banyak media pembelajaran yang ada bersifat satu arah dan kurang menarik, membuat siswa cepat bosan.

**Rumusan Masalah:** Bagaimana strategi Indonesia untuk menerapkan kurikulum K-12 secara efektif jika fondasi matematika dasar siswa masih lemah?

**LuxDraw** hadir sebagai solusi untuk menyediakan media pembelajaran digital yang **interaktif, menyenangkan, dan sejalan dengan kurikulum** untuk membangun fondasi matematika yang kuat sejak dini.

<br>

## ✨ Konsep & Keunggulan Produk

#### Konsep Gagasan
LuxDraw dirancang dengan sistem bimbingan sederhana yang intuitif. Pada tahap purwarupa (prototype) ini, sistem menggunakan **EasyOCR** untuk pengenalan angka, dengan rencana pengembangan lebih lanjut untuk mengintegrasikan logika **Convolutional Neural Network (CNN)** untuk akurasi yang lebih tinggi.

#### Keunggulan Utama
-   **👨‍💻 Open Source**: Dibangun dengan teknologi sumber terbuka yang dapat dikembangkan oleh siapa saja.
-   **👍 Mudah Digunakan**: Antarmuka yang ramah pengguna, dirancang khusus untuk anak-anak.
-   **⚡ Praktis & Efisien**: Media belajar digital yang dapat diakses kapan saja dan di mana saja.

<br>

## ⚙️ Alur Kerja Sistem

**Input Pengguna (Menggambar di Canvas)** → **Pengambilan Frame Gambar (OpenCV & WebRTC)** → **Pra-pemrosesan Gambar (Grayscale, Threshold, Cropping)** → **Inferensi Model OCR (EasyOCR)** → **Ekstraksi Hasil (Teks Angka & Skor Keyakinan)** → **Logika Aplikasi (Validasi Jawaban)** → **Umpan Balik Visual (Update Streamlit UI)**

<br>

## 🧠 Metode AI yang Digunakan

Proyek LuxDraw mengimplementasikan beberapa metode inti dalam bidang **Computer Vision** dan **Deep Learning** untuk mencapai fungsionalitasnya. Berikut adalah rinciannya:

* **Computer Vision (CV)**
    Sebagai fondasi utama, proyek ini menerapkan Computer Vision untuk memungkinkan aplikasi "melihat" dan menginterpretasikan gambar dari input tulisan tangan pengguna secara _real-time_. Seluruh proses, dari pengambilan gambar hingga analisis, berada dalam domain CV.

* **Optical Character Recognition (OCR)**
    Ini adalah metode inti yang digunakan dalam purwarupa saat ini. Kami memanfaatkan *engine* OCR, yaitu **EasyOCR**, untuk mendeteksi dan mengenali karakter angka yang digambar pengguna pada kanvas. Proses ini mengubah data piksel gambar menjadi data teks (`'0'`, `'1'`, `'2'`, dst.) yang dapat diproses oleh logika program.

<br>

## 🛠️ Teknologi & Struktur Proyek

Proyek ini dibangun menggunakan serangkaian teknologi modern di bidang Computer Vision dan pengembangan web.

| Kategori | Teknologi yang Digunakan |
| :--- | :--- |
| **Bahasa & Framework** | `Python`, `Streamlit`, `Streamlit-WebRTC` |
| **Computer Vision** | `OpenCV`, `MediaPipe`, `EasyOCR` |

<br>

#### Struktur Folder Proyek
Berikut adalah arsitektur folder dari proyek LuxDraw:
```sh
AIProject/
├── assets/
│   icons/
│   output/
├── scripts/
│   └── drawing_logic.py
├── .gitignore
├── app.py
├── Poster Project AI.jpg
├── README.md
└── requirements.txt
```

<br>

## 🚀 Instalasi & Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputer Anda.

1.  **Clone repository:**
    ```sh
    git clone https://github.com/HisyamAzzahran/AIProject.git
    cd AIProject
    ```

2.  **Install semua dependensi yang dibutuhkan:**
    ```sh
    pip install -r requirements.txt
    ```

3.  **Jalankan aplikasi Streamlit:**
    ```sh
    streamlit run app.py
    ```
    Aplikasi akan berjalan secara lokal di **`http://localhost:8501`**.

<br>