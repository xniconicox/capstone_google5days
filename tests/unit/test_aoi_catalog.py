import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from capstone.aoi import aoi_catalog


class TestAoiCatalog(unittest.TestCase):
    def test_catalog_ids(self):
        ids = {entry["id"] for entry in aoi_catalog.AOI_CATALOG}
        expected = {
            "japan",
            "usa_mainland",
            "united_kingdom",
            "france",
            "germany",
            "tokyo_area",
            "osaka_area",
            "sapporo_area",
            "nagoya_area",
            "fukuoka_area",
            "hokkaido_east",
            "japan_cloud_free_focused",
        }
        self.assertSetEqual(ids, expected)

    def test_resolve_known_aoi(self):
        result = aoi_catalog.resolve_aoi("eastern Hokkaido")
        self.assertTrue(result["matched"])
        self.assertEqual(result["aoi_id"], "hokkaido_east")
        self.assertEqual(result["bbox"], [143.0, 42.5, 146.0, 45.5])
        self.assertAlmostEqual(result["center"]["lon"], 144.5)
        self.assertAlmostEqual(result["center"]["lat"], 44.0)

    def test_alias_japanese(self):
        result = aoi_catalog.resolve_aoi("東京")
        self.assertTrue(result["matched"])
        self.assertEqual(result["aoi_id"], "tokyo_area")

    def test_cloud_free_default(self):
        result = aoi_catalog.resolve_aoi("japan_cloud_free_focused")
        self.assertTrue(result["matched"])
        self.assertEqual(result.get("default_cloud_cover"), 10.0)

    def test_unmatched(self):
        result = aoi_catalog.resolve_aoi("unknown place")
        self.assertFalse(result["matched"])
        self.assertIsNone(result["bbox"])
        self.assertIsNone(result["aoi_id"])


if __name__ == "__main__":
    unittest.main()
