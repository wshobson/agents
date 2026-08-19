---
name: eskill
description: >
  Skill mẹ tạo skill (meta-skill) — quy trình sản xuất Agent Skills chuẩn top-1:
  theo spec chính thức agentskills.io, quy trình eval của anthropics/skills (skill-creator),
  và kinh nghiệm thực chiến build egram/eseed. Dùng khi cần TẠO skill mới, CẢI THIỆN skill cũ,
  validate/kiểm tra skill, chuẩn bị skill bán thương mại, hoặc khi user nói "tạo skill",
  "làm eskill", "viết SKILL.md", "skill ngon nhất".
license: MIT
compatibility: Python 3.10+
metadata:
  author: hedra
  version: "1.4.1"
---

# eskill — Quy trình tạo Agent Skill (11 trụ cột)

## 11 trụ cột — mỗi trụ 1 kim chỉ nam top-1

```
1. Core         · agentskills.io spec      — format chuẩn (frontmatter, progressive disclosure, refs 1 cấp)
2. UX/UI        · Apple HIG                — cấu trúc skill, quickstart, naming Apple-style
3. Validation   · agentskills.io validator — bắt lỗi sớm bằng máy
4. Docs & Bẫy   · docs chính thức          — docs-driven HARD GATE 100% + bẫy thực chiến
5. Vận hành     · 12-Factor App            — skill gọn, tự chứa, idempotent
6. Eval         · skill-creator Anthropic  — test prompts → forward-test → improver
7. Nội dung     · Apple Writing            — câu ngắn, động từ, không thừa chữ
8. Tăng trưởng  · AARRR                    — description chống undertrigger, adoption
9. Thương mại   · OKX                      — leak scan, LICENSE, marketplace, PnL bán skill
10. Tư vấn      · SPIN + Mom Test          — hỏi đúng nỗi đau, skill theo đúng ý user
11. Thị trường · JTBD + Mom Test + Demand Validation — research trước, build sau
```

## Quickstart (3 câu — user mới bắt đầu từ đây)

1. `Tạo một skill để <việc gì đó> và kiểm tra nó chạy được` → eskill hỏi ít câu rồi build
2. `Cải thiện skill này: <đường dẫn>` → áp eval loop, tìm lỗi, sửa
3. `Validate skill này: <đường dẫn>` → chạy validator

