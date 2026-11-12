import pytest
from fastapi.testclient import TestClient

from main import app, hitung_subnet

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
