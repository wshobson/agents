# Rubric — tiêu chí pass/fail mã hóa TRƯỚC (Trụ 6)

Chấm "định tính nhìn thấy ổn" = không phải chứng minh. Mọi test case phải có **rubric pre-registered** (viết TRƯỚC khi chạy — chống confirmation bias).

## 4 loại rubric

### 1. Artifact — file/đầu ra phải tồn tại
```
PASS nếu: <path> tồn tại · chứa <chuỗi bắt buộc> · kích thước > 0
FAIL nếu: thiếu file / thiếu chuỗi / file rỗng
```

### 2. String/Regex — nội dung phải khớp
```
PASS nếu: output chứa "✅ ..." · KHÔNG chứa "❌" · khớp regex ^SKILL
FAIL nếu: chứa chuỗi cấm (vd token thật, path home cá nhân)
```

### 3. Behavior/Exit — chạy được, mã trả về đúng
```
PASS nếu: exit code = 0 · không exception · log có timestamp
FAIL nếu: exit ≠ 0 · crash · treo > 60s
```

### 4. LLM-as-judge — agent mới chấm theo rubric cố định
```
Câu hỏi judge (đưa output + rubric):
"Output có: (a) đúng format <X>? (b) đủ <N> phần? (c) không bịa số liệu?
Chấm 1-5 mỗi mục + verdict PASS (≥4) / FAIL (<4). KHÔNG thương lượng."
```

## Quy tắc pre-registration

1. **Viết rubric TRƯỚC khi chạy** — ghi vào file test case (vd `tests/rubric.md`), không viết sau khi thấy output
2. **Mỗi case ≥ 1 rubric** — chọn loại phù hợp (artifact cho transform file · string cho format · behavior cho script · judge cho output mở)
3. **Judge độc lập** — agent chấm không được biết kỳ vọng của người viết skill

## Ví dụ thực tế (từ eseed forward-test)

Case: "Xem hiệu suất 20 video — lấy views đúng"
Rubric pre-registered:
- ✅ Nhắc cảnh báo views không tin cậy (chuỗi "views" + "không tin cậy"/"đối chiếu")
- ✅ Dùng post id = PAGE_ID_videoid (chuỗi "PAGE_ID" hoặc "pageid_videoid")
- ❌ FAIL nếu: đề xuất batch /?ids= · đưa số views tuyệt đối không caveat
→ Agent test pass cả 3 — rubric phát hiện được agent bịa (như đã từng: 74.714 vs 7.400)
