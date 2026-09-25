# Interview Guide

## 30-second explanation

> Support Ticket AI Router is a local NLP service that classifies tickets into support domains using TF-IDF and Logistic Regression. It returns confidence-ranked categories, maps the winner to an operational queue, calculates priority with transparent urgency rules, summarizes the ticket, stores routing decisions, and captures human corrections for future retraining.

## Why not use an LLM for everything?

A small supervised classifier is cheaper, deterministic, fast, easy to test, and appropriate for a narrow routing taxonomy. The architecture can add an LLM later for richer summarization or agent assistance without making the core routing depend on an external service.

## Why separate priority from category?

“Technical” does not automatically mean urgent, and “billing” can still involve a severe duplicate charge. Priority is an operational policy layer and should remain transparent and independently adjustable.

## Resume bullets

- Built an NLP ticket-routing service using TF-IDF and Logistic Regression with confidence-ranked classifications and reproducible local training.
- Added deterministic urgency scoring, support-queue mapping, concise summaries, batch inference, routing history, and human-feedback capture.
- Shipped FastAPI endpoints, automated tests, Docker/CI, model metadata, dashboard and architecture documentation.
