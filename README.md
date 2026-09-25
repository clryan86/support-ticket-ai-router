# Support Ticket AI Router

[![CI](https://github.com/clryan86/support-ticket-ai-router/actions/workflows/ci.yml/badge.svg)](https://github.com/clryan86/support-ticket-ai-router/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![NLP](https://img.shields.io/badge/NLP-TF--IDF%20%2B%20Logistic%20Regression-9C6ADE)
![FastAPI](https://img.shields.io/badge/FastAPI-routing-009688)

An applied-NLP support automation service that **classifies incoming tickets, assigns an operations queue, scores urgency, generates a concise summary, exposes confidence/alternatives, supports batch routing, and captures human feedback** for future retraining.

It runs completely locally—no paid LLM API is required.

## Categories

- access → Identity & Access
- billing → Billing Operations
- technical → Technical Support
- feature_request → Product Feedback

## ML pipeline

A reproducible seed corpus trains a TF-IDF + Logistic Regression classifier. Metadata records the held-out accuracy/macro-F1, classes, version and training timestamp. Generated model artifacts are excluded from Git and recreated automatically.

## Engineering features

- local model training and artifact management
- confidence-ranked alternatives
- deterministic urgency heuristics
- model/version metadata
- single and batch routing
- SQLite decision history
- human feedback endpoint
- operations metrics/dashboard
- bounded Pydantic input validation
- automated tests, Docker and CI

## Quick start

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open `/docs` for the REST API and `/` for the routing dashboard.

## Tests

```bash
pytest
ruff check .
```

## Roadmap

- feedback-driven retraining datasets
- calibrated probabilities
- multilingual routing
- semantic embeddings
- SLA prediction
- PII redaction
- agent-assist answer retrieval
- active learning queue
- model registry/version comparison

## Author

**Christopher Ryan**  
Python • Applied AI • NLP • Automation

## License

MIT
