# Spesifikasi Teknis: Kalkulator Subnet & VLSM (`SPEC.md`)

---

## 1. Tujuan

Dokumen spesifikasi teknis ini mendefinisikan arsitektur, kontrak fungsi backend, spesifikasi API, dan kestandaran antarmuka untuk **Kalkulator Subnet & VLSM Berbasis Web**. Aplikasi ini dirancang untuk mendukung guru dan siswa SMK Program Keahlian Teknik Komputer dan Jaringan (TKJ) dalam melakukan verifikasi perhitungan alamat jaringan IPv4 secara akurat, transparan, dan sesuai standar industri.

---

## 2. Aturan Validasi (Validation Rules)

### 2.1. Validasi Alamat IPv4 (`ip: str`)

* **Format Struktur:** Harus terdiri tepat 4 oktet bilangan bulat yang dipisahkan oleh tanda titik (`.`).
* **Rentang Nilai:** Setiap oktet berada pada rentang numerik inklusif $0$ hingga $255$.
* **Karakter Terlarang & Bentuk Malformasi:**
* Tidak boleh mengandung spasi atau karakter alfa/simbol khusus.
* **Zero-padding ditolak:** Angka nol di depan pada tiap oktet tidak diizinkan (contoh: `192.168.01.1` dianggap tidak valid dan wajib menghasilkan `ValueError`).
* Jumlah oktet harus tepat 4 (tidak boleh kurang atau lebih).



### 2.2. Validasi Prefix (`prefix: int` atau parameter CIDR)

* **Rentang Nilai:** Bilangan bulat (`integer`) dari $0$ hingga $32$ inklusif. Nilai di luar rentang ini, tipe data non-integer (seperti string huruf atau float), atau parameter yang hilang wajib memicu kegagalan validasi.

### 2.3. Aturan Alamat Jaringan (Network CIDR Validation)

* **Bit Host Harus Nol:** Alamat jaringan dalam format CIDR (digunakan pada fungsi VLSM atau input network) wajib memiliki bit host yang bernilai nol (merupakan alamat network yang sah). Jika input network memiliki bit host yang tidak nol (contoh: `192.168.1.5/24`), sistem **tidak boleh** melakukan pembulatan otomatis, melainkan wajib menolak dan menaikkan (`raise`) `ValueError`.

---

## 3. Kontrak Fungsi (Function Contracts)

### 3.1. `hitung_subnet(ip: str, prefix: int) -> dict`

Fungsi inti untuk menghitung parameter subnet berdasarkan alamat IPv4 dan prefix CIDR.

* **Parameter:**
* `ip` (str): Alamat IPv4 string.
* `prefix` (int): Nilai prefix CIDR ($0 - 32$).


* **Return (`dict`):** Mengembalikan kamus dengan kunci wajib:
* `mask` (str): Subnet mask dalam format desimal bertitik.
* `network` (str): Alamat jaringan (Network Address).
* `broadcast` (str | None): Alamat siaran (Broadcast Address). Bernilai `None` untuk prefix `/31` dan `/32`.
* `first_host` (str): Alamat host pertama yang dapat digunakan.
* `last_host` (str): Alamat host terakhir yang dapat digunakan.
* `usable_hosts` (int): Jumlah host usable yang tersedia.


* **Aturan Perhitungan Khusus:**
* **Network Address:** Dihitung menggunakan operasi bitwise AND antara representasi integer 32-bit dari IP dan Subnet Mask.
* **Prefix /0 s.d. /30:** Jumlah host usable dihitung dengan formula standard $2^{(32 - \text{prefix})} - 2$.
* **Prefix /31 (RFC 3021 Point-to-Point):** Mendukung 2 host (`first_host` dan `last_host` adalah kedua IP dalam blok tersebut), tanpa network/broadcast tradisional (`broadcast = None`), jumlah host usable = 2.
* **Prefix /32 (Host Route):** 1 host (`first_host` = `last_host` = IP itu sendiri), `broadcast = None`, jumlah host usable = 1.



### 3.2. `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`

Fungsi untuk melakukan pembagian Variable Length Subnet Masking (VLSM) dari suatu network dasar.

* **Parameter:**
* `network_cidr` (str): Network utama dalam format CIDR.
* `kebutuhan_host` (list[int]): Daftar kebutuhan host untuk tiap sub-jaringan.


* **Logika Proses:**
1. Validasi `network_cidr` menggunakan `hitung_subnet` dan pastikan bit host bernilai 0.
2. Validasi `kebutuhan_host`: daftar tidak boleh kosong (`list` kosong ditolak), setiap elemen harus berupa bilangan bulat $\ge 1$ (nilai 0 atau negatif ditolak).
3. Urutkan `kebutuhan_host` secara menurun (*descending*) dari jumlah host terbanyak ke paling sedikit.
4. Untuk setiap kebutuhan host, tentukan ukuran blok minimum (pangkat 2 terkecil yang memenuhi $\text{kebutuhan} + 2$, dengan batas minimum prefix `/30` atau ukuran blok 4).
5. Alokasikan subnet secara berurutan mulai dari alamat network dasar.
6. **Kondisi Error:** Jika total blok yang dibutuhkan melebihi kapasitas sisa dari `network_cidr`, fungsi wajib menaikkan (`raise`) `ValueError`.


