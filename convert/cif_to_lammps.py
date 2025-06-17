def cif_to_lammps(cif_path, lammps_path):
    """
    Converts a PDB-style CIF file to a LAMMPS data file with bonds between COM and
    associated INT atoms (same residue name).

    Assumptions:
    ----------
    1. CIF lines start with "ATOM" and follow the PDB-style format:
       ATOM  <id> <label> <resname> <chain> <x> <y> <z> <occupancy> <bfactor> <element>
    2. COM and INT atoms are grouped by the <chain> field (e.g. "A", "A-2").
    3. Each COM is bonded to all INTs that share the same chain ID.
    4. Atom type is set to 1 for all atoms.
    5. Simulation box is inferred from coordinates with ±10 Å padding.
    6. No velocities, charges, or molecule IDs are written.

    Parameters:
    ----------
    cif_path : str
        Path to the input CIF file.
    lammps_path : str
        Path to the output LAMMPS data file.
    """

    atoms = []
    residues = {}  # chain_id -> {"COM": id, "INT": [ids]}
    atom_index = 1

    with open(cif_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("ATOM"):
            parts = line.split()
            label = parts[2]         # e.g. COM or INT
            chain_id = parts[4]      # e.g. A, A-2, etc.
            x, y, z = map(float, parts[5:8])
            atom_type = 1

            atoms.append((atom_index, atom_type, x, y, z))
            if chain_id not in residues:
                residues[chain_id] = {"COM": None, "INT": []}

            if label == "COM":
                residues[chain_id]["COM"] = atom_index
            elif label == "INT":
                residues[chain_id]["INT"].append(atom_index)

            atom_index += 1

    # Generate bonds: COM to each INT in same chain group
    bonds = []
    bond_id = 1
    bond_type = 1
    for chain, group in residues.items():
        com_id = group["COM"]
        for int_id in group["INT"]:
            if com_id is not None:
                bonds.append((bond_id, bond_type, com_id, int_id))
                bond_id += 1

    # Bounding box
    xs = [a[2] for a in atoms]
    ys = [a[3] for a in atoms]
    zs = [a[4] for a in atoms]
    buffer = 10.0
    xlo, xhi = min(xs) - buffer, max(xs) + buffer
    ylo, yhi = min(ys) - buffer, max(ys) + buffer
    zlo, zhi = min(zs) - buffer, max(zs) + buffer

    # Write LAMMPS data file
    with open(lammps_path, "w") as f:
        f.write("LAMMPS data file with COM-INT bonds\n\n")
        f.write(f"{len(atoms)} atoms\n")
        f.write(f"{len(bonds)} bonds\n")
        f.write("1 atom types\n")
        f.write("1 bond types\n\n")
        f.write(f"{xlo:.3f} {xhi:.3f} xlo xhi\n")
        f.write(f"{ylo:.3f} {yhi:.3f} ylo yhi\n")
        f.write(f"{zlo:.3f} {zhi:.3f} zlo zhi\n\n")

        f.write("Atoms\n\n")
        for atom_id, atom_type, x, y, z in atoms:
            f.write(f"{atom_id} {atom_type} {x:.4f} {y:.4f} {z:.4f}\n")

        f.write("\nBonds\n\n")
        for bond_id, bond_type, atom1, atom2 in bonds:
            f.write(f"{bond_id} {bond_type} {atom1} {atom2}\n")


# -------------------------------
# CLI usage
# -------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python convert_cif_to_lammps.py input.cif output.lmp")
        sys.exit(1)

    input_cif = sys.argv[1]
    output_lmp = sys.argv[2]

    cif_to_lammps(input_cif, output_lmp)

    print(f"Converted {input_cif} → {output_lmp}")