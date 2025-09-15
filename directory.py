import os

def write_directory_tree(root_dir, output_file="directory_structure.txt"):
    def walk(dir_path, prefix=""):
        entries = []
        try:
            items = sorted(os.listdir(dir_path))
        except PermissionError:
            return [f"{prefix}[Permission Denied] {os.path.basename(dir_path)}"]

        for i, item in enumerate(items):
            path = os.path.join(dir_path, item)
            connector = "├── " if i < len(items) - 1 else "└── "
            entries.append(f"{prefix}{connector}{item}")
            if os.path.isdir(path):
                extension = "│   " if i < len(items) - 1 else "    "
                entries.extend(walk(path, prefix + extension))
        return entries

    tree = [os.path.basename(root_dir)]
    tree.extend(walk(root_dir))
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tree))

# --- Cast the spell here ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]
    else:
        root_directory = "."  # default to current directory
    write_directory_tree(root_directory)
    print(f"Directory structure written to directory_structure.txt for root: {root_directory}")
