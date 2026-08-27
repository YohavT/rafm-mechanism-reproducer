from typing import TypeVar, Type

import httpx
import instructor
from openai import AzureOpenAI
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def get_client(cfg: dict):
    """Build an instructor-patched AzureOpenAI client from a config dict."""
    # No connection pooling — each call gets a fresh TCP connection.
    # This prevents stale-connection errors when one stage finishes and
    # the next stage immediately starts a new request to the APIM.
    http_client = httpx.Client(
        timeout=httpx.Timeout(900.0),
        limits=httpx.Limits(max_keepalive_connections=0, max_connections=10),
    )
    kwargs: dict = {
        "api_key": cfg["api_key"],
        "azure_endpoint": cfg["endpoint"],
        "api_version": cfg.get("api_version") or "2024-12-01-preview",
        "http_client": http_client,
    }

    azure_client = AzureOpenAI(**kwargs)
    return instructor.from_openai(azure_client, mode=instructor.Mode.JSON)


def call_llm(
    client,
    model: str,
    system: str,
    user: str,
    response_model: Type[T],
    max_retries: int = 3,
) -> T:
    """
    Call the LLM and return a validated Pydantic object.
    instructor handles schema-level retries automatically (up to max_retries).
    Semantic-level retries (numero existence checks, etc.) are handled by callers.
    """
    return client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_model=response_model,
        max_retries=max_retries,
    )
