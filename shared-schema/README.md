# Shared Schema

This directory contains the canonical JSON schema exchanged between the Express and FastAPI layers.

- `agent_schema.json` — generated from the Pydantic `AgentPayload` model (`llm/schema.py`).
- Keep both runtimes in sync by re-exporting the schema whenever the shared model changes (`python -c "from models.schemas import AgentPayload; import json; print(json.dumps(AgentPayload.model_json_schema(), indent=2))"`).
