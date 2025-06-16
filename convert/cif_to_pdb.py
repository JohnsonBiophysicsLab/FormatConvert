# convert/cif_to_pdb.py

def convert_cif_to_pdb(cif_path, pdb_path):
    """
    Converts a coarse-grained CIF file (PDB-style) to a PDB file.
    """
    with open(cif_path, "r") as f:
        lines = f.readlines()

    atom_lines = [line for line in lines if line.startswith("ATOM")]

    with open(pdb_path, "w") as out:
        for line in atom_lines:
            parts = line.split()
            if len(parts) < 11:
                continue

            serial = int(parts[1])
            atom_name = parts[2]
            res_name = parts[3]
            chain_id = parts[4]
            x = float(parts[5])
            y = float(parts[6])
            z = float(parts[7])
            occupancy = float(parts[8])
            bfactor = float(parts[9])
            element = parts[10]

            out.write(
                f"ATOM  {serial:5d} {atom_name:^4} {res_name:>3} {chain_id:1}   "
                f"1    {x:8.3f}{y:8.3f}{z:8.3f}{occupancy:6.2f}{bfactor:6.2f}          {element:>2}\n"
            )


# -------------------------------------
# CLI usage
# -------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python convert_cif_to_pdb.py input.cif output.pdb")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_cif_to_pdb(input_file, output_file)
    print(f"Converted {input_file} → {output_file}")
