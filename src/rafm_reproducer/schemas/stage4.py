from pydantic import BaseModel


class FormulaBranch(BaseModel):
    condition: str
    scope_relevant: bool
    returns: str


class FormulaDecomposition(BaseModel):
    numero: str
    titre: str
    inputs_used: list[str]
    branches: list[FormulaBranch]
    temporal_self_reference: bool


class SharedSubexpression(BaseModel):
    name: str
    expression: str
    appears_in: list[str]


class KeyIdentity(BaseModel):
    identity: str
    source_formulas: list[str]
    derivation_summary: str


class Stage4Output(BaseModel):
    reasoning: str          # step-by-step analysis before finalising the decomposition
    formulas: list[FormulaDecomposition]
    shared_subexpressions: list[SharedSubexpression]
    key_identities: list[KeyIdentity]
    concerns: list[str]
