# Naming — Đặt tên skill theo chuẩn Apple (đúc từ egram Trụ "Đặt tên dự án")

Spec agentskills.io quy định quy tắc KỸ THUẬT (chữ thường + gạch nối, = tên thư mục).
Lớp này là quy tắc THƯƠNG HIỆU — làm skill thành 1 gia đình nhận diện được.

## Công thức Apple

**tiền tố gia đình + 1 từ chính + (hậu tố phân cấp)** — `i` → iPhone/iPad/iMac · `Mac` → MacBook/Mac mini.

## Quy tắc cho hệ e-family (prefix `e`)

0. **2 tầng tên — brand ≠ prefix**: brand = **tên doanh nghiệp của bạn** (tên hiển thị) · prefix sản phẩm = **`e`** (tên dự án/skill). Khi cần nhấn brand: `Brand eSkill`. KHÔNG nhét brand vào tên skill (`brand-skill` = 4 âm tiết, hỏng).
1. **Chọn 1 tiền tố gia đình DUY NHẤT** — 1-3 ký tự, dễ gõ, không dấu. Hệ này: **`e`** → egram, eSeed, eScan, eSkill, eShare...
2. **Tên = tiền tố + 1 từ chính** — từ chính nói ĐÚNG việc: Skill (meta tạo skill), Seed, Scan, Gram (tin nhắn). KHÔNG 2 từ chính, không mô tả lan man.
3. **Hậu tố phân cấp CHỈ KHI CẦN** — Air/Mini/Pro/Ultra. Đừng gắn Pro cho mọi thứ.
4. **Cách viết nhất quán**: folder/repo = chữ thường (`eskill`) · tên hiển thị = camelCase (`eSkill`). KHÔNG gạch dưới, không số, không viết hoa lộn xộn.
5. **Không số phiên bản trong tên** — version để sau (v2).
6. **Kiểm tra trước khi đặt**: ≤3 âm tiết · gõ không dấu dễ dàng · không trùng skill khác · nghe 1 lần nhớ được.

## Áp dụng vào SKILL.md

- `name` frontmatter = folder = chữ thường (`eskill`) — khớp quy tắc spec
- Nếu đăng marketplace: `metadata.display_name: eSkill` (camelCase hiển thị)

## Checklist

- [ ] Cùng tiền tố gia đình (`e-`)
- [ ] 1 từ chính mô tả đúng việc
- [ ] Không số, không gạch dưới, không 2 từ chính
- [ ] Folder `eskill` · hiển thị `eSkill`
