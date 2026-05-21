import json
from langchain_core.prompts import ChatPromptTemplate

def recommendation_agent(state, llm):
    """Generate remediation recommendations and calculate confidence score."""
    compliance_results = state.get("compliance_results", [])
    covenants = state.get("covenants", [])
    kpis = state.get("kpis", [])
    
    # Identify non-passing covenants
    failed_or_partial = [c for c in compliance_results if c.get("status") in ("FAIL", "PARTIAL")]
    
    recommendations = []
    
    if failed_or_partial:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an ESG remediation strategist for a banking institution. For each failed or partially met ESG covenant, provide actionable remediation recommendations.

For each item, return a JSON object:
- "covenant_id": the covenant ID
- "status": the compliance status (FAIL or PARTIAL)
- "gap_description": brief description of the gap
- "remediation_actions": array of 2-3 specific, actionable steps the borrower should take
- "priority": "HIGH" (for FAIL), "MEDIUM" (for PARTIAL), or "LOW"
- "estimated_timeline": estimated time to achieve compliance (e.g., "6-12 months")
- "risk_if_unaddressed": brief description of risk if not remediated

Be specific and practical. Reference industry best practices.
Return ONLY a valid JSON array. No markdown, no explanation."""),
            ("human", "Non-compliant covenants:\n{data}")
        ])
        
        chain = prompt | llm
        result = chain.invoke({"data": json.dumps(failed_or_partial, indent=2)})
        
        try:
            content = result.content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1]
                content = content.rsplit("```", 1)[0]
            recommendations = json.loads(content)
        except (json.JSONDecodeError, Exception):
            for item in failed_or_partial:
                recommendations.append({
                    "covenant_id": item.get("covenant_id", ""),
                    "status": item.get("status", "FAIL"),
                    "gap_description": item.get("gap", "Gap identified"),
                    "remediation_actions": ["Conduct detailed gap analysis", "Develop corrective action plan", "Engage ESG consultants"],
                    "priority": "HIGH" if item.get("status") == "FAIL" else "MEDIUM",
                    "estimated_timeline": "6-12 months",
                    "risk_if_unaddressed": "Potential loan covenant breach"
                })
    
    # Calculate confidence score
    total = len(compliance_results)
    if total == 0:
        confidence_score = 0
    else:
        passed = sum(1 for c in compliance_results if c.get("status") == "PASS")
        partial = sum(1 for c in compliance_results if c.get("status") == "PARTIAL")
        failed = sum(1 for c in compliance_results if c.get("status") == "FAIL")
        
        # Base score from pass rate
        base_score = (passed * 100 + partial * 50) / total
        
        # Data quality adjustment
        high_confidence_kpis = sum(1 for k in kpis if k.get("confidence") == "HIGH")
        data_quality_factor = high_confidence_kpis / max(len(kpis), 1)
        
        # Final score
        confidence_score = round(base_score * 0.8 + data_quality_factor * 20, 1)
        confidence_score = max(0, min(100, confidence_score))
    
    # Build final report
    final_report = {
        "confidence_score": confidence_score,
        "total_covenants": total,
        "passed": sum(1 for c in compliance_results if c.get("status") == "PASS"),
        "failed": sum(1 for c in compliance_results if c.get("status") == "FAIL"),
        "partial": sum(1 for c in compliance_results if c.get("status") == "PARTIAL"),
        "compliance_results": compliance_results,
        "recommendations": recommendations,
        "summary": f"ESG Compliance Assessment: {confidence_score}/100. "
                   f"{sum(1 for c in compliance_results if c.get('status') == 'PASS')}/{total} covenants fully met."
    }
    
    state["recommendations"] = recommendations
    state["confidence_score"] = confidence_score
    state["final_report"] = final_report
    state["status"] = "Assessment complete"
    return state
