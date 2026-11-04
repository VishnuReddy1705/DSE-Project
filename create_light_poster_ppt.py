from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Light Theme Colors (Canva / Modern Academic Style)
BG_LIGHT    = RGBColor(0xF8, 0xFA, 0xFC) # #F8FAFC
CARD_BG     = RGBColor(0xFF, 0xFF, 0xFF) # #FFFFFF
BORDER_CLR  = RGBColor(0xE2, 0xE8, 0xF0) # #E2E8F0
PRIMARY_BLU = RGBColor(0x1E, 0x40, 0xAF) # #1E40AF (Karunya Navy/Blue)
ACCENT_CYAN = RGBColor(0x02, 0x84, 0xC7) # #0284C7
EMERALD_GRN = RGBColor(0x05, 0x96, 0x69) # #059669
AMBER_GOLD  = RGBColor(0xD9, 0x77, 0x06) # #D97706
ROSE_RED    = RGBColor(0xDC, 0x26, 0x26) # #DC2626
PURPLE_ACC  = RGBColor(0x7C, 0x3A, 0xED) # #7C3AED
TEXT_MAIN   = RGBColor(0x0F, 0x17, 0x2A) # #0F172A
TEXT_MUTED  = RGBColor(0x64, 0x74, 0x8B) # #64748B
DARK_GRAY   = RGBColor(0x33, 0x41, 0x55) # #334155

prs = Presentation()
prs.slide_width  = Inches(16.0) # Widescreen 16:9 large poster format
prs.slide_height = Inches(9.0)

blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)

def add_rect(s, l, t, w, h, fill=None, line=None, line_w=Pt(1)):
    shp = s.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shp.line.width = line_w
    if fill:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = line
    else:
        shp.line.fill.background()
    return shp

def add_txt(s, text, l, t, w, h, size=14, bold=False, color=TEXT_MAIN, align=PP_ALIGN.LEFT, italic=False):
    tb = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.italic = italic
    run.font.name = "Arial"
    return tb

# 1. Main Background
add_rect(slide, 0, 0, 16.0, 9.0, fill=BG_LIGHT)

# 2. Top Header Container
add_rect(slide, 0.4, 0.3, 15.2, 1.4, fill=CARD_BG, line=BORDER_CLR)

# Institution Branding Left
add_txt(slide, "Karunya", 0.6, 0.38, 2.8, 0.4, size=24, bold=True, color=ROSE_RED)
add_txt(slide, "DEEMED UNIVERSITY", 0.6, 0.8, 2.8, 0.25, size=9, bold=True, color=TEXT_MUTED)
add_txt(slide, "NAAC Accredited A++ | Solving Human Problems", 0.6, 1.05, 2.8, 0.25, size=8, color=AMBER_GOLD, bold=True)

# Title & Authors Center
add_txt(slide, "Dynamic Financial Reliability Scoring for Loan Approval & Credit Risk Analysis", 3.4, 0.35, 9.2, 0.5, size=18, bold=True, color=TEXT_MAIN, align=PP_ALIGN.CENTER)
add_txt(slide, "Jenoh Sam  |  Vishnu Reddy  |  Victor Richard  |  Samritha", 3.4, 0.82, 9.2, 0.35, size=12, bold=True, color=PRIMARY_BLU, align=PP_ALIGN.CENTER)
add_txt(slide, "Supervisor: Dr. A. M. Anusha Bamini  |  Department of Computer Science & Engineering", 3.4, 1.15, 9.2, 0.3, size=10, italic=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER)

# Showcase Badge Right
add_txt(slide, "Karunya", 13.0, 0.4, 2.4, 0.3, size=14, bold=True, color=TEXT_MAIN, align=PP_ALIGN.RIGHT)
add_txt(slide, "GLOBAL SHOWCASE", 13.0, 0.7, 2.4, 0.3, size=10, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.RIGHT)
add_txt(slide, "2026", 13.0, 0.95, 2.4, 0.4, size=20, bold=True, color=PRIMARY_BLU, align=PP_ALIGN.RIGHT)

