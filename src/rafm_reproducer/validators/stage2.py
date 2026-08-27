from ..schemas.hierarchy import HierarchyNode
from ..schemas.stage2 import Stage2Output


def validate_stage2(
    output: Stage2Output,
    index: dict[str, HierarchyNode],
) -> list[str]:
    """
    Semantic validation for Stage 2 output.
    Returns a list of error strings (empty = valid).
    """
    errors: list[str] = []
    all_numeros = set(index.keys())

    # --- selected: numero existence + title match ---
    for f in output.selected:
        if f.numero not in all_numeros:
            errors.append(
                f"selected formula [{f.numero}] '{f.titre}' — numero not found in hierarchy"
            )
        else:
            expected = index[f.numero].titre.strip().lower()
            got = f.titre.strip().lower()
            if expected != got:
                errors.append(
                    f"selected [{f.numero}]: title mismatch — "
                    f"hierarchy has '{index[f.numero].titre}', LLM returned '{f.titre}'"
                )

    # --- consumers: numero existence ---
    for c in output.consumers_for_info:
        if c.numero not in all_numeros:
            errors.append(
                f"consumer [{c.numero}] '{c.titre}' — numero not found in hierarchy"
            )

    # --- dependency closure ---
    selected_nums = {f.numero for f in output.selected}
    consumer_nums = {c.numero for c in output.consumers_for_info}
    all_mentioned = selected_nums | consumer_nums

    for dep in output.dependencies_followed:
        if dep.from_numero not in all_mentioned:
            errors.append(
                f"dependency from=[{dep.from_numero}] is not in selected or consumers"
            )
        if dep.to_numero not in all_mentioned:
            errors.append(
                f"dependency to=[{dep.to_numero}] is not in selected or consumers"
            )

    # --- count sanity check (warning, not block) ---
    if len(output.selected) < 3:
        errors.append(
            f"only {len(output.selected)} formula(s) selected — expected at least 3. "
            "If this is intentional for a simple mechanism, this can be ignored."
        )

    return errors
