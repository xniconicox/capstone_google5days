import requests
import pandas as pd
from typing import List, Dict, Optional


BASE_URL = "https://earth-search.aws.element84.com/v1"


def search_satellite_scenes(
    bbox,
    datetime_range: str,
    cloud_cover_max: float,
    limit: int = 10,
    collections=None,
) -> List[Dict]:
    """
    Search Sentinel-2 (or other collections) scenes via STAC API.

    Args:
        bbox: [min_lon, min_lat, max_lon, max_lat]
        datetime_range: "YYYY-MM-DDTHH:MM:SSZ/YYYY-MM-DDTHH:MM:SSZ"
        cloud_cover_max: maximum allowed cloud cover in percent.
        limit: maximum number of results.
        collections: list of STAC collection ids (default: Sentinel-2 L2A).
    """
    if collections is None:
        collections = ["sentinel-2-l2a"]

    search_url = f"{BASE_URL}/search"

    payload = {
        "collections": collections,
        "bbox": bbox,
        "datetime": datetime_range,
        "limit": limit,
        "query": {
            "eo:cloud_cover": {
                "lte": cloud_cover_max
            }
        },
    }

    response = requests.post(search_url, json=payload)
    response.raise_for_status()
    data = response.json()

    features = data.get("features", [])
    rows = []
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


def main():
    bbox = [143.0, 42.5, 146.0, 45.5]
    datetime_range = "2023-06-01T00:00:00Z/2023-08-31T23:59:59Z"
    cloud_cover_max = 10.0

    print("Request parameters:")
    print(
        {
            "bbox": bbox,
            "datetime": datetime_range,
            "cloud_cover_max": cloud_cover_max,
        }
    )

    rows = search_satellite_scenes(
        bbox=bbox,
        datetime_range=datetime_range,
        cloud_cover_max=cloud_cover_max,
        limit=10,
    )

    print(f"\nNumber of features returned: {len(rows)}")

    if not rows:
        print("\nNo scenes found. Try relaxing the filters.")
        return

    df = pd.DataFrame(rows)
    print("\nResults:")
    print(df.to_markdown(index=False))


if __name__ == "__main__":
    main()
