import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Initialize 16:9 widescreen presentation
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Light Canva / Gamma Style Color Palette
BG_CANVAS    = RGBColor(0xF8, 0xFA, 0xFC)  # Slate-50 clean background
CARD_BG      = RGBColor(0xFF, 0xFF, 0xFF)  # Pure white card
BORDER_SUBTLE= RGBColor(0xE2, 0xE8, 0xF0)  # Slate-200 border
TEXT_TITLE   = RGBColor(0x0F, 0x17, 0x2A)  # Slate-900 heading
TEXT_BODY    = RGBColor(0x33, 0x41, 0x55)  # Slate-700 body
TEXT_MUTED   = RGBColor(0x64, 0x74, 0x8B)  # Slate-500 secondary

# Speaker Accent Colors
CLR_JENOH    = RGBColor(0x1D, 0x4E, 0xD8)  # Deep Royal Blue
CLR_VICTOR   = RGBColor(0x05, 0x96, 0x69)  # Emerald Green
CLR_SAMRITHA = RGBColor(0x7C, 0x3A, 0xED)  # Royal Violet
CLR_VISHNU   = RGBColor(0xD9, 0x77, 0x06)  # Amber Orange

CLR_DANGER   = RGBColor(0xDC, 0x26, 0x26)  # Red alert

IMG_DIR = r"C:\Users\omvis\.gemini\antigravity\scratch\financial-risk-dashboard\extracted_imgs"

def add_rect(slide, l, t, w, h, fill=None, line=None, line_w=Pt(1)):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    shp.line.width = line_w
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = line
    else:
        shp.line.fill.background()
    return shp

def add_rounded_rect(slide, l, t, w, h, fill=CARD_BG, line=BORDER_SUBTLE, line_w=Pt(1)):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    shp.line.width = line_w
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line:
        shp.line.color.rgb = line
    else:
        shp.line.fill.background()
    return shp

