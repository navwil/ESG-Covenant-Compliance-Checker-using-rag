import logging
from utils.pdf_parser import extract_text_with_pages

logger = logging.getLogger(__name__)

def parser_agent(state: dict):
    """
    LangGraph node to parse the uploaded PDFs into text.
    Reads from the file paths in the state and outputs compiled text and pages.
    """
    logger.info("Executing parser_agent...")
    
    loan_path = state.get("loan_path")
    report_path = state.get("report_path")
    
    if not loan_path or not report_path:
        return {"errors": ["Missing file paths for loan or report documents."]}

    try:
        # Extract and sanitize pages
        loan_pages = extract_text_with_pages(loan_path)
        report_pages = extract_text_with_pages(report_path)
        
        # Compile full text with page markers for LLM context
        # FIX: Changed 'page' to 'page_num' to match pdf_parser.py
        loan_text = "\n".join([f"[Page {p.get('page_num', '?')}]\n{p.get('text', '')}" for p in loan_pages])
        report_text = "\n".join([f"[Page {p.get('page_num', '?')}]\n{p.get('text', '')}" for p in report_pages])
        
        return {
            "loan_text": loan_text,
            "report_text": report_text,
            "report_pages": report_pages,
            "status": "Documents parsed and sanitized successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in parser_agent: {str(e)}")
        return {
            "errors": [f"Parser Agent failed: {str(e)}"],
            "status": "Failed during parsing"
        }