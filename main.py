from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="Subnet Calculator")

BASE_DIR = Path(__file__).resolve().parent


def _ip_to_int(octets: list[int]) -> int:
    return (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]


def _int_to_ip(val: int) -> str:
    return f"{(val >> 24) & 255}.{(val >> 16) & 255}.{(val >> 8) & 255}.{val & 255}"


def hitung_subnet(ip: str, prefix: int) -> dict[str, Any]:
    # Validasi parameter IP
    if not isinstance(ip, str):
        raise ValueError("Alamat IP harus berupa string.")

    if not ip or ip != ip.strip() or " " in ip:
        raise ValueError("Format IP Address tidak valid (kosong atau mengandung spasi).")

    octets_str = ip.split(".")
    if len(octets_str) != 4:
        raise ValueError(
            f"Format IP Address tidak valid: harus tepat 4 oktet (diterima {len(octets_str)} oktet)."
        )

    octets: list[int] = []
    for octet_str in octets_str:
        if not octet_str or not all("0" <= c <= "9" for c in octet_str):
            raise ValueError(f"Oktet IP harus berupa angka positif: '{octet_str}'.")

        # Larangan zero-padding (misal '01', '001')
        if len(octet_str) > 1 and octet_str.startswith("0"):
            raise ValueError(
                f"Zero-padding tidak diizinkan pada oktet IP: '{octet_str}'."
            )

        val = int(octet_str)
        if val < 0 or val > 255:
            raise ValueError(f"Nilai oktet di luar rentang valid 0-255: {val}.")

        octets.append(val)

    # Validasi parameter Prefix
    if not isinstance(prefix, int) or isinstance(prefix, bool):
        raise ValueError("Prefix harus berupa bilangan bulat.")

    if prefix < 0 or prefix > 32:
        raise ValueError(f"Prefix harus berada pada rentang 0-32 (diterima {prefix}).")

    # Hitung subnet mask integer
    if prefix == 0:
        mask_int = 0
    else:
        mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

    # Representasi integer IP
    ip_int = _ip_to_int(octets)

    # Hitung Network Address dengan operasi bitwise AND antara IP dan subnet mask
    network_int = ip_int & mask_int

    mask = _int_to_ip(mask_int)
    network = _int_to_ip(network_int)

    # Perhitungan khusus berdasarkan prefix
    if prefix == 32:
        broadcast = None
        first_host = network
        last_host = network
        usable_hosts = 1
    elif prefix == 31:
        # RFC 3021 Point-to-Point
        broadcast = None
        first_host = network
        last_host = _int_to_ip(network_int + 1)
        usable_hosts = 2
    else:
        # Standard prefix /0 s.d. /30
        wildcard_int = (1 << (32 - prefix)) - 1
        broadcast_int = network_int | wildcard_int
        broadcast = _int_to_ip(broadcast_int)
        first_host = _int_to_ip(network_int + 1)
        last_host = _int_to_ip(broadcast_int - 1)
        usable_hosts = (1 << (32 - prefix)) - 2

    return {
        "mask": mask,
        "network": network,
        "broadcast": broadcast,
        "first_host": first_host,
        "last_host": last_host,
        "usable_hosts": usable_hosts,
    }


# ---------------------------------------------------------------------------
# Exception Handlers: Override 422 ke 400 Bad Request
# ---------------------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    if errors:
        first_err = errors[0]
        loc = " -> ".join(str(x) for x in first_err.get("loc", []))
        msg = first_err.get("msg", "Validation error")
        detail_msg = f"{loc}: {msg}" if loc else msg
    else:
        detail_msg = "Format data masukan tidak valid."

    return JSONResponse(
        status_code=400,
        content={"detail": detail_msg},
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def get_root():
    index_path = BASE_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html tidak ditemukan.")
    return HTMLResponse(content=index_path.read_text(encoding="utf-8"), status_code=200)


@app.get("/api/subnet")
def api_subnet(request: Request):
    ip = request.query_params.get("ip")
    prefix_str = request.query_params.get("prefix")

    if ip is None:
        raise HTTPException(
            status_code=400, detail="Parameter 'ip' wajib disertakan dalam query."
        )

    if prefix_str is None:
        raise HTTPException(
            status_code=400, detail="Parameter 'prefix' wajib disertakan dalam query."
        )

    try:
        prefix = int(prefix_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=400,
            detail=f"Prefix harus berupa bilangan bulat antara 0 dan 32 (diterima '{prefix_str}').",
        )

    try:
        return hitung_subnet(ip, prefix)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
