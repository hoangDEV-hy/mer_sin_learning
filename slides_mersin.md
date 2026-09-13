# Slide 1 — Kiến thức nền tảng cần nắm

- **RESTful API:** Cơ chế giao tiếp giữa Client và Server qua HTTP.
- **HTTP:** Method, Endpoint, Status Code và Error Handling.
- **Naive Bayes:** Mô hình phân loại dựa trên Prior, Likelihood, Posterior và Argmax.
- **Preprocessing:** Chuẩn bị, làm sạch và kiểm tra dữ liệu đầu vào.
- **Docker:** Đóng gói ứng dụng, Model và Dependencies trong môi trường nhất quán.
- **Testing:** Đánh giá từng thành phần và toàn bộ luồng hệ thống.
- **Production:** Vận hành ổn định với Health Check, Logging, Security và Monitoring.

---

# Slide 2 — RESTful API & HTTP

### RESTful API

- Client gửi Request đến Server thông qua HTTP.
- Server cung cấp chức năng thông qua các Endpoint.
- Request và Response thường sử dụng định dạng JSON.
- API cần có quy ước rõ ràng về dữ liệu và Error Handling.

### HTTP Method

| Method      | Mục đích                 |
| ----------- | ------------------------ |
| `GET`       | Truy vấn dữ liệu         |
| `POST`      | Gửi dữ liệu hoặc dự đoán |
| `PUT/PATCH` | Cập nhật dữ liệu         |
| `DELETE`    | Xóa dữ liệu              |

### Status Code chính

- `200`: Request được xử lý thành công.
- `400/422`: Dữ liệu Input không hợp lệ.
- `404`: Không tìm thấy Endpoint hoặc tài nguyên.
- `500`: Xảy ra lỗi trong Server.
- `503`: Service tạm thời không khả dụng.

**Ví dụ Endpoint:** `POST /api/v1/predict`

---

# Slide 3 — Naive Bayes & Tiền xử lý

### Naive Bayes

`Posterior ∝ Prior × Likelihood`

- **Prior:** Xác suất ban đầu của mỗi lớp.
- **Likelihood:** Mức độ phù hợp của Features với một lớp.
- **Posterior:** Xác suất cập nhật sau khi nhận Input.
- **Argmax:** Lựa chọn lớp có xác suất cao nhất.

### Quy trình tổng quát

`Input → Preprocessing → Naive Bayes → Prediction`

### Tiền xử lý

- Kiểm tra dữ liệu thiếu, rỗng hoặc sai định dạng.
- Chuẩn hóa kiểu dữ liệu và cấu trúc Input.
- Đảm bảo đúng số lượng và định dạng Features.
- Chỉ chuyển dữ liệu hợp lệ đến Model.
- Trả về Error phù hợp khi Input không hợp lệ.

---

# Slide 4 — Docker, Health Check & Production

### Docker

- Đóng gói API, AI Model và Dependencies.
- Tạo môi trường chạy nhất quán giữa Local và Production.
- Docker Compose hỗ trợ quản lý nhiều Service.
- Giúp triển khai, khởi động và dừng hệ thống theo cấu hình chung.

### Health Check

- **Liveness:** Xác nhận Service vẫn đang hoạt động.
- **Readiness:** Xác nhận Service sẵn sàng nhận Request.
- Kiểm tra trạng thái API, Model và AI Service.
- Cung cấp thông tin để phát hiện Service lỗi hoặc không khả dụng.

### Production

- Sử dụng HTTPS và Authentication phù hợp.
- Quản lý Secret thông qua biến môi trường.
- Theo dõi Logs, Metrics và Health Status.
- Chuẩn bị phương án Rollback khi triển khai không thành công.

---

# Slide 5 — Testing & Debugging

### Các loại kiểm thử

- **Unit Test:** Kiểm tra hành vi của từng hàm hoặc Module.
- **Integration Test:** Kiểm tra sự kết nối giữa API và AI.
- **End-to-End Test:** Kiểm tra toàn bộ luồng từ Request đến Response.
- **CLI Test:** Kiểm thử Endpoint bằng Curl hoặc công cụ dòng lệnh.

### Luồng kiểm thử

`Client → API → Preprocessing → AI → Response`

### Debugging

- Kiểm tra Status Code, Response và Logs.
- Kiểm tra Container, Port và Environment.
- Kiểm tra kết nối giữa các Service.
- Phân tích nguyên nhân của lỗi `400`, `500` hoặc `503`.
- Xác nhận từng cấu phần trước khi kiểm tra toàn bộ hệ thống.

---

# Slide 6 — Chiến lược Triển khai AI & Tích hợp Máy chủ Cục bộ

### Mục tiêu