# 3. 4-Member Work Allocation Ribbon
alloc_y = 1.8
add_rect(slide, 0.4, alloc_y, 15.2, 0.6, fill=RGBColor(0xEE, 0xF2, 0xFF), line=RGBColor(0xC7, 0xD2, 0xFE))
members = [
    ("Jenoh Sam (Lead)", "Part 1: Data Preparation & Pipelines", PRIMARY_BLU, 0.6),
    ("Vishnu Reddy", "Part 2: EDA, Statistics & Correlation", EMERALD_GRN, 4.4),
    ("Victor Richard", "Part 3: 8 Signals & 4 ML Classifiers", AMBER_GOLD, 8.2),
    ("Samritha", "Part 4: MongoDB & Power BI Dashboard", PURPLE_ACC, 12.0)
]
for name, role, clr, x in members:
    add_rect(slide, x, alloc_y+0.1, 0.4, 0.4, fill=clr)
    add_txt(slide, name, x+0.48, alloc_y+0.07, 3.0, 0.25, size=10, bold=True, color=TEXT_MAIN)
    add_txt(slide, role, x+0.48, alloc_y+0.32, 3.0, 0.25, size=8.5, color=DARK_GRAY)

# 4. 3 Columns Layout
col_w = 4.88
col1_x = 0.4
col2_x = 5.56
col3_x = 10.72
content_y = 2.5
card_h1 = 5.9

# ─── COLUMN 1: INTRO, DATASETS & METHODS (JENOH SAM) ───
add_rect(slide, col1_x, content_y, col_w, card_h1, fill=CARD_BG, line=BORDER_CLR)
add_rect(slide, col1_x, content_y, col_w, 0.06, fill=PRIMARY_BLU)
add_txt(slide, "1. Introduction & Methodology", col1_x+0.2, content_y+0.15, 4.4, 0.35, size=13, bold=True, color=PRIMARY_BLU)

intro_body = (
    "• Problem: Traditional underwriting relies on fixed salaries & credit history, unfairly rejecting gig workers and self-employed people.\n\n"
    "• Solution: Dynamic Financial Reliability Score (FRS, 0–100) reflecting real-time money management without age, gender, or marital bias.\n\n"
    "• Datasets Analyzed:\n"
    "   - Loan Prediction: 614 applicants × 13 attributes\n"
    "   - UCI Credit Card Default: 30,000 clients × 6 months\n\n"
    "• 5-Phase Pipeline: Data Prep → EDA/Stats → Feature Eng (8 signals) → Machine Learning → Big Data & BI."
)
add_txt(slide, intro_body, col1_x+0.2, content_y+0.55, 4.48, 2.5, size=9.5, color=DARK_GRAY)

# FRS Formula Box inside Col 1
box_y = content_y + 3.2
add_rect(slide, col1_x+0.2, box_y, 4.48, 1.0, fill=PRIMARY_BLU)
add_txt(slide, "DYNAMIC FINANCIAL RELIABILITY SCORE (FRS)", col1_x+0.3, box_y+0.08, 4.2, 0.25, size=9, bold=True, color=RGBColor(0x93, 0xC5, 0xFD), align=PP_ALIGN.CENTER)
add_txt(slide, "FRS = 100 × (1 − P(default))", col1_x+0.3, box_y+0.32, 4.2, 0.35, size=13, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), align=PP_ALIGN.CENTER)
add_txt(slide, "Random Forest, 5-Fold Out-of-Fold Calibration", col1_x+0.3, box_y+0.68, 4.2, 0.25, size=8.5, color=RGBColor(0xBF, 0xDB, 0xFE), align=PP_ALIGN.CENTER)

# 4 Tier Badges
tiers_y = box_y + 1.15
t_w = 1.05
tiers_data = [
    ("Tier A", "≥ 80 (6.5%)", EMERALD_GRN, col1_x+0.2),
    ("Tier B", "60–79 (12.8%)", AMBER_GOLD, col1_x+0.2+t_w+0.09),
    ("Tier C", "40–59 (22.4%)", RGBColor(0xEA, 0x58, 0x0C), col1_x+0.2+(t_w+0.09)*2),
    ("Tier D", "< 40 (55.0%)", ROSE_RED, col1_x+0.2+(t_w+0.09)*3)
]
for t_lbl, t_sub, t_bg, tx in tiers_data:
    add_rect(slide, tx, tiers_y, t_w, 0.6, fill=t_bg)
    add_txt(slide, t_lbl, tx, tiers_y+0.05, t_w, 0.25, size=9.5, bold=True, color=RGBColor(0xFF,0xFF,0xFF), align=PP_ALIGN.CENTER)
    add_txt(slide, t_sub, tx, tiers_y+0.3, t_w, 0.25, size=7.5, color=RGBColor(0xFF,0xFF,0xFF), align=PP_ALIGN.CENTER)

