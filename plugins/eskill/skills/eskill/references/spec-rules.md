# Spec Rules — Agent Skills theo agentskills.io (spec chính thức)

## Frontmatter

| Field | Bắt buộc | Ràng buộc |
|---|---|---|
| `name` | ✅ | 1-64 ký tự · chỉ chữ thường + số + gạch nối `-` · không bắt đầu/kết thúc bằng `-` · không `--` · **PHẢI khớp tên thư mục** |
| `description` | ✅ | 1-1024 ký tự · mô tả CẢ "làm gì" LẪN "khi nào dùng" · kèm trigger keyword |
| `license` | tùy | tên license hoặc file LICENSE đính kèm |
| `compatibility` | tùy | môi trường yêu cầu (≤500 ký tự) — chỉ khi thật cần |
| `metadata` | tùy | key-value tùy ý (author, version...) |
| `allowed-tools` | tùy | tool pre-approved (experimental) |

Mẫu:
```yaml
---
name: pdf-processing
description: Trích text PDF, điền form, gộp file. Dùng khi xử lý tài liệu PDF.
license: MIT
metadata:
  author: <your-name>
  version: "1.0"
---
```

## Body

- Không giới hạn format — khuyến nghị: hướng dẫn từng bước · ví dụ input/output · edge cases
- **Mỗi mảng kèm ví dụ input → output** (spec khuyến nghị) — người đọc biết chính xác vào ra
- **Toàn bộ SKILL.md được load khi skill kích hoạt** → giữ < 500 dòng / < 5000 token
- Cấu trúc lặp đều (kinh nghiệm egram): **quy tắc → code mẫu → checklist** mỗi mảng

## Progressive disclosure (3 tầng)

1. **Metadata** (~100 token): name + description — load ở startup MỌI session
2. **SKILL.md body** (<5000 token): load khi skill được kích hoạt
3. **Resources** (references/ scripts/ assets/): load theo nhu cầu — file nhỏ, focus 1 chủ đề

## File references

- Dùng đường dẫn **tương đối** từ gốc skill: `references/REFERENCE.md`
- **1 cấp duy nhất** từ SKILL.md — cấm lồng sâu (references → con → cháu)
- Không include file ngoài thư mục skill

## Validation

```bash
skills-ref validate ./my-skill     # tool chính thức (npm)
python3 scripts/validate-skill.py ./my-skill [--leak]   # bản tự viết (trong eskill)
```

Chạy validate TRƯỚC khi coi skill là xong — bắt: frontmatter hỏng, name sai quy tắc, ref vỡ, >500 dòng.
