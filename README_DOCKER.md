# Naive Bayes Docker Local Version

## Cài đặt

1. Mở terminal ở thư mục dự án.
2. Chạy:

```bash
docker compose up --build
```

## Kiểm tra API

### Health check
```bash
curl http://localhost:5000/health
```

### Predict
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1,0,1,0,0]}'
```

## Dừng container
```bash
docker compose down
```

## Kết quả mẫu
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
