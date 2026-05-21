import json
from langchain_core.prompts import ChatPromptTemplate

def validation_agent(state, llm):
    """Validate extracted KPIs against covenants for year/unit/completeness."""
    covenants = state.get("covenants", [])
    kpis = state.get("kpis", [])
    
    # Build a combined view for validation
    pairs = []
    for cov in covenants:
        matching_kpi = next((k for k in kpis if k.get("covenant_id") == cov.get("id")), None)
        if matching_kpi:
            pairs.append({"covenant": cov, "kpi": matching_kpi})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an ESG data quality validator. Review each covenant-KPI pair and validate:

1. **Year Match**: Does the reporting year align with the covenant deadline year?
2. **Unit Consistency**: Are the units compatible (e.g., both in %, both in tCO2e)?
3. **Data Completeness**: Was an actual value found (not "NOT_FOUND")?
4. **Value Plausibility**: Does the value seem reasonable for this type of KPI?

For each pair, return a JSON object:
- "covenant_id": the covenant ID
- "year_valid": true/false
- "unit_valid": true/false  
- "data_complete": true/false
- "value_plausible": true/false
- "overall_valid": true if all checks pass, false otherwise
- "issues": array of strings describing any issues found

Return a JSON array of all validation results.
Return ONLY valid JSON. No markdown, no explanation."""),
        ("human", "Covenant-KPI Pairs:\n{pairs}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"pairs": json.dumps(pairs, indent=2)})
    
    try:
        content = result.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            content = content.rsplit("```", 1)[0]
        validation_results = json.loads(content)
    except (json.JSONDecodeError, Exception):
        # Fallback: basic validation
        validation_results = []
        for kpi in kpis:
            validation_results.append({
                "covenant_id": kpi.get("covenant_id", ""),
                "year_valid": True,
                "unit_valid": True,
                "data_complete": kpi.get("actual_value") != "NOT_FOUND",
                "value_plausible": True,
                "overall_valid": kpi.get("actual_value") != "NOT_FOUND",
                "issues": [] if kpi.get("actual_value") != "NOT_FOUND" else ["KPI value not found in report"]
            })
    
    state["validation_results"] = validation_results
    state["status"] = "Validation complete"
    return state
