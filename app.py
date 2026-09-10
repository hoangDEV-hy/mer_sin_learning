import numpy as np
from flask import Flask, jsonify, request

FEATURE_NAMES = ["feature_1", "feature_2", "feature_3", "feature_4", "feature_5"]


def build_training_data():
    rng = np.random.default_rng(42)
    profiles = {
        "class_0": np.array([1, 0, 1, 0, 0], dtype=int),
        "class_1": np.array([0, 1, 0, 1, 1], dtype=int),
        "class_2": np.array([1, 1, 1, 0, 1], dtype=int),
    }

    rows = []
    for label, base in profiles.items():
        for _ in range(120):
            noise = rng.integers(0, 2, size=len(FEATURE_NAMES))
            features = np.clip(base + noise, 0, 2).astype(int)
            row = {name: int(value) for name, value in zip(FEATURE_NAMES, features)}
            row["label"] = label
            rows.append(row)

    return rows


def train_model():
    from sklearn.naive_bayes import MultinomialNB

    rows = build_training_data()
    X = np.array([[row[name] for name in FEATURE_NAMES] for row in rows], dtype=float)
    y = np.array([row["label"] for row in rows], dtype=object)

    model = MultinomialNB(alpha=1.0)
    model.fit(X, y)
    return model


MODEL = train_model()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "success": True,
            "status": 200,
            "message": "Naive Bayes Local Docker API",
            "data": {
                "model": "naive_bayes",
                "endpoint": "/api/v1/predict",
                "health_status": "healthy",
            },
        }
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "success": True,
            "status": 200,
            "message": "Hệ thống sẵn sàng",
            "data": {
                "model": "naive_bayes",
                "health_status": "healthy",
                "feature_names": FEATURE_NAMES,
            },
        }
    )


@app.route("/api/v1/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({
            "success": False,
            "status": 400,
            "message": "Request body phải là JSON hợp lệ",
            "data": {},
        }), 400

    if "features" not in payload:
        return jsonify({
            "success": False,
            "status": 400,
            "message": "Thiếu trường 'features' trong JSON",
            "data": {},
        }), 400

    try:
        features = payload["features"]
        if not isinstance(features, list):
            raise ValueError("features phải là kiểu list")
        if len(features) != len(FEATURE_NAMES):
            raise ValueError(f"features cần đúng {len(FEATURE_NAMES)} phần tử")

        value_array = np.asarray(features, dtype=float).reshape(1, -1)
        probs = MODEL.predict_proba(value_array)[0]
        predicted_label = MODEL.classes_[int(np.argmax(probs))]
        confidence = float(probs[np.argmax(probs)])
    except ValueError as exc:
        return jsonify({
            "success": False,
            "status": 400,
            "message": str(exc),
            "data": {},
        }), 400
    except Exception as exc:
        return jsonify({
            "success": False,
            "status": 500,
            "message": f"Lỗi khi dự đoán: {str(exc)}",
            "data": {},
        }), 500

    return jsonify(
        {
            "success": True,
            "status": 200,
            "message": "Dự đoán Naive Bayes thành công",
            "data": {
                "model": "naive_bayes",
                "endpoint": "/api/v1/predict",
                "prediction": predicted_label,
                "probability": round(confidence, 4),
                "health_status": "healthy",
            },
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
