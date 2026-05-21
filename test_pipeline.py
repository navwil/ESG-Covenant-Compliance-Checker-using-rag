import os
import sys
import json
import shutil
from dotenv import load_dotenv

# Path setup
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Load environment variables
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

print("API_KEY:", os.getenv("API_KEY"))
print("BASE_URL:", os.getenv("BASE_URL"))
print("LLM_MODEL:", os.getenv("LLM_MODEL"))
print("EMBED_MODEL:", os.getenv("EMBED_MODEL"))

from utils.ssl_fix import http_client
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from utils.pdf_parser import extract_text_with_pages
from utils.vector_store import build_vector_store
from graph.workflow import build_graph

def main():
    loan_path = os.path.join(PROJECT_ROOT, "samples", "sample_loan_agreement.pdf")
    report_path = os.path.join(PROJECT_ROOT, "samples", "sample_esg_report.pdf")

    print("\n--- Step 1: Initializing models ---")
    llm = ChatOpenAI(
        base_url=os.getenv("BASE_URL"),
        model=os.getenv("LLM_MODEL"),
        api_key=os.getenv("API_KEY"),
        http_client=http_client,
        temperature=0.1,
        max_tokens=4096,
    )

    embedding = OpenAIEmbeddings(
        base_url=os.getenv("BASE_URL"),
        model=os.getenv("EMBED_MODEL"),
        api_key=os.getenv("API_KEY"),
        http_client=http_client,
    )

    print("Models initialized successfully.")

    print("\n--- Step 2: Extracting text from ESG Report and building Vector Store ---")
    report_pages = extract_text_with_pages(report_path)
    print(f"Extracted {len(report_pages)} pages from ESG report.")

    chroma_dir = os.path.join(PROJECT_ROOT, "chroma_db_test")
    if os.path.exists(chroma_dir):
        shutil.rmtree(chroma_dir)

    vectordb = build_vector_store(report_pages, embedding, persist_dir=chroma_dir)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    print("Vector store built and retriever initialized.")

    print("\n--- Step 3: Compiling LangGraph Workflow ---")
    workflow = build_graph(llm, retriever)
    print("Workflow compiled.")

    # Initial state
    initial_state = {
        "loan_path": loan_path,
        "report_path": report_path,
        "loan_text": "",
        "report_text": "",
        "report_pages": report_pages,
        "covenants": [],
        "kpis": [],
        "validation_results": [],
        "compliance_results": [],
        "recommendations": [],
        "confidence_score": 0.0,
        "final_report": {},
        "status": "initialized",
        "errors": [],
    }

    print("\n--- Step 4: Running Workflow ---")
    try:
        # Create a copy to accumulate state correctly
        final_state = initial_state.copy()
        
        for event in workflow.stream(initial_state):
            for node_name, node_output in event.items():
                print(f"[{node_name}] status: {node_output.get('status')}")
                if node_output.get("errors"):
                    print(f"[{node_name}] errors: {node_output.get('errors')}")
                
                # Update the state instead of overwriting it
                final_state.update(node_output)

        print("\n--- Step 5: Final Report Output ---")
        final_report = final_state.get("final_report", {})
        print(json.dumps(final_report, indent=2))
        
        # Check if we have outputs
        if final_report:
            print("\n[SUCCESS] End-to-end pipeline check PASSED!")
        else:
            print("\n[FAILED] Pipeline completed but final_report is empty.")
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()