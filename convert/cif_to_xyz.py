def convert_cif_to_xyz(cif_path, xyz_path, bonds_path=None):
    """
    Converts a PDB-style CIF file to XYZ format.
    Optionally writes a bonds file connecting atom 0 to all others.

    Parameters:
        cif_path (str): Path to the input CIF file.
        xyz_path (str): Path to save the output XYZ file.
        bonds_path (str, optional): Path to save bonds file.
    """
    with open(cif_path, "r") as f:
        lines = f.readlines()

    atom_lines = [line for line in lines if line.startswith("ATOM")]
    atoms = []

    for line in atom_lines:
        parts = line.split()
        atom = parts[-1]
        x, y, z = parts[5], parts[6], parts[7]
        atoms.append((atom, x, y, z))

    with open(xyz_path, "w") as out:
        out.write(f"{len(atoms)}\n")
        out.write("Converted from CIF to XYZ\n")
        for atom, x, y, z in atoms:
            out.write(f"{atom} {x} {y} {z}\n")

    if bonds_path:
        with open(bonds_path, "w") as bout:
            for i in range(1, len(atoms)):
                bout.write(f"0 {i}\n")  # connect atom 0 to all others (customizable logic)


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

    convert_cif_to_xyz(input_file, output_xyz, output_bonds)

    print(f"Converted {input_file} → {output_xyz}")
    if output_bonds:
        print(f"Bonds written to {output_bonds}")
