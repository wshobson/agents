# agents/openai.yaml — metadata marketplace/UI (không bắt buộc spec, cần khi đăng chợ)

Đặt tại `agents/openai.yaml` trong skill. Dùng cho UI hiển thị (danh sách skill, chips).
Đọc SKILL.md rồi sinh 3 giá trị: `display_name` (tên hiển thị, camelCase kiểu e-family),
`short_description` (1 câu, ≤ ~140 ký tự), `default_prompt` (câu user mở đầu điển hình).

```yaml
display_name: eSkill
short_description: Quy trình tạo Agent Skill chuẩn top-1 (spec agentskills.io + eval loop)
default_prompt: Tạo một skill để ... và kiểm tra nó chạy được
```

## Quy tắc

- `display_name`: camelCase hiển thị (egram → egram, eseed → eSeed, eskill → eSkill)
- `short_description`: 1 câu nêu giá trị + khi nào dùng — giống `description` nhưng ngắn
- `default_prompt`: câu user thật hay gõ để bật skill
- Cập nhật lại mỗi khi SKILL.md đổi (đừng để stale — bài học egram v1)
