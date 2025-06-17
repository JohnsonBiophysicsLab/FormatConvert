def cif_to_xyz(cif_path, xyz_path, bonds_path=None):
    """
    Converts a PDB-style CIF file to XYZ format.

    Assumptions:
    - Each atom line starts with 'ATOM' and follows a PDB-style format.
    - Bonds connect each COM atom to all INT atoms with the same residue name (column 4).

    Parameters:
        cif_path (str): Path to the input CIF file.
        xyz_path (str): Path to save the output XYZ file.
        bonds_path (str, optional): Path to save bonds file.
    """
    with open(cif_path, "r") as f:
        lines = f.readlines()

    atom_lines = [line for line in lines if line.startswith("ATOM")]
    atoms = []
    resname_to_com_index = {}
    bonds = []

    for i, line in enumerate(atom_lines):
        parts = line.split()
        atom_name = parts[2]  # e.g. COM or INT
        resname = parts[3]    # e.g. MOL, MOL-2
        x, y, z = parts[5], parts[6], parts[7]
        atoms.append((parts[-1], x, y, z))  # element symbol, x, y, z

        if atom_name == "COM":
            resname_to_com_index[resname] = i
        elif atom_name == "INT" and resname in resname_to_com_index:
            bonds.append((resname_to_com_index[resname], i))

    # Write XYZ file
    with open(xyz_path, "w") as out:
        out.write(f"{len(atoms)}\n")
        out.write("Converted from CIF to XYZ\n")
        for atom, x, y, z in atoms:
            out.write(f"{atom} {x} {y} {z}\n")

    # Write bonds file
    if bonds_path:
        with open(bonds_path, "w") as bout:
            for i, j in bonds:
                bout.write(f"{i} {j}\n")


# -------------------------
# CLI usage
# -------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) not in (3, 4):
        print("Usage: python cif_to_xyz.py input.cif output.xyz [output.bonds]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_xyz = sys.argv[2]
    output_bonds = sys.argv[3] if len(sys.argv) == 4 else None

    cif_to_xyz(input_file, output_xyz, output_bonds)

    print(f"Converted {input_file} → {output_xyz}")
    if output_bonds:
        print(f"Bonds written to {output_bonds}")
