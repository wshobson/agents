# Checklist Thương Mại — chuẩn bị skill bán / public

Lỗi kinh điển egram v1: lộ chat_id thật, path home cá nhân, tên dịch vụ nội bộ trong code mẫu — phải sửa hàng loạt trước khi public — phải sửa hàng loạt trước khi public. Làm HỆ THỐNG, không làm tay.

## 1. Sanitize rò rỉ (chạy script, không grep tay)

```bash
python3 scripts/validate-skill.py <skill-dir> --leak
```

Bắt: token (`bot\d+:` · `sk-...` · `api_key=...`) · path cá nhân (`/Users/`, `/home/`) · chat_id · brand nội bộ · tên dịch vụ riêng. Nếu dương tính → thay placeholder (`<your_chat_id>`, `<PROJECT_ROOT>`, tên generic).

## 2. Kiểm tra từng file

- [ ] `SKILL.md` — không hardcode path máy, brand nội bộ, ID thật
- [ ] Version semver thống nhất trên mọi file (SKILL.md metadata.version · eval-results.json · README · plugin.json · tag) + `RELEASE-NOTES.md` có mục tương ứng
- [ ] `references/*.py` — code mẫu không import thư viện nội bộ (`tg_ui`, `auto`), không token
- [ ] `README.md` — **đồng bộ với SKILL.md**: số trụ, tên skill, cấu trúc thật (egram v1: README ghi 8 trụ/Hedragram khi skill đã 9 trụ/egram)
- [ ] Không file rác: `.bak*`, `*.pyc`, `.DS_Store`, thư mục rỗng
- [ ] `references/` không chứa symlink vỡ — xóa quy tắc symlink khỏi doc nếu không còn là symlink

## 3. License + phân phối

- [ ] `LICENSE` (MIT/BSD cho bán thương mại) + khai `license` trong frontmatter
- [ ] **Bán quốc tế → dịch SKILL.md + README sang tiếng Anh** (spec gốc + marketplace đều EN)
- [ ] Quyết định: private repo (bán theo quyền) hay public (mọi người tải)
- [ ] Zip đóng gói: `zip -r` bỏ `.git/*` + `*.zip` — kiểm tra lại bằng `unzip -l` trước khi gửi
- [ ] Xác minh code tham khảo từ nguồn khác (monitor.py kiểu Trung Quốc = rủi ro bản quyền → thay bằng code tự viết)
- [ ] (Marketplace) Đăng chợ skill: tạo `agents/openai.yaml` (xem `references/openai-yaml.md`) + đăng ký repo qua skills.sh/plugin marketplace — ngoài zip bán tay

## 4. Bằng chứng hoạt động

- [ ] Smoke test đóng gói trong skill chạy PASS trên máy sạch (không có env nội bộ)
- [ ] `validate-skill.py` chạy PASS
- [ ] Test 1 lần trên máy khác / agent mới trước khi giới thiệu cho người mua

## 5. An toàn khi CÀI skill từ nguồn lạ (phía người dùng)

- Skill = script thực thi được — trước khi cài skill không tin cậy: **đọc hết `scripts/` trước khi chạy**
- Không tự ý chạy script lạ; kiểm tra nó ghi/gửi gì ra ngoài (token, network call)
