### Hướng dẫn tích hợp Máy chủ Cục bộ và Chiến lược Triển khai AI
#### Chủ đề: Thiết lập, Kiểm thử và Triển khai Đa cấu phần có Tích hợp AI (Multi-Component & AI Integration)

#### 1. Mục tiêu
* Vận hành đồng thời máy chủ dịch vụ và máy chủ AI (AI Server) ổn định ngay trên máy tính cục bộ [15].
* Làm chủ hoàn toàn mã nguồn, khuyến khích tự xây dựng và hiểu rõ bản chất hoạt động của hệ thống thay vì sao chép thụ động [1].
* Thực hiện ảo hóa nhanh chóng bằng Docker giúp đồng bộ môi trường phát triển cục bộ và môi trường production [8].
* Đóng gói, kiểm tra mức độ sức khỏe và triển khai ổn định sản phẩm trên môi trường thực tế (Production) [9].

--------------------------------------------------------------------------------

### 2. Công nghệ bắt buộc
* Docker ("Đô-qua") [8]
* AI Server (Máy chủ AI chuyên biệt) [15]
* API Service Server (Máy chủ dịch vụ tích hợp) [15]
* RESTful Endpoint [5]
* Health Check Monitoring (Kiểm tra cấp độ sức khỏe) [9]
* Command Line Testing Tools (Kiểm thử qua dòng lệnh) [12]

--------------------------------------------------------------------------------

### 3. Kiến trúc
Áp dụng kiến trúc đa cấu phần (Multi-component Architecture) để phục vụ phối hợp nhóm hiệu quả [14], phân tách rạch ròi giữa Server dịch vụ và AI Server [15].
```text
Hệ thống tích hợp (Local Integration Suite)

Cục bộ (Local machine) / Container:
 ├── Component 1 (Dịch vụ Endpoint) [5]
 ├── Component 2 (Xử lý Logic) [14]
 ├── AI Server Endpoint (Phục vụ Model AI) [15]
 └── Docker Environment (Môi trường ảo hóa) [8]
```
Không chia sẻ chung tài nguyên khi chưa phân rã Endpoint rõ rệt [5].

--------------------------------------------------------------------------------

### 4. Luồng hoạt động chi tiết
#### 4.1 Thiết kế cấu phần (Component Design)
* Dựng cấu phần đầu tiên để chạy thử nghiệm độc lập [2].
* Phân tách riêng biệt các thành phần nghiệp vụ và các Endpoint để dễ quản lý, tránh viết gộp [5].
* Khởi tạo Endpoint và lấy đường dẫn liên kết (link) để các cấu phần giao tiếp chéo [6].

--------------------------------------------------------------------------------

#### 4.2 Kiểm thử tham số đầu vào (Parameter Testing)
* Hỗ trợ truyền linh hoạt các tham số đầu vào (Parameter) dưới dạng file vật lý hoặc chuỗi ký tự [10, 11].
* Kiểm tra mã trạng thái phản hồi của Endpoint (mong đợi trả về mã 200 thành công) [4].
* Thực thi lệnh kiểm thử trực tiếp từ dòng lệnh (Command) để xác thực tính đúng đắn ngay lập tức [12].

--------------------------------------------------------------------------------

#### 4.3 Tích hợp máy chủ AI cục bộ (Local AI Integration)
* Thiết lập và kết hợp đa cấu phần (Multi-component), phân bổ công việc phối hợp nhóm thay vì tự làm đơn lẻ một mình [14].
* Vận hành song song AI Server và Web Server trên môi trường máy cục bộ để kiểm chứng luồng nghiệp vụ hoàn chỉnh trước khi đưa lên đám mây [15].

--------------------------------------------------------------------------------

#### 4.4 Đóng gói ảo hóa và Triển khai Production (Dockerization & Production)
* Sử dụng Docker để ảo hóa ứng dụng giúp rút ngắn thời gian thiết lập môi trường và chạy nhanh chóng [8].
* Thiết lập kiểm tra sức khỏe hệ thống (Health check level) để phát hiện sự cố tự động [9].
* Thực hiện đóng gói sản phẩm hoàn chỉnh và đẩy lên môi trường sản xuất thực tế (Production) để chạy ổn định [9].

--------------------------------------------------------------------------------

### 5. API Response mẫu
Phản hồi kiểm thử Endpoint thành công:
```json
{
  "success": true,
  "status": 200,
  "message": "Kiểm thử cấu phần cục bộ thành công",
  "data": {
    "component_id": "comp-01",
    "endpoint": "/api/v1/ai-inference",
    "health_status": "healthy"
  }
}
```

--------------------------------------------------------------------------------

### 6. Thao tác Docker cơ bản
Tệp cấu hình chạy thử nghiệm cục bộ nhanh:
```bash
# Khởi chạy toàn bộ hệ thống cục bộ (Dịch vụ & AI Server) bằng Docker
docker compose up --build
```

--------------------------------------------------------------------------------

### 7. Tiêu chí đánh giá
Hạng mục                                  Điểm
--------------------------------------------------------------------------------
Kiến trúc tách cấu phần (Architecture)      20
Xử lý tham số & Kiểm thử đầu vào            20
Tích hợp song song AI Server & API Server   25
Đóng gói Container & Cấu hình Docker        15
Thiết lập Health Check & Triển khai Prod     10
Tư duy tự chủ mã nguồn (Code Ownership)     10
--------------------------------------------------------------------------------

### 8. Yêu cầu nộp bài
* Mã nguồn tích hợp cục bộ hoàn chỉnh.
* Tệp cấu hình Dockerfile và docker-compose.yml [13].
* Tài liệu đặc tả Endpoint và kịch bản test bằng dòng lệnh [12].
* Video/Hình ảnh minh chứng hệ thống chạy song song AI Server thành công [15].
