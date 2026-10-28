import importlib.util
from pathlib import Path
import unittest
path=Path(__file__).resolve().parents[1]/"tools"/"internal-battery-selector.py"
spec=importlib.util.spec_from_file_location("selector",path)
selector=importlib.util.module_from_spec(spec)
spec.loader.exec_module(selector)
sample=[{"slug":"dyson-v7","current_sku":"BATDYSV7_2500","source_sku":"BATDYSV7","compatible_device_codes":["SV11"],"compatible_battery_part_numbers":["BAT-SV11"],"compatible_device_claims":["Dyson V7 Absolute"],"verification_note":"Verify fit"}]
class SelectorTests(unittest.TestCase):
    def test_exact_code(self):
        self.assertEqual(selector.search(sample,"SV11")[0]["sku"],"BATDYSV7_2500")
    def test_model_phrase(self):
        self.assertEqual(selector.search(sample,"Dyson V7 Absolute")[0]["slug"],"dyson-v7")
    def test_no_substring_for_short_query(self):
        with self.assertRaises(ValueError):
            selector.search(sample,"V7")
    def test_unknown(self):
        self.assertEqual(selector.search(sample,"unknown123"),[])
    def test_never_asserts_fit(self):
        self.assertFalse(selector.search(sample,"BAT-SV11")[0]["verified_physical_fit"])
if __name__=="__main__":
    unittest.main()
