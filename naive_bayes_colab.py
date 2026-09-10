import argparse
import json
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from sklearn.naive_bayes import MultinomialNB

FEATURE_NAMES = [
    "feature_1",
    "feature_2",
    "feature_3",
    "feature_4",
    "feature_5",
]

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def build_training_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    profile_map = {
        "class_0": np.array([1, 0, 1, 0, 0], dtype=int),
        "class_1": np.array([0, 1, 0, 1, 1], dtype=int),
        "class_2": np.array([1, 1, 1, 0, 1], dtype=int),
    }

    rows: List[Dict[str, Any]] = []
    for label, base in profile_map.items():
        for _ in range(80):
            noise = rng.integers(0, 2, size=len(FEATURE_NAMES))
            features = np.clip(base + noise, 0, 2).astype(int)

            row = {f"feature_{i + 1}": int(value) for i, value in enumerate(features)}
            row["label"] = label
            rows.append(row)

    return pd.DataFrame(rows)


def train_model() -> MultinomialNB:
    df = build_training_data()
    X = df[FEATURE_NAMES]
    y = df["label"]

    model = MultinomialNB(alpha=1.0)
    model.fit(X, y)
    return model


MODEL = train_model()


def normalize_features(raw_features: Any) -> List[float]:
    if isinstance(raw_features, str):
        raw_features = raw_features.strip().split(",")

    if not isinstance(raw_features, (list, tuple, np.ndarray)):
        raise ValueError("features phải là list/tuple/array hoặc chuỗi phân tách bằng dấu phẩy")

    values = []
    for value in raw_features:
        try:
            values.append(float(value))
        except (TypeError, ValueError):
            raise ValueError(f"Giá trị feature không hợp lệ: {value}")

    if len(values) != len(FEATURE_NAMES):
        raise ValueError(
            f"Mỗi record cần {len(FEATURE_NAMES)} features, nhận được {len(values)}"
        )

    return values


def predict_with_model(raw_features: Any) -> Dict[str, Any]:
    values = normalize_features(raw_features)
    feature_vector = np.asarray([values], dtype=float)
    probabilities = MODEL.predict_proba(feature_vector)[0]
    best_idx = int(np.argmax(probabilities))
    predicted_label = MODEL.classes_[best_idx]
    confidence = float(probabilities[best_idx])

    return {
        "prediction": predicted_label,
        "probability": confidence,
        "probabilities": {
            label: float(probabilities[i]) for i, label in enumerate(MODEL.classes_)
        },
    }


@app.route("/", methods=["GET"])
def root() -> Any:
    return jsonify(
        {
            "success": True,
            "status": 200,
            "message": "Naive Bayes Local AI API",
            "data": {
                "model": "naive_bayes",
                "version": "1.0.0",
                "health_status": "healthy",
                "endpoint": "/api/v1/predict",
            },
        }
    )


@app.route("/health", methods=["GET"])
def health() -> Any:
    return jsonify(
        {
            "success": True,
            "status": 200,
            "message": "Hệ thống sẵn sàng",
            "data": {
                "model": "naive_bayes",
                "health_status": "healthy",
                "features": FEATURE_NAMES,
            },
        }
    )


@app.route("/api/v1/predict", methods=["POST"])
def predict_api() -> Any:
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify(
            {
                "success": False,
                "status": 400,
                "message": "Body request phải là JSON hợp lệ",
                "data": {},
            }
        ), 400

    if "features" not in payload:
        return jsonify(
            {
                "success": False,
                "status": 400,
                "message": "Thiếu field 'features' trong JSON",
                "data": {},
            }
        ), 400

    try:
        result = predict_with_model(payload["features"])
    except ValueError as exc:
        return jsonify(
            {
                "success": False,
                "status": 400,
                "message": str(exc),
                "data": {},
            }
        ), 400
    except Exception as exc:  # pragma: no cover
        return jsonify(
            {
                "success": False,
                "status": 500,
                "message": f"Lỗi khi dự đoán: {str(exc)}",
                "data": {},
            }
        ), 500

    response = {
        "success": True,
        "status": 200,
        "message": "Dự đoán Naive Bayes thành công",
        "data": {
            "model": "naive_bayes",
            "endpoint": "/api/v1/predict",
            "prediction": result["prediction"],
            "probability": round(float(result["probability"]), 4),
            "health_status": "healthy",
        },
    }
    return jsonify(response), 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Naive Bayes Local AI API")
    parser.add_argument("--host", default="0.0.0.0", help="Host bind")
    parser.add_argument("--port", type=int, default=5000, help="Port bind")
    parser.add_argument("--debug", action="store_true", help="Chế độ debug")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug, use_reloader=False)
