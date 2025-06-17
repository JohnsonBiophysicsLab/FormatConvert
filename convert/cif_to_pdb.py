# convert/cif_to_pdb.py

def cif_to_pdb(cif_path, pdb_path):
    """
    Converts a coarse-grained CIF file (PDB-style) to a PDB file.
    """
    atoms = []
    bonds = []

    with open(cif_path, "r") as f:
        for line in f:
            if not line.startswith("ATOM"):
                continue
            parts = line.split()
            if len(parts) < 11:
                continue

            serial = int(parts[1])
            atom_name = parts[2]
            res_name = parts[3]
            chain_id = parts[4]
            x, y, z = map(float, parts[5:8])
            occupancy = float(parts[8])
            bfactor = float(parts[9])
            element = parts[10]

            atoms.append({
                "serial": serial,
                "name": atom_name,
                "res_name": res_name,
                "chain_id": chain_id,
                "x": x, "y": y, "z": z,
                "occupancy": occupancy,
                "bfactor": bfactor,
                "element": element
            })

    # Build a mapping from (res_name, chain_id) to COM and INTs
    from collections import defaultdict
    groups = defaultdict(lambda: {"COM": None, "INTs": []})

    for atom in atoms:
        key = (atom["res_name"], atom["chain_id"])
        if atom["name"] == "COM":
            groups[key]["COM"] = atom["serial"]
        elif atom["name"] == "INT":
            groups[key]["INTs"].append(atom["serial"])

    # Build CONECT records: COM — INT
    for group in groups.values():
        com = group["COM"]
        for int_serial in group["INTs"]:
            if com is not None:
                bonds.append((com, int_serial))

    with open(pdb_path, "w") as out:
        # Write ATOM lines
        for atom in atoms:
            out.write(
                f"ATOM  {atom['serial']:5d} {atom['name']:^4} {atom['res_name']:>3} {atom['chain_id']:1}   "
                f"1    {atom['x']:8.3f}{atom['y']:8.3f}{atom['z']:8.3f}{atom['occupancy']:6.2f}{atom['bfactor']:6.2f}          {atom['element']:>2}\n"
            )

        # Write CONECT lines
        for com, int_atom in bonds:
            out.write(f"CONECT{com:5d}{int_atom:5d}\n")


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

    cif_to_pdb(input_file, output_file)
    print(f"Converted {input_file} → {output_file}")
