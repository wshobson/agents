#!/usr/bin/env python3
"""sales_bot.py — Bot Telegram bán quyền truy cập repo (access selling).

Luồng:
    /buy                          → tạo đơn + gửi địa chỉ OKX USDT + số tiền độc nhất
    /paid <TXID> <gh_username>    → verify blockchain → PASS thì cấp quyền repo
    (admin) /grant <u> · /revoke <u> · /sales

Chạy: python3 sales_bot.py            (cần .env cạnh script — xem .env.mẫu)
Config: TELEGRAM_BOT_TOKEN · SELLER_CHAT_ID (admin) · OKX_USDT_ADDRESS ·
        NETWORK=TRC20 · PRICE_USDT=50 · REPO=owner/name · MIN_CONFIRMATIONS=19

An toàn (trụ 1 egram): lệnh admin whitelist theo chat_id · log mọi lỗi kèm timestamp ·
chỉ tin kết quả verify_payment.py (blockchain), không tin ảnh chụp.
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE = HERE / "sales.json"
LOG = HERE / "sales.log"

# ── .env loader (12-factor: không hardcode) ──
def load_env():
    env = {}
    p = HERE / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip("\"'")
    return env

ENV = load_env()
TOKEN = ENV.get("TELEGRAM_BOT_TOKEN", "")
ADMIN = ENV.get("SELLER_CHAT_ID", "")
ADDRESS = ENV.get("OKX_USDT_ADDRESS", "")
PRICE = float(ENV.get("PRICE_USDT", "50"))
REPO = ENV.get("REPO", "")
API = f"https://api.telegram.org/bot{TOKEN}"

def log(msg):
    line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {msg}"
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

# ── state (nguồn sự thật trên disk — trụ 6) ──
def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"orders": [], "seq": 1}

def save_state(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def tg(method, payload):
    req = urllib.request.Request(f"{API}/{method}", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def reply(chat_id, text):
    try:
        tg("sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
    except Exception as e:
        log(f"LỖI gửi tin tới {chat_id}: {e}")

# ── số tiền độc nhất: giá + đuôi mã đơn (vd 50.37) ──
def order_amount(order_id):
    return round(PRICE + (order_id % 100) / 100, 2)

def find_order(state, chat_id):
    return next((o for o in state["orders"] if o["chat_id"] == chat_id), None)

# ── verify + grant ──
def verify_payment(txid, amount):
    """Gọi verify_payment.py — trả (ok, message)."""
    r = subprocess.run([sys.executable, str(HERE / "verify_payment.py"),
                        txid, str(amount), ADDRESS], capture_output=True, text=True, timeout=60)
    out = (r.stdout or "").strip().splitlines()
    last = out[-1] if out else r.stderr.strip()
    return r.returncode == 0, last

def grant(user):
    r = subprocess.run(["bash", str(HERE / "grant_access.sh"), "grant", user],
                       capture_output=True, text=True, timeout=60)
    return r.returncode == 0, (r.stdout or r.stderr).strip()

# ── xử lý lệnh ──
def handle(cmd, args, chat_id):
    state = load_state()
    if cmd == "/buy":
        order = find_order(state, chat_id)
        if order and order["status"] in ("awaiting", "paid"):
            return f"⏳ Bạn có đơn <b>#{order['order_id']}</b> ({order['amount']:.2f} USDT) chưa hoàn tất. Gửi /paid để tiếp tục."
        seq = state["seq"]; state["seq"] += 1
        amt = order_amount(seq)
        state["orders"].append({"order_id": seq, "chat_id": chat_id, "amount": amt,
                                "status": "awaiting", "txid": "", "gh_user": "", "created": time.time()})
        save_state(state)
        return (f"🧾 Đơn <b>#{seq}</b> — {amt:.2f} USDT (TRC20)\n\n"
                f"📮 Chuyển đúng số tiền <b>{amt:.2f}</b> USDT tới:\n"
                f"<code>{ADDRESS}</code>\n"
                f"🌐 Mạng: <b>TRC20</b> (gửi nhầm mạng = mất tiền)\n\n"
                f"Sau khi chuyển, gửi: /paid &lt;TXID&gt; &lt;github_username&gt;")
    if cmd == "/paid":
        order = find_order(state, chat_id)
        if not order or order["status"] != "awaiting":
            return "Không có đơn đang chờ — gửi /buy trước."
        parts = args.split()
        if len(parts) < 2:
            return "Dùng: /paid &lt;TXID&gt; &lt;github_username&gt;"
        txid, user = parts[0], parts[1]
        order["txid"], order["gh_user"], order["status"] = txid, user, "paid"
        save_state(state)
        ok, msg = verify_payment(txid, order["amount"])
        order["status"] = "verified" if ok else "paid"
        order["verify_msg"] = msg
        save_state(state)
        if ok:
            gok, gmsg = grant(user)
            order["status"] = "granted" if gok else "verified"
            save_state(state)
            log(f"ĐƠN #{order['order_id']} khách {chat_id} trả {order['amount']:.2f} USDT — grant {user}: {'OK' if gok else gmsg}")
            if ADMIN and str(chat_id) != ADMIN:
                reply(ADMIN, f"💰 Đơn #{order['order_id']} — {order['amount']:.2f} USDT\nTXID: {txid[:16]}…\nGH: @{user}\n→ {'Đã cấp quyền' if gok else 'CẦN XỬ LÝ: ' + gmsg}")
            return (f"✅ <b>Thanh toán xác nhận</b> — {msg}\n"
                    f"→ Đã cấp quyền truy cập <b>{REPO}</b> cho @{user}\n"
                    f"Hướng dẫn: <code>git clone https://github.com/{REPO}.git</code> (cần đăng nhập GH bằng tài khoản @{user})")
        log(f"ĐƠN #{order['order_id']} verify FAIL: {msg}")
        return f"❌ {msg}\nKiểm tra lại TXID hoặc chờ confirmed rồi gửi lại /paid."
    if str(chat_id) == ADMIN:
        if cmd == "/grant" and args.strip():
            u = args.strip().split()[0]
            ok, m = grant(u)
            return ("✅ " if ok else "❌ ") + m
        if cmd == "/revoke" and args.strip():
            u = args.strip().split()[0]
            r = subprocess.run(["bash", str(HERE / "grant_access.sh"), "revoke", u],
                               capture_output=True, text=True, timeout=60)
            return (r.stdout or r.stderr).strip()
        if cmd == "/sales":
            orders = state["orders"]
            if not orders:
                return "Chưa có đơn nào."
            lines = [f"🧾 {len(orders)} đơn — {sum(o['amount'] for o in orders if o['status'] == 'granted'):.2f} USDT đã thu"]
            for o in orders[-10:]:
                lines.append(f"#{o['order_id']} {o['status']} {o['amount']:.2f}U @{o['gh_user'] or '-'} {o['txid'][:10] if o['txid'] else ''}")
            return "\n".join(lines)
    return ("Lệnh: /buy · /paid &lt;TXID&gt; &lt;username&gt;\n"
            "Liên hệ hỗ trợ: admin")

def main():
    if not TOKEN or not ADMIN or not ADDRESS or not REPO:
        log("LỖI: thiếu config — copy .env.mẫu thành .env và điền TELEGRAM_BOT_TOKEN/SELLER_CHAT_ID/OKX_USDT_ADDRESS/REPO")
        sys.exit(1)
    log(f"Sales bot chạy — repo {REPO} · giá {PRICE:.2f} USDT · admin {ADMIN}")
    offset = 0
    while True:
        try:
            updates = tg("getUpdates", {"offset": offset, "timeout": 30})
            for u in updates.get("result", []):
                offset = u["update_id"] + 1
                msg = u.get("message") or {}
                text = (msg.get("text") or "").strip()
                chat_id = (msg.get("chat") or {}).get("id")
                if not text or chat_id is None:
                    continue
                cmd, _, args = text.partition(" ")
                if cmd in ("/buy", "/paid", "/grant", "/revoke", "/sales"):
                    try:
                        reply(chat_id, handle(cmd, args.strip(), chat_id))
                    except Exception as e:
                        log(f"LỖI xử lý {cmd} từ {chat_id}: {e}")
                        reply(chat_id, "Lỗi hệ thống — thử lại sau.")
        except Exception as e:
            log(f"LỖI long-poll: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
