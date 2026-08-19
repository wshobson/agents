# 12-Factor for Skills — Trụ 5: vận hành skill bền (theo 12-Factor App)

Adapt chuẩn vận hành app (Heroku) sang bảo trì skill — skill sống lâu, không phải 1 file chết.

## 12 nguyên tắc (chuyển nghĩa cho skill)

1. **Codebase**: 1 skill = 1 thư mục, git-friendly — mọi thứ version control được
2. **Dependencies**: skill TỰ CHỨA (self-contained) — không trỏ ra path/code ngoài thư mục (lỗi egram v1: references trỏ `sale/seeding/auto/` — vỡ)
3. **Config**: mọi tham số có thể đổi → `.env`/frontmatter, KHÔNG hardcode trong SKILL.md (vd ngưỡng gate: MIN_VIEWS/PASS_DELTA)
4. **Backing services**: state trên disk (file JSON) — không lệ thuộc session/trí nhớ
5. **Build/release/run**: phân tách — SKILL.md (thiết kế) · references/ (tài liệu) · scripts/ (chạy) — đổi cái nào cũng không vỡ cái kia
6. **Process**: 1 skill = 1 việc (single responsibility) — đừng gộp "tạo skill + đo ads + bán hàng" vào 1 skill
7. **Port binding**: agent mới mở skill là tự đủ context — không cần hỏi lại lịch sử (progressive disclosure đủ)
8. **Concurrency**: references/ tách theo chủ đề — 2 agent cùng đọc 2 file không cạnh tranh context
9. **Disposability**: script chạy nhanh, thoát sạch — smoke test 1 lệnh, không giữ state
10. **Dev/prod parity**: test trên máy THẬT của user — forward-test = môi trường thật
11. **Logs**: bằng chứng = log — smoke test PASS/FAIL in ra, không "tin lời"
12. **Admin process**: validator chạy định kỳ (validate-skill.py) như admin script

## Quy tắc chốt

- **Idempotent**: mọi patch/script chạy lại 100 lần an toàn (có `.bak` trước khi sửa)
- **Đổi tên/version đồng bộ MỌI file**: SKILL.md frontmatter · README · openai.yaml — validate chéo
- **State thật trên disk**: skill dạy hệ thống ghi state file, không dựa trí nhớ

## Checklist

- [ ] Skill tự chứa (không path ngoài)
- [ ] Tham số đổi được qua env/frontmatter
- [ ] Script idempotent + có backup
- [ ] Smoke test chạy 1 lệnh
- [ ] Tên/version đồng bộ mọi file
