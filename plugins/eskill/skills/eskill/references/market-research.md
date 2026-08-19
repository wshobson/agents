# Market Research — Trụ 11: research TRƯỚC, build SAU (top-1: JTBD + Mom Test + Demand Validation)

Lỗi kinh điển: build skill xong mới hỏi có ai cần không. Trụ 11 đảo ngược: nghiên cứu trước, build sau. Bằng chứng 2026-08: top-1 skill thế giới = obra/superpowers (274K ⭐) và mattpocock/skills (223K ⭐) — cả hai bắt đầu từ nỗi đau của CHÍNH TÁC GIẢ, không phải đoán thị trường.

## 1. Năm nỗi đau người dùng phổ biến nhất (research Reddit/HN/PromptBase/X/Google Trends 2026-08)

1. **Skill bị model bỏ qua** — skill chỉ advisory, model không tự gọi → mất niềm tin. Fix: description trigger mạnh + script deterministic + test thật skill có được gọi không.
2. **Nhầm lẫn khái niệm** — skills vs MCP vs subagents vs commands vs plugins. Fix: SKILL.md nêu rõ khi nào dùng / khi nào KHÔNG (mục Giới hạn).
3. **Hoài nghi chỉ là markdown** — Fix: bằng chứng chạy thật (eval-results.json, smoke test). Điểm eskill ĐÃ có.
4. **Decay** — skill cũ, docs lỗi thời. Fix: version + RELEASE-NOTES + cập nhật định kỳ.
5. **Bảo mật** — skill = script thực thi, sợ RCE / prompt injection. Fix: code review sạch, tối giản quyền, mục an toàn khi cài.

Nguồn bổ sung: X/Twitter (trend AI) · Product Hunt (test demand lúc launch) · Google Trends (đo volume tìm kiếm) · newsletter AI (The Rundown, Matt Wolfe).

## 2. Kênh phân phối ngoài GitHub (research 2026-08 — có bằng chứng)

- **PromptBase** — kênh DUY NHẤT bán skill.md end-to-end hiện tại: 450K+ users, 2,200+ sellers, 20% phí chợ / 0% link riêng, thanh toán Stripe
- **skills.sh (Vercel)** — discovery + cài 1 lệnh: 8,420 skill, 1.26M installs all-time, miễn phí
- **Claude Code / Codex / Cursor marketplace** — native-install; Codex qua review OpenAI, Cursor bắt buộc open-source, Claude mở marketplace.json không phí
- **Gumroad** — storefront tự bán: 10% + $0.50 (30% nếu qua Discover)
- **Lemon Squeezy / Paddle / Ko-fi / Buy Me a Coffee / AppSumo** — storefront thay thế: phí kiểm tra trên trang chủ khi dùng
- Telegram Stars + MCP directories (mcp.so/Glama/Arcade.dev): CHỈ khi sản phẩm thật là bot/MCP — ngoài scope skill, không ưu tiên

Kết luận: GitHub = trust + discovery. PromptBase = kênh bán skill.md sẵn có. Gumroad/Lemon Squeezy = bán trực tiếp khi có traffic. Bán access repo thì dùng funnel Telegram + OKX + GitHub (chi tiết: ban-tren-github.md). KHÔNG bán được ngay trên GitHub (không có cổng thanh toán).

## 3. Top-1 làm gì đúng (benchmark obra/superpowers + mattpocock/skills)

1. Skill QUY TRÌNH có ý kiến — không phải reference docs
2. Cài 1 lệnh qua official plugin marketplace
3. Dual install: subscribe (tự cập nhật) hoặc fork (kiểm soát)
4. Tác giả tự dùng hằng ngày (eat own dogfood)
5. Bắt đầu từ nỗi đau cá nhân thật
6. Cộng đồng + newsletter (mattpocock ~60K subscribers)
7. Repo sống: cập nhật liên tục
8. README kể chuyện, positioning rõ: cho ai, giải quyết gì
9. Enterprise path rõ ràng (obra: email sales)
10. Registry-level distribution (skills.sh)

