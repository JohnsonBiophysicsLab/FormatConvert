import json

def ionerdss_json_to_xyz(json_path, xyz_path):
    """
    Converts an ioNERDSS-style JSON file to XYZ format with:
      - Center of mass at (0, 0, 0)
      - Interface atoms at their given coordinates

    Parameters:
        json_path (str): Path to input .json file
        xyz_path (str): Path to output .xyz file
    """
    with open(json_path, "r") as f:
        data = json.load(f)

    entries = []

    for moltype in data.get("molecule_types", []):
        mol_name = moltype["name"]

        # Add COM at origin
        entries.append((mol_name, 0.0, 0.0, 0.0))

        for iface in moltype.get("interfaces", []):
            iface_name = iface["name"]
            coord = iface["coord"]
            entries.append((iface_name, coord["x"], coord["y"], coord["z"]))

    with open(xyz_path, "w") as out:
        out.write(f"{len(entries)}\n")
        out.write(f"Converted from ioNERDSS JSON to XYZ\n")
        for label, x, y, z in entries:
            out.write(f"{label} {x:.3f} {y:.3f} {z:.3f}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python ionerdss_json_to_xyz.py input.json output.xyz")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    ionerdss_json_to_xyz(input_file, output_file)
    print(f"Converted {input_file} → {output_file}")
