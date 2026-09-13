### TÀI LIỆU HƯỚNG DẪN: TÍCH HỢP MÔ HÌNH VÀ SO SÁNH HIỆU NĂNG TRÊN WEB APPLICATION
#### Chủ đề: Tích hợp Mô hình vào Web App & So sánh Độ chính xác, FPS, Latency, DCN
#### 1. Mục tiêu
*   **Vận hành hệ thống tích hợp**: Xây dựng luồng hoạt động đồng thời giữa API Service Server và mô hình AI chạy ổn định trên máy tính cục bộ [1].
*   **Làm chủ mã nguồn**: Tự phát triển và tách biệt các tầng xử lý (API, tiền xử lý, dự đoán) thay vì sao chép mã nguồn một cách thụ động [4, 11].
*   **Đo lường hiệu năng**: Đánh giá và so sánh các chỉ số vận hành cốt lõi bao gồm Độ chính xác (Accuracy), FPS (Khung hình/giây), Latency (Độ trễ) và khả năng ứng dụng các kiến trúc nâng cao như DCN (Deformable Convolutional Networks).
*   **Ảo hóa bằng Docker**: Đóng gói toàn bộ ứng dụng để đồng bộ môi trường phát triển cục bộ và môi trường sản xuất (Production) [1, 7].

--------------------------------------------------------------------------------

### 2. Công nghệ bắt buộc
*   **Web API Framework** (.NET 8 [26], Node.js hoặc Python FastAPI)
*   **AI Models**: Naive Bayes (Phân loại văn bản/dữ liệu dạng bảng) [1, 2] & Deep Learning Models (Kiến trúc DCN cho thị giác máy tính - *Mở rộng ngoài nguồn*)
*   **Docker & Docker Compose** [2, 7, 34]
*   **RESTful Endpoint & JSON Wrapper** [2, 8, 36]
*   **Benchmark CLI Tools** (Curl, Apache Benchmark hoặc Locust để đo Latency/FPS) [2, 9]
*   **Health Check Monitoring** [2, 7, 36]

--------------------------------------------------------------------------------

### 3. Kiến trúc hệ thống
Áp dụng Kiến trúc tách biệt cấu phần (Multi-component/Clean Architecture) [3, 27] để kiểm thử và đo lường hiệu năng độc lập của từng thành phần [4]:
```text
Hệ thống Tích hợp & Đo lường Hiệu năng (Integration & Benchmark Suite)

Môi trường Container / Máy cục bộ:
 ├── Component 1: API Gateway / Endpoint (Tiếp nhận request) [3]
 ├── Component 2: Tầng Tiền xử lý dữ liệu (Chuẩn hóa input) [3, 4]
 ├── Component 3: Mô hình AI Inference (Thực thi dự đoán)
 │    ├── Bộ xử lý Naive Bayes (Tính toán xác suất Prior & Likelihood) [3, 6]
 │    └── Bộ xử lý Mạng nơ-ron nâng cao (Xử lý hình ảnh, tích hợp DCN)
 └── Component 4: Docker & Monitor (Giám sát Health Check & Đo Latency) [3, 7]
```

--------------------------------------------------------------------------------

### 4. Luồng hoạt động chi tiết và Tác dụng
#### 4.1 Thiết kế cấu phần (Component Design)
*   **Dựng API Endpoint đầu tiên**: Tiếp nhận yêu cầu dự đoán dữ liệu đầu vào để chạy thử nghiệm độc lập [4, 12].
*   **Phân tách cấu phần**: Tách biệt hoàn toàn tầng API, tiền xử lý dữ liệu và logic suy luận của mô hình để dễ dàng kiểm thử độc lập, khoanh vùng lỗi [4].
*   **Xác định đường dẫn giao tiếp**: Khởi tạo rõ ràng các Endpoint (ví dụ: `/api/v1/predict`) để liên kết luồng dữ liệu giữa Web Server và AI Server [4].

--------------------------------------------------------------------------------

