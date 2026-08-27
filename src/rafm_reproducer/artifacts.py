import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from .config import RUNS_DIR


def new_run_dir() -> tuple[str, Path]:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_id, run_dir


def save_json(run_dir: Path, name: str, data: Any) -> Path:
    path = run_dir / f"{name}.json"
    if isinstance(data, BaseModel):
        path.write_text(data.model_dump_json(indent=2), encoding="utf-8")
    elif isinstance(data, list) and data and isinstance(data[0], BaseModel):
        path.write_text(
            json.dumps([item.model_dump() for item in data], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    else:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def save_text(run_dir: Path, name: str, text: str) -> Path:
    path = run_dir / f"{name}.txt"
    path.write_text(text, encoding="utf-8")
    return path


def load_json(run_dir: Path, name: str) -> Any:
    return json.loads((run_dir / f"{name}.json").read_text(encoding="utf-8"))
