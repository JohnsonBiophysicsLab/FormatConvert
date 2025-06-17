import unittest
import os
from convert.cif_to_lammps import cif_to_lammps  # updated function name

class TestCIFToLAMMPS(unittest.TestCase):
    def setUp(self):
        os.makedirs("tests/fixtures", exist_ok=True)
        self.cif_path = "tests/fixtures/test_cif_to_lammps_input.cif"
        self.lmp_path = "tests/fixtures/test_cif_to_lammps_output.lmp"

        # COM-INT CIF input with 2 COM and 2 INT per residue
        with open(self.cif_path, "w") as f:
            f.write("""\
ATOM      1  COM  MOL A   0.000  0.000  0.000  1.00  0.00  C
ATOM      2  INT  MOL A   1.000  0.000  0.000  1.00  0.00  O
ATOM      3  INT  MOL A   0.000  1.000  0.000  1.00  0.00  O
ATOM      4  COM  MOL B   5.000  5.000  5.000  1.00  0.00  C
ATOM      5  INT  MOL B   6.000  5.000  5.000  1.00  0.00  O
ATOM      6  INT  MOL B   5.000  6.000  5.000  1.00  0.00  O
""")

    def test_conversion(self):
        cif_to_lammps(self.cif_path, self.lmp_path)
        self.assertTrue(os.path.exists(self.lmp_path))

        with open(self.lmp_path, "r") as f:
            content = f.read()

        # Check presence of correct sections
        self.assertIn("6 atoms", content)
        self.assertIn("4 bonds", content)
        self.assertIn("Atoms", content)
        self.assertIn("Bonds", content)

        # Validate bond connections
        # Extract bond lines by section
        lines = content.splitlines()
        try:
            start = lines.index("Bonds") + 2  # skip the header and blank line
        except ValueError:
            self.fail("Bonds section not found in output.")

        bond_lines = []
        for line in lines[start:]:
            if line.strip() == "":
                break  # end of Bonds section
            bond_lines.append(line.strip())

        self.assertEqual(len(bond_lines), 4)

        # Expected bond pairs: (1 2), (1 3), (4 5), (4 6)
        expected_pairs = {(1, 2), (1, 3), (4, 5), (4, 6)}
        parsed_pairs = set(tuple(map(int, line.split()[2:4])) for line in bond_lines)
        self.assertEqual(expected_pairs, parsed_pairs)

    def tearDown(self):
        if os.path.exists(self.cif_path):
            os.remove(self.cif_path)
        if os.path.exists(self.lmp_path):
            os.remove(self.lmp_path)

class Test5l93CoarseGrainedCIFtoLammps(unittest.TestCase):
    def setUp(self):
        self.cif_path = "tests/fixtures/5l93_coarse_grained.cif"
        self.lmp_path = "tests/fixtures/5l93_output.lmp"

    def test_bond_counts(self):
        cif_to_lammps(self.cif_path, self.lmp_path)

        self.assertTrue(os.path.exists(self.lmp_path))

        with open(self.lmp_path, "r") as f:
            lines = f.read().splitlines()

        # Confirm atom and bond header counts
        atom_line = next(l for l in lines if l.strip().endswith("atoms") and l.strip().split()[0].isdigit())
        bond_line = next(l for l in lines if l.strip().endswith("bonds") and l.strip().split()[0].isdigit())

        num_atoms = int(atom_line.strip().split()[0])
        num_bonds = int(bond_line.strip().split()[0])

        self.assertEqual(num_atoms, 108)

        # Bonds: one COM per group, bonded to 5 INTs each
        # Should be 18 COMs × 5 = 90 bonds
        self.assertEqual(num_bonds, 90)

        # Extract actual bond section lines
        start = lines.index("Bonds") + 2
        bond_lines = []
        for line in lines[start:]:
            if line.strip() == "":
                break
            bond_lines.append(line.strip())

        self.assertEqual(len(bond_lines), 90)

        # Spot check: ensure each COM has correct number of INT bonds
        # Count COM-to-INT pairings
        com_bond_counts = {}
        for bond in bond_lines:
            parts = bond.split()
            _, _, a1, a2 = map(int, parts)
            for a in (a1, a2):
                com_bond_counts[a] = com_bond_counts.get(a, 0) + 1

        # There should be 18 atoms that appear exactly 5 times (the COMs)
        com_like = [aid for aid, count in com_bond_counts.items() if count == 5]
        self.assertEqual(len(com_like), 18)

    def tearDown(self):
        if os.path.exists(self.lmp_path):
            os.remove(self.lmp_path)

if __name__ == "__main__":
    unittest.main()
