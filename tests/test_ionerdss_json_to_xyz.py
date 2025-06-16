import unittest
import os
import json
from convert.ionerdss_json_to_xyz import ionerdss_json_to_xyz

class TestIonerdssJsonToXYZ(unittest.TestCase):

    def setUp(self):
        os.makedirs("tests/fixtures", exist_ok=True)
        self.json_path = "tests/fixtures/sample_ionerdss.json"
        self.xyz_path = "tests/fixtures/sample_output.xyz"

        sample_data = {
            "name": "5l93",
            "molecule_types": [
                {
                    "name": "A",
                    "interfaces": [
                        {"name": "A1", "coord": {"x": 1.0, "y": 2.0, "z": 3.0}},
                        {"name": "A2", "coord": {"x": 4.0, "y": 5.0, "z": 6.0}}
                    ]
                }
            ]
        }

        with open(self.json_path, "w") as f:
            json.dump(sample_data, f)

    def test_conversion(self):
        bonds_path = "tests/fixtures/sample_output.bonds"
        ionerdss_json_to_xyz(self.json_path, self.xyz_path, bonds_path)

        self.assertTrue(os.path.exists(self.xyz_path))
        self.assertTrue(os.path.exists(bonds_path))

        with open(self.xyz_path, "r") as f:
            lines = f.readlines()

        self.assertEqual(int(lines[0].strip()), 3)
        self.assertIn("A1 1.000 2.000 3.000", lines[3])

        with open(bonds_path, "r") as f:
            bond_lines = f.readlines()

        self.assertEqual(len(bond_lines), 2)  # 2 interfaces
        self.assertEqual(bond_lines[0].strip(), "0 1")
        self.assertEqual(bond_lines[1].strip(), "0 2")

        # Cleanup
        if os.path.exists(bonds_path):
            os.remove(bonds_path)


    def tearDown(self):
        if os.path.exists(self.json_path):
            os.remove(self.json_path)
        if os.path.exists(self.xyz_path):
            os.remove(self.xyz_path)

if __name__ == "__main__":
    unittest.main()