#### 4.2 Kiểm thử tham số đầu vào (Parameter Testing)
*   **Đa dạng hóa định dạng đầu vào**: Thiết lập cấu hình Endpoint hỗ trợ nhận dữ liệu linh hoạt dưới dạng JSON, tệp tin hoặc chuỗi ký tự tùy kịch bản sử dụng [5, 20].
*   **Kiểm tra dữ liệu sau tiền xử lý**: Xác thực chất lượng dữ liệu đã làm sạch trước khi truyền vào mô hình nhằm tránh sai lệch kết quả dự đoán [5].
*   **Xác thực mã phản hồi**: Chạy kiểm thử trực tiếp từ dòng lệnh, đối chiếu kết quả phản hồi của mô hình với thực tế để đảm bảo trả về mã trạng thái thành công (Status Code 200) [5, 14].

--------------------------------------------------------------------------------

#### 4.3 Tích hợp máy chủ AI cục bộ (Local AI Integration)
*   **Vận hành song song**: Khởi chạy đồng thời cả API Server và máy chủ AI (AI Server) ngay trên máy cục bộ để kiểm chứng toàn bộ luồng dữ liệu khép kín [6, 25].
*   **Tính toán suy luận**:
    *   *Mô hình Naive Bayes*: Tính xác suất hậu nghiệm (posterior probability) cho từng lớp dữ liệu đã được huấn luyện sẵn và chọn lớp có xác suất cao nhất làm kết quả đầu ra [6].
    *   *Mô hình Deep Learning*: Chuyển tiếp các mảng Tensor qua các lớp tích chập (nhập luồng hình ảnh/video trực tiếp để đo FPS và độ trễ).

--------------------------------------------------------------------------------

#### 4.4 Đóng gói ảo hóa và Triển khai Production (Dockerization & Production)
*   **Đóng gói môi trường**: Sử dụng Docker đóng gói toàn bộ mã nguồn, mô hình và các dependency cần thiết để hệ thống chạy nhanh, nhẹ và tối ưu hóa tài nguyên phần cứng [7, 18].
*   **Thiết lập Health Check**: Cấu hình cơ chế tự động theo dõi sức khỏe hệ thống (Health Check Level), đảm bảo cả Web API và AI Model luôn ở trạng thái sẵn sàng phục vụ [7, 19].
*   **Triển khai Production**: Hoàn tất đóng gói sản phẩm hoàn chỉnh và đẩy lên môi trường Production chạy ổn định sau khi đã vượt qua các kịch bản kiểm thử dòng lệnh [7, 19].

--------------------------------------------------------------------------------

### 5. Bảng so sánh hiệu năng các mô hình
Dưới đây là bảng phân tích so sánh các chỉ số hiệu năng khi tích hợp các kiến trúc mô hình khác nhau vào ứng dụng Web. 

*Lưu ý: Nguồn tài liệu gốc tập trung chủ yếu vào mô hình phân loại Naive Bayes [1, 2]. Các chỉ số về FPS, Latency (Độ trễ mili-giây) và DCN (Deformable Convolutional Networks) dưới đây được tổng hợp dựa trên khung lý thuyết phân tích hiệu năng tích hợp thực tế:*

| Chỉ số so sánh | Mô hình Naive Bayes (Dữ liệu dạng bảng/văn bản) | Mô hình CNN truyền thống (Thị giác máy tính cơ bản) | Mô hình DCN - Deformable CNN (Thị giác máy tính nâng cao) |
| :--- | :--- | :--- | :--- |
| **Bản chất hoạt động** | Tính toán xác suất hậu nghiệm dựa trên tần suất đặc trưng xuất hiện độc lập [6]. | Tích chập hình học với lưới lọc cố định để trích xuất đặc trưng ảnh. | Tích chập biến dạng tự do, tự động điều chỉnh hình dạng lưới lọc theo đối tượng thực tế. |
| **Độ chính xác (Accuracy)** | Khá tốt trên dữ liệu văn bản/phân loại nhanh [6, 8]. Không phù hợp cho dữ liệu hình ảnh phức tạp. | Đạt độ chính xác trung bình đến tốt trên tập dữ liệu ảnh tiêu chuẩn. | **Đạt độ chính xác cực cao**, vượt trội trong các tác vụ phát hiện đối tượng bị biến dạng, xoay hoặc che khuất. |
| **FPS (Khung hình/giây)** | Cực cao (hàng ngàn request/giây) do chỉ tính toán xác suất toán học đơn giản [6]. | Trung bình (từ 30 - 60 FPS tùy phần cứng GPU/CPU). | Thấp hơn CNN truyền thống (từ 15 - 40 FPS) do phải tính thêm độ lệch (offset) của lưới tích chập biến dạng. |
| **Latency (Độ trễ phản hồi)** | **Cực thấp (< 5ms)**. Khởi chạy và xử lý tức thời ngay trên CPU cục bộ [6, 25]. | Trung bình (15ms - 50ms) tùy thuộc vào độ sâu của mạng nơ-ron tích chập. | Cao hơn (30ms - 80ms) do chi phí tính toán các vị trí lấy mẫu biến dạng lớn hơn. |
| **Khả năng đóng gói Docker** | Cực kỳ gọn nhẹ, dung lượng container thấp [7]. | Dung lượng container lớn hơn do phải đi kèm thư viện Deep Learning (PyTorch/TensorFlow) và driver CUDA. | Dung lượng container lớn nhất, yêu cầu tối ưu hóa cấu hình CUDA và phần cứng GPU chuyên dụng khi lên Production [7]. |

