# 🛰️ Satellite Metadata Search Agent

*Natural-Language STAC Search Agent (MVP)*

## 📌 Overview

Searching for satellite imagery traditionally requires manual configuration across multiple UI fields:

* Selecting regions or entering latitude/longitude
* Setting temporal ranges
* Choosing satellite missions and product levels
* Adjusting filters such as cloud cover
* Understanding STAC query structure

This project introduces an **LLM-based agent** that allows users to simply describe what they want in natural language, and the agent automatically:

* Interprets the request
* Constructs the appropriate STAC query
* Fetches candidate satellite scenes
* Summarizes and recommends the best matches

---

## 🎯 Goal

The agent enables users to search satellite metadata using everyday language.
It performs:

* **Natural language → structured query extraction**
  (time range, AOI, mission, cloud cover)
* **Automated STAC API search**
* **Scene ranking, formatting, and summarization**
* **Optional: session memory for context-aware follow-up queries**

---

## 🏗️ Architecture

```
User Query (Natural Language)
            ↓
      LLM Agent (ADK)
            ↓
 ┌────────────────────────────┐
 │ 1. resolve_aoi             │ → geocoding / bbox resolution
 │ 2. find_satellite_scenes   │ → STAC search (time, AOI, filters)
 └────────────────────────────┘
            ↓
    Agent → summarize & table format
            ↓
         Final Answer
```

Key aspects:

* **Single-agent architecture using Google ADK**
* **MCP-compliant task-oriented tool design**
* Natural-language interpretation → JSON parameters → tool calls

---

## 🧰 Technologies

* **Google ADK (Agent Development Kit)**
* STAC API (Element84 Earth Search / MS Planetary Computer)
* Python (httpx / pystac-client)
* pandas for result presentation

---

## ✨ Features

### ✔ Natural-language satellite data search

Examples:

* *“Show me Sentinel-2 imagery over eastern Hokkaido during summer 2023 with <10% cloud cover.”*
* *“Find nighttime scenes captured by Landsat-8.”*

### ✔ Automatic extraction of:

* Time period (e.g., *“summer 2023” → 2023-06-01 to 2023-08-31*)
* Area of interest (“Hokkaido east side” → bounding box)
* Satellite mission (Sentinel-2, Landsat-8, etc.)
* Filters (cloud cover thresholds)

### ✔ Clean tabular results & summaries

### ✔ Optional session memory

Supports follow-up queries like:
*“Use the same area as before, but show winter data.”*

---

## 🧪 MVP Scope

This project focuses on a minimal but complete pipeline:

* Mission: **Sentinel-2 L2A**
* AOI: limited predefined regions and basic geocoding
* One-shot search (single turn)
* No image processing (metadata search only)

This keeps the MVP simple and demonstrates the full agent loop.

---

## 📅 Development Timeline (Completed)

### **Day 1 — STAC connectivity**

* Hard-coded query test
* Extract basic metadata (id, datetime, cloud cover, preview URL)

### **Day 2 — MCP-style tool design**

* `resolve_aoi`
* `find_satellite_scenes`
* Registered as ADK tools
* Tool-level testing

### **Day 3 — Agent pipeline**

* Prompt design for natural-language → structured JSON conversion
* End-to-end search in notebook demo

---

## 🆚 Value & Novelty

Although similar research prototypes exist (STAC Semantic Search, GeoAgents, Queryable Earth, etc.), they remain **experimental demonstrations**, typically lacking:

| Aspect                               | Existing Prototypes | This Project           |
| ------------------------------------ | ------------------- | ---------------------- |
| Japanese / multilingual support      | ✗                   | ✓                      |
| Production-ready architecture        | ✗                   | ✓ (ADK/MCP)            |
| Tool modularity & extensibility      | Partial             | ✓                      |
| Memory integration                   | Rare                | ✓                      |
| Deployment strategy                  | Not addressed       | ✓ (CI/CD-friendly)     |
| Integration with downstream analysis | Limited             | Designed for extension |

### Unique value of this project:

#### ⭐ Practical, production-oriented design

Based on **Google ADK / MCP whitepapers**, this agent is built with:

* Tool granularity
* Session & memory handling
* Error handling & tool-calling best practices
* Extendable architecture (multi-agent ready)

#### ⭐ Extensible for real-world EO workflows

The design allows natural expansion into:

* multi-mission searches
* Earth Engine/Sentinel Hub integration
* timeseries monitoring
* analysis agents (NDVI, cloud masking, etc.)

#### ⭐ Localized usage (Japanese support possible)

A major differentiator compared to English-only prototypes.

---

## 🚀 Future Roadmap

### 1. Multi-mission support

* Landsat-8/9
* Sentinel-1 SAR
* ALOS/JAXA datasets

### 2. Visualization layer

* Map preview
* Thumbnail mosaics
* Interactive selection

### 3. Integration with analysis agents

* NDVI computation
* Cloud masking
* Time-series analysis
* Change detection

### 4. Automated monitoring

* Scheduled searches (weekly, monthly)
* Alerts for newly available scenes

### 5. Knowledge-augmented reasoning

* “Which sensor is best for agriculture?”
* RAG integration for mission specifications

---

## ⚠️ Limitations (MVP Transparency)

* Ambiguous geographic expressions (“east side of Hokkaido”)
* Seasonal expressions and interpretation issues
* cloud_cover metadata accuracy differences between missions
* Large search results → pagination / truncation needed
* LLM mistakes in structured tool calls
* STAC rate limits / latency

These are known constraints; the architecture supports improving them progressively.

---

## 📚 References

* STAC Specification
* Element84 Earth Search
* Microsoft Planetary Computer
* Google ADK / MCP whitepapers
* Development Seed STAC Semantic Search
* OpenGeoAI GeoAgents

---

## 📄 License

MIT License

---

## 🤝 Contributions

PRs and issues welcome.
