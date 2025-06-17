import unittest
import os
from convert.cif_to_pdb import cif_to_pdb

class TestCIFtoPDB(unittest.TestCase):

    def setUp(self):
        os.makedirs("tests/fixtures", exist_ok=True)
        self.input_cif = "tests/fixtures/test_input.cif"
        self.output_pdb = "tests/fixtures/test_output.pdb"

        with open(self.input_cif, "w") as f:
            f.write("""\
ATOM      1  COM  MOL A   103.679  128.270  141.416  1.00  0.00  C
ATOM      2  INT  MOL A   113.590  120.603  125.681  1.00  0.00  O
""")

    def test_cif_to_pdb_conversion(self):
        cif_to_pdb(self.input_cif, self.output_pdb)
        self.assertTrue(os.path.exists(self.output_pdb))

        with open(self.output_pdb, "r") as f:
            lines = f.readlines()

        self.assertEqual(len(lines), 3)  # 2 ATOM lines + 1 CONECT line
        self.assertTrue("COM" in lines[0])
        self.assertTrue("C" in lines[0])
        self.assertTrue("INT" in lines[1])
        self.assertTrue("O" in lines[1])
        self.assertTrue("CONECT" in lines[2])
        self.assertIn("  2", lines[2])  # INT atom serial
        self.assertIn("  1", lines[2])  # COM atom serial
    
    def test_real_cif_to_pdb(self):
        input_cif = "tests/fixtures/5l93_coarse_grained.cif"
        output_pdb = "tests/fixtures/output_5l93_model.pdb"

        cif_to_pdb(input_cif, output_pdb)

        self.assertTrue(os.path.exists(output_pdb))

        with open(output_pdb, "r") as f:
            lines = f.readlines()

        # Expect 108 atoms and 90 INT atoms → 108 ATOM + 90 CONECT lines
        atom_lines = [line for line in lines if line.startswith("ATOM")]
        conect_lines = [line for line in lines if line.startswith("CONECT")]

        self.assertEqual(len(atom_lines), 108)
        self.assertEqual(len(conect_lines), 90)

        # Spot check
        self.assertTrue(atom_lines[0].startswith("ATOM  "))
        self.assertTrue("COM" in atom_lines[0])
        self.assertTrue("INT" in atom_lines[-1])
        self.assertTrue("O" in atom_lines[-1])
        self.assertTrue(conect_lines[0].startswith("CONECT"))

        # Cleanup
        os.remove(output_pdb)

    def tearDown(self):
        if os.path.exists(self.input_cif):
            os.remove(self.input_cif)
        if os.path.exists(self.output_pdb):
            os.remove(self.output_pdb)

if __name__ == "__main__":
    unittest.main()
