# [Feature] Kalkulator Subnet & VLSM

## Deskripsi

Fitur ini bertujuan untuk mengimplementasikan sistem **Kalkulator Subnet & VLSM Berbasis Web** yang dirancang sebagai sarana pembelajaran interaktif bagi guru dan siswa SMK Program Keahlian Teknik Komputer dan Jaringan (TKJ). Sistem ini memfasilitasi verifikasi perhitungan pengalamatan IPv4, analisis subnet standar, dan pembagian blok jaringan dengan metode Variable Length Subnet Masking (VLSM) secara akurat, transparan, dan sesuai standar RFC.

Sistem terdiri atas:
1. **Core Backend Engine (Python):** Fungsi perhitungan subnet (`hitung_subnet`) dan alokasi VLSM (`alokasi_vlsm`) dengan aturan validasi ketat (larangan *leading zero*, validasi rentang oktet 0–255, prefix 0–32, bit host nol untuk network CIDR, dan penanganan khusus RFC 3021 /31 serta host route /32).
2. **REST API (FastAPI):** Endpoint HTTP untuk melayani antarmuka web, kalkulasi subnet (`GET /api/subnet`), dan alokasi VLSM (`POST /api/vlsm`) dengan standarisasi respons error HTTP 400 Bad Request (meng-override status default 422 FastAPI).
3. **Frontend (Single Page Application):** Halaman web interaktif (`index.html`) berbasis Tailwind CSS dan Vanilla JS yang responsif, intuitif, dan memiliki visualisasi hasil serta banner penanganan error yang jelas.

---

## Tugas

- [ ] **Setup Lingkungan & Struktur Proyek:**
  - Konfigurasi struktur modul backend (`src/`) dan dependencies menggunakan `uv` / `pyproject.toml`.
  - Konfigurasi pengujian otomatis menggunakan `pytest` dan `httpx`.
- [ ] **Implementasi Core Module Subnet (`hitung_subnet`):**
  - Validasi IPv4 (tepat 4 oktet, rentang 0-255, tanpa spasi/simbol, tolak *zero-padding* / *leading zeros*).
  - Validasi prefix integer (0–32).
  - Perhitungan subnet mask, network address (bitwise AND), broadcast address, range first-last host, dan jumlah host usable.
  - Implementasi aturan khusus: Point-to-Point `/31` (RFC 3021, 2 host usable, broadcast `None`) dan Host Route `/32` (1 host usable, first=last, broadcast `None`).
- [ ] **Implementasi Core Module VLSM (`alokasi_vlsm`):**
  - Validasi base network CIDR (harus alamat network valid dengan bit host bernilai nol).
  - Validasi daftar kebutuhan host (tidak boleh kosong, setiap elemen bilangan bulat $\ge 1$).
  - Pengurutan kebutuhan host secara menurun (*descending*).
  - Alokasi subnet secara berurutan (*contiguous*) tanpa overlap dengan ukuran blok pangkat 2 minimum.
  - Penolakan alokasi (*raise* `ValueError`) jika total kebutuhan melampaui kapasitas base network.
- [ ] **Implementasi REST API & Error Handler (FastAPI):**
  - Endpoint `GET /`: Menyajikan antarmuka pengguna `index.html`.
  - Endpoint `GET /api/subnet`: Query params `ip` & `prefix`, mengembalikan JSON subnet calculation.
  - Endpoint `POST /api/vlsm`: Body JSON `network` & `kebutuhan_host`, mengembalikan daftar alokasi subnet.
  - Override status code validasi FastAPI bawaan (422) menjadi HTTP 400 Bad Request dengan format payload `{"detail": "..."}`.
- [ ] **Pengujian Otomatis (Automated Testing / TDD):**
  - Menulis test suite lengkap di `tests/test_main.py` mencakup seluruh skenario normal, batas (*boundary*), dan *edge case*.
