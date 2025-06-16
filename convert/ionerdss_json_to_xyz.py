import json

import json

def ionerdss_json_to_xyz(json_path, xyz_path, bonds_path=None):
    """
    Converts an ioNERDSS-style JSON file to XYZ format with:
      - Center of mass at (0, 0, 0)
      - Interface atoms at their given coordinates
      - Optionally writes bonds file
    """
    with open(json_path, "r") as f:
        data = json.load(f)

    entries = []

    bonds = []  # List of (index1, index2)

    atom_index = 0
    for moltype in data.get("molecule_types", []):
        mol_name = moltype["name"]

        # Add COM
        entries.append((mol_name, 0.0, 0.0, 0.0))
        com_index = atom_index
        atom_index += 1

        for iface in moltype.get("interfaces", []):
            iface_name = iface["name"]
            coord = iface["coord"]
            entries.append((iface_name, coord["x"], coord["y"], coord["z"]))
            bonds.append((com_index, atom_index))  # COM to interface
            atom_index += 1

    with open(xyz_path, "w") as out:
        out.write(f"{len(entries)}\n")
        out.write("Converted from ioNERDSS JSON to XYZ\n")
        for label, x, y, z in entries:
            out.write(f"{label} {x:.3f} {y:.3f} {z:.3f}\n")

    if bonds_path:
        with open(bonds_path, "w") as b:
            for i, j in bonds:
                b.write(f"{i} {j}\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) not in (3, 4):
        print("Usage: python ionerdss_json_to_xyz.py input.json output.xyz [output.bonds]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_xyz = sys.argv[2]
    output_bonds = sys.argv[3] if len(sys.argv) == 4 else None

    ionerdss_json_to_xyz(input_file, output_xyz, output_bonds)

    print(f"Converted {input_file} → {output_xyz}")
    if output_bonds:
        print(f"Bonds written to {output_bonds}")

