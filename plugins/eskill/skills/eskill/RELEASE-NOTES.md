# Release Notes — eSkill

Định dạng theo [Keep a Changelog](https://keepachangelog.com) — version semver, mỗi bản 1 mục.
Quy trình: sửa xong → bump `.version-bump.json` → cập nhật mục này → `gh release create vX.Y.Z`.

## [1.4.1] — 2026-08-20

### Updated
- market-research.md theo audit đội chuyên gia: thêm Google Trends/X/Product Hunt/newsletter · storefront thay thế (Lemon Squeezy/Paddle/Ko-fi/BMAC/AppSumo) · bỏ Telegram Stars + MCP dirs khỏi ưu tiên · fix mâu thuẫn funnel bán · quy tắc kèm URL nguồn

## [1.4.0] — 2026-08-20

### Added
- market-research.md Section 8: Nghiên cứu INSIGHT (JTBD + 5 Whys + behavioral observation + outcome-driven) — nỗi đau là triệu chứng, insight là gốc rễ

## [1.3.0] — 2026-08-19

### Added
- references/numbered-output.md: pattern file 0→n (học từ egram) — pipeline 0-goal → 1-market → 2-plan → 3-SKILL.md → 4-eval → 5-check
- Quy tắc vàng mới: ghi từng bước thành file đánh số

## [1.2.0] — 2026-08-19

### Added
- market-research.md Section 6: Post-launch measurement (skills.sh telemetry, GitHub API, kill/pivot/continue)
- market-research.md Section 7: Research → Plan (Minto Pyramid + SCQA + MECE + JTBD)

## [1.1.0] — 2026-08-19

### Added
- Trụ 11 — Market Research: `references/market-research.md` (nỗi đau người dùng, kênh phân phối ngoài GitHub, benchmark top-1, pricing, demand validation)
- BƯỚC 0 mở rộng: nghiên cứu thị trường trước khi build skill bán

## [1.0.0] — 2026-08-19

Bản đầu tiên đủ điều kiện bán. Eval chính thức: **4/5 PASS** + static PASS
(case lớn 3/5 — cần test phiên thật trước khi bán rộng, xem eval-results.json).

### Added
- Forward-test eval loop đầy đủ: 5 case (chính/biên/nhanh/sai/lớn), rubric pre-registered, evidence ghi trong `eval-results.json`
- Quy tắc mới từ eval (2 patch): BƯỚC 0 auto-mode ("không có user → tự quyết, TIẾN HÀNH") + Bước 3 create-first ("bắt tay tạo file NGAY, KHÔNG mở examples khi tạo mới — template là đủ")
- Đóng gói bán: `RELEASE-NOTES.md`, `.version-bump.json`, plugin manifests (Claude Code / Codex / Cursor), `.github/` templates + FUNDING, `CODE_OF_CONDUCT.md`, `.gitignore`, pre-commit, icon
- Version thống nhất semver `1.0.0` trên mọi file (SKILL.md metadata.version · eval-results.json · README · plugin.json · tag)

### Fixed
- README lệch SKILL.md (thiếu 4 references + eval-skill.py + examples/ trong cây cấu trúc)
- 3 file `.bak` còn sót trong gói
- BƯỚC 0 chặn agent chạy tự động (kẹt cứng chờ hỏi user không có)

## [Unreleased]
- Bản EN (bán quốc tế — spec + marketplace đều EN)
- Marketplace registration (skills.sh / plugin marketplace)
- Re-test case "lớn" trên phiên làm việc thật (có user tương tác, không phải sub-agent harness)
