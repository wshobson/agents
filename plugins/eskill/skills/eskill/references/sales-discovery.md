# Sales Discovery — Trụ 10: hỏi đúng nỗi đau, skill theo đúng ý user (top-1: SPIN + Mom Test + Gap Selling)

Skill chuẩn = 100% chuyên môn + **hỏi đúng người dùng thật sự cần gì**. Mỗi người mỗi ý —
skill build theo giả định của model = sai. Build theo câu trả lời của user = chuẩn.

## 3 nền tảng top-1

1. **The Mom Test (Rob Fitzpatrick)** — cách hỏi KHÔNG bị nhiễu ý kiến: nói về cuộc sống họ, không nói về ý tưởng mình
2. **SPIN Selling (Neil Rackham)** — chuỗi câu hỏi S→P→I→N: tình huống → vấn đề → hệ quả → giá trị
3. **Gap Selling (Keenan)** — hiện tại → mong muốn → rào cản → giải pháp khép gap

## 3 quy tắc Mom Test (bắt buộc khi hỏi)

1. **Nói về CUỘC SỐNG của họ, không về ý tưởng của mình**
   - ❌ "Anh thấy skill này thế nào?" (ý tưởng — ai cũng gật cho lịch sự)
   - ✅ "Dạo này anh xử lý việc X thế nào?" (cuộc sống — câu trả lời thật)
2. **Hỏi SỰ THẬT CỤ THỂ, không hỏi ý kiến tán thành**
   - ❌ "Anh có cần tính năng Y không?" (ý kiến — vô giá trị)
   - ✅ "Lần cuối anh gặp vấn đề Y là khi nào? Chuyện gì xảy ra?" (sự thật)
3. **Lắng nghe, không bán** — commit thật = họ dùng thử/test thật, không phải "nghe hay đấy"

## Chuỗi SPIN (áp vào phỏng vấn skill)

- **S — Situation**: "Anh đang làm việc X như thế nào? Dùng tool gì?" → biết môi trường thật
- **P — Problem**: "Chỗ nào đang khó nhất / tốn thời gian nhất?" → nỗi đau
- **I — Implication**: "Khó đó khiến anh tốn bao nhiêu thời gian/tiền/mất cơ hội?" → định lượng nỗi đau
- **N — Need-payoff**: "Nếu tự động hóa chỗ đó, anh được gì?" → giải pháp phải khép đúng đau

## Gap (tóm tắt trước khi viết)

```
HIỆN TẠI: <cách họ đang làm>      → RÀO CẢN: <tại sao chưa tự động được>
MONG MUỐN: <điều họ mô tả là "chuẩn">  → SKILL: <khép gap giữa 2 bên>
```

## Mẫu phỏng vấn 6 câu (tối đa — hỏi 1 câu/lượt)

1. (S) "Anh đang xử lý <việc> thế nào hiện tại — làm tay hay có tool?"
2. (S) "Mỗi lần làm mất bao lâu / tốn bao nhiêu?"
3. (P) "Chỗ nào thấy khó chịu / lặp đi lặp lại nhất?"
4. (I) "Nếu bỏ được chỗ đó, anh tiết kiệm được gì cụ thể?"
5. (N) "Kết quả mong muốn nhìn như thế nào — anh mô tả 1 lần hoàn hảo?"
6. (C) "Tôi hiểu là <tóm tắt gap>. Đúng ý anh chưa?" → **user xác nhận mới viết skill**

## Quy tắc chốt

- **Hỏi tối đa 6 câu, 1 câu/lượt** — không bắn loạt, không tự trả lời thay user
- **Không hỏi**: "Anh có cần...?" (ý kiến) · "Anh thấy... thế nào?" (khen) · câu dẫn đến câu trả lời mong muốn
- **Mỗi pain = 1 solution** — skill tạo ra phải map được về pain user nói, không phải tính năng model nghĩ ra
- **Ghi đáp án → confirm → mới viết** — tóm tắt gap cho user xác nhận trước khi code (BƯỚC 0)

## Checklist

- [ ] Hỏi về cuộc sống họ, không về ý tưởng mình (Mom Test)
- [ ] Có câu hỏi định lượng nỗi đau (I — SPIN)
- [ ] Tóm tắt gap → user xác nhận
- [ ] Mỗi tính năng skill map về 1 pain user nói