5 GAP mọi ông lớn bỏ lỡ — chỗ skill mới ăn điểm:
1. Không có install-time security verification (NVIDIA SkillSpector tồn tại nhưng ngoài luồng)
2. Không có per-skill semver + changelog
3. Không có usage telemetry (obra tự thú: không biết bao nhiêu người dùng)
4. Không có skill-quality benchmark chung
5. Không có paid distribution tích hợp vào install UX

## 4. Pricing benchmark (research 2026)

- Prompt lẻ: $5-15 · Bundle hệ thống (prompt + workflow + template): $29-69 · Membership: $9-19/tháng
- Người mua trả tiền cho BUNDLE giải quyết 1 nỗi đau — không trả cho prompt lẻ
- Thu nhập thực: beginner $100-500/tháng · niche + direct + subscription: $2K-15K/tháng
- Margin: direct ~3% phí xử lý vs PromptBase 20% vs Gumroad 10%+$0.50 · mọi con số dùng quyết định PHẢI kèm URL nguồn

## 5. Demand validation — 5 cách có bằng chứng

1. Founder-pain test: chính tôi có dùng nó hằng tuần không? (PromptBase, superpowers đều từ đây)
2. Pre-sale: bán trước khi build — có người trả tiền = demand thật (Marc Lou pattern)
3. Signal scan: Reddit/HN/Google Trends/X/search — người ta có đang đau vì vấn đề này?
4. Mom Test: hỏi CUỘC SỐNG, không hỏi anh có cần không (chi tiết: sales-discovery.md)
5. Waitlist / landing page: đo conversion trước khi tốn công build

## Checklist nghiên cứu thị trường (trước khi build skill BÁN)

- [ ] 1 câu: người mua DUY NHẤT + nỗi đau cụ thể của họ
- [ ] Founder-pain test: chính mình dùng hằng tuần không?
- [ ] Scan 3 nơi: Reddit/HN + skills.sh + PromptBase — đã có skill nào chưa, gap gì
- [ ] Benchmark 2 skill top cùng chủ đề — học điểm mạnh, né điểm yếu
- [ ] Định giá theo bundle ($29-69), không theo prompt lẻ ($5)
- [ ] Chọn kênh ≥2: GitHub (trust) + PromptBase (bán) + Gumroad (direct)
- [ ] Demand test tối thiểu TRƯỚC khi build 200 dòng
- [ ] Kế hoạch cập nhật (version + changelog) từ ngày đầu

## 6. Post-launch measurement — đo sau khi ship (đừng tự xây telemetry, dùng thứ CÓ SẴN)

Telemetry ĐÃ tồn tại, public, không cần tự làm:
- **skills.sh** — install count dedup, trending 24h, hot view, weekly sparkline, README badge, public API /api/v1. Số thật 2026-08: npm skills CLI 38.6M downloads/30 ngày · mattpocock 16.7M installs / 51 skills · top skill find-skills 3.0M installs
- **GitHub API** — stars/forks/open issues (public, không cần token) · traffic 14 ngày: clones/views/referrers (cần token)
- **PromptBase** — sales + reviews (kênh bán duy nhất, số liệu bán thật)
- **npm** — downloads/tháng cho package

Feedback channel hiệu quả: GitHub Issues + Discussions (anthropics/skills 1,120 issues mở · mattpocock 370) · HN · r/ClaudeAI · Discord

Nhịp review (tooling đã mã hóa sẵn):
- Mỗi tuần: install sparkline + trending — có tăng không
- Mỗi tháng: sales + issues mới + churn — ai gỡ cài / báo lỗi gì
- Mỗi release: changelog + đối chiếu feedback cũ đã fix chưa

Quyết định (tiếp tục / pivot / kill):
- **Tiếp tục**: installs tăng 2 tuần liên tiếp + feedback tích cực + sales > 0
- **Pivot**: installs ổn nhưng churn cao, hoặc 1 feature được hỏi lặp lại 3+ lần
- **Kill**: 60 ngày không có install mới + không ai hỏi → đóng, học bài học, chuyển nguồn lực

Thực tế top creator: ship liên tục — cả 3 repo đầu bảng đều có commit trong 7 ngày gần nhất. Repo chết = không cập nhật.

## 7. Research → Plan — trình bày logic, dễ hiểu (top-1: Minto Pyramid Principle, McKinsey)