- [ ] **Integrasi Antarmuka Web (Frontend):**
  - Menghubungkan form Subnet dan form VLSM pada `index.html` dengan API backend.
  - Menampilkan hasil kalkulasi dan tabel alokasi VLSM secara informatif.
  - Menampilkan banner alert berwarna merah untuk respons error (HTTP 400).
- [ ] **Integrasi CI (Continuous Integration):**
  - Menyusun workflow GitHub Actions untuk menjalankan automated testing pada setiap commit dan Pull Request.

---

## Kriteria Penerimaan (Acceptance Criteria)

Kriteria penerimaan merujuk secara ketat pada Tabel Kasus Uji di dokumen `SPEC.md` (Bagian 6):

### 1. Perhitungan Subnet Standar
- **Kasus Subnet /25:**
  - Input: `ip=172.16.5.130`, `prefix=25`
  - Hasil: Network = `172.16.5.128`, Broadcast = `172.16.5.255`, Usable Hosts = `126`, Range Host = `172.16.5.129` – `172.16.5.254`, Mask = `255.255.255.128`.
- **Kasus Subnet /30:**
  - Input: `ip=10.0.0.0`, `prefix=30`
  - Hasil: Network = `10.0.0.0`, Broadcast = `10.0.0.3`, Usable Hosts = `2`, Range Host = `10.0.0.1` – `10.0.0.2`, Mask = `255.255.255.252`.
- **Kasus Point-to-Point /31 (RFC 3021):**
  - Input: `ip=192.168.1.0`, `prefix=31`
  - Hasil: Network = `192.168.1.0`, First Host = `192.168.1.0`, Last Host = `192.168.1.1`, Broadcast = `None`, Usable Hosts = `2`.
- **Kasus Host Route /32:**
  - Input: `ip=192.168.1.5`, `prefix=32`
  - Hasil: Network = `192.168.1.5`, First Host = `192.168.1.5`, Last Host = `192.168.1.5`, Broadcast = `None`, Usable Hosts = `1`.

### 2. Validasi Input & Penanganan Edge Case IP/Prefix
- **Oktet > 255:** Input seperti `256.1.1.1/24` memicu `ValueError` di backend dan respons HTTP `400 Bad Request`.
- **Leading Zero (Zero-Padding):** Input seperti `192.168.01.1/24` memicu `ValueError` di backend dan respons HTTP `400 Bad Request`.
- **Format Inkomplet:** Input dengan jumlah oktet tidak sama dengan 4 (contoh: `192.168.1`) memicu `ValueError` / HTTP `400 Bad Request`.
- **Non-Numeric / Simbol:** Input dengan karakter alfabet atau simbol (contoh: `abc`) memicu `ValueError` / HTTP `400 Bad Request`.
- **Input Kosong:** Input string kosong `""` memicu `ValueError` / HTTP `400 Bad Request`.
- **Prefix Tidak Valid:** Prefix > 32 (misal `33`) atau prefix negatif (misal `-1`) memicu `ValueError` / HTTP `400 Bad Request`.

### 3. Kontrak & Status Code API
- **Endpoint `GET /`:** Mengembalikan status `200 OK` dengan Content-Type `text/html` (halaman web antarmuka).
- **Endpoint `GET /api/subnet` Sukses:** Mengembalikan status `200 OK` beserta struktur JSON valid (`mask`, `network`, `broadcast`, `first_host`, `last_host`, `usable_hosts`).
- **Endpoint `GET /api/subnet` Invalid / Missing Param:** Permintaan dengan parameter hilang, IP tidak valid, atau prefix non-integer (misal `prefix=abc`) wajib mengembalikan HTTP `400 Bad Request` dengan payload `{"detail": "..."}` (bukan default FastAPI 422).

### 4. Alokasi VLSM
- **Alokasi Normal:**
  - Base: `192.168.1.0/24`, Kebutuhan: `[100, 50, 20, 2]`
  - Menghasilkan alokasi berurutan tanpa overlap:
    - 100 host $\rightarrow$ `/25` (`192.168.1.0/25`, net: `.0`, usable: 126)
    - 50 host $\rightarrow$ `/26` (`192.168.1.128/26`, net: `.128`, usable: 62)
    - 20 host $\rightarrow$ `/27` (`192.168.1.192/27`, net: `.192`, usable: 30)
    - 2 host $\rightarrow$ `/30` (`192.168.1.224/30`, net: `.224`, usable: 2)
