---
name: template-skill          # ← ĐỔI: chữ thường + gạch nối, PHẢI = tên thư mục (xem references/naming.md)
description: >               # ← ĐỔI: ≤1024 ký tự — "làm gì" + "khi nào dùng" + trigger keyword, viết PUSHY
  Mô tả skill làm gì và khi nào dùng. Nêu rõ trigger: câu chữ user hay dùng, context đi kèm.
  Dùng khi user nói: "...", "...", hoặc làm việc với .... Dù user không gõ đúng tên skill vẫn phải bật
  (chống undertrigger).
# license: MIT              # ← tùy chọn: tên license (bán thương mại thì BẮT BUỘC)
# compatibility:            # ← tùy chọn: yêu cầu môi trường (chỉ khi thật cần)
# metadata:                 # ← tùy chọn: author, version... (đăng chợ: display_name eFamily)
#   author: <your-name>
#   version: "1.0"
---

# <Tên skill> — 1 dòng giá trị

## <Mảng 1 — theo kim chỉ nam đã chọn>

**Quy tắc:**
1. ...
2. ...

**Code mẫu:**
```python
# ví dụ ngắn chạy được
```

**Ví dụ input → output:**
```
Input: ...
Output: ...
```

**Checklist:**
- [ ] ...

## <Mảng 2>

...

## Bẫy — đừng lặp (tài sản lớn nhất của skill)

1. **Triệu chứng lỗi** — fix: ...
2. **Triệu chứng lỗi** — fix: ...

## References (nếu cần — ref 1 cấp, đường dẫn tương đối)

- `references/xxx.md` — mô tả ngắn khi nào mở file này