Kết quả nghiên cứu phải thành 1 trang plan. Framework top-1: Pyramid Principle của Barbara Minto (McKinsey) — kết luận trước, nhóm luận điểm MECE, mở đầu SCQA, ngôn ngữ JTBD. SCQA + MECE + Pyramid là MỘT hệ (Minto phát triển MECE để phục vụ Pyramid).

Cấu trúc 1 trang (đúng thứ tự):

1. **ANSWER — kết luận trước** (1 câu): Làm X cho Y vì Z. Vd: làm skill X cho lập trình viên nhúng vì họ tốn 10h/tuần cho việc Y.
2. **SCQA — mở đầu** (4 dòng):
   - Situation: thị trường Agent Skills bùng nổ, cài bằng 1 lệnh
   - Complication: hầu hết skill generic, không giải quyết nỗi đau cụ thể
   - Question: làm skill gì để thắng được?
   - Answer: chính là câu ở mục 1
3. **Nhóm luận điểm MECE** (3-4 nhóm, không chồng lấn, đủ phủ):
   - Thị trường & nhu cầu · Đối thủ & gap · Kênh & giá · Rủi ro
   - Mỗi nhóm 2-3 dòng + số liệu + nguồn
4. **Rủi ro + cách giảm** — 3 rủi ro lớn nhất, mỗi cái 1 hành động giảm
5. **Next actions** — 3-5 bước, mỗi bước 1 dòng: việc + deadline + người làm

3 quy tắc dễ hiểu:
- **Kết luận trước** — người đọc biết đáp án trong 5 giây, chi tiết phía sau
- **Ngôn ngữ đời thường** — không biệt ngữ; cần thuật ngữ thì định nghĩa 1 lần
- **1 trang, số cụ thể** — không mô tả chung chung; mọi luận điểm có số hoặc nguồn

MECE test sau khi viết xong: gộp 2 nhóm trùng → bỏ nhóm không liên quan → thêm nhóm thiếu → mỗi câu tự hỏi Vậy thì sao?

## 8. Nghiên cứu INSIGHT — nỗi đau là TRIỆU CHỨNG, insight là GỐC RỄ

Nỗi đau trả lời CÁI GÌ (skill bị model bỏ qua). Insight trả lời VÌ SAO (người dùng không TIN skill vì không thấy nó được gọi — vấn đề trust, không phải tính năng). Build theo pain = vá triệu chứng. Build theo insight = trúng gốc rễ.

4 phương pháp đào insight (có bằng chứng):

1. **JTBD — phỏng vấn theo JOB, không theo giải pháp**: hỏi KHI nào + MUỐN làm gì + ĐỂ đạt kết quả gì. Không hỏi anh muốn tính năng nào. Bằng chứng: obra/superpowers thắng vì bắt đúng job cải thiện quy trình code hằng ngày, không phải thêm tính năng X.
2. **5 Whys — đào từ pain xuống gốc**: pain #1 (model bỏ qua skill) → vì sao → description không trigger → vì sao → skill viết chung chung, không nêu khi nào dùng → INSIGHT: skill phải có trigger mạnh + script deterministic + smoke test chứng minh.
3. **Behavioral observation — nhìn họ LÀM, không hỏi họ MUỐN**: người ta không cài skill, họ copy-paste SKILL.md vào project → insight: friction khi cài là rào cản thật → fix: cài 1 lệnh.
4. **Outcome-driven — hỏi kết quả đo được**: tiết kiệm bao nhiêu giờ/tuần, giảm bao nhiêu lỗi — không hỏi chức năng. Kết quả đo được = căn cứ định giá.

Công thức câu insight (đủ 4 phần mới là insight):
Khi [tình huống], người dùng muốn [job] để [kết quả đo được], nhưng bị chặn bởi [rào cản] vì [nguyên nhân gốc].

Ví dụ: Khi tạo skill, người dùng muốn nó tự chạy đúng quy trình để tiết kiệm 2h/ngày, nhưng model không gọi skill vì description không trigger → giải pháp: description pushy + script deterministic + smoke test.

Checklist insight:
- [ ] Với MỖI pain: đã đào 1 insight (nguyên nhân gốc) chưa?
- [ ] Câu insight đủ 4 phần theo công thức?
- [ ] Quyết định build dựa trên insight, không chỉ pain?
