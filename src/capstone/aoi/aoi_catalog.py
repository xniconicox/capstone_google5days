from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

# Load AOI catalog from JSON so notebooks and tests can share one source of truth.
_CATALOG_PATH = Path(__file__).with_suffix(".json")


def _load_catalog() -> List[Dict[str, object]]:
    with _CATALOG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


AOI_CATALOG: List[Dict[str, object]] = _load_catalog()
KNOWN_AOIS: Dict[str, Dict[str, object]] = {entry["id"]: entry for entry in AOI_CATALOG}


def format_known_aois_for_prompt() -> str:
    """
    Render the AOI catalog in a prompt-friendly bullet list.
    """
    lines: List[str] = []
    for entry in AOI_CATALOG:
        bbox = entry["bbox"]
        bbox_text = f"[{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}]"

        extras: List[str] = []
        note: Optional[str] = entry.get("note")  # type: ignore[arg-type]
        default_cloud = entry.get("default_cloud_cover")
        if note:
            extras.append(note)
        if default_cloud is not None:
            extras.append(f"default cloud_cover_max {default_cloud}")

        suffix = f" ({'; '.join(extras)})" if extras else ""
        lines.append(f"- {entry['id']}: {bbox_text}{suffix}")

    return "\n".join(lines)


def _normalize(text: str) -> str:
    return text.strip().lower().replace("-", "_").replace(" ", "_")


def resolve_aoi(location_hint: str) -> Dict[str, object]:
    """
    Resolve a location hint into a known AOI record if possible.

    Args:
        location_hint: Free-text location or AOI id candidate.

    Returns:
        Dict with keys:
            matched (bool)
            aoi_id (str | None)
            bbox (list | None)
            center (dict | None) -> {"lon": float, "lat": float}
            note (str | None)
            default_cloud_cover (float | None)
            message (str)
    """
    norm = _normalize(location_hint)
    for entry in AOI_CATALOG:
        aliases = [entry["id"]] + entry.get("aliases", [])  # type: ignore[list-item]
        aliases_norm = [_normalize(a) for a in aliases]
        if norm in aliases_norm:
            bbox = entry["bbox"]
            center = {
                "lon": (bbox[0] + bbox[2]) / 2,
                "lat": (bbox[1] + bbox[3]) / 2,
            }
            return {
                "matched": True,
                "aoi_id": entry["id"],
                "bbox": bbox,
                "center": center,
                "note": entry.get("note"),
                "default_cloud_cover": entry.get("default_cloud_cover"),
                "message": "Matched known AOI.",
            }

    return {
        "matched": False,
        "aoi_id": None,
        "bbox": None,
        "center": None,
        "note": None,
        "default_cloud_cover": None,
        "message": "No matching known AOI. Ask the user for bbox or coordinates, or propose a rough center coordinate and get consent.",
    }
