import importlib.util
import unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"tools"/"build-compatibility-matrix.py"
# Module builds matrix from existing source data; isolate assertions to output shape.
class CompatibilityParsingTests(unittest.TestCase):
    def test_source_arrays_remain_clean(self):
        import json, subprocess, sys
        subprocess.run([sys.executable,str(path)],check=True,capture_output=True,text=True)
        matrix=json.loads((path.parents[1]/"data"/"compatibility-matrix-review.json").read_text())
        by_slug={p["slug"]:p for p in matrix["products"]}
        self.assertIn("Dyson V7 Absolute",by_slug["dyson-v7"]["compatible_device_claims"])
        self.assertIn("P1904-4S1P-MM",by_slug["xiaomi-1c-5200"]["compatible_battery_part_numbers"])
        for p in matrix["products"]:
            for key in ("compatible_device_claims","compatible_device_codes","compatible_battery_part_numbers"):
                self.assertTrue(all(not v.startswith("[") for v in p[key]))
if __name__=="__main__":
    unittest.main()
