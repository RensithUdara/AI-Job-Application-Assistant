"""
Download Report Component - Provides download functionality for analysis reports.
"""

import streamlit as st
import json
from typing import Dict
from core.report_generator import get_report_generator


def display_download_section(resume_data: Dict, jd_data: Dict, match_data: Dict):
    """Display download report section with multiple format options."""
    st.markdown("### 📥 Download Report")
    
    generator = get_report_generator()
    
    # Format selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Select Report Format:**")
        report_format = st.radio(
            "Choose format",
            ["📄 PDF", "📊 CSV", "📝 TXT", "🔧 JSON"],
            label_visibility="collapsed",
            horizontal=False
        )
    
    with col2:
        st.markdown("**Report Details:**")
        st.write(f"• Detected Role: {resume_data.get('role_compatibility', {}).get('best_match_role', 'Unknown')}")
        st.write(f"• Target Role: {jd_data.get('jd_role', 'Unknown')}")
        st.write(f"• Match Score: {match_data.get('match_score_overall', 0):.1f}%")
    
    st.markdown("---")
    
    # Download button
    format_mapping = {
        "📄 PDF": ("pdf", "application/pdf"),
        "📊 CSV": ("csv", "text/csv"),
        "📝 TXT": ("txt", "text/plain"),
        "🔧 JSON": ("json", "application/json")
    }
    
    file_ext, mime_type = format_mapping[report_format]
    
    # Generate report
    if report_format == "📄 PDF":
        report_content = generator.generate_pdf_report(resume_data, jd_data, match_data)
        file_name = f"job_match_report_{file_ext.upper()}.pdf"
    elif report_format == "📊 CSV":
        report_content = generator.generate_csv_report(resume_data, jd_data, match_data).encode('utf-8')
        file_name = f"job_match_report.csv"
    elif report_format == "📝 TXT":
        report_content = generator.generate_text_report(resume_data, jd_data, match_data).encode('utf-8')
        file_name = f"job_match_report.txt"
    else:  # JSON
        report_content = generator.generate_json_report(resume_data, jd_data, match_data).encode('utf-8')
        file_name = f"job_match_report.json"
    
    # Download button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.download_button(
            label=f"⬇️ Download {report_format}",
            data=report_content,
            file_name=file_name,
            mime=mime_type,
            use_container_width=True
        )
    
    with col2:
        if st.button("👁️ Preview", use_container_width=True):
            st.session_state.show_report_preview = True
    
    # Preview section
    if st.session_state.get('show_report_preview', False):
        st.markdown("---")
        st.markdown("### 📋 Report Preview")
        
        if report_format == "📝 TXT":
            st.text(generator.generate_text_report(resume_data, jd_data, match_data))
        elif report_format == "📊 CSV":
            st.code(generator.generate_csv_report(resume_data, jd_data, match_data), language="csv")
        elif report_format == "🔧 JSON":
            report_json = json.loads(generator.generate_json_report(resume_data, jd_data, match_data))
            st.json(report_json)
        else:
            st.info("PDF preview not available. Download the file to view.")
        
        if st.button("✕ Close Preview"):
            st.session_state.show_report_preview = False
            st.rerun()


def add_download_to_results():
    """Add download button to results section."""
    if st.session_state.get('analysis_done', False) and st.session_state.get('results', {}):
        results = st.session_state.results
        display_download_section(
            results.get('resume_data', {}),
            results.get('jd_data', {}),
            results.get('match_data', {})
        )
