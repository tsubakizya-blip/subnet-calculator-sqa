import pytest
from fastapi.testclient import TestClient

from main import app, alokasi_vlsm, hitung_subnet

client = TestClient(app)


# ---------------------------------------------------------------------------
# Test Unit: hitung_subnet (Kasus Normal & Khusus)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "ip,prefix,expected",
    [
        (
            "172.16.5.130",
            25,
            {
                "mask": "255.255.255.128",
                "network": "172.16.5.128",
                "broadcast": "172.16.5.255",
                "first_host": "172.16.5.129",
                "last_host": "172.16.5.254",
                "usable_hosts": 126,
            },
        ),
        (
            "10.0.0.0",
            30,
            {
                "mask": "255.255.255.252",
                "network": "10.0.0.0",
                "broadcast": "10.0.0.3",
                "first_host": "10.0.0.1",
                "last_host": "10.0.0.2",
                "usable_hosts": 2,
            },
        ),
        (
            "192.168.1.0",
            31,
            {
                "mask": "255.255.255.254",
                "network": "192.168.1.0",
                "broadcast": None,
                "first_host": "192.168.1.0",
                "last_host": "192.168.1.1",
                "usable_hosts": 2,
            },
        ),
        (
            "192.168.1.5",
            32,
            {
                "mask": "255.255.255.255",
                "network": "192.168.1.5",
                "broadcast": None,
                "first_host": "192.168.1.5",
                "last_host": "192.168.1.5",
                "usable_hosts": 1,
            },
        ),
    ],
)
def test_hitung_subnet_valid(ip, prefix, expected):
    result = hitung_subnet(ip, prefix)
    assert result == expected


# ---------------------------------------------------------------------------
# Test Unit: hitung_subnet (Edge Cases & Validasi Input)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "ip,prefix",
    [
        ("256.1.1.1", 24),     # Oktet > 255
        ("192.168.01.1", 24),  # Leading zero / zero-padding
        ("192.168.1", 24),     # Format inkomplet (< 4 oktet)
        ("abc", 24),           # Non-numeric
        ("", 24),              # Input kosong
        ("192.168.1.1", 33),   # Prefix > 32
        ("192.168.1.1", -1),   # Prefix negatif
    ],
)
def test_hitung_subnet_invalid(ip, prefix):
    with pytest.raises(ValueError):
        hitung_subnet(ip, prefix)


# ---------------------------------------------------------------------------
# Test API: GET / (Halaman Statis)
# ---------------------------------------------------------------------------
def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


# ---------------------------------------------------------------------------
# Test API: GET /api/subnet (Sukses)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "ip,prefix,expected",
    [
        (
            "192.168.1.0",
            24,
            {
                "mask": "255.255.255.0",
                "network": "192.168.1.0",
                "broadcast": "192.168.1.255",
                "first_host": "192.168.1.1",
                "last_host": "192.168.1.254",
                "usable_hosts": 254,
            },
        ),
        (
            "172.16.5.130",
            25,
            {
                "mask": "255.255.255.128",
                "network": "172.16.5.128",
                "broadcast": "172.16.5.255",
                "first_host": "172.16.5.129",
                "last_host": "172.16.5.254",
                "usable_hosts": 126,
            },
        ),
        (
            "192.168.1.0",
            31,
            {
                "mask": "255.255.255.254",
                "network": "192.168.1.0",
                "broadcast": None,
                "first_host": "192.168.1.0",
                "last_host": "192.168.1.1",
                "usable_hosts": 2,
            },
        ),
        (
            "192.168.1.5",
            32,
            {
                "mask": "255.255.255.255",
                "network": "192.168.1.5",
                "broadcast": None,
                "first_host": "192.168.1.5",
                "last_host": "192.168.1.5",
                "usable_hosts": 1,
            },
        ),
    ],
)
def test_api_subnet_success(ip, prefix, expected):
    response = client.get(f"/api/subnet?ip={ip}&prefix={prefix}")
    assert response.status_code == 200
    assert response.json() == expected


# ---------------------------------------------------------------------------
# Test API: GET /api/subnet (Invalid / Missing Param -> HTTP 400 Bad Request)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "params",
    [
        {"ip": "abc", "prefix": 24},           # IP non-numeric
        {"ip": "192.168.1.1"},                 # Parameter prefix hilang
        {"prefix": 24},                        # Parameter IP hilang
        {"ip": "192.168.1.1", "prefix": "abc"},  # Prefix non-integer (bukan 422, harus 400)
        {"ip": "256.1.1.1", "prefix": 24},    # Oktet > 255
        {"ip": "192.168.01.1", "prefix": 24},  # Leading zero
        {"ip": "192.168.1", "prefix": 24},     # Format inkomplet
        {"ip": "", "prefix": 24},              # IP kosong
        {"ip": "192.168.1.1", "prefix": 33},   # Prefix > 32
        {"ip": "192.168.1.1", "prefix": -1},   # Prefix negatif
    ],
)
def test_api_subnet_invalid_params(params):
    response = client.get("/api/subnet", params=params)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], str)


