# PANDUAN MENJALANKAN SISTEM JADWAL & RUANGAN

## 🚀 QUICK START (5 MENIT)

### 1. Buka Terminal PowerShell
```powershell
# Navigasi ke folder project
cd c:\Users\erwin\Downloads\MODUL_JADWAL
```

### 2. Aktifkan Virtual Environment
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Output akan menampilkan: (.venv) PS C:\Users\erwin\Downloads\MODUL_JADWAL>
```

### 3. Jalankan API Server
```powershell
python api.py
```
✓ Server akan start di `http://localhost:5000`

### 4. Buka Terminal Baru (Ctrl+Shift+`)
```powershell
# Terminal baru
.\.venv\Scripts\Activate.ps1
python web_dashboard.py
```
✓ Dashboard akan start di `http://localhost:5001`

### 5. Buka Browser
```
Dashboard: http://localhost:5001
API: http://localhost:5000/api
```

---

## 📋 SETUP LENGKAP (FIRST TIME)

### Langkah 1: Setup Virtual Environment
```powershell
# Jika belum ada venv, buat baru
python -m venv .venv

# Aktifkan
.\.venv\Scripts\Activate.ps1
```

### Langkah 2: Install Dependencies
```powershell
# Install semua packages yang diperlukan
pip install -r requirements.txt

# Atau install manual:
pip install flask flask-cors requests
```

### Langkah 3: Verifikasi Instalasi
```powershell
# Cek Python version
python --version

# Cek package installed
pip list | grep -E "flask|requests"
```

---

## 🎯 PILIHAN MENJALANKAN SISTEM

### OPSI 1: Jalankan API + Dashboard Sekaligus

**Terminal 1 - API Server:**
```powershell
cd c:\Users\erwin\Downloads\MODUL_JADWAL
.\.venv\Scripts\Activate.ps1
python api.py

# Output:
# ================================================================================
# Schedule Management System - API Server
# ================================================================================
# API Server Starting...
# Access API at: http://localhost:5000/api
# Running on http://127.0.0.1:5000
```

**Terminal 2 - Web Dashboard:**
```powershell
cd c:\Users\erwin\Downloads\MODUL_JADWAL
.\.venv\Scripts\Activate.ps1
python web_dashboard.py

# Output:
# ================================================================================
# Schedule Management System - Web Dashboard
# ================================================================================
# Access Dashboard at: http://localhost:5001
# Running on http://127.0.0.1:5001
```

**Browser:**
```
Buka: http://localhost:5001
```

---

### OPSI 2: Testing & Verifikasi

**Run Unit Tests:**
```powershell
python test_schedule_system.py

# Output: 25+ tests passing
```

**Run API Tests:**
```powershell
python test_api.py

# Output: API tests dengan 30+ scenarios
```

**Run Success Criteria Verification:**
```powershell
python verify_success_criteria.py

# Output: 
# [OK] KRITERIA 1: DETEKSI SEMUA JENIS BENTROK
# [OK] KRITERIA 2: NOTIFIKASI TERKIRIM SAAT JADWAL BERUBAH
# [OK] KRITERIA 3: SEQUENCE DIAGRAM OBSERVER PATTERN
# [OK] KRITERIA 4: AI SUGGESTIONS UNTUK ADMIN
```

---

### OPSI 3: Demo & Quick Start

**Run Quick Start Demo:**
```powershell
python quick_start.py

# Output: Contoh penggunaan sistem
```

**Run Full Demo:**
```powershell
python demo.py

# Output: Walkthrough semua fitur
```

---

## 📊 FITUR YANG BISA DIAKSES

### 1. Web Dashboard (http://localhost:5001)

**Tab 1: Dashboard**
- Real-time statistics
- Total rooms, schedules, conflicts
- Active observers

**Tab 2: Rooms**
- Create ruangan baru
- List semua ruangan
- Lihat kapasitas

**Tab 3: Schedules**
- Create jadwal baru
- List jadwal
- Edit & delete jadwal

**Tab 4: Conflicts**
- Lihat semua konflik
- Detail setiap konflik
- Severity level

**Tab 5: Suggestions**
- Generate saran alternatif
- AI scoring dijelaskan
- Apply saran

### 2. REST API (http://localhost:5000/api)

**Endpoints Utama:**
```
GET  /api/health                    - Check API status
GET  /api/rooms                     - List semua ruangan
POST /api/rooms                     - Create ruangan
GET  /api/schedules                 - List jadwal
POST /api/schedules                 - Create jadwal
GET  /api/conflicts                 - List konflik
POST /api/suggestions               - Generate saran AI
```

**Contoh API Call:**
```bash
# Curl
curl http://localhost:5000/api/health

# PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/api/health" -Method Get
```

---

## 🔧 TROUBLESHOOTING

### Problem 1: Virtual Environment tidak aktif
**Solusi:**
```powershell
# Pastikan di folder project
cd c:\Users\erwin\Downloads\MODUL_JADWAL

# Aktifkan venv
.\.venv\Scripts\Activate.ps1

# Cek: prompt seharusnya menampilkan (.venv)
```

### Problem 2: ModuleNotFoundError
**Solusi:**
```powershell
# Install dependencies
pip install -r requirements.txt

# Atau install satu per satu
pip install flask
pip install flask-cors
pip install requests
```

