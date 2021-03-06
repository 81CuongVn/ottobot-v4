import logging
from pathlib import Path

import pygount
from pygount import ProjectSummary, SourceAnalysis

logging.getLogger(pygount.__name__).setLevel(logging.CRITICAL)


class Lines:
    """Analyzes the bots source code."""

    def __init__(self) -> None:
        self.py = [str(p) for p in Path(".").glob("ottbot/**/*.py")]
        self.sql = [str(p) for p in Path(".").glob("ottbot/**/*.sql")]
        self.targets = self.py + self.sql

    def __len__(self) -> int:
        return len(self.targets)

    def grab_percents(self) -> tuple[float, float, float]:
        """returns (code, docs, blank) percentages."""
        code_p = self.code / self.total * 100
        docs_p = self.docs / self.total * 100
        blank_p = self.blank / self.total * 100
        return round(code_p, 2), round(docs_p, 2), round(blank_p, 2)

    def count(self) -> None:
        """Counts the code in each file."""
        data = ProjectSummary()

        for file in self.targets:
            analysis = SourceAnalysis.from_file(file, "pygount")
            data.add(analysis)

        self.code = data.total_code_count + data.total_string_count
        self.docs = data.total_documentation_count
        self.blank = data.total_empty_count
        self.total = data.total_line_count