# ---------------------------------------------------------------------------
# Test Unit: alokasi_vlsm (Kasus Normal)
# ---------------------------------------------------------------------------
def test_alokasi_vlsm_normal():
    """VLSM Alokasi Normal: 192.168.1.0/24, kebutuhan [100, 50, 20, 2]"""
    hasil = alokasi_vlsm("192.168.1.0/24", [100, 50, 20, 2])
    assert len(hasil) == 4

    # Subnet 1: 100 host → /25 (blok 128, usable 126)
    s1 = hasil[0]
    assert s1["kebutuhan"] == 100
    assert s1["network_cidr"] == "192.168.1.0/25"
    assert s1["network"] == "192.168.1.0"
    assert s1["broadcast"] == "192.168.1.127"
    assert s1["first_host"] == "192.168.1.1"
    assert s1["last_host"] == "192.168.1.126"
    assert s1["usable_hosts"] == 126
    assert s1["mask"] == "255.255.255.128"

    # Subnet 2: 50 host → /26 (blok 64, usable 62)
    s2 = hasil[1]
    assert s2["kebutuhan"] == 50
    assert s2["network_cidr"] == "192.168.1.128/26"
    assert s2["network"] == "192.168.1.128"
    assert s2["broadcast"] == "192.168.1.191"
    assert s2["first_host"] == "192.168.1.129"
    assert s2["last_host"] == "192.168.1.190"
    assert s2["usable_hosts"] == 62
    assert s2["mask"] == "255.255.255.192"

    # Subnet 3: 20 host → /27 (blok 32, usable 30)
    s3 = hasil[2]
    assert s3["kebutuhan"] == 20
    assert s3["network_cidr"] == "192.168.1.192/27"
    assert s3["network"] == "192.168.1.192"
    assert s3["broadcast"] == "192.168.1.223"
    assert s3["first_host"] == "192.168.1.193"
    assert s3["last_host"] == "192.168.1.222"
    assert s3["usable_hosts"] == 30
    assert s3["mask"] == "255.255.255.224"

    # Subnet 4: 2 host → /30 (blok 4, usable 2)
    s4 = hasil[3]
    assert s4["kebutuhan"] == 2
    assert s4["network_cidr"] == "192.168.1.224/30"
    assert s4["network"] == "192.168.1.224"
    assert s4["broadcast"] == "192.168.1.227"
    assert s4["first_host"] == "192.168.1.225"
    assert s4["last_host"] == "192.168.1.226"
    assert s4["usable_hosts"] == 2
    assert s4["mask"] == "255.255.255.252"


def test_alokasi_vlsm_urutan_descending():
    """Input tidak urut harus diurutkan descending sebelum dialokasikan."""
    hasil = alokasi_vlsm("192.168.1.0/24", [2, 20, 50, 100])
    # Urutan output harus descending berdasarkan kebutuhan
    assert hasil[0]["kebutuhan"] == 100
    assert hasil[1]["kebutuhan"] == 50
    assert hasil[2]["kebutuhan"] == 20
    assert hasil[3]["kebutuhan"] == 2


# ---------------------------------------------------------------------------
# Test Unit: alokasi_vlsm (Edge Cases — harus raise ValueError)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "network_cidr,kebutuhan_host",
    [
        # Overflow: total blok 256+128=384 > kapasitas 256
        ("192.168.1.0/24", [200, 100]),
        # Kebutuhan kosong
        ("192.168.1.0/24", []),
        # Kebutuhan 0
        ("192.168.1.0/24", [50, 0]),
        # Kebutuhan negatif
        ("192.168.1.0/24", [50, -2]),
        # Network CIDR tidak valid (oktet > 255)
        ("192.168.1.999/24", [10]),
        # Host bits non-nol (bukan alamat network)
        ("192.168.1.5/24", [10]),
    ],
)
def test_alokasi_vlsm_invalid(network_cidr, kebutuhan_host):
    with pytest.raises(ValueError):
        alokasi_vlsm(network_cidr, kebutuhan_host)


# ---------------------------------------------------------------------------
# Test API: POST /api/vlsm (Sukses)
# ---------------------------------------------------------------------------
def test_api_vlsm_success():
    """POST /api/vlsm dengan input valid harus mengembalikan 200 dan list alokasi."""
    payload = {"network": "192.168.1.0/24", "kebutuhan_host": [100, 50, 20, 2]}
    response = client.post("/api/vlsm", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4

    # Verifikasi subnet pertama
    assert data[0]["kebutuhan"] == 100
    assert data[0]["network_cidr"] == "192.168.1.0/25"
    assert data[0]["network"] == "192.168.1.0"
    assert data[0]["broadcast"] == "192.168.1.127"
    assert data[0]["usable_hosts"] == 126

    # Verifikasi subnet terakhir
    assert data[3]["kebutuhan"] == 2
    assert data[3]["network_cidr"] == "192.168.1.224/30"
    assert data[3]["usable_hosts"] == 2


# ---------------------------------------------------------------------------
# Test API: POST /api/vlsm (Error — HTTP 400 Bad Request)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "payload",
    [
        # Overflow
        {"network": "192.168.1.0/24", "kebutuhan_host": [200, 100]},
        # Kebutuhan kosong
        {"network": "192.168.1.0/24", "kebutuhan_host": []},
        # Kebutuhan mengandung 0
        {"network": "192.168.1.0/24", "kebutuhan_host": [50, 0]},
        # Kebutuhan negatif
        {"network": "192.168.1.0/24", "kebutuhan_host": [50, -2]},
        # Network CIDR tidak valid
        {"network": "192.168.1.999/24", "kebutuhan_host": [10]},
        # Host bits non-nol
        {"network": "192.168.1.5/24", "kebutuhan_host": [10]},
        # Field 'network' hilang
        {"kebutuhan_host": [10]},
        # Field 'kebutuhan_host' hilang
        {"network": "192.168.1.0/24"},
    ],
)
def test_api_vlsm_invalid(payload):
    response = client.post("/api/vlsm", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], str)