### Problem 3: Port sudah digunakan
**Solusi:**
```powershell
# Kill proses yang menggunakan port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Atau ganti port di api.py
# Line: app.run(host='0.0.0.0', port=5000)
# Ubah ke: app.run(host='0.0.0.0', port=5002)
```

### Problem 4: Browser tidak bisa akses localhost
**Solusi:**
```
1. Pastikan API & Dashboard server running
2. Cek port di terminal (harus tulisan "Running on...")
3. Coba manual URL: http://127.0.0.1:5001
4. Clear browser cache (Ctrl+Shift+Delete)
5. Coba browser lain
```

---

## 📝 WORKFLOW CONTOH

### Skenario: Membuat Jadwal & Deteksi Konflik

**Step 1: Akses Dashboard**
```
Browser: http://localhost:5001
```

**Step 2: Create Ruangan**
```
Tab "Rooms" → Form → Isi:
  - Room ID: R001
  - Room Name: Ruang Kuliah A
  - Capacity: 40
  - Building: Building A
→ Click "Create Room"
```

**Step 3: Create Jadwal 1**
```
Tab "Schedules" → Form → Isi:
  - Schedule ID: SCH001
  - Course Name: Python Basics
  - Course Code: CS101
  - Lecturer: Dr. Smith
  - Day: MONDAY
  - Time: 09:00-11:00
  - Room: R001
  - Students: 30
→ Click "Create Schedule"
```

**Step 4: Create Jadwal 2 (Conflict)**
```
Tab "Schedules" → Form → Isi:
  - Schedule ID: SCH002
  - Course Name: Data Structures
  - Course Code: CS102
  - Lecturer: Dr. Johnson
  - Day: MONDAY
  - Time: 10:00-12:00
  - Room: R001 (SAME ROOM!)
  - Students: 25
→ Click "Create Schedule"

⚠️ KONFLIK TERDETEKSI!
```

**Step 5: Lihat Konflik**
```
Tab "Conflicts" → Akan tampil:
  - Room 'Ruang Kuliah A' double-booked
  - Severity: HIGH
  - Details: Python Basics vs Data Structures
```

**Step 6: Generate Saran AI**
```
Tab "Suggestions" → Select SCH002 → Click "Generate Suggestions"
→ Akan tampil 3 saran alternatif dengan AI score:
  - Suggestion #1: 0.95/1.00 ⭐⭐⭐⭐⭐
  - Suggestion #2: 0.85/1.00 ⭐⭐⭐⭐
  - Suggestion #3: 0.80/1.00 ⭐⭐⭐
→ Click "Apply" untuk pilihan terbaik
```

**Step 7: Konflik Resolved**
```
Tab "Conflicts" → Konflik sudah hilang
→ Jadwal sudah di-update dengan waktu baru
```

---

## 📚 DOKUMENTASI REFERENSI

**Untuk mempelajari lebih lanjut:**

1. **QUICK_REFERENCE.txt** - Quick reference card
2. **FINAL_REPORT.md** - Laporan lengkap
3. **KRITERIA_SUKSES.md** - Detail implementasi
4. **API_QUICKSTART.md** - Panduan API
5. **README.md** - Setup & getting started

---

## 🎯 COMMAND QUICK REFERENCE

```powershell
# Setup
.\.venv\Scripts\Activate.ps1          # Aktifkan venv
pip install -r requirements.txt       # Install packages

# Run System
python api.py                          # Jalankan API (port 5000)
python web_dashboard.py                # Jalankan Dashboard (port 5001)

# Testing
python test_schedule_system.py         # Unit tests
python test_api.py                     # API tests
python verify_success_criteria.py      # Verify criteria

# Demo
python quick_start.py                  # Quick demo
python demo.py                         # Full demo

# Browser
http://localhost:5001                  # Dashboard
http://localhost:5000/api              # API
```

---

## ✅ CHECKLIST MENJALANKAN SISTEM

- [ ] Virtual environment aktif (.venv\Scripts\Activate.ps1)
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] Terminal 1: python api.py running (localhost:5000)
- [ ] Terminal 2: python web_dashboard.py running (localhost:5001)
- [ ] Browser buka http://localhost:5001
- [ ] Dashboard loaded dengan 5 tabs
- [ ] Bisa create rooms
- [ ] Bisa create schedules
- [ ] Conflict detection working
- [ ] AI suggestions working

---

## 📞 STATUS SISTEM

Ketika kedua server running dengan baik, Anda akan melihat:

**Terminal API:**
```
INFO:werkzeug: * Running on http://127.0.0.1:5000
INFO:werkzeug: Press CTRL+C to quit
```

**Terminal Dashboard:**
```
INFO:werkzeug: * Running on http://127.0.0.1:5001
INFO:werkzeug: Press CTRL+C to quit
```

**Browser:**
```
Sistem Jadwal & Ruangan - Dashboard
├─ Dashboard Tab (Real-time stats)
├─ Rooms Tab (Manage ruangan)
├─ Schedules Tab (Manage jadwal)
├─ Conflicts Tab (View konflik)
└─ Suggestions Tab (AI suggestions)
```

---

## 🎉 SELESAI!

Sistem siap digunakan dengan:
- ✅ API Server running
- ✅ Web Dashboard running
- ✅ Semua 4 kriteria sukses verified
- ✅ Conflict detection active
- ✅ Notifications active
- ✅ AI suggestions active

**Enjoy! 🚀**
