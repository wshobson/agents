# Docs-Driven — docs là HARD GATE 100% (quy tắc vàng eskill)

## Vì sao

Model KHÔNG nhớ đúng API docs. Bẫy thật (Graph API, 18/08):
- Field `views` trên Video object — model tin là có → đo sai lệch **10×** (74.714 vs 7.400 thật)
- Thực tế: docs chính thức Video object KHÔNG có field `views` ("removed after v3.2")
- `video_insights total_video_views` mới là metric chính thức — nhưng model cũng không biết cần `period=lifetime`

→ Docs trong trí nhớ = rủi ro. Docs trong skill = bằng chứng. **KHÔNG docs = KHÔNG chạy.**

## Quy trình 4 bước (bước 1 có nhánh bắt buộc)

1. **FETCH docs chính thức** (URL official: developers.facebook.com, core.telegram.org, stripe.com/docs...)
   - ✅ Fetch được → lưu excerpt vào `references/` → tiếp tục bước 2
   - ❌ KHÔNG fetch được (chặn/403/không có quyền/không tìm thấy) → **DỪNG, yêu cầu USER đưa docs**:
     "Cần docs chính thức của <API> để chạy đúng — bạn đưa file/URL/export docs vào, tôi lưu vào references/ rồi mới code."
   - **BẮT BUỘC 100%**: chưa có docs = không code, không chạy, không đoán
2. **LƯU excerpt vào `references/`** của skill: field list, permissions, period hợp lệ, error codes, URL gốc + ngày fetch — file gọn, 1 cấp
3. **GHI CHÚ field/API KHÔNG TIN CẬY** nếu phát hiện (vd views field) — thành bẫy trong SKILL.md
4. **TEST THẬT trước khi tin** — 1 API call so sánh với thực tế user thấy (đối chiếu Meta Business Suite / app thật) — nếu lệch → đào docs tiếp, không đoán

## Khi nào bắt buộc

- Lần ĐẦU dùng 1 API/field/service trong skill
- API có version (Graph v22/v25/v26, Telegram Bot API) — version đổi = docs có thể đổi
- Field trả số liệu được dùng cho QUYẾT ĐỊNH (gate, verdict, budget) — sai số = sai tiền

## Checklist khi thêm API vào skill

- [ ] Đã fetch docs chính thức (hoặc user đưa) + lưu excerpt vào references/ — **BẮT BUỘC**
- [ ] Field list + permissions + periods ghi rõ
- [ ] Field không tin cậy đã ghi thành bẫy
- [ ] Đã test 1 API call thật + đối chiếu nguồn thật (user/app/UI)
- [ ] URL docs ghi trong skill để fetch lại khi version đổi
