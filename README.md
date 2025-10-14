# BlurFace-Recorder F

Proyek "BlurFace-Recorder" adalah aplikasi berbasis web untuk merekam video dari kamera (webcam) dan menerapkan efek blur pada wajah (face blurring) secara real-time atau pada rekaman, menggunakan OpenCV. Tujuan utamanya adalah meningkatkan privasi saat merekam atau menyimpan video yang melibatkan wajah manusia.

README ini berbahasa Indonesia dan mencakup ringkasan, arsitektur, cara instalasi, cara menjalankan backend dan frontend, konfigurasi penting, serta catatan keamanan dan lisensi.

## Fitur utama
- Deteksi wajah menggunakan model Haar cascade (file XML) dari OpenCV.
- Blurring atau pixelation wajah sebelum penyimpanan/streaming.
- Antarmuka web untuk preview kamera, mulai/berhenti rekaman, dan unduh hasil video yang sudah diblur.
- Backend Python (FastAPI/Flask) yang menangani stream video, pemrosesan frame, dan endpoint untuk menyimpan/menyajikan video.

## Struktur proyek (ringkasan)

Folder utama:

- `backend/` - kode server (Python, OpenCV)
	- `app/` - aplikasi backend
		- `routes/` - endpoint API
		- `services/` - modul pemrosesan citra, model Haar cascade (`default_frontal_face.xml`), dll.
		- `main.py` - entrypoint backend
		- `pyproject.toml` / `requirements` - dependensi (jika ada)
- `frontend/` - kode antarmuka web (HTML/CSS/JS atau framework seperti React/Vue)

> Catatan: README ini menuliskan instruksi generik; sesuaikan nama file/skrip jika di repositori berbeda.

## Prasyarat
- Python >= 3.13 dengan pip
- Node.js dan npm/yarn (hanya jika ada frontend berbasis Node)
- Webcam untuk pengujian lokal
- Sistem operasi: Linux/macOS/Windows

## Dependensi (sesuai pyproject.toml)

File `backend/app/services/pyproject.toml` menyatakan dependensi utama:

- `numpy>=2.3.3`
- `opencv-python>=4.11.0.86`

Instal dependency yang diperlukan dengan pip:

```bash
pip install numpy opencv-python
```

Catatan: `pyproject.toml` di repo menggunakan `requires-python = ">=3.13"` — gunakan interpreter Python 3.13 atau lebih baru.

Jika Anda juga ingin menjalankan server web (FastAPI/Flask) selain skrip demo, tambahkan paket yang diperlukan (mis. `fastapi`, `uvicorn`) ke environment atau `pyproject.toml`.

## Menjalankan backend (contoh)

1. Masuk ke folder backend:

```bash
cd backend/app
```

2. Jalankan server (contoh dengan Uvicorn + FastAPI):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. Endpoint yang umum tersedia (sesuaikan dengan implementasi):
- `GET /` - health check atau halaman singkat
- `GET /video_feed` - stream video berisi frame yang sudah diproses (multipart/x-mixed-replace)
- `POST /record` - mulai perekaman / simpan file hasil

Jika backend menggunakan Flask, perintah menjalankan akan berbeda (mis. `python main.py`). Periksa `main.py` untuk instruksi pasti.

### Menjalankan skrip demo OpenCV yang ada di repo

Repository ini berisi skrip demo yang menggunakan OpenCV langsung untuk membuka webcam dan menampilkan hasil blur wajah: `backend/app/services/main.py`.

1. Pastikan Anda berada di folder proyek dan telah menginstal OpenCV:

```bash
pip install opencv-python
```

2. Jalankan skrip:

```bash
python backend/app/services/main.py
```

3. Kontrol:
- Jendela OpenCV akan menampilkan preview dari webcam dengan wajah yang diblur.
- Tekan `q` pada jendela atau fokus keyboard untuk keluar.

Catatan untuk Linux:
- Jika menggunakan lingkungan headless (contoh server tanpa X11), skrip ini membutuhkan tampilan, atau gunakan VNC/Xpra, atau jalankan versi headless yang mengirim frame ke endpoint HTTP.
- Jika `cv2.VideoCapture(0)` gagal, pastikan kamera tidak sedang dipakai oleh aplikasi lain dan perangkat `/dev/video0` tersedia.