Nguồn chuẩn: [agentskills.io/specification](https://agentskills.io/specification) (spec chính thức) · `anthropics/skills` (skill-creator + template) · kinh nghiệm build egram/eseed (đã vấp và sửa).

## 6 bước — BƯỚC 0 quan trọng nhất

1. **BƯỚC 0 — Tư vấn trước, không đoán (Trụ 10 — sales-discovery.md)**: trích mục tiêu từ hội thoại hiện có TRƯỚC (tool đã dùng, thứ tự, input/output, lỗi user sửa). Hỏi 1 câu/lượt, tối đa 6 câu theo chuỗi SPIN (S tình huống → P nỗi đau → I hệ quả → N giá trị) + Mom Test (hỏi CUỘC SỐNG họ, không hỏi "anh có cần...?"). Tóm tắt gap (hiện tại → mong muốn → rào cản) cho user XÁC NHẬN trước khi viết — skill build theo câu trả lời của user, không theo giả định model. **Chế độ tự động (không có user để trả lời): tự quyết từ thông tin có sẵn rồi TIẾN HÀNH — đừng dừng chờ hỏi (đã vấp: agent kẹt cứng ở BƯỚC 0 khi không có user — forward-test 2026-08-19).** **(Nếu build skill bán: làm Trụ 11 — nghiên cứu thị trường TRƯỚC, xem `references/market-research.md`)**
2. **Chọn kim chỉ nam**: mỗi mảng lớn = 1 chuẩn ĐÃ CHỨNG MINH, không viết theo ý kiến. Egram đã dùng: BotFather · Apple HIG · Stripe · Telegram docs · 12-Factor · GitHub Actions · Apple Writing · AARRR · OKX. Tìm nguồn: docs chính thức + `gh search repos --sort stars`.
3. **Viết SKILL.md theo spec** (chi tiết: `references/spec-rules.md`):
   - Frontmatter: `name` (1-64, chữ thường + gạch nối, **= tên thư mục**) · `description` ≤1024 ký tự — nêu CẢ "làm gì" LẪN "khi nào dùng", kèm trigger keyword, viết "pushy" (chống undertrigger — Claude có xu hướng không bật skill dù cần)
   - Body < 500 dòng: mỗi mảng = **quy tắc → code mẫu → checklist** (lặp đều, đọc xong làm được ngay)
   - Chi tiết đẩy xuống `references/` — ref **1 cấp** từ SKILL.md, đường dẫn tương đối
   - **Bắt tay tạo file NGAY**: copy `template/SKILL.md` vào thư mục đích rồi điền dần — đọc references tối thiểu, đừng lang thang đọc hết tài liệu trước khi viết (đã vấp 2 lần: 3/5 rồi 2/3 agent dành hết budget đọc examples/* mà không tạo file — forward-test case lớn 2026-08-19). **KHÔNG mở `examples/` khi TẠO skill mới — `template/SKILL.md` là đủ**; mở `examples/` chỉ khi CẢI THIỆN skill có sẵn
4. **Đóng gói bẫy đã biết**: mục "Bẫy — đừng lặp" — mỗi bẫy 1 dòng: triệu chứng + fix. Đây là tài sản lớn nhất của skill (agent sau không lặp 2 tiếng debug của agent trước).
5. **Test + validate**: vòng lặp test → đánh giá → sửa (`references/eval-loop.md`) · chạy `scripts/validate-skill.py` · bán thương mại → chạy `--leak` + `references/checklist-thuong-mai.md`.
6. **Pin kích hoạt**: skill quan trọng cho 1 project → thêm vào `.deepseek/instructions.md` của project (luôn bật, không chỉ trigger theo description).

## Quy tắc vàng (học từ sai lầm egram — đừng lặp)

- **DOCS-DRIVEN — HARD GATE 100%**: trước khi code/đo với 1 API/service, PHẢI có docs chính thức trong `references/` (tự fetch được HOẶC user đưa vào). **KHÔNG có docs = KHÔNG code, KHÔNG chạy — DỪNG lại yêu cầu user đưa docs** (file/URL/export). Không dựa vào trí nhớ model — nó sai (bẫy thật: field `views` của Graph API không có trong docs Video object nhưng model tin là có → đo sai lệch 10×: 74.714 vs 7.400 thật). Quy trình chi tiết: `references/docs-driven.md`
- **Doc phải tự kiểm chứng**: mọi lệnh/đường dẫn trong SKILL.md/README phải chạy được. Lỗi kinh điển: egram v1 tuyên bố references là symlink nhưng thực tế là copy + thư mục đích không tồn tại.
- **Idempotent + backup**: mọi patch/script chạy lại 100 lần an toàn, có `.bak` trước khi sửa.
- **Smoke test đóng gói**: 1 script chạy 1 lệnh = bằng chứng skill hoạt động, không cần tin lời.
- **Sanitize trước khi public**: grep secret/path/brand/chat_id/token — làm hệ thống, không làm tay (egram lộ chat_id thật + path home cá nhân khi chuẩn bị bán (bài học: thay placeholder `<chat_id>`, `<project_root>`)).
- **Đổi tên/version đồng bộ mọi file**: README/SKILL/frontmatter — validate chéo (egram v1 README ghi "8 trụ/Hedragram" khi skill đã 9 trụ/egram).

- **Ghi từng bước thành file đánh số 0→n**: hỏi/ghi ngay kết quả mỗi bước vào file (0-goal → 1-market → 2-plan → 3-SKILL.md → 4-eval → 5-check) — state trên disk, user duyệt từng lớp, máy kiểm tra được (học từ egram: 0-logic → 5-month). Chi tiết: `references/numbered-output.md`

## Giới hạn (trung thực — khi nào KHÔNG dùng)

- Skill **không thay thế test trên máy thật** của user — eval loop là agent chạy thử, user vẫn phải tự verify trên môi trường thật
- Skill quốc tế → SKILL.md + README nên viết tiếng Anh (eskill bản VN là chuẩn nội bộ của tác giả)

## References

- `references/spec-rules.md` — Trụ 1+3: frontmatter + progressive disclosure + file refs (spec agentskills.io)
- `references/naming.md` — Trụ 2: đặt tên kiểu Apple/e-family (brand ≠ prefix, `e` + 1 từ chính, ≤3 âm tiết)
- `references/sales-discovery.md` — Trụ 10: hỏi đúng nỗi đau (SPIN + Mom Test + Gap) — skill theo ý user
- `references/eval-loop.md` — Trụ 6: vòng lặp test prompts → eval → sửa (skill-creator Anthropic)
- `references/test-prompts-template.md` — Trụ 6: 5 kiểu test prompt giả lập user thật (chính/biên/sai/nhanh/lớn)
- `references/rubric.md` — Trụ 6: tiêu chí pass/fail mã hóa TRƯỚC (4 loại: artifact · string · behavior · LLM-judge)
- `references/docs-driven.md` — Trụ 4: docs là HARD GATE 100% (không docs = không code, yêu cầu user đưa)
- `references/12-factor-skills.md` — Trụ 5: vận hành skill bền (tự chứa, idempotent, state disk)
- `references/apple-writing.md` — Trụ 7: viết SKILL.md ngắn gọn (câu ngắn, động từ, specific)
- `references/openai-yaml.md` — Trụ 9: agents/openai.yaml cho marketplace/UI (display_name, short_description, default_prompt)
- `references/checklist-thuong-mai.md` — Trụ 9: chuẩn bị bán: sanitize rò rỉ + LICENSE + README đồng bộ + an toàn khi cài skill lạ
- `references/ban-tren-github.md` — Trụ 9: bán trên GitHub: push repo · cấp quyền từng khách (private) · tag/release · chuyển public
- `template/SKILL.md` — khung SKILL.md copy dùng ngay (frontmatter đủ field + quy tắc → code mẫu → ví dụ → checklist + Bẫy)
- `examples/echeck/` — SKILL MẪU HOÀN CHỈNH (kiểm tra URL sống) — hình mẫu đối chiếu cho mọi skill tạo ra
- `scripts/validate-skill.py` — validator: frontmatter, quy tắc name, độ dài, refs; `--leak` quét rò rỉ; `--brand "a,b"` quét brand nội bộ
- `scripts/eval-skill.py` — eval harness: static check + test set versioned (eval-results.json) + trace verdict · `--verify` tổng kết pass rate/trigger rate + rubric bắt buộc per case

- `references/market-research.md` — Trụ 11: research trước build sau (nỗi đau user, kênh phân phối, pricing, demand validation)
- `references/numbered-output.md` — pattern file 0→n (học từ egram): ghi từng bước thành file, duyệt từng lớp
