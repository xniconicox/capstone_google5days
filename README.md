# Satellite Metadata Search Agent

Natural-language interface for searching satellite imagery metadata using **STAC** and the **Google Agent Development Kit (ADK)**.

This repository is my submission for the **“Agents Intensive Capstone Project”** Kaggle competition.

---

## 1. Overview

Searching satellite imagery normally requires detailed knowledge of:

* Bounding boxes and polygon AOIs
* Date ranges and seasonal interpretation
* Cloud cover thresholds
* STAC API structure (collections, filters, pagination)

This project implements an **LLM-based agent** that abstracts all of that.
Users can ask in natural language, and the agent:

1. Resolves location text into a **bounding box (AOI)**
2. Interprets **time ranges** and **cloud constraints**
3. Calls a real **STAC API** (Sentinel-2 L2A)
4. Returns a **structured result table** with relevant scenes

The design focuses on:

* Deterministic tool usage
* Production-aligned prompting
* Full ADK evaluation (normal / clarification / boundary cases)

---

## 2. Repository structure

```
capstone/
├── README.md
├── README_jp.md
├── pyproject.toml
├── uv.lock
├── src/
│   └── capstone/
│       ├── agent/
│       │   ├── prompts.py
│       │   └── stac_agent_adk.py
│       ├── aoi/
│       │   ├── aoi_catalog.json
│       │   └── aoi_catalog.py
│       ├── tools/
│       │   └── stac_search.py
│       └── scripts/
│           ├── run_eval.py
│           └── eval/
│               ├── agent.py
│               ├── normal.evalset.json
│               ├── clarification.evalset.json
│               └── boundary.evalset.json
├── tests/
│   └── unit/
│       ├── test_aoi_catalog.py
│       ├── test_adk_eval.py
│       └── adk_test_cases.txt
└── doc/
    ├── TESTING.md
    ├── KAGGLE_BUILD_AND_TEST.md
    └── 衛星データメタデータ検索エージェントの深掘り調査.pdf
```

---

## 3. Authentication Setup (Gemini API)

The project uses Gemini via ADK.
**You only need:**

1. A Gemini API key
2. A `.env` file in the project root

### Steps

```bash
cp .env.example .env
```

Edit:

```env
GOOGLE_API_KEY=YOUR_KEY
```

Load:

```bash
set -a
source .env
set +a
```

No `gcloud` login or ADC credentials are required.

---

## 4. Running the agent

### Interactive mode (ADK Web UI)

```bash
adk web src/capstone/scripts/
```
you can start chatting.

### Programmatic eval (fast smoke test)

```bash
.venv/bin/python -m capstone.scripts.run_eval
```

## 5. Testing & Kaggle

* For local and CI testing: see **doc/TESTING.md**
* For Kaggle build & test instructions: see **doc/KAGGLE_BUILD_AND_TEST.md**