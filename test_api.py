"""
Quick API connectivity test.
Run: python test_api.py
Verifies: config loading, AzureOpenAI client, instructor structured output.
"""

from pydantic import BaseModel
from src.rafm_reproducer.config import load_config
from src.rafm_reproducer.llm_client import get_client, call_llm


class Ping(BaseModel):
    message: str
    model_used: str


def main():
    cfg = load_config()
    print(f"Model   : {cfg['model']}")
    print(f"Endpoint: {cfg['endpoint']}")
    print(f"API ver : {cfg['api_version']}")
    print()

    client = get_client(cfg)
    print("Client created. Sending test call...")

    result = call_llm(
        client=client,
        model=cfg["model"],
        system="You are a test assistant. Return only valid JSON.",
        user='Reply with {"message": "pong", "model_used": "<your model name>"}',
        response_model=Ping,
    )

    print(f"Response: message='{result.message}'  model_used='{result.model_used}'")
    print("\nAPI connection OK.")


if __name__ == "__main__":
    main()
