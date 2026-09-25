from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

import joblib

from .training import train

QUEUE_MAP = {
    "access": "Identity & Access",
    "billing": "Billing Operations",
    "technical": "Technical Support",
    "feature_request": "Product Feedback",
}
URGENT = re.compile(r"\b(outage|down|urgent|production|security|breach|cannot access|locked out|500 error|unavailable)\b", re.I)
HIGH = re.compile(r"\b(failed|error|charged twice|refund|crash|timeout|blocked)\b", re.I)


def summarize(text: str, max_words=22) -> str:
    clean = " ".join(text.split())
    words = clean.split()
    return " ".join(words[:max_words]) + ("…" if len(words) > max_words else "")


def priority(text: str, category: str) -> tuple[str, int]:
    score = 50
    if category == "technical":
        score += 8
    if URGENT.search(text):
        score += 30
    elif HIGH.search(text):
        score += 15
    if re.search(r"\b(critical|asap|immediately)\b", text, re.I):
        score += 10
    score = min(100, score)
    level = "critical" if score >= 90 else "high" if score >= 70 else "normal"
    return level, score


class TicketRouter:
    def __init__(self, artifact_dir: Path, version="1.0.0"):
        self.dir = Path(artifact_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        model = self.dir / "router.joblib"
        meta = self.dir / "metadata.json"
        if not model.exists() or not meta.exists():
            train(self.dir, version)
        self.model = joblib.load(model)
        self.metadata = json.loads(meta.read_text())

    def route(self, subject: str, body: str) -> dict[str, Any]:
        text = f"{subject}. {body}".strip()
        probs = self.model.predict_proba([text])[0]
        classes = list(self.model.classes_)
        idx = int(probs.argmax())
        category = classes[idx]
        confidence = float(probs[idx])
        order = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:3]
        level, score = priority(text, category)
        return {
            "category": category,
            "queue": QUEUE_MAP[category],
            "confidence": round(confidence, 6),
            "alternatives": [{"category": c, "probability": round(float(p), 6)} for c, p in order],
            "priority": level,
            "priority_score": score,
            "summary": summarize(body or subject),
            "model_version": self.metadata["version"],
        }
