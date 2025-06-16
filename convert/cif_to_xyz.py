# convert/cif_to_xyz.py

def convert_cif_to_xyz(cif_path, xyz_path):
    """
    Converts a PDB-style CIF file to XYZ format compatible with OVITO.

    Parameters:
        cif_path (str): Path to the input CIF file.
        xyz_path (str): Path to save the output XYZ file.
    """
    with open(cif_path, "r") as f:
        lines = f.readlines()

    atom_lines = [line for line in lines if line.startswith("ATOM")]

    with open(xyz_path, "w") as out:
        out.write(f"{len(atom_lines)}\n")
        out.write("Converted from CIF to XYZ for OVITO\n")
        for line in atom_lines:
            parts = line.split()
            atom = parts[-1]
            x, y, z = parts[5], parts[6], parts[7]
            out.write(f"{atom} {x} {y} {z}\n")


# -------------------------
# CLI usage
# -------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python cif_to_xyz.py input.cif output.xyz")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_cif_to_xyz(input_file, output_file)
    print(f"Converted: {input_file} → {output_file}")
