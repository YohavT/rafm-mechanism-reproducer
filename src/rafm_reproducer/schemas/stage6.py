from typing import Literal

from pydantic import BaseModel


class Omission(BaseModel):
    kind: Literal["deliberate", "branch", "concerning"]
    summary: str
    impact_one_line: str
    source_formula_number: str
    source_excerpt: str


class Stage6Output(BaseModel):
    omissions: list[Omission]
    overall_concerns: list[str]
