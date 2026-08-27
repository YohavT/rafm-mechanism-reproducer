import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = _ROOT / "config.yaml"
PROMPTS_DIR = Path(__file__).parent / "prompts"
RUNS_DIR = _ROOT / "runs"


def _build_cfg(raw: dict, model: str) -> dict:
    endpoint = os.getenv("RAFM_ENDPOINT") or raw.get("endpoints", {}).get("tel_aviv", "")
    api_key = os.getenv("RAFM_API_KEY") or raw.get("api_keys", {}).get("tel_aviv", "")
    api_version = raw.get("llm_api_versions", {}).get(model) or "2024-12-01-preview"
    return {"model": model, "endpoint": endpoint, "api_key": api_key, "api_version": api_version}


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    model = os.getenv("RAFM_MODEL") or raw.get("llm_deployment", "gpt-5.4-deployment")
    return _build_cfg(raw, model)


def load_premium_cfg() -> dict:
    """Config for the premium model (GPT-5.5) used for stages 4 and 5."""
    with open(CONFIG_PATH, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    model = raw.get("llm_deployment_premium") or raw.get("llm_deployment", "GPT-5.5")
    return _build_cfg(raw, model)


def load_prompt(name: str, **kwargs: str) -> str:
    """Load a prompt .txt file and fill {placeholders} with kwargs."""
    path = PROMPTS_DIR / f"{name}.txt"
    text = path.read_text(encoding="utf-8")
    if kwargs:
        text = text.format_map(kwargs)
    return text


def available_models() -> list[str]:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return list(raw.get("llm_api_versions", {}).keys())
