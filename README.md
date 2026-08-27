# RAFM Mechanism Reproducer

Takes a parsed RAFM actuarial model and a user description of a mechanism,
and produces a functional Excel calculation an actuary can understand and re-derive.

## Setup

```bash
pip install -e .
cp .env.example .env
# edit .env if you need to override config.yaml values
```

## Run

```bash
streamlit run app.py
```

## Required data files (not in this repo)

The client model artifacts are excluded from version control. Place them in `docs/`
before running:

| File | Used by |
|------|---------|
| `docs/Hierarchy_Harel_High.json` | Stage 2 formula selection |
| `docs/hierarchie_harel_Low.json` | Stage 3 verbatim code lookup |
| `docs/MF_BOR_model.xlsx` | Reference Excel |

Paths can be overridden in the sidebar under **Advanced**.

## Project structure

```
docs/                        Reference artifacts (High/Low JSON, reference Excel)
src/rafm_reproducer/
  config.py                  Load config.yaml + env overrides
  llm_client.py              AzureOpenAI + instructor wrapper
  artifacts.py               Save/load run artifacts
  orchestrator.py            Pipeline runner
  schemas/                   Pydantic models for every stage
  prompts/                   Prompt .txt files (edit without touching code)
  stages/                    One module per pipeline stage
  validators/                Post-LLM validation for stages 1 and 2
runs/                        Auto-created; one subfolder per run (gitignored)
```

## Pipeline (Stages 1-2 implemented; 3-7 stubs)

| Step | Type | What it does |
|------|------|-------------|
| Stage 1 | LLM | Understands the user request |
| Checkpoint 1 | Human | Approve or correct interpretation |
| Stage 2 | LLM | Selects formulas from the High hierarchy |
| Checkpoint 2 | Human | Approve or correct formula selection |
| Stage 3 | Mech | Looks up verbatim code from Low JSON |
| Stage 4 | LLM | Decomposes formulas analytically |
| Stage 5 | LLM | Produces Excel JSON spec |
| Stage 6 | LLM | Self-reviews for omissions |
| Stage 7 | Mech | Generates Excel via openpyxl |

## Model switching

Set `RAFM_MODEL` in `.env` or `llm_deployment` in `config.yaml`.
Primary: `claude-opus-4-5`. Secondary: `gpt-5.4-deployment`.
