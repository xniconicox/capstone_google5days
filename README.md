# Satellite Metadata Search Agent

Natural-language interface for searching satellite imagery metadata using **STAC** and the **Google Agent Development Kit (ADK)**.

This repository is my submission for the **“Agents Intensive Capstone Project”** Kaggle competition.

---

## 0. Environment Setup

This project uses `uv` for dependency management.

Install dependencies:

```bash
uv sync
```

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

Then:

1. Open the printed URL in your browser
2. You can chat with Agent.
ex.)
"Find Sentinel-2 images over eastern Hokkaido between 2023-06-15 and 2023-06-30 with less than 20% cloud cover."
"Find high-resolution optical images over eastern Hokkaido in summer 2023 with less than 10% cloud."

## 5. Testing & Kaggle

* For local and CI testing: see **doc/TESTING.md**
* For Kaggle build & test instructions: see **doc/KAGGLE_BUILD_AND_TEST.md**
  
## 6. Supported Sensors and AOIs

### Supported Satellite Collection
The agent currently supports the following STAC collection:

- **Sentinel-2 Level-2A (optical)**  
  *(STAC collection ID: `sentinel-2-l2a`)*

Other sensors (Sentinel-1 SAR, Landsat-8/9, PRISMA, MODIS, etc.) can be added.

---

### Supported AOIs (Location Coverage)

Location resolution is based on a curated AOI catalog that maps  
natural-language location hints (English + Japanese) to **canonical bounding boxes**.

The catalog includes:

- Country-level regions (Japan, USA mainland, UK, France, Germany)
- Major metropolitan areas (Tokyo, Osaka, Nagoya, Sapporo, Fukuoka)
- Regional subsets (Eastern Hokkaido)
- Special AOIs with default cloud-cover constraints  
  (e.g., *japan_cloud_free_focused*)

Rather than embedding the full JSON here, the complete list of supported AOIs is available at:

👉 **[`src/capstone/aoi/aoi_catalog.json`](src/capstone/aoi/aoi_catalog.json)**

Each entry defines:  
- `id`  
- `bbox`  
- `note`  
- `aliases` (English & Japanese)  
- optional `default_cloud_cover`

You can extend coverage by editing `aoi_catalog.json`.
