"""
Data Inventory - Scan available data files for a paper.

This module provides tools to:
1. Scan a paper's data directory and catalog available files
2. Track what variables/columns are available in each data source
3. Verify statistical claims against available data
4. Flag claims that reference data we don't have
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class DataType(Enum):
    """Types of data sources."""
    SPREADSHEET = "spreadsheet"  # .xlsx, .csv
    INTERVIEW = "interview"      # transcripts
    FIELDNOTES = "fieldnotes"   # observation notes
    SURVEY = "survey"           # survey responses
    IMAGE = "image"             # figures, diagrams
    UNKNOWN = "unknown"


@dataclass
class DataFile:
    """Metadata about a data file."""
    path: Path
    name: str
    data_type: DataType
    extension: str
    size_bytes: int
    columns: list[str] = field(default_factory=list)  # For tabular data
    variables: list[str] = field(default_factory=list)  # Key variables mentioned
    notes: str = ""

    @property
    def available(self) -> bool:
        """Whether the file actually exists and is readable."""
        return self.path.exists() and self.size_bytes > 0


@dataclass
class DataClaim:
    """A claim in the manuscript that references data."""
    text: str
    claim_type: str  # 'statistic', 'count', 'variable', 'quote'
    location: str    # Where in manuscript
    verified: bool = False
    source_file: Optional[str] = None
    notes: str = ""


@dataclass
class InventoryResult:
    """Result of scanning a data directory."""
    files: list[DataFile]
    total_files: int
    tabular_files: int
    interview_files: int
    missing_common: list[str]  # Common data types we don't have

    def has_data_type(self, data_type: DataType) -> bool:
        """Check if we have any files of this type."""
        return any(f.data_type == data_type for f in self.files)

    def get_files_by_type(self, data_type: DataType) -> list[DataFile]:
        """Get all files of a specific type."""
        return [f for f in self.files if f.data_type == data_type]


class DataInventory:
    """
    Scans data directories and tracks what data is available for a paper.

    This prevents hallucination of statistics by verifying claims against
    available data sources.

    Usage:
        inventory = DataInventory()
        result = inventory.scan("/path/to/paper/data")

        # Check if we have survey data
        if not result.has_data_type(DataType.SURVEY):
            print("WARNING: No survey data available")

        # Verify a claim
        claim = "136 workers responded to the survey"
        verified = inventory.verify_claim(claim, result)
    """

    # File extension mappings
    EXTENSION_MAP = {
        '.xlsx': DataType.SPREADSHEET,
        '.xls': DataType.SPREADSHEET,
        '.csv': DataType.SPREADSHEET,
        '.tsv': DataType.SPREADSHEET,
        '.dta': DataType.SPREADSHEET,  # Stata
        '.rds': DataType.SPREADSHEET,  # R
        '.sav': DataType.SPREADSHEET,  # SPSS
        '.txt': DataType.INTERVIEW,    # Often transcripts
        '.rtf': DataType.INTERVIEW,
        '.docx': DataType.INTERVIEW,
        '.doc': DataType.INTERVIEW,
        '.png': DataType.IMAGE,
        '.jpg': DataType.IMAGE,
        '.jpeg': DataType.IMAGE,
        '.pdf': DataType.IMAGE,  # Often figures
    }

    # Keywords that suggest survey data
    SURVEY_KEYWORDS = [
        'survey', 'response', 'questionnaire', 'likert',
        'weekly', 'daily', 'responses', 'scale',
    ]

    # Keywords that suggest interview data
    INTERVIEW_KEYWORDS = [
        'interview', 'transcript', 'field', 'observation',
        'notes', 'memo', 'ethnograph',
    ]

    def __init__(self):
        """Initialize the inventory scanner."""
        self._stat_patterns = self._compile_stat_patterns()

    def scan(self, data_path: str | Path) -> InventoryResult:
        """
        Scan a data directory and catalog available files.

        Args:
            data_path: Path to the paper's data directory

        Returns:
            InventoryResult with cataloged files
        """
        data_path = Path(data_path)
        files = []

        if not data_path.exists():
            return InventoryResult(
                files=[],
                total_files=0,
                tabular_files=0,
                interview_files=0,
                missing_common=["data directory not found"],
            )

        # Walk the directory
        for root, dirs, filenames in os.walk(data_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for filename in filenames:
                if filename.startswith('.'):
                    continue

                filepath = Path(root) / filename
                ext = filepath.suffix.lower()

                data_type = self.EXTENSION_MAP.get(ext, DataType.UNKNOWN)

                # Refine type based on filename keywords
                name_lower = filename.lower()
                if any(kw in name_lower for kw in self.SURVEY_KEYWORDS):
                    data_type = DataType.SURVEY
                elif any(kw in name_lower for kw in self.INTERVIEW_KEYWORDS):
                    data_type = DataType.INTERVIEW

                try:
                    size = filepath.stat().st_size
                except OSError:
                    size = 0

                data_file = DataFile(
                    path=filepath,
                    name=filename,
                    data_type=data_type,
                    extension=ext,
                    size_bytes=size,
                )

                files.append(data_file)

        # Count by type
        tabular = sum(1 for f in files if f.data_type == DataType.SPREADSHEET)
        interview = sum(1 for f in files if f.data_type in [DataType.INTERVIEW, DataType.FIELDNOTES])

        # Check for common missing data types
        missing = []
        if not any(f.data_type == DataType.SURVEY for f in files):
            missing.append("survey response data")
        if not any(f.data_type == DataType.INTERVIEW for f in files):
            missing.append("interview transcripts")

        return InventoryResult(
            files=files,
            total_files=len(files),
            tabular_files=tabular,
            interview_files=interview,
            missing_common=missing,
        )

    def verify_claim(self, claim: str, inventory: InventoryResult) -> DataClaim:
        """
        Attempt to verify a data claim against available sources.

        Args:
            claim: The text of the claim to verify
            inventory: The data inventory to check against

        Returns:
            DataClaim with verification status
        """
        claim_type = self._classify_claim(claim)

        # Check if we have the right type of data
        verified = False
        source_file = None
        notes = ""

        if claim_type == "survey_stat":
            if inventory.has_data_type(DataType.SURVEY):
                survey_files = inventory.get_files_by_type(DataType.SURVEY)
                source_file = survey_files[0].name if survey_files else None
                notes = "Survey data available; verify specific values"
                verified = False  # Needs manual verification
            else:
                notes = "NO SURVEY DATA AVAILABLE - claim cannot be verified"
                verified = False

        elif claim_type == "count":
            # Counts from HR data, etc.
            if inventory.has_data_type(DataType.SPREADSHEET):
                notes = "Tabular data available; verify specific counts"
                verified = False
            else:
                notes = "No tabular data found"
                verified = False

        elif claim_type == "quote":
            if inventory.has_data_type(DataType.INTERVIEW):
                notes = "Interview data available; quote may be verifiable"
                verified = False
            else:
                notes = "No interview transcripts found"
                verified = False

        return DataClaim(
            text=claim,
            claim_type=claim_type,
            location="",  # To be filled by caller
            verified=verified,
            source_file=source_file,
            notes=notes,
        )

    def _classify_claim(self, claim: str) -> str:
        """Classify what type of data claim this is."""
        claim_lower = claim.lower()

        # Survey statistics
        survey_indicators = [
            'survey', 'respondent', 'response rate', 'likert',
            'weekly measure', 'scale', 'questionnaire',
        ]
        if any(ind in claim_lower for ind in survey_indicators):
            return "survey_stat"

        # Worker counts, sample sizes
        count_patterns = [
            r'\d+\s*workers?', r'\d+\s*employees?', r'\d+\s*participants?',
            r'sample\s+of\s+\d+', r'n\s*=\s*\d+', r'\d+\s*interviews?',
        ]
        for pattern in count_patterns:
            if re.search(pattern, claim_lower):
                return "count"

        # Statistical results
        stat_patterns = [
            r'β\s*=', r'p\s*[<>=]', r'coefficient', r'significant',
            r'percentage\s*point', r'mean\s*=', r'sd\s*=', r'correlation',
        ]
        for pattern in stat_patterns:
            if re.search(pattern, claim_lower):
                return "statistic"

        # Quotes
        if '"' in claim or '"' in claim or 'said' in claim_lower or 'noted' in claim_lower:
            return "quote"

        return "other"

    def _compile_stat_patterns(self) -> list:
        """Compile regex patterns for statistical claims."""
        patterns = [
            r'\d+\s*workers?',
            r'\d+\s*weeks?',
            r'\d+%\s*response\s*rate',
            r'mean\s*[=:]?\s*\d+\.?\d*',
            r'[Ss][Dd]\s*[=:]?\s*\d+\.?\d*',
            r'kappa\s*[=:]?\s*\d+\.?\d*',
            r'α\s*[=:]?\s*\d+\.?\d*',
            r'β\s*=\s*[\d\.\-]+',
            r'p\s*[<>=]\s*[\d\.]+',
            r'n\s*=\s*\d+',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]

    def extract_statistical_claims(self, text: str) -> list[str]:
        """
        Extract all statistical claims from text for verification.

        Args:
            text: The manuscript text

        Returns:
            List of statistical claim strings
        """
        claims = []

        for pattern in self._stat_patterns:
            for match in pattern.finditer(text):
                # Get some context around the match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                claims.append(context)

        return claims


def scan_paper_data(paper_path: str | Path) -> InventoryResult:
    """
    Convenience function to scan a paper's data directory.

    Args:
        paper_path: Path to the paper directory (parent of 'data' folder)

    Returns:
        InventoryResult
    """
    paper_path = Path(paper_path)
    data_path = paper_path / "data"

    if not data_path.exists():
        # Try finding data directory
        for subdir in ['data', 'Data', 'analysis', 'Analysis']:
            candidate = paper_path / subdir
            if candidate.exists():
                data_path = candidate
                break

    inventory = DataInventory()
    return inventory.scan(data_path)
