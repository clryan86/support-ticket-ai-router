from pathlib import Path

from nlp.router import TicketRouter, priority, summarize
from nlp.training import train

def test_model_routes_obvious_examples(tmp_path: Path):
    train(tmp_path, version="test")
    router = TicketRouter(tmp_path, "test")
    assert router.route("Invoice problem", "I was charged twice for my subscription")["category"] == "billing"
    assert router.route("Login blocked", "I cannot log in and my account says unauthorized")["category"] == "access"

def test_priority_and_summary():
    level, score = priority("Production is down and service unavailable", "technical")
    assert level in {"high", "critical"}
    assert score >= 70
    assert summarize("one two three four", max_words=3).endswith("…")
