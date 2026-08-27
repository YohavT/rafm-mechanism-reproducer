from typing import Literal

from pydantic import BaseModel


class Stage1Output(BaseModel):
    confirmed_request: str        # "You want to reproduce X for Y, in model(s) Z."
    interpretation: str
    relevant_branches: list[str]
    keyword_hints: list[str] = []
    assumptions: list[str]
    ambiguities: list[str]        # one sentence each, starting with "Clarify..." or "Confirm..."
    confidence: Literal["high", "medium", "low"]
    halt_reason: str | None = None
