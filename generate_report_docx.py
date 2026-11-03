import re
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_styled_document():
    doc = Document()
    
    # 1. Page Setup: A4, Margins: Left=1.25", Right=0.75", Top=1", Bottom=1"
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(0.75)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        
        # Add Page numbering in footer (bottom and center)
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run()
        f_run.font.name = 'Times New Roman'
        f_run.font.size = Pt(10)
        
        # XML for Page Number
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        f_p._p.append(fldSimple)
        
    # Set default style to Times New Roman, 12pt, 1.5 line spacing
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    
    return doc

def add_title(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.bold = True
    
    if level == 1:
        # Chapter Title: 14pt, BOLD & CAPS, Centered or Left
        run.font.size = Pt(14)
        run.text = text.upper()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(12)
    elif level == 2:
        # Subsection Title: 13pt, BOLD & CAPS
        run.font.size = Pt(13)
        run.text = text.upper()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
    elif level == 3:
        # Sub-subsections: 13pt, Title Case
        run.font.size = Pt(13)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(6)
    return p

def add_body_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.bold = True
        
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_table_heading(doc, caption_text):
    # For tables, captions should be above the tabular column (10pt, Title Case)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(caption_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    run.bold = True
    return p

def add_figure_caption(doc, caption_text):
    # For figures, captions should be at the bottom (10pt, Title Case)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run(caption_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    run.bold = True
    run.italic = True
    return p

def build_docx_report():
    md_path = r"C:\Users\omvis\.gemini\antigravity\scratch\financial-risk-dashboard\FINANCIAL_LOAN_CREDIT_RISK_PROJECT_REPORT.md"
    docx_path = r"C:\Users\omvis\.gemini\antigravity\scratch\financial-risk-dashboard\FINANCIAL_LOAN_CREDIT_RISK_PROJECT_REPORT.docx"
    
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    doc = create_styled_document()
    
    in_code_block = False
    code_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Check code fence
        if line.startswith("```"):
            if in_code_block:
                in_code_block = False
                # Add code block paragraph
                p = doc.add_paragraph()
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(6)
                r = p.add_run("\n".join(code_lines))
                r.font.name = 'Courier New'
                r.font.size = Pt(9.5)
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue
            
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
            
        if not line.strip():
            i += 1
            continue
            
        # Parse Markdown Headings
        if line.startswith("# "):
            add_title(doc, line[2:].strip(), level=1)
        elif line.startswith("## "):
            add_title(doc, line[3:].strip(), level=1)
        elif line.startswith("### "):
            add_title(doc, line[4:].strip(), level=2)
        elif line.startswith("#### "):
            add_title(doc, line[5:].strip(), level=3)
        elif line.startswith("##### "):
            add_title(doc, line[6:].strip(), level=3)
        elif line.startswith("|") and i + 1 < len(lines) and "|---" in lines[i+1]:
            # Markdown table detected!
            table_lines = [line]
            i += 2  # skip header and delimiter
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
                
            # Process table
            headers = [c.strip() for c in table_lines[0].split("|")[1:-1]]
            rows = []
            for r_line in table_lines[1:]:
                cells = [c.strip() for c in r_line.split("|")[1:-1]]
                rows.append(cells)
                
            tbl = doc.add_table(rows=len(rows)+1, cols=len(headers))
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            
            # Format header
            hdr_cells = tbl.rows[0].cells
            for idx, text in enumerate(headers):
                hdr_cells[idx].text = text
                for p in hdr_cells[idx].paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.name = 'Times New Roman'
                        r.font.size = Pt(10)
                        r.bold = True
                # Light grey background
                shd = parse_xml(r'<w:shd {} w:fill="EAEAEA"/>'.format(nsdecls('w')))
                hdr_cells[idx]._tc.get_or_add_tcPr().append(shd)
                
            # Format body rows
            for r_idx, row_data in enumerate(rows):
                row_cells = tbl.rows[r_idx+1].cells
                for c_idx, cell_value in enumerate(row_data):
                    if c_idx < len(row_cells):
                        row_cells[c_idx].text = cell_value
                        for p in row_cells[c_idx].paragraphs:
                            for r in p.runs:
                                r.font.name = 'Times New Roman'
                                r.font.size = Pt(9.5)
                                
            # Space after table
            p_after = doc.add_paragraph()
            p_after.paragraph_format.space_after = Pt(6)
            continue
        elif line.strip().startswith("**Table ") or line.strip().startswith("Table "):
            # Table caption
            add_table_heading(doc, line.replace("**", "").strip())
        elif line.strip().startswith("**Fig") or line.strip().startswith("Fig ") or line.strip().startswith("**Figure ") or line.strip().startswith("Figure "):
            # Figure caption
            add_figure_caption(doc, line.replace("**", "").strip())
        else:
            # Normal paragraph
            clean_text = line.replace("**", "").replace("`", "")
            add_body_p(doc, clean_text)
            
        i += 1
        
    doc.save(docx_path)
    print(f"Successfully generated DOCX report at: {docx_path}")

if __name__ == '__main__':
    build_docx_report()
