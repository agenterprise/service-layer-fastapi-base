from pathlib import Path
from pyproject_parser import PyProject


def generate_docs_toc(docs_dir: str = "docs/generated", output_file: str = "docs/generated/INDEX.md") -> None:
    """
    Recursively traverse docs/generated directory and create a table of contents.
    
    Args:
        docs_dir: Root directory to traverse
        output_file: Output markdown file path
    """
    docs_path = Path(docs_dir)
    
    if not docs_path.exists():
        return
    
    toc_lines = ["# Documentation\n"]
    
    def traverse_directory(current_path: Path, toc_list: list, level: int = 0) -> None:
        """Recursively traverse directories and build TOC."""
        try:
            # Get sorted items
            items = sorted(current_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            
            for item in items:
                if item.name.startswith("."):
                    continue
                
                indent = "  " * level
                
                if item.is_dir():
                    # Add directory as heading
                    toc_list.append(f"{indent}## {item.name.replace('_', ' ').title()}\n")
                    traverse_directory(item, toc_list, level + 1)
                elif item.suffix == ".md":
                    # Add markdown file as link
                    relative_path = item.relative_to(docs_path)
                    file_title = item.stem.replace("_", " ").title()
                    toc_list.append(f"{indent}- [{file_title}]({relative_path})\n")
        except PermissionError:
            pass
    
    traverse_directory(docs_path, toc_lines)
    
    # Write TOC file
    output_path = Path(output_file)
    output_path.write_text("".join(toc_lines))


# Generate table of contents
generate_docs_toc()

# Merge pyproject configurations
masterpyproject = PyProject().load("pyproject.toml")
layerpyproject = PyProject().load(".layerconfig/{{cookiecutter.layername}}/pyproject.toml")

masterpyproject.dependency_groups.update(layerpyproject.dependency_groups)
masterpyproject.dump("pyproject.toml")


