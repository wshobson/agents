# Numbered Output — ghi từng bước thành file 0→n (học từ egram: hỏi → 0-logic → 1-menu → ... → 5-month)

Pattern egram: hỏi người dùng → GHI NGAY câu trả lời vào 0-logic.txt → lần lượt sinh 1-menu → 2-seed → ... mỗi file 1 lớp, user duyệt từng cái. Kết quả: dễ dùng, không mất state, máy kiểm tra được.

Áp dụng cho eskill — pipeline tạo skill BÁN thành file đánh số:

- 0-goal.txt — GỐC: câu trả lời BƯỚC 0 (SPIN + Mom Test). Ghi NGAY từng câu khi user trả lời.
- 1-market.txt — Trụ 11: người mua + nỗi đau + đối thủ + giá (research 1 trang)
- 2-plan.txt — Section 7: kết luận 1 trang (ANSWER → SCQA → MECE → rủi ro → next actions)
- 3-SKILL.md — draft theo spec (frontmatter, <500 dòng, refs 1 cấp)
- 4-eval.md — 5 test prompt + rubric TRƯỚC khi chạy eval
- 5-check.md — checklist thương mại (leak scan, LICENSE, README đồng bộ)

6 quy tắc:
1. Hỏi trước → ghi NGAY thành file 0 — không giữ câu trả lời trong hội thoại (state trên disk, restart không mất)
2. File sau phụ thuộc file trước — duyệt TỪNG LỚP: user fix file 0 → điều chỉnh các lớp sau
3. Skeleton trước, điền dần — sinh khung 6 file ngay, điền theo kết quả từng bước
4. Số thứ tự = thứ tự build = thứ tự duyệt — user không cần hỏi tiếp theo làm gì
5. Mỗi dự án 1 bộ file RIÊNG, độc lập — không mở/copy bộ file dự án khác
6. Máy kiểm tra được: đủ 6 file? thiếu file nào? — quy trình thành checklist chạy được

Code mẫu (khởi tạo bộ file):
```bash
touch 0-goal.txt 1-market.txt 2-plan.txt 3-SKILL.md 4-eval.md 5-check.md
```

Ví dụ nội dung 0-goal.txt (ghi khi user trả lời, 1 câu/câu):
```
# Mục tiêu
- Bot/skill làm gì: ...
- Ai dùng: ...
- Nỗi đau đang giải quyết: ...
```

Checklist trước khi build:
- [ ] 0-goal.txt có câu trả lời THẬT của user (không phải suy diễn model)
- [ ] 1-market.txt đủ: người mua + nỗi đau + 2 đối thủ + giá
- [ ] 2-plan.txt 1 trang: ANSWER đầu tiên + MECE + rủi ro + next actions
- [ ] 3-SKILL.md draft xong → validate PASS
- [ ] 4-eval.md có 5 test prompt + rubric
- [ ] 5-check.md: leak scan + LICENSE + README đồng bộ
