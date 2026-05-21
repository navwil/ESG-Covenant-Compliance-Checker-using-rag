import json
from langchain_core.prompts import ChatPromptTemplate

def kpi_agent(state, llm, retriever):
    """Extract actual KPI values from ESG report using RAG."""
    covenants = state.get("covenants", [])
    kpis = []
    
    for cov in covenants:
        # Build a targeted query for this covenant
        query = f"""Find the actual value for: {cov.get('kpi_name', '')}
Looking for metrics related to: {cov.get('clause', '')}
Target year: {cov.get('deadline_year', '')}
Baseline year: {cov.get('baseline_year', 'not specified')}"""
        
        # Retrieve relevant chunks from ESG report
        docs = retriever.invoke(query)
        context = "\n\n".join([
            f"[Source: Page {doc.metadata.get('page_num', 'N/A')}]\n{doc.page_content}" 
            for doc in docs
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an ESG data extraction specialist. Extract the ACTUAL reported value for the requested KPI from the sustainability report context provided.

Return a JSON object with these exact fields:
- "covenant_id": the covenant ID provided
- "actual_value": the numerical value found (as a string, e.g., "12.5")
- "actual_unit": the unit of the value found (e.g., "%", "tCO2e", "MWh")
- "reporting_year": the year the value corresponds to
- "source_page": page number where the value was found
- "source_section": section name or heading where found
- "confidence": "HIGH", "MEDIUM", or "LOW" based on how clearly the value was stated
- "notes": any important context about the value
- "baseline_value": baseline value if found, else null

If the exact KPI cannot be found, set actual_value to "NOT_FOUND" and confidence to "LOW".
Return ONLY valid JSON. No markdown, no explanation."""),
            ("human", """Covenant: {covenant}

ESG Report Context:
{context}

Extract the actual KPI value for covenant {cov_id}.""")
        ])
        
        chain = prompt | llm
        result = chain.invoke({
            "covenant": json.dumps(cov),
            "context": context,
            "cov_id": cov.get("id", "")
        })
        
        try:
            content = result.content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1]
                content = content.rsplit("```", 1)[0]
            kpi_data = json.loads(content)
            kpi_data["covenant_id"] = cov.get("id", "")
            kpis.append(kpi_data)
        except (json.JSONDecodeError, Exception):
            kpis.append({
                "covenant_id": cov.get("id", ""),
                "actual_value": "NOT_FOUND",
                "actual_unit": "N/A",
                "reporting_year": "N/A",
                "source_page": "N/A",
                "source_section": "N/A",
                "confidence": "LOW",
                "notes": "Failed to extract KPI from report",
                "baseline_value": None
            })
    
    state["kpis"] = kpis
    state["status"] = f"Extracted {len(kpis)} KPIs"
    return state