## Menjalankan frontend (contoh)

Jika frontend adalah aplikasi statis (HTML/JS), cukup buka `frontend/index.html` di browser atau server statis.

Jika menggunakan framework Node (React/Vue):

```bash
cd frontend
npm install
npm run dev    # atau npm start / npm run build
```

Frontend harus melakukan: meminta akses kamera pengguna (getUserMedia), menampilkan preview, dan mengirim frame ke backend (mis. WebRTC, WebSocket, atau fetch POST tiap frame) tergantung arsitektur.

## Contoh alur kerja (end-to-end)

1. Pengguna membuka halaman web.
2. Frontend meminta akses kamera dan menampilkan preview.
3. Frame dikirim ke backend (atau diproses di frontend jika menggunakan WASM atau face-api.js).
4. Backend mendeteksi wajah menggunakan Haar cascade (`default_frontal_face.xml`) dan menerapkan blur pada area wajah.
5. Frame yang sudah diproses dikembalikan ke frontend sebagai stream atau disimpan di server.
6. Pengguna dapat memulai/berhenti rekaman dan mengunduh video hasil blur.

## Contoh kode: deteksi & blur wajah (Python + OpenCV)

Berikut contoh fungsi singkat untuk mendeteksi dan memburamkan wajah pada sebuah frame menggunakan Haar cascade:

```python
import cv2

face_cascade = cv2.CascadeClassifier('services/default_frontal_face.xml')

def blur_faces(frame, scaleFactor=1.1, minNeighbors=5, ksize=(23, 23)):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
		for (x, y, w, h) in faces:
				roi = frame[y:y+h, x:x+w]
				# Gaussian blur
				blurred = cv2.GaussianBlur(roi, ksize, 30)
				frame[y:y+h, x:x+w] = blurred
		return frame
```

Catatan: path cascade yang digunakan oleh skrip demo adalah `backend/app/services/default_frontal_face.xml`. Pastikan file itu ada di folder yang sama dengan skrip `backend/app/services/main.py`.

## Konfigurasi & tuning
- Ubah parameter `scaleFactor` dan `minNeighbors` pada detektor untuk menyeimbangkan kecepatan dan akurasi.
- Untuk hasil blur lebih halus gunakan kernel blur yang lebih besar atau multiple-pass blur.
- Untuk privasi lebih kuat, gunakan pixelation (downscale+upscale) atau mengganti area wajah dengan overlay solid color.

## Pertimbangan performa
- Pemrosesan frame di server membutuhkan CPU; untuk real-time, pertimbangkan:
	- mengurangi resolusi frame yang dikirim
	- melakukan deteksi pada setiap N-th frame
	- memanfaatkan GPU (dengan OpenVINO/CUDA) jika tersedia
	- gunakan multiprocessing/worker pool untuk menangani banyak klien

## Keamanan & privasi
- Jangan menyimpan video yang mengandung wajah tanpa izin. Jika menyimpan, enkripsi file dan berikan kontrol penghapusan.
- Batasi akses endpoint penyimpanan dengan autentikasi (JWT/API key).
- Sanitasi input dan batasi ukuran upload untuk mencegah DoS.

## Testing
- Uji dengan berbagai kondisi pencahayaan dan sudut wajah.
- Tambahkan unit tests untuk fungsi pemrosesan citra (mis. memastikan area wajah berubah) jika proyek skala besar.

## Lisensi
Sertakan lisensi yang sesuai (mis. MIT) di file `LICENSE`. Saat ini README ini tidak mengandung lisensi bawaan.

## Referensi
- OpenCV Haar Cascades: https://docs.opencv.org/
- FastAPI: https://fastapi.tiangolo.com/ (jika digunakan)

## Kontak
Jika Anda memerlukan bantuan lebih lanjut untuk menyesuaikan README ini dengan kode dalam repository (mis. mengisi perintah exact run pada `main.py` atau menambahkan instruksi `frontend`), beri tahu berkas apa yang ingin saya buka dan saya akan melengkapinya.

---

README dibuat otomatis — sesuaikan bagian "Menjalankan backend" dan "Menjalankan frontend" jika struktur file/entrypoint berbeda di repo Anda.
