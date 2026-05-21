from typing import TypedDict, Any


class ESGState(TypedDict):
    """State object for the LangGraph ESG compliance pipeline."""
    # Input paths
    loan_path: str
    report_path: str
    
    # Parsed text
    loan_text: str
    report_text: str
    report_pages: list
    
    # Pipeline outputs
    covenants: list          # Extracted covenant definitions
    kpis: list               # Extracted KPI actuals
    validation_results: list # Validation checks
    compliance_results: list # Pass/Fail/Partial per covenant
    recommendations: list    # Remediation actions
    confidence_score: float  # Overall score 0-100
    final_report: dict       # Complete structured report
    
    # Metadata
    status: str              # Current pipeline status
    errors: list             # Any errors encountered