add_txt(slide, "Speaker: Jenoh Sam (Part 1 Lead)", col1_x+0.2, content_y+5.4, 4.4, 0.25, size=8.5, bold=True, color=PRIMARY_BLU)

# ─── COLUMN 2: STATS, CORRELATION & ML (VISHNU & VICTOR) ───
add_rect(slide, col2_x, content_y, col_w, card_h1, fill=CARD_BG, line=BORDER_CLR)
add_rect(slide, col2_x, content_y, col_w, 0.06, fill=EMERALD_GRN)
add_txt(slide, "2. Statistical EDA & Machine Learning", col2_x+0.2, content_y+0.15, 4.4, 0.35, size=13, bold=True, color=EMERALD_GRN)

eda_txt = (
    "• Approval Drivers (χ² Tests):\n"
    "   - Credit history: χ² = 180.1, p < 10⁻³⁹ (Good: 79.6% vs Bad: 7.9%)\n"
    "   - Self-employment: χ² = 0.00, p = 1.00 (Salaried: 68.8% vs Self-emp: 68.3%)\n"
    "   - Income: Welch's t-test p = 0.87 (No statistical difference!)\n\n"
    "• Default Correlation (Pearson r, n = 29,965):\n"
    "   - Delays (+0.40) & Longest Delay (+0.37) raise risk\n"
    "   - Payment-to-bill (-0.10) & Avg payment (-0.15) lower risk"
)
add_txt(slide, eda_txt, col2_x+0.2, content_y+0.55, 4.48, 2.1, size=9.0, color=DARK_GRAY)

# Model Benchmark Table
tbl_y = content_y + 2.8
add_txt(slide, "Table 1: Model Benchmark (Test Set, n = 123)", col2_x+0.2, tbl_y, 4.4, 0.25, size=9.5, bold=True, color=TEXT_MAIN)

tbl_shape = slide.shapes.add_table(5, 5, Inches(col2_x+0.2), Inches(tbl_y+0.3), Inches(4.48), Inches(1.3))
tbl = tbl_shape.table
tbl.columns[0].width = Inches(1.58)
tbl.columns[1].width = Inches(0.72)
tbl.columns[2].width = Inches(0.72)
tbl.columns[3].width = Inches(0.72)
tbl.columns[4].width = Inches(0.74)

headers = ["Model", "Acc %", "Prec %", "Rec %", "F1 %"]
for i, h in enumerate(headers):
    cell = tbl.cell(0, i)
    cell.text = h
    cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(0xF1, 0xF5, 0xF9)
    for p in cell.text_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        for r in p.runs:
            r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = TEXT_MAIN

rows_data = [
    ("Logistic Reg.", "85.4", "83.2", "98.8", "90.3"),
    ("Decision Tree", "85.4", "83.2", "98.8", "90.3"),
    ("Random Forest", "81.3", "81.0", "95.3", "87.6"),
    ("KNN (k=5)", "75.6", "75.2", "96.5", "84.5")
]
for row_idx, r_data in enumerate(rows_data):
    for col_idx, val in enumerate(r_data):
        cell = tbl.cell(row_idx+1, col_idx)
        cell.text = val
        cell.fill.solid()
        if row_idx < 2:
            cell.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xFF)
        else:
            cell.fill.fore_color.rgb = CARD_BG
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER
            for r in p.runs:
                r.font.size = Pt(8.0); r.font.color.rgb = TEXT_MAIN

# ROC-AUC Gain Callout
auc_box_y = tbl_y + 1.75
add_rect(slide, col2_x+0.2, auc_box_y, 4.48, 0.7, fill=RGBColor(0xEC, 0xFD, 0xF5), line=EMERALD_GRN)
add_txt(slide, "ROC-AUC GAIN: Static Profile (0.62) → Dynamic FRS (0.77)", col2_x+0.3, auc_box_y+0.08, 4.28, 0.25, size=9.5, bold=True, color=EMERALD_GRN, align=PP_ALIGN.CENTER)
add_txt(slide, "+0.15 average AUC boost across all 4 machine learning models!", col2_x+0.3, auc_box_y+0.35, 4.28, 0.25, size=8.5, color=DARK_GRAY, align=PP_ALIGN.CENTER)

add_txt(slide, "Speakers: Vishnu Reddy (Part 2) & Victor Richard (Part 3)", col2_x+0.2, content_y+5.4, 4.4, 0.25, size=8.5, bold=True, color=EMERALD_GRN)

