# src/capstone/tools/stac_search.py

import requests
from typing import Optional


BASE_URL = "https://earth-search.aws.element84.com/v1"


def search_satellite_scenes(
    bbox: list[float],
    datetime_range: str,
    cloud_cover_max: float,
    limit: int = 10,
    collections: Optional[list[str]] = None,
) -> list[dict]:
    """
    Search satellite scenes via the Element84 Earth Search v1 STAC API.

    This function queries the STAC endpoint and returns a list of scene
    metadata records. It is intended to be used as the core logic for
    an agent tool.

    Args:
        bbox:
            Spatial search extent as [min_lon, min_lat, max_lon, max_lat].
        datetime_range:
            Temporal filter in STAC "interval" format:
            "YYYY-MM-DDTHH:MM:SSZ/YYYY-MM-DDTHH:MM:SSZ".
        cloud_cover_max:
            Maximum allowed cloud cover (percent, inclusive).
        limit:
            Maximum number of scenes to return.
        collections:
            List of STAC collection IDs to search.
            If None, defaults to ["sentinel-2-l2a"].

    Returns:
        List[Dict]: A list of records, each with at least:
            - "id"          (str): STAC item ID.
            - "datetime"    (str | None): Acquisition datetime (ISO 8601).
            - "cloud_cover" (float | None): Cloud cover percentage.
            - "preview_url" (str | None): URL of a quick-look/thumbnail image.
    """
    if len(bbox) != 4:
        raise ValueError(f"bbox must be a sequence of 4 numbers, got: {bbox}")

    if limit <= 0:
        raise ValueError(f"limit must be positive, got: {limit}")

    if collections is None:
        collections = ["sentinel-2-l2a"]

    search_url = f"{BASE_URL}/search"

    payload = {
        "collections": list(collections),
        "bbox": list(bbox),
        "datetime": datetime_range,
        "limit": limit,
        "query": {
            "eo:cloud_cover": {
                "lte": cloud_cover_max
            }
        },
    }

    try:
        response = requests.post(search_url, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"STAC search request failed: {e}, payload={payload}") from e

    data = response.json()
    features = data.get("features", [])

    rows: List[Dict] = []
    for feat in features:
        props = feat.get("properties", {})
        assets = feat.get("assets", {})

        scene_id = feat.get("id")
        dt = props.get("datetime")
        cloud = props.get("eo:cloud_cover")

        thumb: Optional[str] = None
        for key in ["thumbnail", "overview", "true_color", "preview"]:
            if key in assets:
                thumb = assets[key].get("href")
                break

        rows.append(
            {
                "id": scene_id,
                "datetime": dt,
                "cloud_cover": cloud,
                "preview_url": thumb,
            }
        )

    return rows


SEARCH_STAC_SCENES_TOOL_SPEC = {
    "name": "search_stac_scenes",
    "description": (
        "Search satellite scenes via the Element84 Earth Search v1 STAC API. "
        "Given a bounding box, time range, and maximum cloud cover, this tool "
        "returns a list of matching scenes with basic metadata and a preview URL."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "bbox": {
                "type": "array",
                "description": (
                    "Spatial search extent as [min_lon, min_lat, max_lon, max_lat] in WGS84."
                ),
                "items": {"type": "number"},
                "minItems": 4,
                "maxItems": 4,
            },
            "datetime_range": {
                "type": "string",
                "description": (
                    'Temporal filter in STAC interval format: '
                    '"YYYY-MM-DDTHH:MM:SSZ/YYYY-MM-DDTHH:MM:SSZ".'
                ),
            },
            "cloud_cover_max": {
                "type": "number",
                "description": "Maximum allowed cloud cover (percent, inclusive).",
                "minimum": 0,
                "maximum": 100,
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of scenes to return.",
                "minimum": 1,
                "default": 10,
            },
            "collections": {
                "type": "array",
                "description": (
                    'List of STAC collection IDs to search. '
                    'If omitted, defaults to ["sentinel-2-l2a"].'
                ),
                "items": {"type": "string"},
            },
        },
        "required": ["bbox", "datetime_range", "cloud_cover_max"],
    },
    "output_schema": {
        "type": "array",
        "description": "List of scene metadata records matching the query.",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "STAC item ID."},
                "datetime": {
                    "type": "string",
                    "description": "Acquisition datetime (ISO 8601).",
                },
                "cloud_cover": {
                    "type": "number",
                    "description": "Cloud cover percentage.",
                },
                "preview_url": {
                    "type": "string",
                    "description": "URL of a quick-look or thumbnail image, if available.",
                },
            },
            "required": ["id", "datetime", "cloud_cover", "preview_url"],
        },
    },
}
