# Test Prompts Template — giả lập user thật (forward-test)

Tạo 3-10 câu từ các kiểu dưới, thay `<nội dung>` theo skill. **KHÔNG lộ việc đang test skill.**

## 5 kiểu test (mỗi skill nên có đủ)

1. **Chính** — user yêu cầu ĐÚNG việc skill làm: "Dùng skill `<tên>` tại `<path>` để `<việc>` với `<input>`"
2. **Biên (undertrigger)** — user yêu cầu gần giống, KHÔNG gõ tên skill — agent có tự bật skill không? Đây là test quan trọng nhất cho `description` "pushy"
3. **Sai** — input không hợp lệ — skill báo lỗi gọn, không vỡ
4. **Nhanh** — user vội, câu ngắn — output vẫn đúng format
5. **Lớn** — input to (file dài, transcript) — có vượt context / progressive disclosure có được dùng không

## Mẫu câu

- `"Dùng skill <tên> tại <path> để <việc chính> với <input>"`
- `"<input thật> — xử lý giúp tôi"` (không nhắc skill — test trigger)
- `"Làm <việc lân cận có thể dùng skill>"` (test biên)
- `"Input này sai/thiếu, báo lỗi rõ ràng"` (test sai)

## Chấm pass

- Agent TỰ tìm + dùng skill ĐÚNG cách (không làm tay qua loa)
- Output đúng format, đúng luồng, đúng giọng điệu
- Fail ở test biên = description chưa đủ "pushy" → sửa description, không sửa body

## Quy tắc forward-test

- Fresh thread mỗi lần · không lộ đáp án/bài học · dọn artifact giữa các lần (chống contamination)
- Pass nhờ leaked context = skill chưa đủ → tighten lại
