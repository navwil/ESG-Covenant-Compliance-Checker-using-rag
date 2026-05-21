from functools import partial

from langgraph.graph import StateGraph, END

from models.state import ESGState
from agents.parser_agent import parser_agent
from agents.covenant_agent import covenant_agent
from agents.kpi_agent import kpi_agent
from agents.validation_agent import validation_agent
from agents.compliance_agent import compliance_agent
from agents.recommendation_agent import recommendation_agent


def build_graph(llm, retriever):
    """
    Build the LangGraph workflow for ESG compliance analysis.
    
    The pipeline flows:
    parser → covenant_extraction → kpi_extraction → validation → compliance → recommendation
    
    Args:
        llm: ChatOpenAI instance for GPT-4o
        retriever: ChromaDB retriever for RAG
    
    Returns:
        Compiled LangGraph workflow
    """
    graph = StateGraph(ESGState)

    # Bind LLM and retriever to agent functions using partial
    covenant_node = partial(covenant_agent, llm=llm)
    kpi_node = partial(kpi_agent, llm=llm, retriever=retriever)
    validation_node = partial(validation_agent, llm=llm)
    compliance_node = partial(compliance_agent, llm=llm)
    recommendation_node = partial(recommendation_agent, llm=llm)

    # Add all nodes
    graph.add_node("parser", parser_agent)
    graph.add_node("covenant_extraction", covenant_node)
    graph.add_node("kpi_extraction", kpi_node)
    graph.add_node("validation", validation_node)
    graph.add_node("compliance", compliance_node)
    graph.add_node("recommendation", recommendation_node)

    # Define the linear pipeline
    graph.set_entry_point("parser")
    graph.add_edge("parser", "covenant_extraction")
    graph.add_edge("covenant_extraction", "kpi_extraction")
    graph.add_edge("kpi_extraction", "validation")
    graph.add_edge("validation", "compliance")
    graph.add_edge("compliance", "recommendation")
    graph.add_edge("recommendation", END)

    return graph.compile()