# ─── COLUMN 3: BIG DATA, DASHBOARD & DISCUSSIONS (SAMRITHA) ───
add_rect(slide, col3_x, content_y, col_w, card_h1, fill=CARD_BG, line=BORDER_CLR)
add_rect(slide, col3_x, content_y, col_w, 0.06, fill=PURPLE_ACC)
add_txt(slide, "3. Big Data, Power BI & Discussions", col3_x+0.2, content_y+0.15, 4.4, 0.35, size=13, bold=True, color=PURPLE_ACC)

# 4 KPIs in 2x2 grid
kpi_w = 2.18
kpi_h = 0.65
kpi_data = [
    ("0.78", "FRS Model ROC-AUC", PRIMARY_BLU, col3_x+0.2, content_y+0.55),
    ("+0.15", "AUC Gain vs Static", EMERALD_GRN, col3_x+2.5, content_y+0.55),
    ("8.4 ×", "Risk Spread (D vs A)", ROSE_RED, col3_x+0.2, content_y+1.28),
    ("0", "Protected Bias Signals", PURPLE_ACC, col3_x+2.5, content_y+1.28)
]
for kv, kl, kc, kx, ky in kpi_data:
    add_rect(slide, kx, ky, kpi_w, kpi_h, fill=RGBColor(0xF8, 0xFA, 0xFC), line=BORDER_CLR)
    add_txt(slide, kv, kx, ky+0.05, kpi_w, 0.35, size=15, bold=True, color=kc, align=PP_ALIGN.CENTER)
    add_txt(slide, kl, kx, ky+0.38, kpi_w, 0.22, size=7.5, bold=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER)

# MapReduce to Mongo Box
mr_y = content_y + 2.05
add_rect(slide, col3_x+0.2, mr_y, 4.48, 0.95, fill=RGBColor(0xF1, 0xF5, 0xF9))
add_txt(slide, "HDFS MapReduce → MongoDB Sync Pipeline (29,965 Clients)", col3_x+0.3, mr_y+0.06, 4.28, 0.25, size=8.5, bold=True, color=TEXT_MAIN)
add_txt(slide, "HDFS Records → Map(tier, default) → Shuffle → Reduce(Σ stats) → MongoDB JSON Docs", col3_x+0.3, mr_y+0.32, 4.28, 0.3, size=7.5, color=DARK_GRAY)
add_txt(slide, "MapReduce & MongoDB return identical stats to Pandas in <25 ms latency.", col3_x+0.3, mr_y+0.62, 4.28, 0.25, size=7.5, italic=True, color=EMERALD_GRN)

# Discussions
disc_y = mr_y + 1.1
discussions_txt = (
    "• Takeaway 1: Today's approvals strictly reproduce rigid credit rules (χ²=180.1), ignoring income (p=0.87).\n\n"
    "• Takeaway 2: Dynamic behavioural signals elevate AUC from 0.62 to 0.77 and cleanly separate Tier A (6.5% default) from Tier D (55.0%).\n\n"
    "• Takeaway 3: MongoDB and MapReduce pipelines ensure instant scalability to millions of loan applications in real time.\n\n"
    "• Future Work: Live UPI / Open Banking APIs, SHAP explainability audits, and LSTM continuous repayment monitoring."
)
add_txt(slide, discussions_txt, col3_x+0.2, disc_y, 4.48, 2.1, size=8.8, color=DARK_GRAY)

add_txt(slide, "Speaker: Samritha (Part 4 Lead)", col3_x+0.2, content_y+5.4, 4.4, 0.25, size=8.5, bold=True, color=PURPLE_ACC)

# 5. Bottom Status Bar
add_rect(slide, 0.4, 8.5, 15.2, 0.35, fill=CARD_BG, line=BORDER_CLR)
add_txt(slide, "Karunya Global Showcase 2026 | Department of Computer Science & Engineering", 0.6, 8.57, 6.0, 0.25, size=8.5, color=TEXT_MUTED)
add_txt(slide, "Live System: http://localhost:8000  |  GitHub: VishnuReddy1705/DSE-Project", 8.0, 8.57, 7.4, 0.25, size=8.5, bold=True, color=PRIMARY_BLU, align=PP_ALIGN.RIGHT)

out_pptx = r"C:\Users\omvis\.gemini\antigravity\scratch\financial-risk-dashboard\Karunya_Poster_Light.pptx"
prs.save(out_pptx)
print("Saved light poster PPTX to:", out_pptx)