* **Return (`list[dict]`):** Daftar kamus di mana setiap elemen memuat informasi: `kebutuhan`, `network_cidr`, beserta seluruh kunci hasil `hitung_subnet`.

---

## 4. Kontrak API (API Contracts)

Backend dibangun menggunakan FastAPI (Python 3.12).

### 4.1. Penanganan HTTP Status Code untuk Error (Override 422 ke 400)

* **Kebijakan Penting:** Secara default, FastAPI mengembalikan status code `422 Unprocessable Entity` untuk kesalahan validasi tipe data atau parameter hilang. Berdasarkan spesifikasi ini, seluruh kesalahan input—termasuk prefix yang bukan bilangan bulat (misalnya `"abc"`), parameter query yang hilang, atau pelanggaran format IP—**wajib ditangkap dan dikembalikan sebagai HTTP `400 Bad Request**` dengan format JSON standar `{"detail": "pesan kesalahan yang deskriptif"}`.

### 4.2. Endpoint Statis

* **`GET /`**
* **Deskripsi:** Mengembalikan halaman antarmuka pengguna utama (`index.html`).
* **Response:** `200 OK` (Content-Type: `text/html`).



### 4.3. Endpoint Subnet Standar

* **`GET /api/subnet`**
* **Query Parameters:**
* `ip` (string, wajib)
* `prefix` (integer/string, wajib)


* **Response Sukses (`200 OK`):**
```json
{
  "mask": "255.255.255.128",
  "network": "172.16.5.128",
  "broadcast": "172.16.5.255",
  "first_host": "172.16.5.129",
  "last_host": "172.16.5.254",
  "usable_hosts": 126
}

```


* **Response Error (`400 Bad Request`):**
```json
{
  "detail": "Format IP Address atau prefix tidak valid."
}

```





### 4.4. Endpoint Alokasi VLSM

* **`POST /api/vlsm`**
* **Request Body (`application/json`):**
```json
{
  "network": "192.168.1.0/24",
  "kebutuhan_host": [100, 50, 20, 2]
}

```


* **Response Sukses (`200 OK`):**
```json
[
  {
    "kebutuhan": 100,
    "network_cidr": "192.168.1.0/25",
    "mask": "255.255.255.128",
    "network": "192.168.1.0",
    "broadcast": "192.168.1.127",
    "first_host": "192.168.1.1",
    "last_host": "192.168.1.126",
    "usable_hosts": 126
  }
]

```


* **Response Error (`400 Bad Request`):**
```json
{
  "detail": "Kapasitas base network tidak mencukupi untuk menampung seluruh kebutuhan host."
}

```





---

## 5. Halaman Web (Web UI Specification)

* **Arsitektur:** Single Page Application (SPA) berbasis satu file `index.html` yang memuat styling (Tailwind CSS via CDN) dan logika interaksi JavaScript (Vanilla JS).
* **Fitur Utama Antarmuka:**
1. **Navigasi Mode:** Tombol tab untuk beralih antara **Mode Subnet Standar** dan **Mode VLSM**.
2. **Form Subnet:** Input teks untuk IP Address, input angka untuk Prefix (0–32), tombol "Hitung", serta area kartu hasil (*result card*) yang menampilkan Network, Broadcast, Range Host, dan Jumlah Host.
3. **Form VLSM:** Input teks untuk Base Network (CIDR) dan area input untuk daftar kebutuhan host, tombol "Alokasi", serta tabel hasil pembagian blok subnet.
4. **Penanganan Error Visual:** Kotak notifikasi peringatan (*alert banner*) berwarna merah yang menampilkan pesan `detail` dari server secara jelas apabila terjadi kesalahan input atau kegagalan validasi (HTTP 400).



---

## 6. Tabel Test Case (Test Case Table)

Tabel berikut menjadi acuan utama pengujian otomatis (`test_main.py` dengan `pytest`) maupun validasi manual oleh penguji/guru:

| Kasus Uji | Input | Hasil yang Diharapkan | Status (Pasti / Perlu Keputusan) |
| --- | --- | --- | --- |
| **Subnet Standard /25** | `172.16.5.130/25` | • Network: `172.16.5.128`<br>

<br>• Broadcast: `172.16.5.255`<br>

<br>• Usable Hosts: `126`<br>

<br>• Range: `172.16.5.129` – `172.16.5.254` | **Pasti** |
| **Subnet Standard /30** | `10.0.0.0/30` | • Network: `10.0.0.0`<br>

