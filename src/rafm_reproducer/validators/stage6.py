from ..schemas.stage6 import Stage6Output
from ..schemas.pipeline_state import EnrichedFormula


def validate_stage6(output: Stage6Output, enriched: list[EnrichedFormula]) -> list[str]:
    enriched_numeros = {f.numero for f in enriched}
    errors: list[str] = []

    for omission in output.omissions:
        if omission.source_formula_number not in enriched_numeros:
            errors.append(
                f"Omission '{omission.summary[:60]}' cites source formula "
                f"[{omission.source_formula_number}] which is not in Stage 3 enriched output."
            )

    return errors