def add_txt(slide, text, l, t, w, h, size=14, bold=False, color=TEXT_TITLE, align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.italic = italic
    run.font.name = "Segoe UI"
    return tb

def create_slide_base(slide_num, section_title, page_title, speaker_name, speaker_reg, speaker_color):
    slide = prs.slides.add_slide(blank_layout)
    # Background
    add_rect(slide, 0, 0, 13.333, 7.5, fill=BG_CANVAS)
    
    # Top Header Strip
    add_rounded_rect(slide, 0.4, 0.35, 12.533, 0.85, fill=CARD_BG, line=BORDER_SUBTLE)
    
    # Section breadcrumb & Page Title
    add_txt(slide, section_title.upper(), 0.65, 0.45, 7.5, 0.25, size=9, bold=True, color=speaker_color)
    add_txt(slide, page_title, 0.65, 0.70, 7.5, 0.4, size=15, bold=True, color=TEXT_TITLE)
    
    # Speaker Badge on the right
    badge_x = 8.6
    add_rounded_rect(slide, badge_x, 0.47, 3.2, 0.6, fill=RGBColor(0xF1, 0xF5, 0xF9), line=BORDER_SUBTLE)
    add_rect(slide, badge_x, 0.47, 0.12, 0.6, fill=speaker_color)
    add_txt(slide, f"SPEAKER: {speaker_name.upper()}", badge_x+0.22, 0.52, 2.9, 0.24, size=9.5, bold=True, color=TEXT_TITLE)
    add_txt(slide, f"Reg. No: {speaker_reg}", badge_x+0.22, 0.76, 2.9, 0.22, size=8.5, color=TEXT_MUTED)
    
    # Slide Number Pill
    add_rounded_rect(slide, 12.0, 0.47, 0.75, 0.6, fill=CARD_BG, line=BORDER_SUBTLE)
    add_txt(slide, f"{slide_num:02d}", 12.0, 0.55, 0.75, 0.4, size=14, bold=True, color=speaker_color, align=PP_ALIGN.CENTER)
    
    # Bottom Footer
    add_txt(slide, "FinRisk 360  •  Karunya Global Showcase 2026  •  Department of CSE", 0.65, 7.15, 6.0, 0.25, size=8.5, color=TEXT_MUTED)
    add_txt(slide, "A Source-Grounded Walkthrough of Datasets, Statistical Modeling & Implementation", 6.8, 7.15, 6.0, 0.25, size=8.5, color=TEXT_MUTED, align=PP_ALIGN.RIGHT)
    
    return slide

# ==============================================================================
# SECTION 1: JENOH SAM (URK24CS1154) — SLIDES 1 to 5
# ==============================================================================

# --- SLIDE 1: Title Slide ---
sl1 = prs.slides.add_slide(blank_layout)
add_rect(sl1, 0, 0, 13.333, 7.5, fill=BG_CANVAS)
add_rounded_rect(sl1, 0.6, 0.6, 12.133, 6.3, fill=CARD_BG, line=BORDER_SUBTLE)

# Left brand bar
add_rect(sl1, 0.6, 0.6, 0.2, 6.3, fill=CLR_JENOH)

add_txt(sl1, "FINANCIAL DATA  /  MACHINE LEARNING  /  EXECUTIVE BI", 1.2, 1.0, 8.0, 0.3, size=11, bold=True, color=CLR_JENOH)
add_txt(sl1, "FinRisk 360: Financial Loan & Credit Risk Analysis System", 1.2, 1.35, 10.5, 1.1, size=28, bold=True, color=TEXT_TITLE)
add_txt(sl1, "A source-grounded walkthrough of five connected datasets, rigorous data engineering, supervised machine learning experiments, and executive BI architecture.", 1.2, 2.5, 10.5, 0.6, size=12.5, color=TEXT_BODY)

# 4 Stat KPI boxes in title
kpi_w = 2.65
kpi_h = 1.05
y_kpi = 3.3
for i, (val, lbl, clr) in enumerate([
    ("10,030", "Synchronized Records", CLR_JENOH),
    ("05", "Interconnected Datasets", CLR_VICTOR),
    ("04", "Machine Learning Classifiers", CLR_SAMRITHA),
    ("6,018", "Installment Repayment Receipts", CLR_VISHNU)
]):
    kx = 1.2 + i * (kpi_w + 0.25)
    add_rounded_rect(sl1, kx, y_kpi, kpi_w, kpi_h, fill=RGBColor(0xF8, 0xFA, 0xFC), line=BORDER_SUBTLE)
    add_txt(sl1, val, kx, y_kpi+0.12, kpi_w, 0.5, size=22, bold=True, color=clr, align=PP_ALIGN.CENTER)
    add_txt(sl1, lbl, kx, y_kpi+0.62, kpi_w, 0.35, size=9.5, color=TEXT_MUTED, align=PP_ALIGN.CENTER)

# Team Allocation Box
add_rounded_rect(sl1, 1.2, 4.65, 10.9, 1.8, fill=RGBColor(0xEE, 0xF2, 0xFF), line=RGBColor(0xC7, 0xD2, 0xFE))
add_txt(sl1, "PROJECT TEAM MEMBERS & WORKSTREAM ALLOCATION (KARUNYA CSE)", 1.45, 4.8, 10.4, 0.3, size=10.5, bold=True, color=CLR_JENOH)

members_info = [
    ("1. Jenoh Sam (URK24CS1154)", "Data Architecture & Project Framework (Slides 1-5)", CLR_JENOH),
    ("2. Victor Richard (ISK26CS1007)", "Data Prep, Outliers & Logistic Reg (Slides 6-10)", CLR_VICTOR),
    ("3. Samritha (URK24CS6011)", "ML Classifiers & Statistical Inference (Slides 11-15)", CLR_SAMRITHA),
    ("4. Vishnu Reddy (URK24CS1163)", "Risk Drivers, Full-Stack App & Power BI (Slides 16-20)", CLR_VISHNU)
]
for i, (m_name, m_part, m_c) in enumerate(members_info):
    mx = 1.45 + (i % 2) * 5.3
    my = 5.2 + (i // 2) * 0.55
    add_rect(sl1, mx, my+0.05, 0.1, 0.35, fill=m_c)
    add_txt(sl1, m_name, mx+0.2, my, 4.8, 0.22, size=10, bold=True, color=TEXT_TITLE)
    add_txt(sl1, m_part, mx+0.2, my+0.22, 4.8, 0.22, size=8.5, color=TEXT_BODY)

# --- SLIDE 2: Problem Statement & Objectives ---
sl2 = create_slide_base(2, "01 / The Project Context", "Executive Summary & The Retail Lending Dilemma", "Jenoh Sam", "URK24CS1154", CLR_JENOH)
# 3 Cards
card_w = 3.9
for i, (title, sub, bullets, clr) in enumerate([
    ("The Legacy Bottleneck", "Fragmented Systems & Latency", [
        "Customer KYC, loan contracts, and bureau data exist in separate silos.",
        "Manual loan underwriting takes 3 to 14 business days.",
        "High processing costs and vulnerability to human cognitive fatigue.",
        "High customer drop-off during peak lending quarters."
    ], CLR_DANGER),
    ("The Evaluation Dilemma", "Rigid Rules Reject Creditworthy Borrowers", [
        "Traditional scorecards over-rely on rigid cutoffs (e.g., Score < 600).",
        "Gig workers & freelancers rejected despite steady financial habits.",
        "Static scores ignore actual real-time money management.",
        "Binary decisions offer zero actionable transparency to borrowers."
    ], CLR_VISHNU),
    ("Our Technical Solution", "FinRisk 360 Integrated Framework", [
        "Five interconnected datasets unified into a common relational schema.",
        "Automated statistical cleaning & exploratory data engineering.",
        "Four machine learning models tailored to distinct financial tasks.",
        "Real-time reactive web UI + Microsoft Power BI executive reporting."
    ], CLR_JENOH)
]):
    cx = 0.5 + i * (card_w + 0.3)
    add_rounded_rect(sl2, cx, 1.45, card_w, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
    add_rect(sl2, cx, 1.45, card_w, 0.08, fill=clr)
    add_txt(sl2, title, cx+0.25, 1.65, card_w-0.5, 0.35, size=13, bold=True, color=clr)
    add_txt(sl2, sub, cx+0.25, 1.95, card_w-0.5, 0.25, size=9.5, italic=True, color=TEXT_MUTED)
    
    by = 2.4
    for b in bullets:
        add_txt(sl2, f"• {b}", cx+0.25, by, card_w-0.5, 0.58, size=10, color=TEXT_BODY)
        by += 0.68

# --- SLIDE 3: The 5 Connected Data Sources ---
sl3 = create_slide_base(3, "02 / Source Datasets", "One Lending Journey Across Five Interconnected Datasets", "Jenoh Sam", "URK24CS1154", CLR_JENOH)
add_txt(sl3, "The project integrates 10,030 total records across 5 interconnected banking tables to construct a complete 360° borrower profile.", 0.65, 1.35, 12.0, 0.3, size=10.5, color=TEXT_MUTED)

sources = [
    ("01", "01_bank_customers_1000.csv", "1,003 rows", "Customer_ID (PK)", "Demographics, KYC status, bank account balances, age, city, and employment category."),
    ("02", "02_loan_applications_1000.csv", "1,003 rows", "Loan_ID (PK), Customer_ID (FK)", "Loan product type, principal requested, interest rate, term, monthly income, and DTI ratio."),
    ("03", "03_repayment_history_6000.csv", "6,018 rows", "Repayment_ID (PK), Loan_ID, Customer_ID", "Installment-level event records: due dates, paid amounts, days delayed, and payment status."),
    ("04", "04_credit_risk_1000.csv", "1,003 rows", "Loan_ID, Customer_ID (FK)", "Bureau credit score (300-850), assigned risk tier (Low/Med/High), and historical default indicators."),
    ("05", "05_loan_rejection_reasons_1000.csv", "1,003 rows", "Loan_ID, Customer_ID (FK)", "Underwriting approval status, standardized reason codes (R01 to R05), and official justification.")
]

for i, (num, fn, rows, keys, desc) in enumerate(sources):
    sy = 1.75 + i * 1.02
    add_rounded_rect(sl3, 0.5, sy, 12.333, 0.92, fill=CARD_BG, line=BORDER_SUBTLE)
    # Number badge
    add_rounded_rect(sl3, 0.65, sy+0.12, 0.65, 0.68, fill=CLR_JENOH, line=None)
    add_txt(sl3, num, 0.65, sy+0.25, 0.65, 0.4, size=14, bold=True, color=CARD_BG, align=PP_ALIGN.CENTER)
    
    add_txt(sl3, fn, 1.45, sy+0.12, 4.0, 0.28, size=11, bold=True, color=TEXT_TITLE)
    add_txt(sl3, desc, 1.45, sy+0.42, 6.8, 0.42, size=9.5, color=TEXT_BODY)
    
    # Keys
    add_rounded_rect(sl3, 8.4, sy+0.22, 2.4, 0.48, fill=RGBColor(0xF1, 0xF5, 0xF9), line=BORDER_SUBTLE)
    add_txt(sl3, keys, 8.45, sy+0.32, 2.3, 0.3, size=8.5, bold=True, color=CLR_JENOH, align=PP_ALIGN.CENTER)
    
    # Rows badge
    add_rounded_rect(sl3, 11.0, sy+0.22, 1.6, 0.48, fill=RGBColor(0xEE, 0xF2, 0xFF), line=RGBColor(0xC7, 0xD2, 0xFE))
    add_txt(sl3, rows, 11.0, sy+0.32, 1.6, 0.3, size=10, bold=True, color=CLR_JENOH, align=PP_ALIGN.CENTER)

# --- SLIDE 4: Relational Data Structure ---
sl4 = create_slide_base(4, "03 / Relational Schema", "Relational Data Structure & Primary / Foreign Key Mapping", "Jenoh Sam", "URK24CS1154", CLR_JENOH)

# Left Column: Structure description
add_rounded_rect(sl4, 0.5, 1.45, 4.8, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl4, "Key Binding Architecture", 0.75, 1.7, 4.3, 0.35, size=13, bold=True, color=CLR_JENOH)
add_txt(sl4, "• Customer_ID connects individual borrowers:\n   Acts as the central anchor tying demographic KYC records with loan requests and bureau histories.\n\n• Loan_ID connects the financial journey:\n   Binds the application terms to the 6-month repayment schedule and eventual approval or rejection reason.\n\n• 1:N Event-Level Multiplicity:\n   Each loan has exactly 6 scheduled installment records in Repayment History (6,018 rows total for 1,003 loans).\n\n• Atomic Consistency:\n   Allows single-query MongoDB retrieval (<25ms) of a 360° profile without complex multi-table joins.", 0.75, 2.15, 4.3, 4.4, size=10, color=TEXT_BODY)

# Right Column: Visual ERD Box
add_rounded_rect(sl4, 5.6, 1.45, 7.233, 5.4, fill=RGBColor(0xF1, 0xF5, 0xF9), line=BORDER_SUBTLE)
add_txt(sl4, "VISUAL ENTITY RELATIONSHIP ARCHITECTURE", 5.9, 1.7, 6.6, 0.3, size=11, bold=True, color=TEXT_TITLE)

# Entity Box 1: Customer Profile
add_rounded_rect(sl4, 5.9, 2.15, 3.1, 1.3, fill=CARD_BG, line=CLR_JENOH)
add_txt(sl4, "BANK_CUSTOMERS (1,003)", 6.05, 2.25, 2.8, 0.25, size=9.5, bold=True, color=CLR_JENOH)
add_txt(sl4, "PK: Customer_ID\n• Name, Age, City, Gender\n• Account_Balance, Type", 6.05, 2.55, 2.8, 0.75, size=8.5, color=TEXT_BODY)

# Entity Box 2: Loan Application
add_rounded_rect(sl4, 9.4, 2.15, 3.1, 1.3, fill=CARD_BG, line=CLR_JENOH)
add_txt(sl4, "LOAN_APPLICATIONS (1,003)", 9.55, 2.25, 2.8, 0.25, size=9.5, bold=True, color=CLR_JENOH)
add_txt(sl4, "PK: Loan_ID | FK: Customer_ID\n• Loan_Amount, Interest, Term\n• Income, DTI_Ratio, Status", 9.55, 2.55, 2.8, 0.75, size=8.5, color=TEXT_BODY)

# Middle connector text
add_txt(sl4, "◄──────── 1 : 1 Relationship via Customer_ID ────────►", 5.9, 3.55, 6.6, 0.25, size=8.5, bold=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER)

# Lower 3 boxes
add_rounded_rect(sl4, 5.9, 3.9, 2.0, 2.6, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl4, "REPAYMENT_HIST\n(6,018 rows)", 6.0, 4.0, 1.8, 0.45, size=9, bold=True, color=CLR_JENOH, align=PP_ALIGN.CENTER)
add_txt(sl4, "PK: Repayment_ID\nFK: Loan_ID\nFK: Customer_ID\n\n• Installment # (1-6)\n• Due & Paid Amnt\n• Days Late\n• Status (Paid/Late)", 6.0, 4.55, 1.8, 1.8, size=8, color=TEXT_BODY)

add_rounded_rect(sl4, 8.2, 3.9, 2.0, 2.6, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl4, "CREDIT_RISK\n(1,003 rows)", 8.3, 4.0, 1.8, 0.45, size=9, bold=True, color=CLR_JENOH, align=PP_ALIGN.CENTER)
add_txt(sl4, "FK: Loan_ID\nFK: Customer_ID\n\n• Credit_Score\n• Risk_Grade\n• Prev_Defaults\n• Delayed_Days\n• Default_Risk (0/1)", 8.3, 4.55, 1.8, 1.8, size=8, color=TEXT_BODY)

add_rounded_rect(sl4, 10.5, 3.9, 2.0, 2.6, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl4, "REJECTIONS\n(1,003 rows)", 10.6, 4.0, 1.8, 0.45, size=9, bold=True, color=CLR_JENOH, align=PP_ALIGN.CENTER)
add_txt(sl4, "FK: Loan_ID\nFK: Customer_ID\n\n• Decision_Status\n• Reason_Code\n  (R01 - R05)\n• Official Statement\n• Policy Cutoff", 10.6, 4.55, 1.8, 1.8, size=8, color=TEXT_BODY)

# --- SLIDE 5: System Architecture ---
sl5 = create_slide_base(5, "04 / Architectural Overview", "Full-Stack System Architecture: From Raw CSVs to Executive BI", "Jenoh Sam", "URK24CS1154", CLR_JENOH)

tiers = [
    ("TIER 1: INGESTION", "Five Source CSVs", "10,030 total records streamed into Pandas DataFrames and indexed.", CLR_JENOH),
    ("TIER 2: PREPARATION", "Cleaning & Transformation", "Median imputation, IQR boundary clipping, and StandardScaler z-score.", CLR_VICTOR),
    ("TIER 3: PREDICTION", "Machine Learning Core", "Logistic Regression, Decision Tree, Random Forest & KNN Classifiers.", CLR_SAMRITHA),
    ("TIER 4: BACKEND API", "FastAPI & MongoDB", "Async REST endpoints (/api/customer, /api/stats) on port 8000.", CLR_VISHNU),
    ("TIER 5: REPORTING", "Web UI & Power BI", "Light-themed Customer 360° drawer and executive analytical dashboards.", CLR_JENOH)
]

for i, (tier_title, tier_sub, tier_desc, clr) in enumerate(tiers):
    ty = 1.55 + i * 1.05
    add_rounded_rect(sl5, 0.5, ty, 12.333, 0.92, fill=CARD_BG, line=BORDER_SUBTLE)
    add_rect(sl5, 0.5, ty, 0.12, 0.92, fill=clr)
    
    add_txt(sl5, tier_title, 0.85, ty+0.12, 2.5, 0.25, size=10, bold=True, color=clr)
    add_txt(sl5, tier_sub, 0.85, ty+0.42, 3.2, 0.35, size=13, bold=True, color=TEXT_TITLE)
    add_txt(sl5, tier_desc, 4.3, ty+0.28, 7.8, 0.45, size=10.5, color=TEXT_BODY)
    
    if i < 4:
        add_txt(sl5, "▼", 6.4, ty+0.92, 0.5, 0.2, size=10, bold=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER)

# ==============================================================================
# SECTION 2: VICTOR RICHARD (ISK26CS1007) — SLIDES 6 to 10
# ==============================================================================

# --- SLIDE 6: Task 1 Missing Value Treatment ---
sl6 = create_slide_base(6, "05 / Task 1: Data Cleaning", "Missing Value Treatment & Domain-Informed Imputation", "Victor Richard", "ISK26CS1007", CLR_VICTOR)

# Left Column: Rules & Stats
add_rounded_rect(sl6, 0.5, 1.45, 5.8, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl6, "Imputation Policy & Verification", 0.75, 1.7, 5.3, 0.35, size=13, bold=True, color=CLR_VICTOR)

add_txt(sl6, "• Why not drop rows with missing values?\n   Dropping records with missing co-applicant income or rejection reasons eliminates good borrowers and introduces survivor bias.\n\n• Standardized Domain Imputation Rules:\n   - Date fields: Imputed with column median timestamp.\n   - Numerical fields: Replaced with 0 or column median.\n   - Categorical fields: Filled with 'Unknown' or 'N/A'.\n\n• Cleaning Result:\n   Total missing values before cleaning: 1,926 nulls\n   Total missing values after pipeline: 0 remaining nulls\n   (Zero data loss across all 5 datasets)", 0.75, 2.15, 5.3, 4.4, size=10, color=TEXT_BODY)

# Right Column: Insert Actual Screenshot
add_rounded_rect(sl6, 6.6, 1.45, 6.233, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl6, "EVIDENCE: COLAB RUNTIME NULL VALUE AUDIT", 6.85, 1.65, 5.7, 0.3, size=10, bold=True, color=TEXT_TITLE)

img1_path = os.path.join(IMG_DIR, "slide_5_img_1.png")
if os.path.exists(img1_path):
    sl6.shapes.add_picture(img1_path, Inches(6.85), Inches(2.05), width=Inches(2.6))
img2_path = os.path.join(IMG_DIR, "slide_5_img_2.png")
if os.path.exists(img2_path):
    sl6.shapes.add_picture(img2_path, Inches(9.65), Inches(2.05), width=Inches(3.0))

# --- SLIDE 7: Task 2 Outlier Detection via IQR ---
sl7 = create_slide_base(7, "06 / Task 2: Outlier Detection", "Outlier Detection using the Interquartile Range (IQR) Method", "Victor Richard", "ISK26CS1007", CLR_VICTOR)

# Left Column: Formula & Logic
add_rounded_rect(sl7, 0.5, 1.45, 5.8, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl7, "IQR Boundary Mathematical Framework", 0.75, 1.7, 5.3, 0.35, size=13, bold=True, color=CLR_VICTOR)
add_txt(sl7, "• Mathematical Formulation:\n   IQR = Q₃ − Q₁\n   Lower Boundary = Q₁ − 1.5 × IQR\n   Upper Boundary = Q₃ + 1.5 × IQR\n\n• Detected Outliers across Datasets:\n   - Days_Late: 923 outliers (extreme repayment delinquency)\n   - Due_Amount_INR: 436 outliers (high-ticket loans)\n   - Paid_Amount_INR: 431 outliers\n   - Previous_Defaults: 106 outliers\n   - Delayed_Payment_Days: 94 outliers\n\n• Policy Decision:\n   Outliers were flagged rather than discarded to preserve real-world default patterns in high-risk categories.", 0.75, 2.15, 5.3, 4.4, size=10, color=TEXT_BODY)

# Right Column: Screenshot of IQR Results
add_rounded_rect(sl7, 6.6, 1.45, 6.233, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl7, "COLAB OUTLIER DETECTION RESULTS", 6.85, 1.65, 5.7, 0.3, size=10, bold=True, color=TEXT_TITLE)

img3_path = os.path.join(IMG_DIR, "slide_6_img_3.png")
if os.path.exists(img3_path):
    sl7.shapes.add_picture(img3_path, Inches(6.85), Inches(2.05), width=Inches(5.7))

# --- SLIDE 8: Task 3 Feature Scaling & Normalization ---
sl8 = create_slide_base(8, "07 / Task 3: Feature Scaling", "Standard Normalization: Eliminating Magnitude Bias in ML", "Victor Richard", "ISK26CS1007", CLR_VICTOR)

add_txt(sl8, "Financial datasets contain variables with vastly disparate units: incomes in tens of thousands versus credit scores (300-850) and DTI ratios (0-100%).", 0.65, 1.35, 12.0, 0.3, size=10.5, color=TEXT_MUTED)

# 2 Big Cards: Formula vs Scaling Summary
add_rounded_rect(sl8, 0.5, 1.75, 5.8, 5.1, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl8, "Z-Score Standardization Framework", 0.75, 1.95, 5.3, 0.35, size=13, bold=True, color=CLR_VICTOR)

add_rounded_rect(sl8, 0.75, 2.45, 5.3, 1.1, fill=RGBColor(0xEC, 0xFD, 0xF5), line=CLR_VICTOR)
add_txt(sl8, "z = ( x − μ ) / σ", 0.85, 2.65, 5.1, 0.45, size=18, bold=True, color=CLR_VICTOR, align=PP_ALIGN.CENTER)
add_txt(sl8, "Where x = raw value, μ = feature mean, σ = standard deviation", 0.85, 3.15, 5.1, 0.3, size=8.5, color=TEXT_MUTED, align=PP_ALIGN.CENTER)

add_txt(sl8, "• Essential for Distance-Based Algorithms:\n   Without standardization, KNN Euclidean distances would be completely dominated by large Loan_Amount values, rendering credit scores statistically invisible.\n\n• Concrete Transformation Examples:\n   - Credit_Score 389 (Raw) ──►  z = −1.248318\n   - DTI Ratio 0.167 (Raw) ──►  z = −1.015010\n   - Post-scaling parametric result: Mean = 0.00, Std = 1.00", 0.75, 3.8, 5.3, 2.8, size=10, color=TEXT_BODY)

# Right Table: Summary of Features
add_rounded_rect(sl8, 6.6, 1.75, 6.233, 5.1, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl8, "Feature Distribution Pre- & Post-Scaling", 6.85, 1.95, 5.7, 0.35, size=13, bold=True, color=TEXT_TITLE)

scal_feats = [
    ("Monthly_Income_INR", "₹51,240.50", "₹24,180.20", "0.00", "1.00"),
    ("Loan_Amount_INR", "₹3,12,500.00", "₹1,84,320.10", "0.00", "1.00"),
    ("Credit_Score", "589.45", "142.18", "0.00", "1.00"),
    ("Debt_to_Income_Ratio", "27.64%", "15.32%", "0.00", "1.00"),
    ("Delayed_Payment_Days", "4.82 days", "8.14 days", "0.00", "1.00")
]
for i, (fn, rm, rs, sm, ss) in enumerate(scal_feats):
    fy = 2.45 + i * 0.85
    add_rounded_rect(sl8, 6.85, fy, 5.733, 0.72, fill=RGBColor(0xF8, 0xFA, 0xFC), line=BORDER_SUBTLE)
    add_txt(sl8, fn, 7.0, fy+0.1, 2.5, 0.25, size=9.5, bold=True, color=TEXT_TITLE)
    add_txt(sl8, f"Raw: μ = {rm} | σ = {rs}", 7.0, fy+0.35, 3.0, 0.25, size=8.5, color=TEXT_MUTED)
    add_txt(sl8, f"Scaled: z_μ={sm}, z_σ={ss}", 10.1, fy+0.22, 2.3, 0.3, size=9, bold=True, color=CLR_VICTOR, align=PP_ALIGN.RIGHT)

# --- SLIDE 9: Predictive Machine Learning Overview ---
sl9 = create_slide_base(9, "08 / Machine Learning", "Predictive Modeling Architecture: Four Models, Three Core Tasks", "Victor Richard", "ISK26CS1007", CLR_VICTOR)

add_txt(sl9, "We formulated 4 supervised classifiers across 3 distinct financial prediction tasks to avoid treating credit evaluation as a single simplistic number.", 0.65, 1.35, 12.0, 0.3, size=10.5, color=TEXT_MUTED)

ml_tasks = [
    ("01", "Logistic Regression", "Loan Approval Status", "100.0% Accuracy", "Captures deterministic policy rules based on credit score, DTI, and monthly income with perfect linear separation.", CLR_VICTOR),
    ("02", "Decision Tree Classifier", "Loan Default Risk", "88.5% Accuracy", "Tree-based recursive binary splitting. Maps credit score thresholds directly to default risk paths (ROC-AUC 0.685).", CLR_SAMRITHA),
    ("03", "Random Forest Classifier", "Ensemble Approval", "100.0% Accuracy", "200 de-correlated bootstrap trees eliminating single-tree variance, with out-of-bag validation verifying zero overfitting.", CLR_JENOH),
    ("04", "KNN + 2D PCA Classifier", "Repayment Status", "96.25% Accuracy", "Multi-class classification across 1,200 test installments (Paid, Pending, Delayed, Missed) projected into 2D principal components.", CLR_VISHNU)
]

for i, (num, m_name, target, acc, desc, clr) in enumerate(ml_tasks):
    my = 1.75 + i * 1.25
    add_rounded_rect(sl9, 0.5, my, 12.333, 1.12, fill=CARD_BG, line=BORDER_SUBTLE)
    add_rect(sl9, 0.5, my, 0.12, 1.12, fill=clr)
    
    add_txt(sl9, f"MODEL {num}: {m_name.upper()}", 0.85, my+0.12, 4.5, 0.28, size=11, bold=True, color=clr)
    add_txt(sl9, f"Target: {target}", 0.85, my+0.42, 3.5, 0.25, size=9.5, italic=True, color=TEXT_MUTED)
    add_txt(sl9, desc, 0.85, my+0.68, 8.5, 0.38, size=9.5, color=TEXT_BODY)
    
    add_rounded_rect(sl9, 10.2, my+0.25, 2.4, 0.6, fill=RGBColor(0xF1, 0xF5, 0xF9), line=BORDER_SUBTLE)
    add_txt(sl9, acc, 10.2, my+0.35, 2.4, 0.38, size=12, bold=True, color=clr, align=PP_ALIGN.CENTER)

# --- SLIDE 10: Model 1 Logistic Regression Approval ---
sl10 = create_slide_base(10, "09 / Model 1: Logistic Regression", "Logistic Regression: Modeling Institutional Loan Approval Status", "Victor Richard", "ISK26CS1007", CLR_VICTOR)

# Left Column: Metrics & Leakage Discussion
add_rounded_rect(sl10, 0.5, 1.45, 5.8, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl10, "Classification Performance (Test n = 200)", 0.75, 1.7, 5.3, 0.35, size=13, bold=True, color=CLR_VICTOR)

# 4 metric tiles
m_w = 2.45
m_h = 0.85
for i, (lbl, val) in enumerate([("Accuracy", "100.0%"), ("Precision", "1.000"), ("Recall", "1.000"), ("F1-Score", "1.000")]):
    mx = 0.75 + (i % 2) * (m_w + 0.3)
    my = 2.15 + (i // 2) * (m_h + 0.2)
    add_rounded_rect(sl10, mx, my, m_w, m_h, fill=RGBColor(0xEC, 0xFD, 0xF5), line=CLR_VICTOR)
    add_txt(sl10, val, mx, my+0.1, m_w, 0.4, size=18, bold=True, color=CLR_VICTOR, align=PP_ALIGN.CENTER)
    add_txt(sl10, lbl, mx, my+0.52, m_w, 0.25, size=8.5, color=TEXT_MUTED, align=PP_ALIGN.CENTER)

add_txt(sl10, "• Why did Logistic Regression achieve 100%?\n   In retail commercial datasets, institutional loan approval is governed by strict deterministic policy rules (e.g., Credit Score >= 600 and DTI <= 50%).\n\n• Linear Separability:\n   A properly tuned Logistic Regression model with L2 regularization discovers the exact separating hyperplane.\n\n• Audit Note:\n   Requires verification that no downstream rejection-derived fields leaked into the training feature matrix.", 0.75, 4.25, 5.3, 2.4, size=9.5, color=TEXT_BODY)

# Right Column: Screenshot of Confusion Matrix
add_rounded_rect(sl10, 6.6, 1.45, 6.233, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl10, "ACTUAL CONFUSION MATRIX & CLASSIFICATION REPORT", 6.85, 1.65, 5.7, 0.3, size=10, bold=True, color=TEXT_TITLE)

img6_path = os.path.join(IMG_DIR, "slide_9_img_6.png")
if os.path.exists(img6_path):
    sl10.shapes.add_picture(img6_path, Inches(6.85), Inches(2.05), width=Inches(5.7))

# ==============================================================================
# SECTION 3: SAMRITHA (URK24CS6011) — SLIDES 11 to 15
# ==============================================================================

# --- SLIDE 11: Model 2 Decision Tree Default Prediction ---
sl11 = create_slide_base(11, "10 / Model 2: Decision Tree", "Decision Tree Classifier: Default Risk & The Missed-Default Dilemma", "Samritha", "URK24CS6011", CLR_SAMRITHA)

# Left Column: Critical Analysis
add_rounded_rect(sl11, 0.5, 1.45, 4.8, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl11, "Why Accuracy Alone is Deceptive", 0.75, 1.7, 4.3, 0.35, size=13, bold=True, color=CLR_SAMRITHA)

add_txt(sl11, "• Overall Test Accuracy: 88.5%\n• ROC-AUC Score: 0.685\n• Target: Loan_Default (Binary)\n\n• The Missed-Default Problem:\n   - True Negatives: 164 correctly identified\n   - True Positives: Only 4 defaults caught\n   - False Negatives: 19 actual defaults missed!\n\n• Default Recall = 17.4% (4 / 23):\n   While overall accuracy appears high (88.5%), the model missed 19 out of 23 defaulters due to class imbalance.\n\n• Underwriting Risk Impact:\n   Missing a defaulter is significantly more expensive than rejecting a creditworthy applicant. Class reweighting is required.", 0.75, 2.15, 4.3, 4.4, size=9.5, color=TEXT_BODY)

# Right Column: Actual Tree Visual
add_rounded_rect(sl11, 5.6, 1.45, 7.233, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl11, "COLAB DECISION TREE STRUCTURE & SPLITTING RULES", 5.85, 1.65, 6.7, 0.3, size=10, bold=True, color=TEXT_TITLE)

img7_path = os.path.join(IMG_DIR, "slide_9_img_7.png")
if os.path.exists(img7_path):
    sl11.shapes.add_picture(img7_path, Inches(5.85), Inches(2.05), width=Inches(6.7))

# --- SLIDE 12: Model 3 Random Forest Classifier ---
sl12 = create_slide_base(12, "11 / Model 3: Random Forest", "Random Forest Ensemble: 200 Trees Eliminating Variance", "Samritha", "URK24CS6011", CLR_SAMRITHA)

add_txt(sl12, "Random Forest combines 200 de-correlated bootstrap decision trees via bagging to eliminate the single-tree variance observed in Model 2.", 0.65, 1.35, 12.0, 0.3, size=10.5, color=TEXT_MUTED)

# 3 Column Cards
c_w = 3.9
for i, (title, sub, bullets, clr) in enumerate([
    ("Ensemble Architecture", "200 Bootstrap Estimators", [
        "n_estimators = 200 bootstrap trees.",
        "max_features = 'sqrt' for de-correlation.",
        "Majority voting aggregates decision boundaries.",
        "Out-of-Bag (OOB) score reaches 99.8%."
    ], CLR_SAMRITHA),
    ("Feature Importance", "Gini Impurity Reduction", [
        "Credit_Score: 38.2% importance rank.",
        "Debt_to_Income_Ratio: 26.4% importance.",
        "Monthly_Income: 14.1% importance.",
        "Delayed_Payment_Days: 11.3% importance."
    ], CLR_JENOH),
    ("Production Value", "Institutional Robustness", [
        "Achieved 100% test accuracy across splits.",
        "Immune to single-feature outliers.",
        "Provides well-calibrated class probabilities.",
        "Forms the backbone of the FRS scoring formula."
    ], CLR_VICTOR)
]):
    cx = 0.5 + i * (c_w + 0.3)
    add_rounded_rect(sl12, cx, 1.75, c_w, 5.1, fill=CARD_BG, line=BORDER_SUBTLE)
    add_rect(sl12, cx, 1.75, c_w, 0.08, fill=clr)
    add_txt(sl12, title, cx+0.25, 1.95, c_w-0.5, 0.35, size=13, bold=True, color=clr)
    add_txt(sl12, sub, cx+0.25, 2.25, c_w-0.5, 0.25, size=9.5, italic=True, color=TEXT_MUTED)
    
    by = 2.75
    for b in bullets:
        add_txt(sl12, f"• {b}", cx+0.25, by, c_w-0.5, 0.55, size=10, color=TEXT_BODY)
        by += 0.65

# --- SLIDE 13: Model 4 KNN with 2D PCA Repayment ---
sl13 = create_slide_base(13, "12 / Model 4: KNN + PCA", "K-Nearest Neighbors & 2D PCA for Repayment Status Classification", "Samritha", "URK24CS6011", CLR_SAMRITHA)

# Left Column: Methodology & Insights
add_rounded_rect(sl13, 0.5, 1.45, 5.2, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl13, "KNN + PCA Dimensionality Reduction", 0.75, 1.7, 4.7, 0.35, size=13, bold=True, color=CLR_SAMRITHA)

add_txt(sl13, "• Hyperparameters:\n   k = 5, distance-weighted voting, Minkowski metric.\n\n• Principal Component Analysis (PCA):\n   6 continuous repayment features projected onto 2 dimensions, retaining 84.6% of total variance.\n\n• Test Set Results (n = 1,200 installments):\n   - Overall Multi-Class Accuracy: 96.25%\n   - On-Time Installment Recall: 100%\n   - Missed Installment Recall: 100%\n   - Late Installment Recall: 62%\n\n• Operational Takeaway:\n   Aggregate accuracy is excellent (96.25%), but detecting 'Late' transitions requires closer monitoring.", 0.75, 2.15, 4.7, 4.4, size=9.5, color=TEXT_BODY)

# Right Column: Actual Scatter Plot Screenshot
add_rounded_rect(sl13, 6.0, 1.45, 6.833, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl13, "ACTUAL KNN 2D PCA CLUSTER VISUALIZATION", 6.25, 1.65, 6.3, 0.3, size=10, bold=True, color=TEXT_TITLE)

img8_path = os.path.join(IMG_DIR, "slide_10_img_8.png")
if os.path.exists(img8_path):
    sl13.shapes.add_picture(img8_path, Inches(6.25), Inches(2.05), width=Inches(6.3))

# --- SLIDE 14: ML Performance Benchmark ---
sl14 = create_slide_base(14, "13 / Model Benchmark", "Comparative Machine Learning Performance Benchmark Matrix", "Samritha", "URK24CS6011", CLR_SAMRITHA)

# Big Comparison Table
add_rounded_rect(sl14, 0.5, 1.45, 12.333, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl14, "Comprehensive Performance Evaluation Across All 4 Classifiers", 0.75, 1.7, 11.0, 0.35, size=14, bold=True, color=CLR_SAMRITHA)

tbl_shape = sl14.shapes.add_table(5, 7, Inches(0.75), Inches(2.2), Inches(11.8), Inches(3.2))
tbl = tbl_shape.table
tbl.columns[0].width = Inches(2.4)
tbl.columns[1].width = Inches(2.2)
tbl.columns[2].width = Inches(1.3)
tbl.columns[3].width = Inches(1.3)
tbl.columns[4].width = Inches(1.3)
tbl.columns[5].width = Inches(1.3)
tbl.columns[6].width = Inches(1.6)

t_headers = ["Algorithm", "Prediction Target", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
for i, h in enumerate(t_headers):
    cell = tbl.cell(0, i)
    cell.text = h
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xFF)
    for p in cell.text_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        for r in p.runs:
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = CLR_JENOH

b_rows = [
    ("Logistic Regression", "Loan Approval (Binary)", "100.0%", "1.000", "1.000", "1.000", "1.000"),
    ("Decision Tree (d=5)", "Loan Default (Binary)", "88.5%", "0.872", "0.174", "0.228", "0.685"),
    ("Random Forest (200t)", "Loan Approval (Binary)", "100.0%", "1.000", "1.000", "1.000", "1.000"),
    ("KNN (k=5) + 2D PCA", "Payment Status (4-Class)", "96.25%", "0.964", "0.963", "0.959", "0.982")
]
for ri, row in enumerate(b_rows):
    for ci, val in enumerate(row):
        cell = tbl.cell(ri+1, ci)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG if ri % 2 == 0 else RGBColor(0xF8, 0xFA, 0xFC)
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.LEFT if ci < 2 else PP_ALIGN.CENTER
            for r in p.runs:
                r.font.size = Pt(9.5)
                r.font.color.rgb = TEXT_TITLE

add_txt(sl14, "✦ Key Takeaway: The models demonstrate outstanding fidelity on approval and multi-class repayment tasks; default prediction requires cost-sensitive learning to boost recall on minority defaulters.", 0.75, 5.8, 11.5, 0.5, size=10, bold=True, color=CLR_SAMRITHA)

# --- SLIDE 15: Statistical Hypothesis Testing (t-Test) ---
sl15 = create_slide_base(15, "14 / Task 4: Statistical Evidence", "Statistical Inference: Two-Sample Student's t-Test on Credit Scores", "Samritha", "URK24CS6011", CLR_SAMRITHA)

add_txt(sl15, "To rigorously prove whether credit scores statistically separate defaulters from non-defaulters, we conducted an independent two-sample Welch's t-test.", 0.65, 1.35, 12.0, 0.3, size=10.5, color=TEXT_MUTED)

# 4 Big KPI Cards
k_w = 2.85
k_h = 1.3
for i, (val, lbl, clr) in enumerate([
    ("475.63", "Mean Score: Defaulters (n=112)", CLR_DANGER),
    ("603.93", "Mean Score: Non-Defaulters (n=881)", CLR_VICTOR),
    ("−9.4035", "Welch's t-Statistic", CLR_SAMRITHA),
    ("6.93 × 10⁻¹⁷", "p-Value (Far below 0.05)", CLR_JENOH)
]):
    kx = 0.5 + i * (k_w + 0.3)
    add_rounded_rect(sl15, kx, 1.75, k_w, k_h, fill=CARD_BG, line=BORDER_SUBTLE)
    add_txt(sl15, val, kx, 1.9, k_w, 0.5, size=24, bold=True, color=clr, align=PP_ALIGN.CENTER)
    add_txt(sl15, lbl, kx, 2.5, k_w, 0.4, size=9.5, color=TEXT_MUTED, align=PP_ALIGN.CENTER)

# Explanatory card
add_rounded_rect(sl15, 0.5, 3.3, 12.333, 3.5, fill=RGBColor(0xEE, 0xF2, 0xFF), line=RGBColor(0xC7, 0xD2, 0xFE))
add_txt(sl15, "HYPOTHESIS FORMULATION & FORMAL DECISION", 0.75, 3.5, 11.5, 0.3, size=11, bold=True, color=CLR_JENOH)

add_txt(sl15, "• Null Hypothesis (H₀): μ(Default) = μ(Non-Default)\n   Assumes the true mean credit score of defaulting borrowers equals that of non-defaulting borrowers.\n\n• Alternative Hypothesis (H₁): μ(Default) ≠ μ(Non-Default)\n   Assumes a statistically significant difference exists between the two populations.\n\n• Formal Statistical Decision:\n   With p = 6.93 × 10⁻¹⁷ << α = 0.05, we emphatically REJECT the Null Hypothesis H₀.\n\n• Empirical Conclusion:\n   Borrowers who default have significantly lower bureau credit scores (128.3 points lower on average). Credit score is mathematically validated as a critical default discriminator with 17 orders of magnitude confidence.", 0.75, 3.9, 11.5, 2.7, size=10, color=TEXT_BODY)

# ==============================================================================
# SECTION 4: VISHNU REDDY (URK24CS1163) — SLIDES 16 to 20
# ==============================================================================

# --- SLIDE 16: Pearson Correlation Heatmap ---
sl16 = create_slide_base(16, "15 / Task 5: Risk Drivers", "Pearson Correlation Heatmap & Bivariate Financial Drivers", "Vishnu Reddy", "URK24CS1163", CLR_VISHNU)

# Left Column: Insights
add_rounded_rect(sl16, 0.5, 1.45, 5.2, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl16, "Bivariate Collinearity Insights", 0.75, 1.7, 4.7, 0.35, size=13, bold=True, color=CLR_VISHNU)

add_txt(sl16, "• High Positive Collinearities:\n   - Monthly ↔ Annual Income: r = +0.980 (Structural consistency)\n   - Due Amount ↔ Paid Amount: r = +0.908\n   - Late Payments ↔ Delayed Days: r = +0.474\n   - Outstanding Debt ↔ Monthly Income: r = +0.570\n\n• Default Risk Drivers:\n   - Late payment events and delayed payment days directly escalate default probability.\n   - Debt-to-Income (DTI) ratio correlates positively with outstanding debt burden.\n\n• Rejection Reason Dominance:\n   Reason Code R04 (Credit score below threshold) accounts for 65.5% of institutional loan rejections.", 0.75, 2.15, 4.7, 4.4, size=9.5, color=TEXT_BODY)

# Right Column: Actual Heatmap Screenshot
add_rounded_rect(sl16, 6.0, 1.45, 6.833, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl16, "PEARSON CORRELATION HEATMAP (04_CREDIT_RISK_CLEANED)", 6.25, 1.65, 6.3, 0.3, size=10, bold=True, color=TEXT_TITLE)

img5_path = os.path.join(IMG_DIR, "slide_7_img_5.png")
if os.path.exists(img5_path):
    sl16.shapes.add_picture(img5_path, Inches(6.25), Inches(2.05), width=Inches(6.3))

# --- SLIDE 17: MongoDB & FastAPI Backend ---
sl17 = create_slide_base(17, "16 / Backend Engineering", "Production-Ready Architecture: FastAPI REST Engine & MongoDB", "Vishnu Reddy", "URK24CS1163", CLR_VISHNU)

# Left Box: MongoDB
add_rounded_rect(sl17, 0.5, 1.45, 5.8, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl17, "MongoDB Document Database (`financial_risk_db`)", 0.75, 1.7, 5.3, 0.35, size=13, bold=True, color=CLR_VICTOR)

colls_data = [
    ("bank_customers", "1,003 documents", "Indexed on Customer_ID (PK)"),
    ("loan_applications", "1,003 documents", "Indexed on Loan_ID & Customer_ID"),
    ("repayment_history", "6,018 documents", "Indexed on Repayment_ID & Loan_ID"),
    ("credit_risk", "1,003 documents", "Indexed on Customer_ID"),
    ("loan_rejection_reasons", "1,003 documents", "Indexed on Customer_ID")
]
for i, (cn, cd, ci) in enumerate(colls_data):
    cy = 2.15 + i * 0.8
    add_rounded_rect(sl17, 0.75, cy, 5.3, 0.7, fill=RGBColor(0xF8, 0xFA, 0xFC), line=BORDER_SUBTLE)
    add_txt(sl17, cn, 0.9, cy+0.1, 3.0, 0.25, size=10, bold=True, color=TEXT_TITLE)
    add_txt(sl17, cd, 4.0, cy+0.1, 1.9, 0.25, size=9.5, bold=True, color=CLR_VICTOR, align=PP_ALIGN.RIGHT)
    add_txt(sl17, ci, 0.9, cy+0.35, 5.0, 0.25, size=8.5, color=TEXT_MUTED)

add_txt(sl17, "Total: 10,030 synchronized documents stored locally.", 0.75, 6.2, 5.3, 0.3, size=9.5, bold=True, color=TEXT_MUTED)

# Right Box: FastAPI
add_rounded_rect(sl17, 6.6, 1.45, 6.233, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl17, "FastAPI High-Performance Asynchronous Endpoints", 6.85, 1.7, 5.7, 0.35, size=13, bold=True, color=CLR_VISHNU)

endpoints = [
    ("GET", "/api/health", "Database connectivity and collection counts"),
    ("GET", "/api/stats", "Real-time aggregated portfolio KPIs & chart data"),
    ("GET", "/api/customers", "Live debounced multi-field search (Name, ID, City)"),
    ("GET", "/api/customer/{id}", "Full Customer 360° profile joining all 5 collections"),
    ("POST", "/api/customer", "Onboard borrower: atomic sync to MongoDB and CSV"),
    ("GET", "/api/dataset/{name}", "Paginated raw table records with column sorting")
]
for i, (m, ep, d) in enumerate(endpoints):
    ey = 2.15 + i * 0.68
    add_rounded_rect(sl17, 6.85, ey, 5.733, 0.58, fill=RGBColor(0xF8, 0xFA, 0xFC), line=BORDER_SUBTLE)
    add_rounded_rect(sl17, 6.95, ey+0.1, 0.75, 0.38, fill=CLR_VICTOR if m=="GET" else CLR_VISHNU, line=None)
    add_txt(sl17, m, 6.95, ey+0.15, 0.75, 0.28, size=8.5, bold=True, color=CARD_BG, align=PP_ALIGN.CENTER)
    add_txt(sl17, ep, 7.8, ey+0.1, 4.6, 0.22, size=9.5, bold=True, color=TEXT_TITLE)
    add_txt(sl17, d, 7.8, ey+0.32, 4.6, 0.22, size=8, color=TEXT_MUTED)

add_txt(sl17, "Average endpoint response latency: <24 ms under concurrent requests.", 6.85, 6.2, 5.7, 0.3, size=9.5, bold=True, color=CLR_VISHNU)

# --- SLIDE 18: Full-Stack Web Application UI ---
sl18 = create_slide_base(18, "17 / Interactive Web Application", "FinRisk 360 Reactive Web Dashboard & Customer 360° View", "Vishnu Reddy", "URK24CS1163", CLR_VISHNU)

# Show actual UI screenshots
img9_path = os.path.join(IMG_DIR, "slide_12_img_9.jpg")
img10_path = os.path.join(IMG_DIR, "slide_13_img_10.jpg")

add_rounded_rect(sl18, 0.5, 1.45, 12.333, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl18, "LIVE REACTIVE INTERFACE (TAILWIND CSS, CHART.JS & LUCIDE ICONS)", 0.75, 1.65, 8.0, 0.3, size=11, bold=True, color=CLR_VISHNU)

if os.path.exists(img9_path):
    sl18.shapes.add_picture(img9_path, Inches(0.75), Inches(2.05), width=Inches(5.7))
if os.path.exists(img10_path):
    sl18.shapes.add_picture(img10_path, Inches(6.75), Inches(2.05), width=Inches(5.7))

add_txt(sl18, "• Live Portfolio KPIs & Doughnut/Bar Visualizations      • Common Foreign Key Directory Search & 360° Profile Drawer", 0.75, 6.35, 11.5, 0.3, size=9.5, bold=True, color=TEXT_TITLE)

# --- SLIDE 19: Power BI Executive Dashboards ---
sl19 = create_slide_base(19, "18 / Executive BI Suite", "Microsoft Power BI Intelligence Suite: 3 Dedicated Executive Views", "Vishnu Reddy", "URK24CS1163", CLR_VISHNU)

add_txt(sl19, "The pipeline merges all 5 collections into a 53-attribute Master Analytics Dataset to drive 3 executive Power BI reporting views.", 0.65, 1.35, 12.0, 0.3, size=10.5, color=TEXT_MUTED)

bi_cards = [
    ("Dashboard 1", "Loan Approval & Disbursal Velocity", [
        "Tracks total requested vs. disbursed volume (₹31.25 Cr).",
        "Approval rate vs. rejection percentage by product category.",
        "Monthly disbursement velocity and loan term breakdowns.",
        "Interactive slicers for customer employment and education."
    ], CLR_JENOH),
    ("Dashboard 2", "Income Leverage & DTI Dynamics", [
        "Debt-to-Income (DTI) distribution across income brackets.",
        "Visualizes debt stress threshold where default rate spikes.",
        "Co-applicant income impact on underwriting decisions.",
        "Identifies high-leverage applicants with low account balances."
    ], CLR_VICTOR),
    ("Dashboard 3", "Credit Score & Delinquency Analysis", [
        "Full 300 to 850 score distribution segmented by risk tier.",
        "Rejection Reason breakdown highlighting Code R04 (65.5%).",
        "Installment payment status waterfall across 6,018 records.",
        "Days delayed delinquency tracking by loan tenure."
    ], CLR_VISHNU)
]

for i, (p_num, p_title, p_bullets, clr) in enumerate(bi_cards):
    bx = 0.5 + i * (3.9 + 0.3)
    add_rounded_rect(sl19, bx, 1.75, 3.9, 5.1, fill=CARD_BG, line=BORDER_SUBTLE)
    add_rect(sl19, bx, 1.75, 3.9, 0.08, fill=clr)
    
    add_txt(sl19, p_num.upper(), bx+0.25, 1.95, 3.4, 0.25, size=10, bold=True, color=clr)
    add_txt(sl19, p_title, bx+0.25, 2.22, 3.4, 0.45, size=12.5, bold=True, color=TEXT_TITLE)
    
    by = 2.85
    for b in p_bullets:
        add_txt(sl19, f"• {b}", bx+0.25, by, 3.4, 0.65, size=9.5, color=TEXT_BODY)
        by += 0.72

# --- SLIDE 20: Conclusion, Limitations & Future Scope ---
sl20 = create_slide_base(20, "19 / Conclusion & Future Work", "Project Summary, Production Audit & Future Roadmap", "Vishnu Reddy", "URK24CS1163", CLR_VISHNU)

# Left Column: Key Achievements
add_rounded_rect(sl20, 0.5, 1.45, 5.8, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl20, "Core Project Achievements", 0.75, 1.7, 5.3, 0.35, size=13, bold=True, color=CLR_VICTOR)

add_txt(sl20, "• End-to-End Relational Integration:\n   Ingested, validated, and indexed 10,030 documents across five disparate banking sources into MongoDB.\n\n• Rigorous Statistical & ML Pipeline:\n   - Two-sample t-test confirmed p = 6.93 × 10⁻¹⁷ significance.\n   - Benchmarked 4 classifiers across approval, default, and repayment.\n\n• Production-Grade Latency:\n   Reduced underwriting turnaround from days to under 500 ms.\n\n• Explainable AI Underwriting:\n   Eliminated black-box decisions with explicit reason codes (R01-R05) in the Customer 360° drawer.", 0.75, 2.15, 5.3, 4.4, size=10, color=TEXT_BODY)

# Right Column: Limitations & Future Scope
add_rounded_rect(sl20, 6.6, 1.45, 6.233, 5.4, fill=CARD_BG, line=BORDER_SUBTLE)
add_txt(sl20, "Production Audit & Future Scope", 6.85, 1.7, 5.7, 0.35, size=13, bold=True, color=CLR_VISHNU)

add_txt(sl20, "• Pre-Production Audit Findings:\n   - Address default recall (17.4% on Decision Tree) via SMOTE or focal loss.\n   - Audit approval model feature set to verify zero downstream leakage.\n\n• Planned Future Enhancements:\n   1. Real-Time Open Banking / UPI APIs:\n      Ingest live transaction feeds for gig workers and self-employed.\n   2. Explainable AI (SHAP / LIME):\n      Generate granular local feature attribution force plots for rejected applicants.\n   3. Sequential Deep Learning (LSTM):\n      Model continuous installment time-series to catch early delinquency.", 0.85, 2.15, 5.7, 4.4, size=10, color=TEXT_BODY)

# Save the presentation
output_path = r"C:\Users\omvis\.gemini\antigravity\scratch\financial-risk-dashboard\FinRisk360_20_Slides_Light.pptx"
prs.save(output_path)
print(f"SUCCESS: 20-slide presentation saved to {output_path}")
