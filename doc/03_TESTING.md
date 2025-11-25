# Testing Guide

Satellite Metadata Search Agent

This document summarizes how to test the Satellite Metadata Search Agent.
The workflow follows ADK’s recommended evaluation structure and supports development, CI, and production release.

---

## 1. Unit Tests (pytest)

Run deterministic tests:

```bash
.venv/bin/pytest tests/unit -q
```

Validates:

* AOI catalog behavior
* Time / cloud-cover parsing logic
* Basic ADK wiring

---

## 2. Programmatic ADK Evaluation (CI Smoke Test)

Quick validation using `AgentEvaluator`:

```bash
.venv/bin/python -m capstone.scripts.run_eval
```

Confirms:

* Evalset files load correctly
* Agent imports correctly
* No fatal runtime errors

Used for CI and local development.

---

## 3. Manual Evaluation (ADK Web UI)

Launch interactive UI:

```bash
adk web src/capstone/scripts/
```

Then:

1. Open the printed URL in your browser
2. Select the **Eval** tab
3. Choose the configured eval agent
4. Start a chat or run specific eval cases

Check:

* Clarification behavior
* Cloud-cover mapping
* Correct tool flow
* Reasonable final output formatting

Use during prompt tuning and debugging.

---

## 4. Full ADK CLI Evaluation (Detailed Metrics)

Run complete evaluation:

```bash
adk eval src/capstone/scripts/eval \
    src/capstone/scripts/eval/normal.evalset.json \
    src/capstone/scripts/eval/clarification.evalset.json \
    src/capstone/scripts/eval/boundary.evalset.json \
  --config_file_path=src/capstone/scripts/eval/test_config.json \
  --print_detailed_results > src/capstone/scripts/eval/result.txt
```

Outputs:

* Rubric scores
* `response_match_score`
* Tool trajectory
* Eval history files

Required before PR merge and release.

---

## 5. Recommended Workflow

### Local Development

* `.venv/bin/pytest`
* `adk web src/capstone/scripts/` for interactive testing
* Optional: `.venv/bin/python -m capstone.scripts.run_eval`

### CI (Push)

* `.venv/bin/pytest`
* `.venv/bin/python -m capstone.scripts.run_eval`

### Pull Request (Quality Gate)

* Full ADK CLI evaluation
* Confirm **all cases pass**
* Reviewer checks `result.txt`

### Release / Production

* Full ADK evaluation on `main`
* Ensure no regressions
* Deploy

---

This layered workflow ensures:

* Fast feedback
* Reliable safety checks
* High-confidence releases

---