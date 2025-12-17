"""
Report Generator - Generate downloadable analysis reports in multiple formats.
"""

from datetime import datetime
from typing import Dict, List
import csv
import io


class ReportGenerator:
    """Generate analysis reports in various formats."""
    
    def __init__(self):
        """Initialize report generator."""
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_pdf_report(self, resume_data: Dict, jd_data: Dict, match_data: Dict) -> bytes:
        """
        Generate PDF report (requires reportlab).
        Falls back to text if PDF not available.
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            
            # Create PDF
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=30,
                alignment=1  # Center
            )
            elements.append(Paragraph("📊 Application Match Analysis Report", title_style))
            elements.append(Spacer(1, 0.3*inch))
            
            # Overall Match Score
            match_score = match_data.get('match_score_overall', 0)
            elements.append(Paragraph(f"<b>Overall Match Score: {match_score:.1f}%</b>", styles['Heading2']))
            elements.append(Spacer(1, 0.2*inch))
            
            # Key Metrics
            metrics_data = [
                ['Metric', 'Value'],
                ['Detected Role', resume_data.get('role_compatibility', {}).get('best_match_role', 'Unknown')],
                ['Target Role', jd_data.get('jd_role', 'Unknown')],
                ['Resume Quality', f"{resume_data.get('quality_score', 0):.0f}/100"],
                ['Skills Match', f"{match_data.get('skill_match', {}).get('match_percentage', 0):.1f}%"],
                ['ATS Score', f"{resume_data.get('ats_analysis', {}).get('score', 0):.0f}/100"],
                ['Experience Level', jd_data.get('seniority', 'Not specified')],
            ]
            
            metrics_table = Table(metrics_data)
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(metrics_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Skills Analysis
            elements.append(Paragraph("<b>Skills Analysis</b>", styles['Heading2']))
            matched_skills = match_data.get('matched_skills', [])
            missing_skills = match_data.get('missing_skills', [])
            
            elements.append(Paragraph(f"<b>Matched Skills ({len(matched_skills)}):</b>", styles['Normal']))
            if matched_skills:
                for skill in matched_skills[:10]:
                    elements.append(Paragraph(f"• {skill}", styles['Normal']))
            
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(f"<b>Missing Skills ({len(missing_skills)}):</b>", styles['Normal']))
            if missing_skills:
                for skill in missing_skills[:10]:
                    elements.append(Paragraph(f"• {skill}", styles['Normal']))
            
            # Build PDF
            doc.build(elements)
            pdf_buffer.seek(0)
            return pdf_buffer.getvalue()
            
        except ImportError:
            # Fallback to text report
            return self.generate_text_report(resume_data, jd_data, match_data).encode('utf-8')
    
    def generate_csv_report(self, resume_data: Dict, jd_data: Dict, match_data: Dict) -> str:
        """Generate CSV report."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['AI Job Application Assistant - Analysis Report'])
        writer.writerow(['Generated:', self.timestamp])
        writer.writerow([])
        
        # Overall Metrics
        writer.writerow(['OVERALL MATCH SUMMARY'])
        writer.writerow(['Metric', 'Value'])
        match_score = match_data.get('match_score_overall', 0)
        writer.writerow(['Overall Match Score', f"{match_score:.1f}%"])
        writer.writerow(['Detected Role', resume_data.get('role_compatibility', {}).get('best_match_role', 'Unknown')])
        writer.writerow(['Target Role', jd_data.get('jd_role', 'Unknown')])
        writer.writerow(['Resume Quality', f"{resume_data.get('quality_score', 0):.0f}/100"])
        writer.writerow(['Skills Match %', f"{match_data.get('skill_match', {}).get('match_percentage', 0):.1f}%"])
        writer.writerow(['ATS Score', f"{resume_data.get('ats_analysis', {}).get('score', 0):.0f}/100"])
        writer.writerow(['Experience Level', jd_data.get('seniority', 'Not specified')])
        writer.writerow([])
        
        # Skills Analysis
        writer.writerow(['SKILLS ANALYSIS'])
        matched_skills = match_data.get('matched_skills', [])
        missing_skills = match_data.get('missing_skills', [])
        critical_missing = match_data.get('priority_analysis', {}).get('critical_missing', [])
        
        writer.writerow(['Total Required Skills', len(jd_data.get('all_jd_skills_list', []))])
        writer.writerow(['Matched Skills', len(matched_skills)])
        writer.writerow(['Missing Skills', len(missing_skills)])
        writer.writerow(['Critical Gaps', len(critical_missing)])
        writer.writerow([])
        
        # Matched Skills
        writer.writerow(['MATCHED SKILLS'])
        for skill in matched_skills:
            writer.writerow([skill])
        writer.writerow([])
        
        # Missing Skills
        writer.writerow(['MISSING SKILLS'])
        for skill in missing_skills:
            writer.writerow([skill])
        writer.writerow([])
        
        # Critical Missing
        writer.writerow(['CRITICAL MISSING SKILLS'])
        for skill in critical_missing:
            writer.writerow([skill])
        writer.writerow([])
        
        # Market Analysis
        market_analysis = match_data.get('market_analysis', {})
        writer.writerow(['MARKET ANALYSIS'])
        writer.writerow(['Market Position', market_analysis.get('market_position', 'Unknown')])
        writer.writerow(['Salary Range', market_analysis.get('salary_range', 'Not available')])
        writer.writerow(['Demand Level', market_analysis.get('demand_level', 'Medium')])
        writer.writerow(['Competitiveness', f"{market_analysis.get('competitiveness_score', 0):.0f}%"])
        writer.writerow([])
        
        # Strengths
        writer.writerow(['KEY STRENGTHS'])
        for strength in market_analysis.get('strengths', []):
            writer.writerow([strength])
        writer.writerow([])
        
        # Improvement Areas
        writer.writerow(['AREAS FOR IMPROVEMENT'])
        for improvement in market_analysis.get('improvement_areas', []):
            writer.writerow([improvement])
        
        return output.getvalue()
    
    def generate_text_report(self, resume_data: Dict, jd_data: Dict, match_data: Dict) -> str:
        """Generate plain text report."""
        report = []
        report.append("=" * 80)
        report.append("AI JOB APPLICATION ASSISTANT - ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: {self.timestamp}\n")
        
        # Overall Summary
        report.append("OVERALL MATCH SUMMARY")
        report.append("-" * 40)
        match_score = match_data.get('match_score_overall', 0)
        report.append(f"Overall Match Score: {match_score:.1f}%")
        report.append(f"Detected Role: {resume_data.get('role_compatibility', {}).get('best_match_role', 'Unknown')}")
        report.append(f"Target Role: {jd_data.get('jd_role', 'Unknown')}")
        report.append(f"Resume Quality: {resume_data.get('quality_score', 0):.0f}/100")
        report.append(f"Skills Match: {match_data.get('skill_match', {}).get('match_percentage', 0):.1f}%")
        report.append(f"ATS Score: {resume_data.get('ats_analysis', {}).get('score', 0):.0f}/100")
        report.append(f"Experience Level: {jd_data.get('seniority', 'Not specified')}")
        report.append(f"Required Experience: {jd_data.get('experience_range', 'Not specified')}\n")
        
        # Match Interpretation
        if match_score >= 70:
            report.append("RECOMMENDATION: 🟢 STRONG MATCH - Apply now!")
        elif match_score >= 50:
            report.append("RECOMMENDATION: 🟡 MODERATE MATCH - Apply with gaps addressed")
        else:
            report.append("RECOMMENDATION: 🔴 LOW MATCH - Build skills first")
        report.append("")
        
        # Skills Analysis
        report.append("\nSKILLS ANALYSIS")
        report.append("-" * 40)
        matched_skills = match_data.get('matched_skills', [])
        missing_skills = match_data.get('missing_skills', [])
        critical_missing = match_data.get('priority_analysis', {}).get('critical_missing', [])
        
        report.append(f"Total Required Skills: {len(jd_data.get('all_jd_skills_list', []))}")
        report.append(f"Matched Skills: {len(matched_skills)}")
        report.append(f"Missing Skills: {len(missing_skills)}")
        report.append(f"Critical Gaps: {len(critical_missing)}\n")
        
        # Matched Skills
        if matched_skills:
            report.append("✓ MATCHED SKILLS:")
            for skill in matched_skills[:15]:
                report.append(f"  • {skill}")
            if len(matched_skills) > 15:
                report.append(f"  ... and {len(matched_skills) - 15} more\n")
            else:
                report.append("")
        
        # Critical Missing
        if critical_missing:
            report.append("\n⚠️  CRITICAL MISSING SKILLS (PRIORITY):")
            for skill in critical_missing[:10]:
                report.append(f"  • {skill}")
            if len(critical_missing) > 10:
                report.append(f"  ... and {len(critical_missing) - 10} more\n")
            else:
                report.append("")
        
        # Other Missing
        if missing_skills and missing_skills != critical_missing:
            report.append("\n📚 OTHER MISSING SKILLS:")
            other_missing = [s for s in missing_skills if s not in critical_missing]
            for skill in other_missing[:10]:
                report.append(f"  • {skill}")
            if len(other_missing) > 10:
                report.append(f"  ... and {len(other_missing) - 10} more\n")
            else:
                report.append("")
        
        # Market Analysis
        report.append("\n\nMARKET ANALYSIS")
        report.append("-" * 40)
        market_analysis = match_data.get('market_analysis', {})
        report.append(f"Market Position: {market_analysis.get('market_position', 'Unknown')}")
        report.append(f"Salary Range: {market_analysis.get('salary_range', 'Not available')}")
        report.append(f"Demand Level: {market_analysis.get('demand_level', 'Medium')}")
        report.append(f"Competitiveness Score: {market_analysis.get('competitiveness_score', 0):.0f}%\n")
        
        # Strengths
        strengths = market_analysis.get('strengths', [])
        if strengths:
            report.append("STRENGTHS:")
            for i, strength in enumerate(strengths, 1):
                report.append(f"  {i}. {strength}")
            report.append("")
        
        # Improvements
        improvements = market_analysis.get('improvement_areas', [])
        if improvements:
            report.append("\nAREAS FOR IMPROVEMENT:")
            for i, improvement in enumerate(improvements, 1):
                report.append(f"  {i}. {improvement}")
            report.append("")
        
        # Footer
        report.append("\n" + "=" * 80)
        report.append("End of Report")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_json_report(self, resume_data: Dict, jd_data: Dict, match_data: Dict) -> str:
        """Generate JSON report."""
        import json
        
        report_data = {
            'timestamp': self.timestamp,
            'overall_score': match_data.get('match_score_overall', 0),
            'detected_role': resume_data.get('role_compatibility', {}).get('best_match_role', 'Unknown'),
            'target_role': jd_data.get('jd_role', 'Unknown'),
            'resume_quality': resume_data.get('quality_score', 0),
            'skills_match_percentage': match_data.get('skill_match', {}).get('match_percentage', 0),
            'ats_score': resume_data.get('ats_analysis', {}).get('score', 0),
            'matched_skills': match_data.get('matched_skills', []),
            'missing_skills': match_data.get('missing_skills', []),
            'critical_missing_skills': match_data.get('priority_analysis', {}).get('critical_missing', []),
            'market_analysis': match_data.get('market_analysis', {}),
        }
        
        return json.dumps(report_data, indent=2)


def get_report_generator() -> ReportGenerator:
    """Get singleton instance of ReportGenerator."""
    return ReportGenerator()
