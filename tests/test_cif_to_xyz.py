# tests/test_cif_to_xyz.py

import unittest
import os
from convert.cif_to_xyz import cif_to_xyz

class TestCIFtoXYZ(unittest.TestCase):

    def setUp(self):
        # make sure fixture file exist
        os.makedirs("tests/fixtures", exist_ok=True)
        
        self.test_cif = "tests/fixtures/test_input.cif"
        self.test_xyz = "tests/fixtures/test_output.xyz"
        with open(self.test_cif, "w") as f:
            f.write("""\
ATOM      1  COM  MOL A   103.679  128.270  141.416  1.00  0.00  C
ATOM      2  INT  MOL A   113.590  120.603  125.681  1.00  0.00  O
""")

    def test_conversion(self):
        cif_to_xyz(self.test_cif, self.test_xyz)
        with open(self.test_xyz, "r") as f:
            lines = f.readlines()

        self.assertEqual(lines[0].strip(), "2")
        self.assertIn("C 103.679 128.270 141.416", lines[2])
        self.assertIn("O 113.590 120.603 125.681", lines[3])
        
    def test_real_coarse_grained_file(self):
        input_cif = "tests/fixtures/5l93_coarse_grained.cif"
        output_xyz = "tests/output_5l93_model.xyz"

        cif_to_xyz(input_cif, output_xyz)

        # Verify file was written
        self.assertTrue(os.path.exists(output_xyz))

        with open(output_xyz, "r") as f:
            lines = f.readlines()

        # There should be 108 atoms
        self.assertEqual(int(lines[0].strip()), 108)

        # Check a few lines for expected atom symbols and coordinates
        self.assertTrue("C 103.679" in lines[2])
        self.assertTrue("O 113.590" in lines[3])
        self.assertTrue(any("O 174.905" in line for line in lines), "Expected atom not found.")

        # Cleanup
        os.remove(output_xyz)

    def tearDown(self):
        if os.path.exists(self.test_cif):
            os.remove(self.test_cif)
        if os.path.exists(self.test_xyz):
            os.remove(self.test_xyz)

if __name__ == "__main__":
    unittest.main()
