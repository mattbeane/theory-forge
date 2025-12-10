"""
Statistics Validator - Flag unverified statistical claims.

This module catches hallucinated statistics by:
1. Extracting all statistical claims from text
2. Checking against known data sources
3. Flagging claims that cannot be verified
4. Requiring explicit data source attribution

The key insight: LLMs will confidently fabricate statistics that "sound right."
Every specific number in a manuscript must trace back to actual data.
"""

import re
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from .data_inventory import DataInventory, InventoryResult, DataType


class StatClaimType(Enum):
    """Types of statistical claims."""
    SAMPLE_SIZE = "sample_size"      # N = 136, 500 workers
    PERCENTAGE = "percentage"         # 62% response rate
    REGRESSION = "regression"         # β = 0.21, p < .001
    CORRELATION = "correlation"       # r = 0.45
    MEAN_SD = "mean_sd"              # mean = 3.8, SD = 1.9
    COUNT = "count"                   # 50 weeks, 14 interviews
    RELIABILITY = "reliability"       # Cronbach's α = 0.82, kappa = 0.79
    EFFECT_SIZE = "effect_size"       # d = 0.5, percentage points
    TEMPORAL = "temporal"             # 18-month period
    OTHER = "other"


class VerificationStatus(Enum):
    """Status of claim verification."""
    VERIFIED = "verified"             # Confirmed in data
    UNVERIFIED = "unverified"         # Not yet checked
    SUSPICIOUS = "suspicious"          # Looks fabricated
    NO_DATA_SOURCE = "no_data_source"  # No data file exists
    PLACEHOLDER = "placeholder"        # Marked as TODO


@dataclass
class StatisticalClaim:
    """A statistical claim extracted from text."""
    raw_text: str           # The exact text containing the claim
    claim_type: StatClaimType
    value: str              # The extracted value (e.g., "136", "0.21")
    context: str            # Surrounding text for context
    location: str           # Where in document (line number, section)
    status: VerificationStatus = VerificationStatus.UNVERIFIED
    data_source: Optional[str] = None
    notes: str = ""

    @property
    def needs_attention(self) -> bool:
        """Whether this claim needs human verification."""
        return self.status in [
            VerificationStatus.SUSPICIOUS,
            VerificationStatus.NO_DATA_SOURCE,
            VerificationStatus.UNVERIFIED,
        ]


@dataclass
class ValidationReport:
    """Report from validating statistics in a document."""
    total_claims: int
    verified_claims: int
    suspicious_claims: int
    no_data_claims: int
    claims: list[StatisticalClaim]

    @property
    def needs_review(self) -> bool:
        """Whether any claims need human review."""
        return self.suspicious_claims > 0 or self.no_data_claims > 0

    def get_suspicious(self) -> list[StatisticalClaim]:
        """Get claims flagged as suspicious."""
        return [c for c in self.claims if c.status == VerificationStatus.SUSPICIOUS]

    def get_unverified(self) -> list[StatisticalClaim]:
        """Get claims that couldn't be verified."""
        return [c for c in self.claims
                if c.status in [VerificationStatus.UNVERIFIED, VerificationStatus.NO_DATA_SOURCE]]


