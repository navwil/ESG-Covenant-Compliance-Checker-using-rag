import os
import sys
import json
import tempfile
import shutil
import time
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import streamlit.components.v1 as components
from utils.text_sanitizer import (
    streamline_text,
    sanitize_documents
)
# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------------------------------
# Environment & SSL setup (must happen before any LangChain imports)
# ---------------------------------------------------------------------------
from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

from utils.ssl_fix import http_client

import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from utils.pdf_parser import extract_text_with_pages
from utils.vector_store import build_vector_store
from graph.workflow import build_graph

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ESG Covenant Compliance Checker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# CUSTOM CSS — Premium Dark Theme with Glassmorphism
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #0f4c3a 0%, #1a6b4f 30%, #0d7a5f 60%, #0a9d6e 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(10, 157, 110, 0.25);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: rgba(255,255,255,0.85);
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    /* Glass card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(10, 157, 110, 0.4);
        box-shadow: 0 4px 24px rgba(10, 157, 110, 0.15);
    }

    /* Pipeline steps */
    .pipeline-container {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        padding: 1rem 0;
    }
    .pipeline-step {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .pipeline-step.active {
        background: linear-gradient(135deg, #0a9d6e, #0d7a5f);
        color: white;
        border-color: #0a9d6e;
        animation: pulse 1.5s infinite;
    }
    .pipeline-step.done {
        background: rgba(10, 157, 110, 0.2);
        color: #4ade80;
        border-color: rgba(74, 222, 128, 0.3);
    }
    .pipeline-step.waiting {
        background: rgba(255,255,255,0.03);
        color: rgba(255,255,255,0.4);
    }
    .pipeline-arrow {
        color: rgba(255,255,255,0.3);
        font-size: 1.2rem;
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(10, 157, 110, 0.4); }
        50% { box-shadow: 0 0 0 8px rgba(10, 157, 110, 0); }
    }

    /* Score gauge */
    .score-container {
        text-align: center;
        padding: 2rem;
    }
    .score-value {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    .score-label {
        font-size: 1rem;
        color: rgba(255,255,255,0.6);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 500;
    }
    .score-high { color: #4ade80; }
    .score-medium { color: #fbbf24; }
    .score-low { color: #f87171; }

    /* Status badges */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-pass {
        background: rgba(74, 222, 128, 0.15);
        color: #4ade80;
        border: 1px solid rgba(74, 222, 128, 0.3);
    }
    .badge-fail {
        background: rgba(248, 113, 113, 0.15);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.3);
    }
    .badge-partial {
        background: rgba(251, 191, 36, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }

    /* Stat cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .stat-label {
        font-size: 0.8rem;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Remediation cards */
    .remediation-card {
        background: rgba(248, 113, 113, 0.05);
        border: 1px solid rgba(248, 113, 113, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #f87171;
    }
    .remediation-card.medium {
        background: rgba(251, 191, 36, 0.05);
        border-color: rgba(251, 191, 36, 0.2);
        border-left-color: #fbbf24;
    }

    /* Upload area styling */
    .upload-area {
        border: 2px dashed rgba(10, 157, 110, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .upload-area:hover {
        border-color: rgba(10, 157, 110, 0.6);
        background: rgba(10, 157, 110, 0.05);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(15, 25, 35, 0.95);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0a9d6e 0%, #0d7a5f 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(10, 157, 110, 0.4);
        transform: translateY(-2px);
    }

    /* Divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(10, 157, 110, 0.3), transparent);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🌱 ESG Covenant Compliance Checker</h1>
    <p>Automated ESG covenant verification for Green Loans & Sustainability-Linked Loans — powered by GenAI Agents</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# SIDEBAR — Pipeline Info
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔬 Analysis Pipeline")
    st.markdown("""
    <div style="padding: 0.5rem 0;">
        <div style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.06);">
            <span style="font-size: 1.3rem;">📄</span>
            <div>
                <div style="font-weight: 600; font-size: 0.9rem;">1. Document Parser</div>
                <div style="color: rgba(255,255,255,0.45); font-size: 0.75rem;">Extract text from PDFs</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.06);">
            <span style="font-size: 1.3rem;">📜</span>
            <div>
                <div style="font-weight: 600; font-size: 0.9rem;">2. Covenant Extractor</div>
                <div style="color: rgba(255,255,255,0.45); font-size: 0.75rem;">Identify ESG covenants</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.06);">
            <span style="font-size: 1.3rem;">📊</span>
            <div>
                <div style="font-weight: 600; font-size: 0.9rem;">3. KPI Extractor (RAG)</div>
                <div style="color: rgba(255,255,255,0.45); font-size: 0.75rem;">Retrieve actual metrics</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.06);">
            <span style="font-size: 1.3rem;">✅</span>
            <div>
                <div style="font-weight: 600; font-size: 0.9rem;">4. Data Validator</div>
                <div style="color: rgba(255,255,255,0.45); font-size: 0.75rem;">Check data quality</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.06);">
            <span style="font-size: 1.3rem;">⚖️</span>
            <div>
                <div style="font-weight: 600; font-size: 0.9rem;">5. Compliance Assessor</div>
                <div style="color: rgba(255,255,255,0.45); font-size: 0.75rem;">Determine Pass/Fail</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0;">
            <span style="font-size: 1.3rem;">💡</span>
            <div>
                <div style="font-weight: 600; font-size: 0.9rem;">6. Remediation Advisor</div>
                <div style="color: rgba(255,255,255,0.45); font-size: 0.75rem;">Generate recommendations</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Configuration")
    st.markdown(f"""
    - **LLM**: `{os.getenv('LLM_MODEL', 'N/A')}`
    - **Embeddings**: `{os.getenv('EMBED_MODEL', 'N/A')}`
    - **Vector Store**: ChromaDB
    - **Framework**: LangGraph
    """)


# ---------------------------------------------------------------------------
# UPLOAD SECTION
# ---------------------------------------------------------------------------
st.markdown("### 📂 Upload Documents")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h4 style="margin-top:0;">📘 Loan Agreement</h4>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">
            Green Loan / SLL Agreement with ESG covenants
        </p>
    </div>
    """, unsafe_allow_html=True)
    loan_file = st.file_uploader(
        "Upload Loan Agreement PDF",
        type=["pdf"],
        key="loan_upload",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("""
    <div class="glass-card">
        <h4 style="margin-top:0;">📗 ESG Report</h4>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">
            Annual Sustainability Report (GRI/SASB)
        </p>
    </div>
    """, unsafe_allow_html=True)
    report_file = st.file_uploader(
        "Upload ESG Report PDF",
        type=["pdf"],
        key="report_upload",
        label_visibility="collapsed"
    )

# Upload status
col1, col2 = st.columns(2)
with col1:
    if loan_file:
        st.success(f"✅ {loan_file.name} uploaded")
    else:
        st.info("⏳ Awaiting Loan Agreement PDF")
with col2:
    if report_file:
        st.success(f"✅ {report_file.name} uploaded")
    else:
        st.info("⏳ Awaiting ESG Report PDF")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ANALYSIS BUTTON
# ---------------------------------------------------------------------------
analyze_btn = st.button("🚀 Run ESG Compliance Analysis", use_container_width=True)


# ---------------------------------------------------------------------------
# PIPELINE PROGRESS HELPER
# ---------------------------------------------------------------------------
PIPELINE_STEPS = [
    ("📄", "Parsing Documents"),
    ("📜", "Extracting Covenants"),
    ("📊", "Extracting KPIs"),
    ("✅", "Validating Data"),
    ("⚖️", "Assessing Compliance"),
    ("💡", "Generating Recommendations"),
]

def render_pipeline_progress(current_step: int):
    """Render the pipeline progress indicator."""
    html_parts = ['<div class="pipeline-container">']
    for i, (icon, label) in enumerate(PIPELINE_STEPS):
        if i < current_step:
            cls = "done"
        elif i == current_step:
            cls = "active"
        else:
            cls = "waiting"
        html_parts.append(f'<div class="pipeline-step {cls}">{icon} {label}</div>')
        if i < len(PIPELINE_STEPS) - 1:
            html_parts.append('<span class="pipeline-arrow">→</span>')
    html_parts.append('</div>')
    return "".join(html_parts)


# ---------------------------------------------------------------------------
# RESULTS RENDERING
# ---------------------------------------------------------------------------
def render_score_gauge(score: float):
    """Render the confidence score gauge."""
    if score >= 70:
        color_class = "score-high"
        label = "Strong Compliance"
    elif score >= 40:
        color_class = "score-medium"
        label = "Partial Compliance"
    else:
        color_class = "score-low"
        label = "Weak Compliance"

    return f"""
    <div class="score-container">
        <div class="score-value {color_class}">{score:.0f}</div>
        <div class="score-label">{label}</div>
        <div style="color: rgba(255,255,255,0.4); font-size: 0.85rem; margin-top: 0.5rem;">
            ESG Compliance Confidence Score (0-100)
        </div>
    </div>
    """


def render_status_badge(status: str) -> str:
    """Render a colored status badge."""
    status_upper = status.upper()
    if status_upper == "PASS":
        return '<span class="badge badge-pass">✓ PASS</span>'
    elif status_upper == "FAIL":
        return '<span class="badge badge-fail">✗ FAIL</span>'
    else:
        return '<span class="badge badge-partial">◐ PARTIAL</span>'


def render_covenant_table(compliance_results: list):
    """Render the covenant scorecard table."""
    if not compliance_results:
        st.warning("No compliance results to display.")
        return

    table_html = """
    <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
        <thead>
            <tr style="border-bottom: 2px solid rgba(255,255,255,0.15);">
                <th style="padding: 0.8rem 0.5rem; text-align: left; color: rgba(255,255,255,0.6);">Covenant</th>
                <th style="padding: 0.8rem 0.5rem; text-align: left; color: rgba(255,255,255,0.6);">KPI</th>
                <th style="padding: 0.8rem 0.5rem; text-align: center; color: rgba(255,255,255,0.6);">Target</th>
                <th style="padding: 0.8rem 0.5rem; text-align: center; color: rgba(255,255,255,0.6);">Actual</th>
                <th style="padding: 0.8rem 0.5rem; text-align: center; color: rgba(255,255,255,0.6);">Year</th>
                <th style="padding: 0.8rem 0.5rem; text-align: center; color: rgba(255,255,255,0.6);">Source</th>
                <th style="padding: 0.8rem 0.5rem; text-align: center; color: rgba(255,255,255,0.6);">Status</th>
            </tr>
        </thead>
        <tbody>
    """

    for item in compliance_results:
        badge = render_status_badge(item.get("status", "PARTIAL"))
        table_html += f"""
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
            <td style="padding: 0.7rem 0.5rem; font-weight: 500;">{item.get('covenant_id', 'N/A')}</td>
            <td style="padding: 0.7rem 0.5rem;">{item.get('kpi_name', 'N/A')}</td>
            <td style="padding: 0.7rem 0.5rem; text-align: center;">{item.get('target_value', 'N/A')}</td>
            <td style="padding: 0.7rem 0.5rem; text-align: center;">{item.get('actual_value', 'N/A')}</td>
            <td style="padding: 0.7rem 0.5rem; text-align: center;">{item.get('reporting_year', 'N/A')}</td>
            <td style="padding: 0.7rem 0.5rem; text-align: center;">Page {item.get('source_page', 'N/A')}</td>
            <td style="padding: 0.7rem 0.5rem; text-align: center;">{badge}</td>
        </tr>
        """

    table_html += "</tbody></table>"
    components.html(table_html, height=500, scrolling=True)


    


def render_remediation_cards(recommendations: list):
    """Render remediation recommendation cards."""
    if not recommendations:
        st.success("🎉 No remediation needed — all covenants passed!")
        return

    for rec in recommendations:
        priority = rec.get("priority", "MEDIUM")
        card_class = "medium" if priority == "MEDIUM" else ""
        priority_color = "#f87171" if priority == "HIGH" else "#fbbf24" if priority == "MEDIUM" else "#4ade80"

        actions_html = ""
        for action in rec.get("remediation_actions", []):
            actions_html += f'<li style="margin-bottom: 0.3rem;">{action}</li>'

        st.markdown(f"""
        <div class="remediation-card {card_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong>{rec.get('covenant_id', 'N/A')} — {rec.get('status', 'FAIL')}</strong>
                <span style="color: {priority_color}; font-weight: 600; font-size: 0.8rem;">
                    ● {priority} PRIORITY
                </span>
            </div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-bottom: 0.5rem;">
                {rec.get('gap_description', 'Gap identified in covenant compliance.')}
            </div>
            <div style="font-size: 0.85rem;">
                <strong>Recommended Actions:</strong>
                <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                    {actions_html}
                </ul>
            </div>
            <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem; margin-top: 0.5rem;">
                ⏱️ Timeline: {rec.get('estimated_timeline', 'TBD')} &nbsp;|&nbsp;
                ⚠️ Risk: {rec.get('risk_if_unaddressed', 'Potential covenant breach')}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------------------------
if analyze_btn:
    if loan_file is None:
        st.error("❌ Please upload the Loan Agreement PDF")
        st.stop()
    if report_file is None:
        st.error("❌ Please upload the ESG Report PDF")
        st.stop()

    # Create temp directory for uploaded files
    tmp_dir = tempfile.mkdtemp()
    loan_path = os.path.join(tmp_dir, "loan.pdf")
    report_path = os.path.join(tmp_dir, "report.pdf")

    with open(loan_path, "wb") as f:
        f.write(loan_file.read())
    with open(report_path, "wb") as f:
        f.write(report_file.read())

    # Pipeline progress placeholder
    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    try:
        # Step 0: Initialize models
        progress_placeholder.markdown(render_pipeline_progress(0), unsafe_allow_html=True)
        status_placeholder.info("🔧 Initializing AI models...")

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

        # Step 1: Parse documents & build vector store
        progress_placeholder.markdown(render_pipeline_progress(0), unsafe_allow_html=True)
        status_placeholder.info("📄 Parsing documents and building vector store...")

        report_pages = extract_text_with_pages(report_path)

        # Place Chroma in the unique temp directory to avoid WinError 32 file locks
        chroma_dir = os.path.join(tmp_dir, "chroma_db")
        vectordb = build_vector_store(report_pages, embedding, persist_dir=chroma_dir)
        
        retriever = vectordb.as_retriever(search_kwargs={"k": 5})

        # Step 2: Build and run the graph
        status_placeholder.info("🔗 Building LangGraph pipeline...")
        workflow = build_graph(llm, retriever)

        # Initial state
        initial_state = {
            "loan_path": loan_path,
            "report_path": report_path,
            "loan_text": "",
            "report_text": "",
            "report_pages": report_pages, # Ensure pages are passed to state
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

        # Run the pipeline with progress updates
        step_names = {
            "parser": 0,
            "covenant_extraction": 1,
            "kpi_extraction": 2,
            "validation": 3,
            "compliance": 4,
            "recommendation": 5,
        }

        # Stream through the graph to show progress
        final_state = initial_state.copy() # Copy initial state
        
        for event in workflow.stream(initial_state):
            for node_name, node_output in event.items():
                step_idx = step_names.get(node_name, 0)
                progress_placeholder.markdown(
                    render_pipeline_progress(step_idx + 1),
                    unsafe_allow_html=True
                )
                status_placeholder.info(
                    f"{PIPELINE_STEPS[step_idx][0]} {PIPELINE_STEPS[step_idx][1]}... ✓ Complete"
                )
                
                # Accumulate state safely
                final_state.update(node_output) 

        # Clear progress indicators
        progress_placeholder.markdown(
            render_pipeline_progress(len(PIPELINE_STEPS)),
            unsafe_allow_html=True
        )
        status_placeholder.success("✅ Analysis complete!")

        if final_state is None:
            st.error("Pipeline returned no results.")
            st.stop()

        final_report = final_state.get("final_report", {})
        compliance_results = final_report.get("compliance_results", [])
        recommendations = final_report.get("recommendations", [])
        confidence_score = final_report.get("confidence_score", 0)

        # ---------------------------------------------------------------
        # RESULTS DASHBOARD
        # ---------------------------------------------------------------
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("## 📊 Compliance Dashboard")

        # Score & Stats Row
        score_col, stats_col = st.columns([1, 2])

        with score_col:
            st.markdown(render_score_gauge(confidence_score), unsafe_allow_html=True)

        with stats_col:
            total = final_report.get("total_covenants", 0)
            passed = final_report.get("passed", 0)
            failed = final_report.get("failed", 0)
            partial = final_report.get("partial", 0)

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number" style="color: #60a5fa;">{total}</div>
                    <div class="stat-label">Total Covenants</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number" style="color: #4ade80;">{passed}</div>
                    <div class="stat-label">Passed</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number" style="color: #f87171;">{failed}</div>
                    <div class="stat-label">Failed</div>
                </div>
                """, unsafe_allow_html=True)
            with c4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number" style="color: #fbbf24;">{partial}</div>
                    <div class="stat-label">Partial</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # Covenant Scorecard Table
        st.markdown("### 📋 Covenant-by-Covenant Scorecard")
        render_covenant_table(compliance_results)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # Remediation Recommendations
        st.markdown("### 💡 Remediation Recommendations")
        render_remediation_cards(recommendations)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # Detailed Compliance Reasoning (expandable)
        st.markdown("### 🔍 Detailed Reasoning")
        for item in compliance_results:
            with st.expander(
                f"{item.get('covenant_id', 'N/A')} — {item.get('kpi_name', 'N/A')} — {item.get('status', 'N/A')}"
            ):
                st.markdown(f"""
                **KPI Evaluated:** {item.get('kpi_name', 'N/A')}

                **Target:** {item.get('target_value', 'N/A')}

                **Actual:** {item.get('actual_value', 'N/A')}

                **Gap:** {item.get('gap', 'N/A')}

                **Reporting Year:** {item.get('reporting_year', 'N/A')}

                **Source:** Page {item.get('source_page', 'N/A')}

                **Reasoning:** {item.get('reasoning', 'N/A')}
                """)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # Export JSON
        st.markdown("### 📥 Export Results")
        col_export1, col_export2 = st.columns(2)
        with col_export1:
            st.download_button(
                label="📄 Download Full Report (JSON)",
                data=json.dumps(final_report, indent=2, default=str),
                file_name="esg_compliance_report.json",
                mime="application/json",
                use_container_width=True,
            )
        with col_export2:
            # Summary text export
            summary_text = f"""ESG COVENANT COMPLIANCE REPORT
{'='*50}
Confidence Score: {confidence_score}/100
Total Covenants: {total}
Passed: {passed} | Failed: {failed} | Partial: {partial}
{'='*50}

COVENANT SCORECARD:
"""
            for item in compliance_results:
                status_icon = "✓" if item.get("status") == "PASS" else "✗" if item.get("status") == "FAIL" else "◐"
                summary_text += f"\n{status_icon} {item.get('covenant_id', 'N/A')} - {item.get('kpi_name', 'N/A')}"
                summary_text += f"\n  Target: {item.get('target_value', 'N/A')} | Actual: {item.get('actual_value', 'N/A')}"
                summary_text += f"\n  Status: {item.get('status', 'N/A')} | {item.get('reasoning', '')}\n"

            st.download_button(
                label="📝 Download Summary (TXT)",
                data=summary_text,
                file_name="esg_compliance_summary.txt",
                mime="text/plain",
                use_container_width=True,
            )

    except Exception as e:
        st.error(f"❌ Pipeline error: {str(e)}")
        st.exception(e)

    finally:
        # Cleanup temp files
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)