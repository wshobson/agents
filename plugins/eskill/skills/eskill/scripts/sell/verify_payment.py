#!/usr/bin/env python3
"""verify_payment.py — Xác minh thanh toán USDT (TRC20) qua tronscan public API.

Chạy:
    python3 verify_payment.py <TXID> <số_tiền_kỳ_vọng> [địa_chỉ_nhận_kỳ_vọng]

Output: PASS nếu địa chỉ nhận + số tiền + confirmations đều khớp, FAIL kèm lý do.
Chỉ tin bằng chứng blockchain — không tin ảnh chụp.

Không cần API key — dùng tronscan public endpoint.
"""
import json
import sys
import urllib.request

TRONSCAN_API = "https://apilist.tronscanapi.com/api/transaction-info?hash={txid}"
MIN_CONFIRMATIONS = 19  # TRC20 an toàn sau ~19 blocks (~1-2 phút)


def fetch_tx(txid: str) -> dict:
    url = TRONSCAN_API.format(txid=txid.strip())
    req = urllib.request.Request(url, headers={"User-Agent": "eskill-sell/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def verify(txid: str, expected_amount: float, expected_to: str = "") -> tuple[bool, str]:
    txid = txid.strip()
    if len(txid) != 64 or not all(c in "0123456789abcdefABCDEF" for c in txid):
        return False, f"TXID không hợp lệ (cần 64 ký tự hex): {txid[:20]}…"
    try:
        data = fetch_tx(txid)
    except Exception as e:
        return False, f"Lỗi tra cứu tronscan: {e}"

    # TXID tồn tại không?
    if not data.get("hash"):
        return False, "TXID không tồn tại trên blockchain (khách gửi TXID giả?)"

    # Token phải là USDT (TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t) — tránh token scam
    if data.get("contractData", {}).get("contract_address", "").lower() != "tr7nhqjekqxgtci8q8zy4pl8otszgjlj6t":
        return False, "Token KHÔNG phải USDT TRC20 — từ chối"

    # Địa chỉ nhận
    to_addr = data.get("toAddress", "")
    if expected_to:
        expected_to = expected_to.strip().lower()
        if to_addr.lower() != expected_to:
            return False, f"Địa chỉ nhận không khớp: {to_addr} ≠ {expected_to}"

    # Số tiền (đơn vị sun, 1 USDT = 1e6 sun)
    try:
        amount = int(data.get("contractData", {}).get("amount", 0)) / 1e6
    except (TypeError, ValueError):
        amount = 0.0
    if amount < expected_amount - 0.01:  # sai số 0.01 USDT
        return False, f"Số tiền không đủ: {amount:.2f} < {expected_amount:.2f}"

    # Confirmations
    confirmed = data.get("confirmed", False)
    if not confirmed:
        return False, "Giao dịch chưa confirmed — chờ vài phút rồi thử lại"

    return True, (
        f"PASS — USDT {amount:.2f} → {to_addr[:8]}…{to_addr[-6:]} | "
        f"from {data.get('ownerAddress', '')[:8]}… | confirmed"
    )


def main():
    if len(sys.argv) < 3:
        print("Dùng: python3 verify_payment.py <TXID> <số_tiền_kỳ_vọng> [địa_chỉ_nhận_kỳ_vọng]")
        sys.exit(2)
    ok, msg = verify(sys.argv[1], float(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "")
    print(("✅ " if ok else "❌ ") + msg)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