--------------------------------------------------------------------------------

### 6. API Response mẫu tích hợp và đo lường
Phản hồi kết quả dự đoán thành công kèm thông số đo lường hiệu năng thực tế từ Endpoint [8]:
```json
{
  "success": true,
  "status": 200,
  "message": "Dự đoán và đo lường hiệu năng thành công",
  "data": {
    "model_configuration": {
      "active_model": "naive_bayes_classifier",
      "architecture_type": "probability_based",
      "endpoint": "/api/v1/predict"
    },
    "prediction_results": {
      "predicted_class": "class_1",
      "confidence_probability": 0.87
    },
    "performance_metrics": {
      "inference_latency_ms": 2.4,
      "estimated_fps": null,
      "hardware_utilization": "CPU_only",
      "health_status": "healthy"
    }
  }
}
```

--------------------------------------------------------------------------------

### 7. Thao tác kiểm thử hiệu năng qua dòng lệnh
Tập lệnh khởi chạy và giả lập kiểm thử hiệu năng tải cục bộ nhanh [9]:
```bash
# 1. Khởi chạy toàn bộ hệ thống Web API và AI Model qua Docker Compose
docker compose up --build

# 2. Gửi request kiểm thử dự đoán và kiểm tra phản hồi HTTP 200
curl -X POST http://localhost:3000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features":["feature_1","feature_2","feature_3"]}'

# 3. Sử dụng công cụ Apache Benchmark (ab) đo lường Latency thực tế của API
ab -n 1000 -c 10 http://localhost:3000/api/v1/predict
```

--------------------------------------------------------------------------------

### 8. Tiêu chí đánh giá chất lượng triển khai
#### Hạng mục đánh giá | Thang điểm
*   **Kiến trúc tách biệt cấu phần (Architecture)**: Thiết kế API độc lập, phân tách rõ ràng tầng tiền xử lý và suy luận của mô hình [4]. | **20 điểm** [10]
*   **Chất lượng tiền xử lý & kiểm thử dữ liệu đầu vào**: Khả năng xử lý đa dạng định dạng đầu vào (JSON, file, string) [5] và làm sạch dữ liệu. | **20 điểm** [10]
*   **Độ chính xác và Hiệu năng suy luận**: Triển khai thuật toán suy luận chính xác [6], đạt độ trễ tối ưu cho từng loại mô hình cụ thể. | **25 điểm** [10]
*   **Đóng gói Container & Cấu hình Docker**: Dockerfile tối ưu dung lượng, cấu hình docker-compose chạy đồng thời toàn bộ dịch vụ mượt mà [7, 9]. | **15 điểm** [10]
*   **Health Check & Giám sát Production**: Thiết lập đầy đủ kịch bản kiểm tra trạng thái sức khỏe dịch vụ khi triển khai thực tế [7]. | **10 điểm** [10]
*   **Tư duy tự chủ mã nguồn (Code Ownership)**: Hiểu rõ cơ chế hoạt động, tự thực hiện tích hợp thay vì sao chép thụ động [11]. | **10 điểm** [10]