- **Kapasitas Kurang / Overflow:**
  - Base: `192.168.1.0/24`, Kebutuhan: `[200, 100]`
  - Ditolak dengan `ValueError` dan respons HTTP `400 Bad Request` (total alokasi blok 384 melebihi kapasitas 256 pada `/24`).
- **Kebutuhan Kosong:** Kebutuhan `[]` memicu `ValueError` / HTTP `400 Bad Request`.
- **Kebutuhan $\le 0$:** Kebutuhan berisi nilai $\le 0$ (contoh `[50, 0]` atau `[50, -2]`) memicu `ValueError` / HTTP `400 Bad Request`.
- **Network CIDR Dasar Invalid:** Base network format tidak valid (contoh `192.168.1.999/24`) memicu `ValueError` / HTTP `400 Bad Request`.
- **Host Bits Non-Nol:** Base network dengan bit host bukan nol (contoh `192.168.1.5/24`) wajib ditolak dengan `ValueError` / HTTP `400 Bad Request`.

---

## Alur Kerja (Workflow)

Pengembangan fitur ini mengikuti alur rekayasa perangkat lunak terstruktur dan disiplin TDD (Test-Driven Development):

$$\text{Issue} \longrightarrow \text{Branch} \longrightarrow \text{Test Dulu} \longrightarrow \text{Implementasi} \longrightarrow \text{Commit} \longrightarrow \text{Pull Request} \longrightarrow \text{CI} \longrightarrow \text{Merge}$$

1. **Issue:**
   Mendokumentasikan seluruh spesifikasi, daftar tugas, dan kriteria penerimaan ke dalam GitHub Issue ini sebagai acuan utama pelacakan progress fitur.
2. **Branch:**
   Membuat branch fitur baru dari branch `main` dengan format penamaan standar:
   ```bash
   git checkout -b feature/issue-<nomor>-subnet-calculator main
   ```
3. **Test Dulu (Test-Driven Development - TDD):**
   - Menuliskan skenario pengujian di `tests/test_main.py` menggunakan framework `pytest` sebelum logika fitur diimplementasikan secara penuh.
   - Menguji kasus normal, kasus batas (*boundary conditions*), dan penanganan error sesuai tabel pengujian pada `SPEC.md` (tahap *Red*).
4. **Implementasi:**
   - Menulis kode implementasi pada modul backend (`src/`) dan API FastAPI hingga seluruh unit test dan API test berhasil lulus 100% (tahap *Green*).
   - Melakukan refactoring kode untuk menjaga keterbacaan, efisiensi, dan kebersihan kode tanpa merusak test (tahap *Refactor*).
   - Menghubungkan dan memvalidasi interaksi frontend (`index.html`) dengan backend.
5. **Commit:**
   - Melakukan commit kode secara berkala dan atomik dengan pesan commit deskriptif mengikuti format *Conventional Commits* (contoh: `test: ...`, `feat: ...`, `docs: ...`, `fix: ...`).
6. **Pull Request (PR):**
   - Membuka Pull Request dari branch fitur ke branch `main`.
   - Melampirkan ringkasan perubahan dan mereferensikan issue terkait (contoh: `Closes #<nomor>`).
7. **CI (Continuous Integration):**
   - GitHub Actions workflow akan secara otomatis terpicu untuk menjalankan linter dan test suite (`pytest`).
   - Seluruh pemeriksaan CI wajib berstatus hijau (*passed*) sebelum branch diizinkan untuk di-merge.
8. **Merge:**
   - Setelah CI berhasil dan review selesai, Pull Request di-merge ke branch `main`.
   - Issue terkait ditutup secara otomatis oleh GitHub.
