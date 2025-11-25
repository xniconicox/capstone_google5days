# Kaggle Build & Test Guide  
Satellite Metadata Search Agent

This document describes exactly how a Kaggle reviewer can build and test this project locally.

Assumptions:

- Standard Python 3.11+ environment
- Repository cloned locally
- `uv` is available
- Gemini API key is configured as described in `README.md` (for ADK-based tests)

Covers:

1. Clone & environment setup  
2. Install dependencies with `uv`  
3. Run unit tests  
4. Run ADK eval tests (golden cases)  
5. Optional: ADK Web UI  
6. Project structure reference  
7. TL;DR  

---

## 1. Clone

```bash
git clone <REPO_URL>
cd capstone
````

---

## 2. Environment Setup (uv + .venv)

Install dependencies and create `.venv`:

```bash
uv sync
```

This:

* Creates `.venv/` in the project root
* Installs dependencies from `pyproject.toml`

(You may optionally `source .venv/bin/activate`,
but commands below use `.venv/bin/...` explicitly.)

---

## 3. Unit Tests

Run Python unit tests:

```bash
.venv/bin/pytest tests/unit
```

Ensures:

* AOI resolution (`aoi_catalog`) works correctly
* Core utilities behave deterministically

---

## 4. ADK Eval Tests (Golden Cases)

Run all evalsets through the helper script:

```bash
.venv/bin/python -m capstone.scripts.run_eval
```

This:

* Loads `normal.evalset.json`, `clarification.evalset.json`, and `boundary.evalset.json`
* Evaluates the ADK agent against the golden cases
* Prints an aggregated summary to stdout

---

## 5. Optional: ADK Web UI

You can also test interactively via ADK Web UI.

Start the UI:

```bash
adk web src/capstone/scripts/
```

Then:

1. Open the printed URL (example: `http://localhost:8000`)
2. Select the eval agent / Eval tab
3. Chat with the agent using natural-language queries such as:

   * “Find Sentinel-2 images over eastern Hokkaido between 2023-06-15 and 2023-06-30 with less than 20% cloud cover.”
   * “Show me almost cloud-free images over Japan in 2023.”
   * “Find cloud-free images around Sapporo in September.”

     * → The agent should ask for a more precise date range.

The behavior should match the golden-case evals.

---

## 6. Project Structure (Quick Reference)

```text
src/capstone/
  agent/
    prompts.py
    stac_agent_adk.py
  aoi/
    aoi_catalog.json
    aoi_catalog.py
  tools/
    stac_search.py
  scripts/
    run_eval.py
    eval/
      agent.py
      normal.evalset.json
      clarification.evalset.json
      boundary.evalset.json

tests/
  unit/
    test_aoi_catalog.py
    test_adk_eval.py
```

Archived directories are unused.

---

## 7. TL;DR

```bash
# 1. Clone
git clone <REPO_URL>
cd capstone

# 2. Install deps (uv + .venv)
uv sync

# 3. Run unit tests
.venv/bin/pytest tests/unit

# 4. Run golden-case evals
.venv/bin/python -m capstone.scripts.run_eval

# 5. (Optional) Launch ADK Web UI
adk web src/capstone/scripts/
```

This completes the build & test process for a Kaggle reviewer using `uv` and the bundled `.venv`.
