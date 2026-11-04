[Uploading README-VI.md…]()
# Bộ Codex skill MythicMobs — boss, mechanics và particles

Gói 1.0.0, nghiên cứu ngày **05/11/2026 (Asia/Bangkok)**. Mốc phát hành được xác minh: MythicMobs **5.14.0 — 30/10/2026**. Gói lưu kiến thức đã chọn lọc để Codex có thể dùng lại ngoại tuyến cho các trường hợp được bao phủ.

## Có gì trong gói

- Một skill `mythicmobs-boss-particles`: viết boss/mob, hiệu ứng hạt, review và chuyển đổi cấu hình.
- Tài liệu tham khảo về mechanic, target/origin, particle data, hình học, ngân sách hạt, mẫu tổ chức file và chuyển đổi.
- Các template YAML tự viết: palette, ring/sphere/box/line/helix/orbital, projectile, slam, aura, vùng cảnh báo cố định, mob demo; hình học và tham số Premium đặt riêng.
- Nguồn chính thức và ví dụ YAML cộng đồng có tác giả/đường dẫn, ngày truy cập, phân loại và giới hạn bằng chứng.
- Công cụ kiểm tra YAML, khóa trùng, callback, tham chiếu nội bộ và một tập cú pháp hữu hạn; báo cáo và bộ thử lỗi đi kèm.

**Đã kiểm tra YAML và cấu trúc ngoại tuyến; chưa chạy MythicMobs/Minecraft.** Không nên hiểu “validated” là đã xác nhận gameplay, hình dạng, sát thương hoặc hiệu năng trên server. Không có plugin JAR, boss pack trả phí hay bộ chuyển đổi đa nền tảng tự động trong gói.

## Cài vào Codex trên máy này

1. Giải nén ZIP. Tìm thư mục `skills/mythicmobs-boss-particles` có file `SKILL.md` ngay bên trong.
2. Với cấu hình Codex đang dùng trong phiên này, chép **cả thư mục** `mythicmobs-boss-particles` vào `C:\Users\HOANG NAM\.codex\skills\`. Kết quả là `C:\Users\HOANG NAM\.codex\skills\mythicmobs-boss-particles\SKILL.md`.
3. Bản Codex theo tài liệu hiện hành cũng có thể khám phá skill cá nhân tại `%USERPROFILE%\.agents\skills\`; skill theo dự án tại `<project>\.agents\skills\`. Chọn một vị trí mà bản Codex của bạn hỗ trợ, tránh cài trùng tên ở nhiều nơi. Nếu dùng `CODEX_HOME` riêng, dùng thư mục skills của cấu hình đó. Xem [tài liệu OpenAI](https://learn.chatgpt.com/docs/build-skills).
4. Kiểm tra danh sách Skills; nếu chưa xuất hiện, khởi động lại Codex. Gọi bằng `$mythicmobs-boss-particles` hoặc chọn từ danh sách. Gói không tự sửa cấu hình hay tự cài vào thư mục cá nhân.

Chỉ chép thư mục skill, không đặt toàn bộ gói có nhiều tầng ZIP vào thư mục skills. Giữ nguyên các thư mục con `references/`, `assets/`, `scripts/`, `agents/`.

## Dùng ngay

```text
$mythicmobs-boss-particles
Tạo boss lửa cho Paper [phiên bản], MythicMobs [build], [Free/Premium].
Dùng kiến thức trong gói: vòng cảnh báo, windup 1.5 giây, projectile có trail,
tránh chồng cast bằng GCD. Ghi rõ giả định và trạng thái kiểm tra.
```

```text
$mythicmobs-boss-particles
Review và chuyển YAML tôi cung cấp sang MythicMobs [build]. Giữ hành vi gốc,
liệt kê addon, tên particle cũ, điểm chỉ chuyển gần đúng và các bước test.
```

Với phiên bản nằm trong phạm vi ghi chú, Codex đọc tài liệu cục bộ trước. Khi bạn yêu cầu “mới nhất”, dùng build mới hơn hoặc gặp mechanic chưa có trong gói, Codex cần đối chiếu lại nguồn; đây là snapshot có ngày, không phải cơ sở dữ liệu tự cập nhật.

## Dùng template trong Minecraft

Template là **cấu hình MythicMobs**, không phải thư mục Codex skill. Lấy `skills/mythicmobs-boss-particles/assets/templates/core/`, chép thành `plugins/MythicMobs/packs/nxk_demo/` trên server thử nghiệm. Không chép toàn bộ gói Codex vào plugins. Sau đó theo `references/validation.md`: `/mm reload`, kiểm tra console, chạy `/mm test cast NXK_Demo_Showcase` trong game và thử mob demo. Boss demo có gây sát thương; kiểm tra ở khu vực thử nghiệm.

File `optional/premium-parameters.skills.yml` cần Premium; các file optional phải được chọn riêng. Phần tương thích ghi rõ các thay đổi 5.11–5.14, tên particle cũ, tính năng WIP và điểm phụ thuộc addon.

## Tự chạy kiểm tra

Trong thư mục skill, dùng Python 3.10+:

```text
python -m pip install -r scripts/requirements.txt
python scripts/validate_templates.py --root assets/templates --report validation.json
python scripts/test_validator.py
```

Xem `validation-report.json`, `validation-tests.txt`, `skill-validation.txt` và `SHA256SUMS.txt` ở gốc gói để biết kết quả lúc đóng gói. Bộ kiểm tra chỉ hỗ trợ cú pháp template của gói; báo “unsupported” không đồng nghĩa cú pháp bên ngoài chắc chắn sai.
