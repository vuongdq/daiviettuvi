# Lá Số Tử Vi

Lá Số Tử Vi là một ứng dụng web giúp bạn xem và phân tích lá số tử vi của mình. Ứng dụng này được xây dựng bằng Django và sử dụng CSS để tạo giao diện đẹp mắt.

## Chức năng

- Hiển thị lá số tử vi với các cung và sao theo đúng vị trí.
- Cung cấp thông tin chi tiết về các sao chính và sao phụ.
- Hiển thị màu sắc tương ứng với ngũ hành của từng cung.
- Hỗ trợ người dùng xem và phân tích lá số tử vi của mình một cách dễ dàng.

## Hướng dẫn cài đặt

1. **Clone repository:**
   ```bash
   git clone https://github.com/your-username/lasotuvi-django.git
   cd lasotuvi-django
   ```

2. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Cấu hình cơ sở dữ liệu:**
   - Mở file `lasotuvi/settings.py` và cấu hình cơ sở dữ liệu theo nhu cầu của bạn.
   - Tạo cơ sở dữ liệu và chạy các lệnh sau để tạo bảng:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

4. **Chạy server:**
   ```bash
   python manage.py runserver
   ```

5. **Truy cập ứng dụng:**
   Mở trình duyệt và truy cập `http://localhost:8000` để sử dụng ứng dụng.

## Lưu ý

- Đảm bảo rằng file `texture.jpg` trong thư mục `static` là một file hình ảnh hợp lệ và không bị hỏng.
- Nếu gặp vấn đề với việc load CSS, hãy thử xóa cache trình duyệt hoặc mở trang trong chế độ ẩn danh.

Chúc bạn thành công với việc sử dụng Lá Số Tử Vi!# daiviettuvi
