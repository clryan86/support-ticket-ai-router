from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    artifact_dir: Path
    database_path: Path
    app_name: str = "Support Ticket AI Router"

    @classmethod
    def from_env(cls):
        root = Path(__file__).resolve().parents[1]
        return cls(
            Path(os.getenv("ARTIFACT_DIR", root / "artifacts")),
            Path(os.getenv("DATABASE_PATH", root / "data" / "tickets.db")),
        )
