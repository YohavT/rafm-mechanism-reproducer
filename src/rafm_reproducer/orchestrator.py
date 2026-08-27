"""
Orchestrator: thin wrappers that enforce stage ordering and save state.
The Streamlit app calls these functions directly.
"""

from datetime import datetime

from .artifacts import new_run_dir, save_json
from .config import load_premium_cfg
from .llm_client import get_client
from .schemas.pipeline_state import CheckpointAction, PipelineState
from .schemas.user_input import UserPrompt
from .stages.stage1 import run_stage1
from .stages.stage2 import run_stage2
from .stages.stage3 import run_stage3


def start_run(
    high_json_path,
    low_json_path,
    model_name: str,
    user_prompt: UserPrompt,
    client,
    cfg: dict,
) -> PipelineState:
    run_id, run_dir = new_run_dir()
    state = PipelineState(
        run_id=run_id,
        run_dir=run_dir,
        high_json_path=high_json_path,
        low_json_path=low_json_path,
        model_name=model_name,
        user_prompt=user_prompt,
    )
    save_json(run_dir, "user_prompt", user_prompt)
    save_json(
        run_dir,
        "run_config",
        {"run_id": run_id, "model": model_name, "started_at": datetime.now().isoformat()},
    )
    return run_stage1(state, client, cfg)


def apply_checkpoint1_approve(state: PipelineState) -> PipelineState:
    state.checkpoint1 = CheckpointAction(
        action="approve",
        timestamp=datetime.now().isoformat(),
    )
    save_json(state.run_dir, "checkpoint1_action", state.checkpoint1)
    return state


def apply_checkpoint1_correct(state: PipelineState, correction: str, client, cfg: dict) -> PipelineState:
    state.checkpoint1 = CheckpointAction(
        action="correct",
        correction=correction,
        timestamp=datetime.now().isoformat(),
    )
    save_json(state.run_dir, "checkpoint1_action", state.checkpoint1)
    return run_stage1(state, client, cfg)


def trigger_stage2(state: PipelineState, client, cfg: dict) -> PipelineState:
    return run_stage2(state, client, cfg)


def apply_checkpoint2_approve(state: PipelineState) -> PipelineState:
    state.checkpoint2 = CheckpointAction(
        action="approve",
        timestamp=datetime.now().isoformat(),
    )
    save_json(state.run_dir, "checkpoint2_action", state.checkpoint2)
    return state


def apply_checkpoint2_correct(state: PipelineState, correction: str, client, cfg: dict) -> PipelineState:
    state.checkpoint2 = CheckpointAction(
        action="correct",
        correction=correction,
        timestamp=datetime.now().isoformat(),
    )
    save_json(state.run_dir, "checkpoint2_action", state.checkpoint2)
    return run_stage2(state, client, cfg)


def trigger_stages_3_to_7(
    state: PipelineState,
    client,
    cfg: dict,
    progress_callback=None,
) -> PipelineState:
    """
    Run the full generation pipeline: Stage 3 → 4 → 5 → 6 → 7.
    progress_callback(stage_number, label) is called before each stage if provided.
    Imports are deferred so any import error surfaces with the real traceback.
    """
    from .stages.stage4 import run_stage4
    from .stages.stage5 import run_stage5
    from .stages.stage6 import run_stage6
    from .stages.stage7 import run_stage7

    # Stages 4 and 5 use the premium model (GPT-5.5) for deeper reasoning
    premium_cfg = load_premium_cfg()
    premium_client = get_client(premium_cfg)

    def _cb(n, label):
        if progress_callback:
            progress_callback(n, label)

    # Each stage is skipped if its output already exists — safe to retry
    if not state.stage3_enriched:
        _cb(3, "Stage 3 — Loading source code for selected formulas…")
        state = run_stage3(state)
    else:
        _cb(3, "Stage 3 — Already done ✓")

    if state.stage4_output is None:
        _cb(4, f"Stage 4 — Decomposing formulas analytically [{premium_cfg['model']}]…")
        state = run_stage4(state, premium_client, premium_cfg)
    else:
        _cb(4, "Stage 4 — Already done ✓")

    if state.stage5_output is None:
        _cb(5, f"Stage 5 — Generating Excel specification [{premium_cfg['model']}]…")
        state = run_stage5(state, premium_client, premium_cfg)
    else:
        _cb(5, "Stage 5 — Already done ✓")

    if state.stage6_output is None:
        _cb(6, "Stage 6 — Self-reviewing specification against source code…")
        state = run_stage6(state, client, cfg)
    else:
        _cb(6, "Stage 6 — Already done ✓")

    if state.output_xlsx_path is None or not state.output_xlsx_path.exists():
        _cb(7, "Stage 7 — Building Excel workbook…")
        state = run_stage7(state)
    else:
        _cb(7, "Stage 7 — Already done ✓")

    return state
