"""
Create a markdown index of all markdown files in working dir.

Assumes one markdown file per directory.
Display name is the parent directory name of file.
"""
import os
from pathlib import Path
import re
import string

IGNORE_REGEX_PATTERNS = [".vscode", ".git", "(?i)readme.md", "(?i)index.md"]


def get_markdown_file_paths(start_dir=".") -> iter:
    for root, folders, files in os.walk(start_dir):
        for file_name in files:

            if not file_name.endswith(".md"): continue
            file_path = os.path.join(root, file_name)

            matches = any(re.search(p, file_name) for p in IGNORE_REGEX_PATTERNS)
            if matches: continue

            yield file_path


def create_markdown(file_paths: list) -> string:
    hierarchy = sort_paths_into_hierarchy(file_paths)
    header = "# index\n"
    return header + create_hierarchy_markdown(hierarchy)


def create_hierarchy_markdown(hierarchy, indent=0):
    output = ""
    for key, value in hierarchy.items():

        if isinstance(value, str):
            output += get_prefix_str(indent) + get_file_hyperlink(value) + "\n"
            continue

        output += get_prefix_str(indent) + key + "\n"
        output += create_hierarchy_markdown(value, indent + 1)
    return output


def get_file_hyperlink(file_path: str) -> str:
    parts = Path(file_path).parts
    parent_folder_name = parts[-2]
    return "[%s](%s)" % (parent_folder_name, file_path)


def get_prefix_str(indent_level: int):
    #if indent_level == 0:
    #    return ""
    return "\t" * indent_level + "  - "


def sort_paths_into_hierarchy(file_paths: list) -> dict:
    hierarchy = {}
    for file_path in file_paths:
        parts = list(Path(file_path).parts)
        parts[-1] = file_path
        add_value_to_dict_hierarchy(hierarchy, parts)
    return hierarchy


def add_value_to_dict_hierarchy(hierarchy: dict, value_parts: list) -> None:
    # i know this method is a little gross but gimme some slack, it's an adhoc script
    # get sub dict/ensure exists
    current_sub_dict = hierarchy
    for part in value_parts[:-2]:
        if part not in current_sub_dict:
            current_sub_dict[part] = {}
        current_sub_dict = current_sub_dict[part]
    # set it!
    current_sub_dict[value_parts[-2]] = value_parts[-1]


def write_to_file(markdown, file_path="index.md"):
    with open(file_path, "w") as file:
        file.write(markdown)


def main():
    file_paths = get_markdown_file_paths()
    markdown = create_markdown(list(file_paths))
    write_to_file(markdown, "README.md")


if __name__ == "__main__":
    main()