class StatisticsValidator:
    """
    Validates statistical claims against available data sources.

    This is a critical safeguard against LLM hallucination of statistics.
    Every number in the paper should trace back to real data.

    Usage:
        validator = StatisticsValidator()

        # Scan data directory first
        inventory = DataInventory().scan("/path/to/paper/data")

        # Validate manuscript text
        report = validator.validate(manuscript_text, inventory)

        if report.needs_review:
            for claim in report.get_suspicious():
                print(f"SUSPICIOUS: {claim.raw_text}")
                print(f"  Notes: {claim.notes}")
    """

    # Patterns for extracting different types of statistics
    PATTERNS = {
        StatClaimType.SAMPLE_SIZE: [
            r'[Nn]\s*=\s*(\d+)',
            r'(\d+)\s*workers?',
            r'(\d+)\s*employees?',
            r'(\d+)\s*participants?',
            r'(\d+)\s*respondents?',
            r'sample\s+of\s+(\d+)',
            r'(\d+)\s+individuals?',
        ],
        StatClaimType.PERCENTAGE: [
            r'(\d+(?:\.\d+)?)\s*%',
            r'(\d+(?:\.\d+)?)\s*percent',
            r'response\s+rate\s+(?:of\s+)?(\d+(?:\.\d+)?)',
        ],
        StatClaimType.REGRESSION: [
            r'[βb]\s*=\s*([\-\d\.]+)',
            r'coefficient\s+(?:of\s+)?([\-\d\.]+)',
            r'p\s*[<>=]\s*([\d\.]+)',
            r'[Ss]ignificant\s+at\s+(?:the\s+)?([\d\.]+)',
        ],
        StatClaimType.MEAN_SD: [
            r'[Mm]ean\s*[=:]\s*([\d\.]+)',
            r'[Mm]\s*=\s*([\d\.]+)',
            r'[Ss][Dd]\s*[=:]\s*([\d\.]+)',
            r'[Ss]tandard\s+deviation\s+(?:of\s+)?([\d\.]+)',
        ],
        StatClaimType.RELIABILITY: [
            r'[αa]lpha\s*[=:]\s*([\d\.]+)',
            r"[Cc]ronbach'?s?\s*[αa]\s*[=:]\s*([\d\.]+)",
            r'[Kk]appa\s*[=:]\s*([\d\.]+)',
            r'[Ii]nter-?rater\s+reliability\s+(?:of\s+)?([\d\.]+)',
            r'ICC\s*[=:]\s*([\d\.]+)',
        ],
        StatClaimType.COUNT: [
            r'(\d+)\s*weeks?',
            r'(\d+)\s*months?',
            r'(\d+)\s*interviews?',
            r'(\d+)\s*observations?',
            r'(\d+)\s*facilities',
            r'(\d+)\s*sites?',
        ],
        StatClaimType.EFFECT_SIZE: [
            r'(\d+(?:\.\d+)?)\s*percentage\s*points?',
            r"[Cc]ohen'?s?\s*d\s*[=:]\s*([\d\.]+)",
            r'effect\s+size\s+(?:of\s+)?([\d\.]+)',
        ],
        StatClaimType.TEMPORAL: [
            r'(\d+)\s*-?\s*(?:month|year)\s*period',
            r'(?:over|during)\s+(\d+)\s*(?:weeks?|months?|years?)',
        ],
    }

    # Suspicious patterns - claims that look fabricated
    SUSPICIOUS_PATTERNS = [
        # Overly precise reliability metrics from missing data
        (r'kappa\s*=\s*0\.\d{2}', "Kappa value without coding data"),
        (r'α\s*=\s*0\.\d{2}', "Cronbach's alpha without survey items"),
        # Round numbers that seem made up
        (r'(?:exactly\s+)?(?:50|100|150|200)\s+(?:workers?|respondents?)', "Suspiciously round sample size"),
        # Response rates without survey data
        (r'\d+%\s*response\s*rate', "Response rate without survey data"),
    ]

    def __init__(self):
        """Initialize the statistics validator."""
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for efficiency."""
        self._compiled = {}
        for claim_type, patterns in self.PATTERNS.items():
            self._compiled[claim_type] = [
                re.compile(p, re.IGNORECASE) for p in patterns
            ]
        self._suspicious_re = [
            (re.compile(p, re.IGNORECASE), msg)
            for p, msg in self.SUSPICIOUS_PATTERNS
        ]

    def validate(
        self,
        text: str,
        inventory: Optional[InventoryResult] = None,
    ) -> ValidationReport:
        """
        Validate all statistical claims in text.

        Args:
            text: The manuscript text to validate
            inventory: Optional data inventory to check against

        Returns:
            ValidationReport with all claims and their status
        """
        claims = self._extract_claims(text)

        # Check each claim
        for claim in claims:
            self._verify_claim(claim, inventory)

        verified = sum(1 for c in claims if c.status == VerificationStatus.VERIFIED)
        suspicious = sum(1 for c in claims if c.status == VerificationStatus.SUSPICIOUS)
        no_data = sum(1 for c in claims if c.status == VerificationStatus.NO_DATA_SOURCE)

        return ValidationReport(
            total_claims=len(claims),
            verified_claims=verified,
            suspicious_claims=suspicious,
            no_data_claims=no_data,
            claims=claims,
        )

    def _extract_claims(self, text: str) -> list[StatisticalClaim]:
        """Extract all statistical claims from text."""
        claims = []
        lines = text.split('\n')

        for line_num, line in enumerate(lines, 1):
            for claim_type, patterns in self._compiled.items():
                for pattern in patterns:
                    for match in pattern.finditer(line):
                        # Get context (surrounding text)
                        start = max(0, match.start() - 30)
                        end = min(len(line), match.end() + 30)
                        context = line[start:end].strip()

                        claim = StatisticalClaim(
                            raw_text=match.group(0),
                            claim_type=claim_type,
                            value=match.group(1) if match.groups() else match.group(0),
                            context=context,
                            location=f"Line {line_num}",
                        )
                        claims.append(claim)

        # Deduplicate by raw_text
        seen = set()
        unique_claims = []
        for claim in claims:
            key = (claim.raw_text, claim.location)
            if key not in seen:
                seen.add(key)
                unique_claims.append(claim)

        return unique_claims

    def _verify_claim(
        self,
        claim: StatisticalClaim,
        inventory: Optional[InventoryResult],
    ):
        """Verify a single claim against available data."""
        # Check for explicit TODO/placeholder markers
        if any(marker in claim.context.lower() for marker in ['todo', 'placeholder', 'tbd', 'pending']):
            claim.status = VerificationStatus.PLACEHOLDER
            claim.notes = "Marked as placeholder in manuscript"
            return

        # Check suspicious patterns
        for pattern, message in self._suspicious_re:
            if pattern.search(claim.context):
                # Only flag if we don't have the relevant data
                if inventory:
                    if "survey" in message.lower() and not inventory.has_data_type(DataType.SURVEY):
                        claim.status = VerificationStatus.SUSPICIOUS
                        claim.notes = f"{message} - no survey data available"
                        return
                    elif "coding" in message.lower() and not self._has_coding_data(inventory):
                        claim.status = VerificationStatus.SUSPICIOUS
                        claim.notes = f"{message} - no coding/transcript data available"
                        return
                else:
                    claim.status = VerificationStatus.SUSPICIOUS
                    claim.notes = message
                    return

        # Check against inventory
        if inventory:
            self._check_against_inventory(claim, inventory)
        else:
            claim.status = VerificationStatus.UNVERIFIED
            claim.notes = "No data inventory provided"

    def _check_against_inventory(
        self,
        claim: StatisticalClaim,
        inventory: InventoryResult,
    ):
        """Check claim against data inventory."""
        # Map claim types to required data types
        type_requirements = {
            StatClaimType.SAMPLE_SIZE: [DataType.SPREADSHEET],
            StatClaimType.PERCENTAGE: [DataType.SPREADSHEET, DataType.SURVEY],
            StatClaimType.REGRESSION: [DataType.SPREADSHEET],
            StatClaimType.MEAN_SD: [DataType.SPREADSHEET, DataType.SURVEY],
            StatClaimType.RELIABILITY: [DataType.SURVEY, DataType.INTERVIEW],
            StatClaimType.COUNT: [DataType.SPREADSHEET, DataType.INTERVIEW],
            StatClaimType.EFFECT_SIZE: [DataType.SPREADSHEET],
            StatClaimType.TEMPORAL: [DataType.SPREADSHEET],
        }

        required_types = type_requirements.get(claim.claim_type, [DataType.SPREADSHEET])

        # Check if we have any of the required data types
        has_required = any(
            inventory.has_data_type(dt) for dt in required_types
        )

        if has_required:
            # We have potential source data
            sources = []
            for dt in required_types:
                sources.extend(inventory.get_files_by_type(dt))
            if sources:
                claim.data_source = sources[0].name
            claim.status = VerificationStatus.UNVERIFIED
            claim.notes = "Data source exists; manual verification needed"
        else:
            # No source data available
            claim.status = VerificationStatus.NO_DATA_SOURCE
            claim.notes = f"No data source for {claim.claim_type.value} claims"

    def _has_coding_data(self, inventory: InventoryResult) -> bool:
        """Check if inventory has interview/coding data."""
        return (
            inventory.has_data_type(DataType.INTERVIEW) or
            inventory.has_data_type(DataType.FIELDNOTES)
        )

    def flag_for_verification(
        self,
        text: str,
        inventory: Optional[InventoryResult] = None,
    ) -> list[str]:
        """
        Get a simple list of claims that need verification.

        This is a convenience method for quick checking.

        Args:
            text: Manuscript text
            inventory: Optional data inventory

        Returns:
            List of claim strings that need attention
        """
        report = self.validate(text, inventory)
        flagged = []

        for claim in report.claims:
            if claim.needs_attention:
                flagged.append(
                    f"[{claim.claim_type.value}] {claim.raw_text}\n"
                    f"  Location: {claim.location}\n"
                    f"  Status: {claim.status.value}\n"
                    f"  Notes: {claim.notes}"
                )

        return flagged


def validate_manuscript_statistics(
    text: str,
    data_path: Optional[str] = None,
) -> ValidationReport:
    """
    Convenience function to validate statistics in a manuscript.

    Args:
        text: The manuscript text
        data_path: Optional path to data directory

    Returns:
        ValidationReport
    """
    validator = StatisticsValidator()

    inventory = None
    if data_path:
        from .data_inventory import scan_paper_data
        inventory = scan_paper_data(data_path)

    return validator.validate(text, inventory)
