# [Feature] Alokasi VLSM (Variable Length Subnet Masking)

## Deskripsi

Fitur ini mengimplementasikan **Alokasi VLSM** sebagai ekstensi dari Kalkulator Subnet yang sudah ada. VLSM memungkinkan pembagian satu blok jaringan IPv4 utama menjadi beberapa sub-jaringan dengan ukuran yang bervariasi sesuai kebutuhan host masing-masing departemen, menggunakan metode *greedy descending* (alokasi dari kebutuhan terbesar ke terkecil).

Fitur ini mencakup:
1. **Core Function `alokasi_vlsm`** – logika backend Python untuk membagi blok CIDR menjadi sub-jaringan berurutan tanpa overlap.
2. **REST Endpoint `POST /api/vlsm`** – antarmuka API untuk menerima permintaan alokasi dan mengembalikan tabel subnet terstruktur.
3. **Frontend VLSM Tab** – menghubungkan form VLSM di `index.html` ke API backend agar tabel hasil tampil secara dinamis.

---

## Tugas

- [ ] **Implementasi `alokasi_vlsm(network_cidr, kebutuhan_host)` di `main.py`:**
  - Validasi `network_cidr` menggunakan `hitung_subnet`, pastikan bit host bernilai 0.
  - Validasi `kebutuhan_host`: tidak boleh kosong, setiap elemen bilangan bulat ≥ 1.
  - Urutkan kebutuhan secara menurun (*descending*).
  - Tentukan ukuran blok minimum (pangkat 2 terkecil ≥ kebutuhan + 2, minimum `/30` / blok 4).
  - Alokasikan subnet berurutan dari alamat network dasar.
  - Raise `ValueError` jika total blok melebihi kapasitas base network.
- [ ] **Implementasi endpoint `POST /api/vlsm` di `main.py`:**
  - Request body JSON: `{ "network": "...", "kebutuhan_host": [...] }`.
  - Response sukses `200 OK`: list dict berisi `kebutuhan`, `network_cidr`, dan semua field `hitung_subnet`.
  - Response error `400 Bad Request`: `{ "detail": "..." }`.
- [ ] **Penulisan Test VLSM di `test_main.py` (TDD — test ditulis lebih dulu):**
  - Test unit `alokasi_vlsm` untuk kasus normal (4 subnet), overflow, kebutuhan kosong, kebutuhan ≤ 0, CIDR invalid, host bits non-nol.
  - Test API `POST /api/vlsm` untuk sukses dan semua error (400).
- [ ] **Integrasi Frontend Tab VLSM di `index.html`:**
  - Hubungkan `onVlsmCalculateClick()` ke `POST /api/vlsm`.
  - Render tabel hasil secara dinamis ke `#vlsm-res-tbody`.
  - Tampilkan banner error `#vlsm-view-error` saat HTTP 400.
  - Tampilkan `#vlsm-view-empty` saat belum ada hasil.

---

## Kriteria Penerimaan (Acceptance Criteria)

Merujuk pada Tabel Kasus Uji `SPEC.md` Bagian 6 — hanya kasus VLSM:

### 1. Alokasi VLSM Normal
- **Input:** Base `192.168.1.0/24`, Kebutuhan `[100, 50, 20, 2]`
- **Output (berurutan, tanpa overlap):**
  | # | Kebutuhan | Network CIDR       | Mask              | Usable |
  |---|----------|--------------------|-------------------|--------|
  | 1 | 100      | 192.168.1.0/25     | 255.255.255.128   | 126    |
  | 2 | 50       | 192.168.1.128/26   | 255.255.255.192   | 62     |
  | 3 | 20       | 192.168.1.192/27   | 255.255.255.224   | 30     |
  | 4 | 2        | 192.168.1.224/30   | 255.255.255.252   | 2      |

### 2. Overflow / Kapasitas Kurang
- **Input:** Base `192.168.1.0/24`, Kebutuhan `[200, 100]`
- **Output:** `ValueError` / HTTP `400 Bad Request` — total blok 384 melebihi kapasitas 256 pada `/24`.

### 3. Edge Case — Kebutuhan Kosong
- **Input:** Base `192.168.1.0/24`, Kebutuhan `[]`
- **Output:** `ValueError` / HTTP `400 Bad Request`.

### 4. Edge Case — Kebutuhan ≤ 0
- **Input:** Base `192.168.1.0/24`, Kebutuhan `[50, 0]` atau `[50, -2]`
- **Output:** `ValueError` / HTTP `400 Bad Request`.

### 5. Edge Case — Network CIDR Invalid
- **Input:** Base `192.168.1.999/24`, Kebutuhan `[10]`
- **Output:** `ValueError` / HTTP `400 Bad Request`.

### 6. Edge Case — Host Bits Non-Nol
- **Input:** Base `192.168.1.5/24`, Kebutuhan `[10]`
- **Output:** `ValueError` / HTTP `400 Bad Request`.

---

## Alur Kerja (Workflow)

$$\text{Issue} \longrightarrow \text{Branch} \longrightarrow \text{Test Dulu (Merah)} \longrightarrow \text{Implementasi (Hijau)} \longrightarrow \text{Commit} \longrightarrow \text{Pull Request} \longrightarrow \text{CI} \longrightarrow \text{Merge}$$

1. **Issue:** Dokumen ini sebagai acuan pelacakan fitur VLSM.
2. **Branch:** `feature/issue-<nomor>-vlsm` dari `main` terbaru.
3. **TDD Red:** Tulis semua test VLSM di `test_main.py`, buat kerangka fungsi/endpoint yang belum diimplementasikan → test merah.
4. **TDD Green:** Implementasikan `alokasi_vlsm` dan `POST /api/vlsm` hingga semua test hijau.
5. **Frontend:** Hubungkan tab VLSM di `index.html` ke endpoint `/api/vlsm`.
6. **Commit & PR:** Push branch, buka Pull Request ke `main` dengan `Closes #<nomor>`.
7. **CI:** Pastikan GitHub Actions pipeline hijau.
8. **Merge:** `gh pr merge --merge`.
