import json
from langchain_core.prompts import ChatPromptTemplate

def compliance_agent(state, llm):
    """Compare actual KPIs against covenant targets to determine Pass/Fail."""
    covenants = state.get("covenants", [])
    kpis = state.get("kpis", [])
    validation = state.get("validation_results", [])
    
    # Build comprehensive comparison data
    comparison_data = []
    for cov in covenants:
        kpi = next((k for k in kpis if k.get("covenant_id") == cov.get("id")), {})
        val = next((v for v in validation if v.get("covenant_id") == cov.get("id")), {})
        comparison_data.append({
            "covenant": cov,
            "actual_kpi": kpi,
            "validation": val
        })
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an ESG compliance officer at a major bank. Assess whether each covenant is met based on the actual KPI values extracted from the borrower's sustainability report.

For each covenant, determine:
- **PASS**: The borrower MEETS or EXCEEDS the covenant target
- **FAIL**: The borrower DOES NOT meet the covenant target  
- **PARTIAL**: The borrower shows progress but falls short, OR data quality issues prevent definitive assessment

Return a JSON array where each element has:
- "covenant_id": the covenant ID
- "kpi_name": the KPI being evaluated
- "target_value": the covenant target (with unit)
- "actual_value": the reported actual value (with unit)
- "status": "PASS", "FAIL", or "PARTIAL"
- "gap": description of the gap (e.g., "3% below target", "Exceeds by 5%")
- "reporting_year": year the actual data is from
- "source_page": page reference from the ESG report
- "reasoning": 1-2 sentence explanation of the determination

Be rigorous and precise. If data is missing or unreliable, mark as PARTIAL.
Return ONLY valid JSON. No markdown, no explanation."""),
        ("human", "Compliance Assessment Data:\n{data}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"data": json.dumps(comparison_data, indent=2)})
    
    try:
        content = result.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            content = content.rsplit("```", 1)[0]
        compliance_results = json.loads(content)
    except (json.JSONDecodeError, Exception):
        compliance_results = []
        for cov in covenants:
            compliance_results.append({
                "covenant_id": cov.get("id", ""),
                "kpi_name": cov.get("kpi_name", ""),
                "target_value": f"{cov.get('target_value', 'N/A')} {cov.get('target_unit', '')}",
                "actual_value": "Unable to assess",
                "status": "PARTIAL",
                "gap": "Assessment failed",
                "reporting_year": "N/A",
                "source_page": "N/A",
                "reasoning": "Automated assessment encountered an error."
            })
    
    state["compliance_results"] = compliance_results
    state["status"] = "Compliance assessment complete"
    return state
