---
name: echeck
description: >
  Kiểm tra 1 URL còn hoạt động không (status + title + thời gian phản hồi).
  Dùng khi cần verify trang web/link còn sống, kiểm tra link hỏng trong tài liệu,
  hoặc xác nhận site đã deploy thành công. Trả kết quả 1 dòng: ✅/❌ + status + title.
license: MIT
metadata:
  author: hedra
  version: "1.0"
---

# echeck — Kiểm tra URL còn sống

## Quickstart

1. `Kiểm tra https://example.com còn chạy không` → trả ✅/❌ + status + title
2. `Quét mọi link trong <file.md> xem link nào hỏng` → bảng link hỏng
3. `Xác nhận site vừa deploy chưa` → 3 lần thử, 30s giãn cách

## Quy tắc

1. **Fetch bằng requests (timeout 15s)** — KHÔNG dùng browser trừ khi cần JS
2. **Chuẩn hoá URL**: thêm `https://` nếu thiếu scheme; bỏ khoảng trắng
3. **Phân loại kết quả**:
   - 200 → `✅ 200 · <title>`
   - 3xx → `🔁 <code> → <Location>` (đi tiếp tối đa 2 hop)
   - 4xx/5xx → `❌ <code> · <lý do ngắn>`
   - timeout/lỗi mạng → `⚠️ timeout/không kết nối được`
4. **Cloudflare/403** (`cf-browser-verify`, "Just a moment") → báo `🔒 bị chặn (Cloudflare)` — KHÔNG coi là chết
5. **JS-render**: nếu HTML rỗng nhưng site trả 200 → ghi chú "có thể cần JS" — không báo lỗi

## Code mẫu

```python
import re, requests

def check_url(url, timeout=15, max_hop=2):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    hop = 0
    while hop <= max_hop:
        try:
            r = requests.get(url, timeout=timeout, allow_redirects=False,
                             headers={"User-Agent": "Mozilla/5.0"})
            if 300 <= r.status_code < 400 and r.headers.get("Location"):
                url = r.headers["Location"]
                hop += 1
                continue
            if "cf-browser-verify" in r.text or "Just a moment" in r.text:
                return "🔒 bị chặn (Cloudflare)", r.status_code
            title = re.search(r"<title[^>]*>([^<]+)</title>", r.text, re.I)
            return ("✅" if r.status_code == 200 else "❌") + f" {r.status_code}", (title.group(1).strip()[:60] if title else "")
        except requests.exceptions.Timeout:
            return "⚠️ timeout", None
        except Exception as e:
            return f"⚠️ {str(e)[:40]}", None
    return "🔁 quá nhiều redirect", None
```

## Ví dụ

- `echeck("https://example.com")` → `✅ 200 · Example Domain`
- `echeck("https://example.com/404")` → `❌ 404`
- `echeck("https://example.com")` (Cloudflare) → `🔒 bị chặn (Cloudflare), 403`

## Checklist

- [ ] URL chuẩn hoá (https:// + trim)
- [ ] 200/3xx/4xx/5xx/timeout/Cloudflare phân biệt rõ
- [ ] Redirect tối đa 2 hop
- [ ] Báo title khi có — HTML escape
- [ ] Không crash với mọi input ('' · 'abc' · 'http://' trần)

## Bẫy

1. **Cloudflare ≠ chết** — "Just a moment" là chặn bot, site vẫn sống
2. **Redirect về http** — giữ nguyên, đừng tự nâng lên https
3. **Timeout là chậm, không phải hỏng** — ghi ⚠️, đề nghị thử lại sau 30s
