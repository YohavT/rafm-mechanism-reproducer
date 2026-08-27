from ..schemas.stage1 import Stage1Output


def validate_stage1(output: Stage1Output) -> list[str]:
    """
    Semantic validation for Stage 1 output.
    Returns a list of error strings (empty = valid).
    Schema-level validation is handled upstream by instructor/Pydantic.
    """
    if output.halt_reason:
        return []  # halt is a valid terminal state, not an error

    errors: list[str] = []

    if not output.interpretation or not output.interpretation.strip():
        errors.append("interpretation is empty")

    if not output.relevant_branches:
        errors.append(
            "relevant_branches is empty — Stage 2 cannot proceed without knowing "
            "which model groups to search"
        )

    if output.confidence == "high" and output.ambiguities:
        errors.append(
            f"confidence is 'high' but {len(output.ambiguities)} ambiguit(y/ies) "
            f"are non-empty: {output.ambiguities}. "
            "Lower confidence to 'medium' or resolve the ambiguities."
        )

    return errors
