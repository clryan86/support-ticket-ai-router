# Architecture

```mermaid
flowchart TD
    T[Incoming Ticket] --> API[FastAPI]
    API --> R[Ticket Router]
    R --> V[TF-IDF Vectorizer]
    V --> C[Logistic Regression]
    R --> P[Priority Rules]
    R --> S[Summarizer]
    R --> DB[(Routing History)]
    H[Human Feedback] --> DB
    DB --> M[Metrics Dashboard]
```

Classification and priority are deliberately separate. The statistical model predicts issue category; deterministic business rules score operational urgency. That keeps escalation policy inspectable rather than hiding it inside the classifier.
