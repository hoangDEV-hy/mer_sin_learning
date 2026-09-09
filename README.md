# Hướng dẫn chạy và nộp bài: Local Server AI Strategy - Naive Bayes

## 1. Mục tiêu dự án

Dự án này triển khai một hệ thống AI cục bộ theo mô hình sau:
- API server nhận dữ liệu đầu vào
- Tiền xử lý dữ liệu
- Huấn luyện và dự đoán bằng mô hình Naive Bayes
- Trả kết quả dự đoán và xác suất
- Cấu hình Docker để chạy local và production-like
- Health check để xác nhận trạng thái hệ thống

Mục tiêu chính là tạo ra một ứng dụng AI hoàn chỉnh, dễ kiểm thử, dễ chạy ở môi trường cục bộ và có thể đóng gói bằng Docker theo đúng yêu cầu của đề tài.

---

## 2. Cấu trúc mã nguồn

Thư mục dự án bao gồm:

```text
hocmaycoban/
├── app.py                  # API Flask + mô hình Naive Bayes
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Cấu hình chạy nhiều service / container
├── requirements.txt        # Dependencies cần thiết
├── README_DOCKER.md        # Hướng dẫn chạy Docker
├── README_SUBMISSION.md    # Tài liệu nộp bài
├── local-server-ai-strategy-naive-bayes.md
├── naive_bayes_colab.py    # Phiên bản chạy trên Colab
├── naive_bayes_colab.ipynb # Notebook Colab
└── .dockerignore           # Bỏ qua file không cần trong Docker image
```

---

## 3. Mô tả dữ liệu đầu vào

Dữ liệu đầu vào là một vector 5 thuộc tính:

```json
{
  "features": [1, 0, 1, 0, 0]
}
```

Các feature tương ứng:
- feature_1
- feature_2
- feature_3
- feature_4
- feature_5

### Giải thích
- Mỗi feature là một số nguyên hoặc số thực
- Mỗi feature phải có đúng 5 giá trị
- API sẽ kiểm tra độ dài mảng đầu vào trước khi đưa vào mô hình
- Nếu thiếu hoặc sai số lượng feature, API trả về lỗi 400

---

## 4. Quy trình huấn luyện mô hình Naive Bayes

Mô hình Naive Bayes được huấn luyện theo quy trình sau:

1. Tạo tập dữ liệu giả lập cho 3 lớp:
   - class_0
   - class_1
   - class_2
2. Sinh dữ liệu với các pattern đặc trưng cho từng lớp
3. Thêm nhiễu ngẫu nhiên để mô phỏng dữ liệu thực tế
4. Chuyển dữ liệu thành ma trận feature
5. Huấn luyện mô hình MultinomialNB từ scikit-learn
6. Tính xác suất của từng lớp
7. Chọn lớp có xác suất lớn nhất làm prediction

### Mã huấn luyện chính

```python
from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB(alpha=1.0)
model.fit(X_train, y_train)
```

### Tính xác suất dự đoán

```python
probabilities = model.predict_proba(feature_vector)[0]
best_index = int(np.argmax(probabilities))
predicted_label = model.classes_[best_index]
confidence = float(probabilities[best_index])
```

---

## 5. Quy trình dự đoán

Khi người dùng gửi request JSON lên endpoint:

```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1,0,1,0,0]}'
```

API sẽ thực hiện các bước:
1. Kiểm tra body JSON hợp lệ
2. Kiểm tra có trường `features` không
3. Kiểm tra số lượng feature
4. Chuyển về ma trận dạng 2D
5. Chạy mô hình Naive Bayes
6. Trả về:
   - prediction
   - probability
   - health_status
   - message

### Response mẫu thành công

```json
{
  "success": true,
  "status": 200,
  "message": "Dự đoán Naive Bayes thành công",
  "data": {
    "model": "naive_bayes",
    "endpoint": "/api/v1/predict",
    "prediction": "class_0",
    "probability": 0.8,
    "health_status": "healthy"
  }
}
```

---

## 6. Endpoint API

### 6.1 Endpoint kiểm tra trạng thái

```http
GET /health
```

### Ví dụ response

```json
{
  "success": true,
  "status": 200,
  "message": "Hệ thống sẵn sàng",
  "data": {
    "model": "naive_bayes",
    "health_status": "healthy",
    "feature_names": ["feature_1", "feature_2", "feature_3", "feature_4", "feature_5"]
  }
}
```

