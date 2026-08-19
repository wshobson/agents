# Bán skill trên GitHub — quy trình publish + bán

Phần này đi SAU `checklist-thuong-mai.md` (chuẩn bị skill). Ở đây là đưa skill lên GitHub và bán.

## 1. Chuẩn bị xong chưa? (chạy trước khi push)

```bash
python3 scripts/validate-skill.py <skill-dir> --leak --brand "brand1,brand2"
```
PASS → mới push. FAIL → sửa (xem checklist-thuong-mai.md).

## 2. Tạo repo + push (private mặc định)

```bash
cd <skill-dir>
git init -b main && git add -A && git commit -m "Initial commit"
gh repo create <tên> --private --source=. --push --description "<1 câu giá trị>"
```

- **`--private` MẶC ĐỊNH** — chưa sẵn sàng công khai thì giữ private
- `.gitignore`: `.DS_Store`, `__pycache__/`, `*.pyc`, `*.zip` (zip bản phát hành không đẩy lên repo)
- Tên repo = tên skill (e-family: `egram`, `eseed`, `eskill`)

## 3. Bán PRIVATE — cấp quyền từng khách

Bán skill = bán quyền truy cập repo. Mỗi khách cần username GitHub:

```bash
# Cấp quyền ĐỌC (clone về dùng — đủ cho người mua)
gh api -X PUT repos/<owner>/<repo>/collaborators/<username> -f permission=pull

# (nếu 2 bên cùng phát triển) nâng lên push
gh api -X PUT repos/<owner>/<repo>/collaborators/<username> -f permission=push

# Thu hồi khi khách không gia hạn / trả tiền
gh api -X DELETE repos/<owner>/<repo>/collaborators/<username>
```

- Kiểm tra ai đang có quyền: `gh api repos/<owner>/<repo>/collaborators --paginate`
- **Gửi kèm hướng dẫn cài**: `cp -R <skill> ~/.deepseek/skills/<skill>` (hoặc `~/.claude/skills/`)
- Khách cần môi trường agent load skill (DeepSeek TUI / Claude Code) — nói rõ khi bán

## 4. Phiên bản + cập nhật

```bash
# Mỗi bản bán — 3 bước: bump → notes → tag
# 1) Sửa .version-bump.json (version mới) + đồng bộ version trong SKILL.md / README / eval-results.json / plugin.json
# 2) Thêm mục [x.y.z] vào RELEASE-NOTES.md (định dạng Keep a Changelog)
gh release create v1.0.1 --title "v1.0.1" --notes "Bản cập nhật — chi tiết trong RELEASE-NOTES.md"

# Khách lấy bản mới
cd <nơi clone> && git pull
```

- Version semver thống nhất: `SKILL.md metadata.version` = `eval-results.json` = `README` = `plugin.json` = tag — `.version-bump.json` liệt kê file phải đồng bộ
- Mỗi bản đổi → cập nhật `RELEASE-NOTES.md` + README + agents/openai.yaml + tag mới (bài học đồng bộ egram)

## 5. Chuyển PUBLIC (khi sẵn sàng bán rộng rãi)

```bash
gh repo edit <owner>/<repo> --visibility public
```
- Public = ai cũng tải được — chỉ khi skill đã sanitize + README EN + demo hoạt động
- (Tùy chọn) đăng ký marketplace qua skills.sh / plugin marketplace — kênh phân phối thêm



---

## Funnel bán thực chiến — Telegram + OKX USDT + GitHub (access selling)

Bán access repo = khách trả tiền → cấp quyền pull. GitHub KHÔNG có cổng thanh toán —
tiền chạy ngoài (USDT/OKX), GitHub chỉ giao repo. Stack đề xuất đã có sẵn script trong `../scripts/sell/`.

### Vận hành 3 mức (bắt đầu mức 1, nâng dần)

1. **Mức 1 — thủ công**: khách chuyển USDT vào ví OKX → khách gửi TXID → check tronscan → `../scripts/sell/grant_access.sh grant <user>`
2. **Mức 2 — bot Telegram**: `../scripts/sell/sales_bot.py` tự làm cả luồng /buy → /paid → verify → grant (xem dưới)
3. **Mức 3 — webhook auto**: cổng thanh toán → webhook → GitHub Actions cấp quyền (khi khách đông)

### Quy trình xác nhận thanh toán (4 bước — CHỈ tin blockchain, không tin ảnh chụp)

1. Khách gửi: TXID (64 hex) + mạng + số tiền + nguồn gửi
2. Tra tronscan: `python3 ../scripts/sell/verify_payment.py <TXID> <tiền> <địa_chỉ_nhận>`
   - Địa chỉ nhận khớp 100% · token là USDT (TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t) · confirmed · tiền đủ
3. Attribution (ai gửi — TXID không chứng minh người gửi):
   - **Ví cá nhân** → khớp địa chỉ "From" trên explorer với địa chỉ khách khai
   - **Sàn (OKX/Binance)** → "From" là ví hot sàn, vô nghĩa → dùng **số tiền độc nhất**: mỗi đơn 1 đuôi thập phân (vd 50.37, .37 = mã đơn) + ảnh lịch sử rút từ app sàn
   - **Trả hộ / trung gian** → TỪ CHỐI (không định danh được)
4. Khớp → cấp quyền. Thiếu 1 trong 3 (TXID · số tiền độc nhất · nguồn gửi khớp) → không cấp

### Sales bot (../scripts/sell/) — chạy trên máy bán

```bash
cd <skill>/scripts/sell
cp .env.mẫu .env   # điền: TELEGRAM_BOT_TOKEN (BotFather) · SELLER_CHAT_ID (userinfobot)
                   #       OKX_USDT_ADDRESS · PRICE_USDT · REPO
python3 sales_bot.py   # long-poll, chạy nền (nohup / launchd)
```

Lệnh khách: `/buy` (trả địa chỉ + số tiền độc nhất) → `/paid <TXID> <gh_username>` (tự verify + grant).
Lệnh admin (whitelist SELLER_CHAT_ID): `/grant` `/revoke` `/sales`. State trên disk `sales.json`, log `sales.log`.

### Ràng buộc vận hành (check trước khi bán)

- **Private repo gói GitHub Free: giới hạn collaborators** — bán nhiều khách → cần GitHub Pro (xác nhận con số hiện tại trên docs.github.com)
- `gh` phải auth trên máy bán (`gh auth login`) — grant_access.sh dựa vào `gh api`
- Giá trị khách hàng = cập nhật định kỳ → thu hồi quyền khi hết hạn (`grant_access.sh revoke <user>`), gia hạn thì cấp lại
- Không gửi `.env` thật lên git — `.gitignore` đã chặn

### Mô hình kiếm tiền — bài học

GitHub không có cổng thanh toán; người kiếm tiền trên GitHub chủ yếu từ: sản phẩm cloud (repo = marketing) ·
open-core · việc làm/tư vấn · sponsors (nhỏ, VN không rút được) · bán add-on/access (mô hình này — trần thấp nếu thiếu discovery).
Chiến lược hybrid: **public bản basic (MIT) lấy stars + discovery → bán bản Pro qua funnel trên**.

## Checklist bán

- [ ] validate `--leak --brand` PASS trước khi push
- [ ] Repo private + `.gitignore` đúng
- [ ] Khách có username GitHub → `gh api PUT collaborators -f permission=pull`
- [ ] Gửi hướng dẫn cài + yêu cầu môi trường (agent có load skill)
- [ ] Tag version khi bán bản mới · thu hồi quyền khi khách hết hạn