- Tích hợp **API Server** và **AI Server** trong cùng một hệ thống.
- Xây dựng kiến trúc nhiều cấu phần với trách nhiệm rõ ràng.
- Cho phép phát triển và kiểm thử độc lập từng thành phần.
- Đóng gói hệ thống bằng Docker để thuận tiện triển khai.
- Chuẩn bị nền tảng chuyển đổi từ Local lên Production.

**Mô hình AI:** Naive Bayes

### Luồng hệ thống

`Client → API → Preprocessing → AI Model → Response`

---

# Slide 7 — Kiến trúc Hệ thống

### Các thành phần

- **Client:** Tạo và gửi Request đến hệ thống.
- **API Server:** Tiếp nhận Request, điều phối xử lý và trả Response.
- **Preprocessing:** Làm sạch, chuẩn hóa và xác thực dữ liệu.
- **AI Server:** Cung cấp chức năng huấn luyện và dự đoán.
- **Docker:** Quản lý môi trường, Container và Dependencies.

### Lợi ích

- Tách biệt trách nhiệm giữa các cấu phần.
- Dễ phát triển, kiểm thử và bảo trì.
- Dễ xác định vị trí phát sinh lỗi.
- Có thể mở rộng hoặc thay đổi từng Service.
- Hỗ trợ triển khai nhất quán giữa Local và Production.

---

# Slide 8 — Giai đoạn 1 & 2: Thiết kế và Kiểm thử

### Component Design

- Xây dựng Endpoint cho chức năng dự đoán.
- Phân tách rõ Input, Preprocessing, Model và Response.
- Xác định cách các Component giao tiếp với nhau.
- Kiểm thử từng thành phần trước khi tích hợp toàn bộ.

### Parameter Testing

- Hỗ trợ Input dạng JSON, File hoặc String.
- Kiểm tra cấu trúc, kiểu dữ liệu và giá trị Input.
- Chuẩn hóa dữ liệu trước khi gọi Model.
- Kiểm thử Endpoint bằng CLI/Curl.
- Xác nhận Response và Status Code `200 OK` khi xử lý thành công.

---

# Slide 9 — Giai đoạn 3 & 4: AI Integration → Production

### Local AI Integration

**Training**

- Chuẩn hóa Dataset phục vụ huấn luyện.
- Tính toán Prior và Likelihood.
- Lưu các tham số cần thiết của Model.
- Kiểm tra khả năng sử dụng Model sau khi Training.

**Prediction**

`Request → Preprocessing → Posterior → Argmax → Prediction`

- Nhận dữ liệu từ API.
- Tính Posterior cho các lớp.
- Sử dụng Argmax để chọn Prediction.
- Trả kết quả và Probability về API.

### Docker & Production

- Đóng gói API, Model và Dependencies.
- Quản lý các Service bằng Docker Compose.
- Thiết lập Health Check cho hệ thống.
- Kiểm thử trong môi trường Container.
- Triển khai từ Local lên Production theo cấu hình thống nhất.

---

# Slide 10 — API Response & Kiểm thử CLI

### API Response mẫu

```json
{
  "model": "naive_bayes",
  "model_version": "1.0.0",
  "prediction": "class_1",
  "probability": 0.87,
  "health_status": "healthy"
}
```

**HTTP Status:** `200 OK`

### Khởi chạy hệ thống

```bash
docker compose up --build
```

### Health Check

```bash
curl http://localhost:3000/health
```

### Prediction

```bash
curl -X POST http://localhost:3000/api/v1/predict \
-H "Content-Type: application/json" \
-d '{"features":["feature_1","feature_2"]}'
```

### Dừng hệ thống

```bash
docker compose down
```

### Nội dung cần xác nhận

- API Server khởi động thành công.
- Health Check trả về trạng thái phù hợp.
- Input được Preprocessing chính xác.
- AI Model trả về Prediction và Probability.
- API Response có cấu trúc và Status Code đúng.

---

# Slide 11 — Tiêu chí Đánh giá

| Tiêu chí                   |    Điểm |
| -------------------------- | ------: |
| Kiến trúc tách cấu phần    |      15 |
| Tiền xử lý và Validation   |      15 |
| Naive Bayes                |      20 |
| Docker và Container        |      15 |
| Health Check và Production |      10 |
| Testing và Debugging       |      10 |
| Bảo mật và cấu hình        |       5 |
| Code Ownership và tài liệu |      10 |
| **Tổng**                   | **100** |

### Hồ sơ bàn giao

- Source Code / Git.
- Dockerfile / Docker Compose.
- Model và Dataset mẫu.
- Tài liệu API và hướng dẫn cài đặt.
- File cấu hình môi trường mẫu.
- Unit Test, Integration Test và CLI Script.
- Tài liệu Health Check.
- Hình ảnh hoặc Video minh chứng.
- Báo cáo đánh giá Model và kết quả kiểm thử.
- Mô tả cách triển khai từ Local lên Production.
