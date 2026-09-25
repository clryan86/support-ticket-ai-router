from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

CATEGORIES = ["access", "billing", "technical", "feature_request"]
SEED = {
    "access": [
        "I cannot log in to my account", "password reset link does not work",
        "locked out after too many attempts", "two factor code never arrives",
        "SSO login is failing", "account says unauthorized", "need access to the admin portal",
        "my credentials are rejected", "invite link expired", "cannot sign into dashboard",
        "permission denied for my user", "forgot password and cannot reset",
    ],
    "billing": [
        "charged twice for my subscription", "invoice amount is incorrect", "need a copy of my receipt",
        "credit card was billed after cancellation", "refund has not arrived", "pricing on invoice is wrong",
        "update billing address", "payment failed but card is valid", "unexpected charge on account",
        "need VAT information on invoice", "subscription renewal charge question", "where can I download invoices",
    ],
    "technical": [
        "application crashes when uploading file", "API returns a 500 error", "dashboard is extremely slow",
        "data export fails every time", "integration stopped syncing", "webhook requests are timing out",
        "mobile app freezes on launch", "reports are missing recent records", "search endpoint returns empty results",
        "CSV import throws an error", "notification service is unavailable", "page shows server error",
    ],
    "feature_request": [
        "please add dark mode", "would like CSV scheduled exports", "can you support another SSO provider",
        "please add bulk editing", "need an API for this workflow", "would like custom dashboard widgets",
        "add support for multiple currencies", "please add Slack notifications", "need role based permissions",
        "would like a mobile widget", "add more report filters", "can you support recurring reports",
    ],
}


def dataset():
    rows = []
    for label, texts in SEED.items():
        for text in texts:
            rows.append({"text": text, "label": label})
    return pd.DataFrame(rows)


def train(artifact_dir: Path, version="1.0.0"):
    artifact_dir = Path(artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    df = dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        df.text, df.label, test_size=.25, random_state=42, stratify=df.label
    )
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), stop_words="english")),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    meta = {
        "version": version,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "classes": list(pipe.classes_),
        "training_rows": len(X_train),
        "test_rows": len(X_test),
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "macro_f1": round(float(f1_score(y_test, pred, average="macro")), 4),
        "report": classification_report(y_test, pred, output_dict=True, zero_division=0),
    }
    joblib.dump(pipe, artifact_dir / "router.joblib")
    (artifact_dir / "metadata.json").write_text(json.dumps(meta, indent=2))
    return meta
