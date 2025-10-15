
# BlurFace Recorder

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistem Pemburaman Wajah Realtime Berbasis Web**

BlurFace Recorder adalah aplikasi web yang mampu melakukan deteksi dan pemburaman wajah secara realtime untuk melindungi privasi individu pada saat perekaman atau transmisi video secara langsung.

---

## 📋 Deskripsi

BlurFace Recorder merupakan implementasi sinergi antara frontend web technologies dan computer vision backend berbasis Flask dan OpenCV. Sistem ini dirancang untuk memproses video secara realtime guna mendeteksi serta memburamkan wajah pengguna, dengan tetap menjaga privasi dan tanpa menyimpan data di server.

---

## 🏗️ Arsitektur Sistem

Sistem ini dibangun dengan arsitektur **client-server**:

### Frontend (Client)
- **Teknologi**: HTML, CSS, JavaScript
- **Fungsi**: 
  - Mengakses kamera pengguna melalui Web API (`getUserMedia()`)
  - Menangkap frame video secara berkala
  - Mengirim frame ke server untuk diproses
  - Menampilkan hasil pemburaman wajah secara realtime

### Backend (Server)
- **Framework**: Python Flask
- **Library**: OpenCV
- **Fungsi**:
  - Menerima frame dari client
  - Melakukan deteksi wajah
  - Menerapkan efek blur pada area wajah
  - Mengembalikan hasil ke client

### Komunikasi Data
- **Protokol**: HTTP POST
- **Format**: JSON dengan payload base64-encoded image
- **Endpoint**: `/process_frame`

---

## 🔄 Alur Kerja Sistem

```
1. Browser meminta akses kamera → Pengguna memberikan izin
2. JavaScript mengambil frame dari video → Konversi ke base64
3. Kirim frame ke Flask server melalui HTTP POST
4. Server: Decode base64 → Deteksi wajah (OpenCV) → Blur area wajah
5. Server: Encode hasil ke base64 → Kirim kembali ke client
6. Browser: Tampilkan frame hasil blur secara realtime
```

---

## ✨ Fitur

- ✅ **Deteksi Wajah Realtime** menggunakan Haar Cascade atau DNN
- ✅ **Pemburaman Otomatis** pada area wajah yang terdeteksi
- ✅ **Berbasis Web** - tidak perlu instalasi aplikasi desktop
- ✅ **Privacy-Focused** - tidak menyimpan data di server
- ✅ **Multi-Platform** - berjalan di browser modern
- ✅ **Responsive Interface** - dapat digunakan di berbagai perangkat

---

## 🛠️ Teknologi yang Digunakan

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **OpenCV** - Computer vision library untuk deteksi dan pemburaman wajah
- **NumPy** - Manipulasi array dan data gambar

### Frontend
- **HTML5** - Struktur halaman
- **CSS3** - Styling dan responsiveness
- **JavaScript (ES6+)** - Logic dan komunikasi dengan backend
- **Canvas API** - Pengambilan dan rendering frame video

---

## 🚀 Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Webcam/kamera yang terhubung ke perangkat

### Langkah Instalasi

1. **Clone repository**
```bash
git clone https://github.com/XeDiaulhaq/BlurFace-Recorder.git
cd BlurFace-Recorder
```

2. **Buat virtual environment (opsional tapi direkomendasikan)**
```bash
python -m venv venv
source venv/bin/activate  # untuk Linux/Mac
# atau
venv\Scripts\activate  # untuk Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download Haar Cascade model (jika belum tersedia)**
```bash
# Model biasanya sudah tersedia di OpenCV
# Atau download manual dari:
# https://github.com/opencv/opencv/tree/master/data/haarcascades
```

---

## 💻 Cara Penggunaan

1. **Jalankan Flask server**
```bash
python app.py
```

2. **Buka browser**
```
http://localhost:5000
```

3. **Izinkan akses kamera**
   - Browser akan meminta izin akses kamera
   - Klik "Allow" atau "Izinkan"

4. **Mulai recording**
   - Wajah akan otomatis terdeteksi dan diburamkan
   - Hasil ditampilkan secara realtime di layar

---

## 🔬 Metode Deteksi Wajah

### Haar Cascade Classifier
- ✅ **Kelebihan**: Ringan, cepat, cocok untuk perangkat low-spec
- ⚠️ **Kekurangan**: Kurang akurat pada pencahayaan ekstrem

### DNN (Deep Neural Network)
- ✅ **Kelebihan**: Lebih akurat, tahan terhadap variasi sudut wajah
- ⚠️ **Kekurangan**: Membutuhkan daya komputasi lebih besar

---

## 🎨 Teknik Pemburaman

### 1. Gaussian Blur (Default)
- Efek halus dan natural
- Menggunakan `cv2.GaussianBlur()`

### 2. Pixelation (Block Blur)
- Efek "mosaic" atau blok-blok besar
- Menurunkan resolusi lokal

### 3. Median/Box Blur
- Efek seragam
- Lebih ringan dibanding Gaussian

---
## 🎯 Tujuan Proyek

1. Membangun sistem berbasis web yang mampu melakukan pemburaman wajah secara realtime
2. Melindungi privasi individu pada saat perekaman atau transmisi video
3. Implementasi nyata dari penggabungan teknologi computer vision dan web programming

---

## 💡 Manfaat

- 🎥 **Pembuatan Konten**: Menjaga privasi subjek dalam video
- 🔒 **Sistem Pemantauan**: Anonimisasi wajah dalam CCTV publik
- 📰 **Wawancara Anonim**: Melindungi identitas narasumber
- 💼 **Konferensi Video**: Privasi dalam meeting online

---

## ⚠️ Batasan Sistem

1. **Ketergantungan Jaringan**: Performa bergantung pada kualitas jaringan
2. **Frame Rate Terbatas**: Proses melalui HTTP dan base64 encoding
3. **Kondisi Pencahayaan**: Deteksi bisa gagal pada pencahayaan rendah
4. **Sudut Wajah**: Kesulitan mendeteksi wajah dengan sudut ekstrem
5. **Multi-Wajah**: Memerlukan optimasi tambahan untuk banyak wajah

---

## 📝 Requirements

```txt
Flask>=2.0.0
opencv-python>=4.5.0
numpy>=1.19.0
Pillow>=8.0.0
```

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

---

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Authors & Contributors

**Project Lead**: [@XeDiaulhaq](https://github.com/XeDiaulhaq)

**Contributors**: 
[@Mpakmal](https://github.com/Mpakmal) • [@ZiiHubb](https://github.com/ZiiHubb) • [@wildanhkim](https://github.com/wildanhkim)

---

**Repository**: [BlurFace-Recorder](https://github.com/XeDiaulhaq/BlurFace-Recorder)

*Terima kasih kepada semua kontributor! 🙏*
---

## 🙏 Acknowledgments

- OpenCV Community untuk library computer vision yang luar biasa
- Flask Framework untuk kemudahan pembuatan web application
- Haar Cascade dan DNN models untuk deteksi wajah

---

## 📞 Kontak & Support

Jika ada pertanyaan atau issue, silakan:
- Buka [Issue](https://github.com/XeDiaulhaq/BlurFace-Recorder/issues)
- Atau hubungi melalui GitHub

---

<p align="center">Made with ❤️ for Privacy Protection</p>

---