<br>• Broadcast: `10.0.0.3`<br>

<br>• Usable Hosts: `2`<br>

<br>• Range: `10.0.0.1` – `10.0.0.2` | **Pasti** |
| **Point-to-Point (/31)** | `192.168.1.0/31` | • Network: `192.168.1.0`<br>

<br>• First Host: `192.168.1.0`<br>

<br>• Last Host: `192.168.1.1`<br>

<br>• Broadcast: `None`<br>

<br>• Usable Hosts: `2` | **Pasti** (mengikuti standar RFC 3021) |
| **Host Route (/32)** | `192.168.1.5/32` | • Network: `192.168.1.5`<br>

<br>• Broadcast: `None`<br>

<br>• First/Last Host: `192.168.1.5`<br>

<br>• Usable Hosts: `1` | **Pasti** |
| **Edge Case: Oktet > 255** | `256.1.1.1/24` | Memicu `ValueError` / HTTP 400 | **Pasti** |
| **Edge Case: Leading Zero** | `192.168.01.1/24` | Memicu `ValueError` / HTTP 400 | **Pasti** |
| **Edge Case: Format Inkomplet** | `192.168.1` | Memicu `ValueError` / HTTP 400 | **Pasti** |
| **Edge Case: Non-Numeric** | `abc` | Memicu `ValueError` / HTTP 400 | **Pasti** |
| **Edge Case: Input Kosong** | `""` (kosong) | Memicu `ValueError` / HTTP 400 | **Pasti** |
| **Edge Case: Prefix > 32** | Prefix `33` | Memicu `ValueError` / HTTP 400 | **Pasti** |
| **Edge Case: Prefix Negatif** | Prefix `-1` | Memicu `ValueError` / HTTP 400 | **Pasti** |
| **API Endpoint: GET /** | `GET /` | Status `200 OK` (mengembalikan halaman web) | **Pasti** |
| **API Endpoint: GET /api/subnet Sukses** | `GET /api/subnet?ip=192.168.1.0&prefix=24` | Status `200 OK` dengan JSON hasil subnet | **Pasti** |
| **API Endpoint: Invalid / Missing Param** | `GET /api/subnet?ip=abc&prefix=24` atau parameter hilang / prefix non-integer (`prefix=abc`) | Status `400 Bad Request` dengan field `detail` (bukan 422) | **Pasti** |
| **VLSM Alokasi Normal** | Base: `192.168.1.0/24`<br>

<br>Kebutuhan: `[100, 50, 20, 2]` | Alokasi berurutan tanpa *overlap*:<br>

<br>• 100 host $\rightarrow$ `/25` (`.0`)<br>

<br>• 50 host $\rightarrow$ `/26` (`.128`)<br>

<br>• 20 host $\rightarrow$ `/27` (`.192`)<br>

<br>• 2 host $\rightarrow$ `/30` (`.224`) | **Pasti** |
| **VLSM Overflow / Kapasitas Kurang** | Base: `192.168.1.0/24`<br>

<br>Kebutuhan: `[200, 100]` | Ditolak (HTTP 400): Kebutuhan 200 host memerlukan blok 256 dan 100 host memerlukan blok 128, total 384 melebihi kapasitas 256 pada `/24`. | **Pasti** |
| **VLSM Edge Case: Kebutuhan Kosong** | Base: `192.168.1.0/24`<br>

<br>Kebutuhan: `[]` (kosong) | Memicu `ValueError` / HTTP 400 karena daftar kebutuhan tidak boleh kosong. | **Pasti** |
| **VLSM Edge Case: Kebutuhan $\le 0$** | Base: `192.168.1.0/24`<br>

<br>Kebutuhan: `[50, 0]` atau `[50, -2]` | Memicu `ValueError` / HTTP 400 karena kebutuhan host minimal 1. | **Pasti** |
| **VLSM Edge Case: Network CIDR Invalid** | Base: `192.168.1.999/24`<br>

<br>Kebutuhan: `[10]` | Memicu `ValueError` / HTTP 400 karena alamat jaringan dasar tidak valid. | **Pasti** |
| **VLSM Edge Case: Host Bits Non-Nol** | Base: `192.168.1.5/24`<br>

<br>Kebutuhan: `[10]` | Memicu `ValueError` / HTTP 400 karena `192.168.1.5` bukan alamat jaringan yang valid (bit host tidak nol). | **Pasti** |

---

## 7. Di Luar Cakupan (Out of Scope)

* Dukungan pengalamatan IPv6 (kalkulator ini difokuskan khusus untuk IPv4 sesuai kurikulum dasar TKJ).
* Penyimpanan data persisten (database) atau sistem autentikasi/manajemen pengguna.
* Visualisasi topologi jaringan fisik secara grafis berbasis node/router (hanya berfokus pada tabel kalkulasi IP dan alokasi blok).