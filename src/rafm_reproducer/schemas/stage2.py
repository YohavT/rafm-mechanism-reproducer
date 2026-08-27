from pydantic import BaseModel, Field, ConfigDict


class SelectedFormula(BaseModel):
    numero: str
    titre: str
    role_one_line: str
    why_defining: str
    branches_in_scope: list[str]


class ConsumerFormula(BaseModel):
    numero: str
    titre: str
    consumes_what: str


class Dependency(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_numero: str = Field(alias="from")
    to_numero: str = Field(alias="to")
    reason: str


class Stage2Output(BaseModel):
    selected: list[SelectedFormula]
    consumers_for_info: list[ConsumerFormula]
    dependencies_followed: list[Dependency]
    concerns: list[str]
