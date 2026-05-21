import json
from langchain_core.prompts import ChatPromptTemplate

def covenant_agent(state, llm):
    """Extract ESG covenants from loan agreement using LLM."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert ESG compliance analyst specializing in green loan agreements.
Extract ALL ESG covenants from the loan agreement text below.

For each covenant, return a JSON object with these exact fields:
- "id": sequential identifier like "COV-1", "COV-2", etc.
- "kpi_name": the specific ESG metric (e.g., "Scope 2 GHG Emissions", "Renewable Energy Usage")
- "target_value": the numerical target (e.g., "15", "30", "10000")
- "target_unit": the unit of measurement (e.g., "%", "tCO2e", "MWh", "% reduction")
- "deadline_year": the target year (e.g., "FY2026", "2025")
- "clause": the full clause or requirement text (e.g., "Reduce Scope 2 emissions by 15% compared to FY2023 baseline")
- "direction": "decrease" or "increase" or "maintain" - whether the KPI should go up or down
- "baseline_year": baseline year if mentioned, else null
- "category": one of "Environmental", "Social", "Governance"

Return ONLY a valid JSON array. No markdown, no explanation."""),
        ("human", "Loan Agreement Text:\n\n{loan_text}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"loan_text": state["loan_text"]})
    
    # Parse the JSON response
    try:
        content = result.content.strip()
        # Handle markdown code blocks if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            content = content.rsplit("```", 1)[0]
        covenants = json.loads(content)
    except (json.JSONDecodeError, Exception) as e:
        covenants = []
        state["errors"] = state.get("errors", []) + [f"Covenant extraction failed: {str(e)}"]
    
    state["covenants"] = covenants
    state["status"] = f"Extracted {len(covenants)} covenants"
    return state
