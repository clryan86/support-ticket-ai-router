from __future__ import annotations
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from nlp.router import TicketRouter
from .config import Settings
from .schemas import BatchRequest, FeedbackRequest, TicketRequest
from .store import Store

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = Jinja2Templates(directory=str(ROOT / "templates"))

def create_app(settings: Settings | None = None):
    settings = settings or Settings.from_env()
    router = TicketRouter(settings.artifact_dir)
    store = Store(settings.database_path)
    app = FastAPI(title=settings.app_name, version="1.0.0")
    app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")

    @app.get("/healthz")
    def health():
        return {"ok": True, "model_version": router.metadata["version"]}

    @app.get("/", response_class=HTMLResponse)
    def dashboard(request: Request):
        return TEMPLATES.TemplateResponse(
            request=request,
            name="index.html",
            context={"app_name": settings.app_name, "tickets": store.recent(15), "metrics": store.metrics(), "model": router.metadata},
        )

    def process(item: TicketRequest):
        result = router.route(item.subject, item.body)
        ticket_id = store.save(item.subject, item.body, result)
        return {"ticket_id": ticket_id, **result}

    @app.post("/api/route")
    def route(item: TicketRequest):
        return process(item)

    @app.post("/api/route/batch")
    def batch(req: BatchRequest):
        return [process(i) for i in req.items]

    @app.get("/api/tickets")
    def tickets(limit: int = 50):
        return store.recent(max(1, min(limit, 500)))

    @app.get("/api/model")
    def model():
        return router.metadata

    @app.get("/api/metrics")
    def metrics():
        return store.metrics()

    @app.post("/api/tickets/{ticket_id}/feedback")
    def feedback(ticket_id: int, req: FeedbackRequest):
        if not any(t["id"] == ticket_id for t in store.recent(10000)):
            raise HTTPException(404, "Ticket not found")
        store.feedback(ticket_id, req.correct_category, req.notes)
        return {"ok": True}

    return app

app = create_app()