### 6.2 Endpoint dự đoán

```http
POST /api/v1/predict
```

Body JSON:

```json
{
  "features": [1, 0, 1, 0, 0]
}
```

---

## 7. Cấu hình Docker

### 7.1 Dockerfile

Dockerfile sử dụng Python 3.11 slim image và cài các dependency từ requirements.txt:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### 7.2 docker-compose.yml

```yaml
version: "3.9"

services:
  naive-bayes-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: naive-bayes-api
    ports:
      - "5000:5000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()"]
      interval: 15s
      timeout: 5s
      retries: 5
      start_period: 20s
```

### 7.3 Requirements

```txt
flask==3.0.3
numpy==2.1.3
pandas==2.2.3
scikit-learn==1.5.2
```

---

## 8. Hướng dẫn chạy local bằng Docker

### Bước 1: Mở terminal trong thư mục dự án

```bash
cd d:\hocmaycoban
```

### Bước 2: Build và chạy container

```bash
docker compose up --build
```

### Bước 3: Kiểm tra API

```bash
curl http://localhost:5000/health
```

### Bước 4: Gửi request dự đoán

```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1,0,1,0,0]}'
```

### Bước 5: Dừng container

```bash
docker compose down
```

---

## 9. Kịch bản kiểm thử endpoint bằng dòng lệnh

### 9.1 Kiểm thử Health Check

```bash
curl -i http://localhost:5000/health
```

Kỳ vọng:
- status code = 200
- JSON chứa `health_status: "healthy"`

### 9.2 Kiểm thử dự đoán hợp lệ

```bash
curl -i -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1,0,1,0,0]}'
```

Kỳ vọng:
- status code = 200
- field `success` = true
- field `prediction` có giá trị lớp dự đoán
- field `probability` có xác suất > 0

### 9.3 Kiểm thử dữ liệu đầu vào sai

```bash
curl -i -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1,0,1]}'
```

Kỳ vọng:
- status code = 400
- message báo lỗi thiếu hoặc sai số lượng feature

### 9.4 Kiểm thử request không có body

```bash
curl -i -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json"
```

Kỳ vọng:
- status code = 400
- message yêu cầu JSON hợp lệ

---

## 10. Video / hình ảnh minh chứng hệ thống chạy thành công

Để đáp ứng yêu cầu nộp bài, bạn có thể ghi chép hoặc quay video theo các bước sau:

1. Mở terminal
2. Chạy:
   ```bash
   docker compose up --build
   ```
3. Chạy lệnh health check và prediction check
4. Ghi lại màn hình terminal hiển thị output JSON
5. Lưu thành file:
   - `demo_naive_bayes.mp4`
   - hoặc `demo_naive_bayes.png` nếu chỉ cần ảnh chụp màn hình

### Nội dung cần ghi lại
- Container đang chạy
- Endpoint /health trả về status 200
- Endpoint /api/v1/predict trả về prediction và probability
- Không có lỗi trong log container

### Mẫu mô tả trong báo cáo

> Hệ thống Naive Bayes đã được chạy bằng Docker trên môi trường local. API trả về trạng thái healthy và dự đoán thành công với xác suất tương ứng. Quy trình kiểm thử được thực hiện qua curl với đầu vào JSON và kết quả được ghi lại trong video minh chứng.

---

## 11. Checklist nộp bài

Trước khi nộp bài, đảm bảo có đầy đủ các mục sau:

- [ ] Mã nguồn API và mô hình Naive Bayes hoàn chỉnh
- [ ] Tệp Dockerfile
- [ ] Tệp docker-compose.yml
- [ ] Tệp requirements.txt
- [ ] Tài liệu mô tả dữ liệu đầu vào, quy trình huấn luyện, dự đoán và Endpoint
- [ ] Kịch bản kiểm thử bằng dòng lệnh
- [ ] Video hoặc hình ảnh minh chứng hệ thống chạy thành công

---

## 12. Kết luận

Dự án đã hoàn thành đúng mục tiêu theo đề bài: xây dựng hệ thống AI cục bộ với mô hình Naive Bayes, cung cấp endpoint dự đoán, kiểm tra trạng thái hệ thống bằng health check, và đóng gói bằng Docker để chạy trên môi trường local và production-like.

Nếu cần, bạn có thể dùng file này như tài liệu chính để nộp bài, kèm theo các file mã nguồn và hình ảnh/video minh chứng.
