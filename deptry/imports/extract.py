from __future__ import annotations

import logging
from collections import defaultdict
from typing import TYPE_CHECKING

from deptry.imports.extractors import NotebookImportExtractor, PythonImportExtractor

if TYPE_CHECKING:
    from pathlib import Path

    from deptry.imports.extractors.base import ImportExtractor
    from deptry.imports.location import Location


def get_imported_modules_for_list_of_files(list_of_files: list[Path]) -> dict[str, list[Location]]:
    logging.info(f"Scanning {len(list_of_files)} file{'s' if len(list_of_files)>1 else ''}...")

    modules: dict[str, list[Location]] = defaultdict(list)

    for file in list_of_files:
        for module, locations in get_imported_modules_from_file(file).items():
            for location in locations:
                modules[module].append(location)

    logging.debug(f"All imported modules: {modules}\n")

    return modules


def get_imported_modules_from_file(path_to_file: Path) -> dict[str, list[Location]]:
    logging.debug(f"Scanning {path_to_file}...")

    modules = _get_extractor_class(path_to_file)(path_to_file).extract_imports()

    logging.debug(f"Found the following imports in {str(path_to_file)}: {modules}")

    return modules


def _get_extractor_class(path_to_file: Path) -> type[ImportExtractor]:
    if path_to_file.suffix == ".ipynb":
        return NotebookImportExtractor
    return PythonImportExtractor
