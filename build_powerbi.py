import json
import zipfile
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

print("Processing master dataset for Power BI...")
c1 = pd.read_csv(os.path.join(DATA_DIR, '01_bank_customers_1000.csv'))
c2 = pd.read_csv(os.path.join(DATA_DIR, '02_loan_applications_1000.csv'))
c3 = pd.read_csv(os.path.join(DATA_DIR, '03_repayment_history_6000.csv'))
c4 = pd.read_csv(os.path.join(DATA_DIR, '04_credit_risk_1000.csv'))
c5 = pd.read_csv(os.path.join(DATA_DIR, '05_loan_rejection_reasons_1000.csv'))

# Repayment aggregates per Customer_ID
rep_summary = c3.groupby('Customer_ID').agg(
    Total_Installments=('Installment_Number', 'count'),
    Total_Due_INR=('Due_Amount_INR', 'sum'),
    Total_Paid_INR=('Paid_Amount_INR', 'sum'),
    On_Time_Payments=('Repayment_Status', lambda s: (s == 'On Time').sum()),
    Late_Payments_Recorded=('Repayment_Status', lambda s: (s == 'Late').sum()),
    Missed_Payments_Recorded=('Repayment_Status', lambda s: (s == 'Missed').sum()),
    Max_Days_Late=('Days_Late', 'max')
).reset_index()

# Merge into Master Analytics DataFrame
df = c1.merge(c2.drop(columns=['Rejection_Reason_Code', 'Rejection_Reason'], errors='ignore'), on='Customer_ID', how='left')
df = df.merge(c4.drop(columns=['Monthly_Income_INR', 'Outstanding_Debt_INR', 'Delayed_Payment_Days', 'Late_Payments', 'Previous_Defaults', 'Previous_Loans', 'Debt_to_Income_Ratio', 'Credit_Score'], errors='ignore'), on=['Customer_ID', 'Loan_ID'], how='left')
df = df.merge(c5.drop(columns=['Loan_Approval_Status'], errors='ignore'), on=['Customer_ID', 'Loan_ID'], how='left')
df = df.merge(rep_summary, on='Customer_ID', how='left')

# Categorical Bins
def score_band(s):
    if pd.isna(s): return 'Unknown'
    if s < 580: return '<580 (Poor)'
    if s < 670: return '580-669 (Fair)'
    if s < 740: return '670-739 (Good)'
    if s < 800: return '740-799 (Very Good)'
    return '800+ (Exceptional)'

def inc_band(inc):
    if pd.isna(inc): return 'Unknown'
    if inc < 25000: return '<₹25k (Low)'
    if inc < 50000: return '₹25k-₹50k (Lower-Mid)'
    if inc < 75000: return '₹50k-₹75k (Mid)'
    if inc < 100000: return '₹75k-₹1L (Upper-Mid)'
    return '>₹1L (Affluent)'

def dti_band(d):
    if pd.isna(d): return 'Unknown'
    if d < 0.20: return '<20% (Conservative)'
    if d < 0.35: return '20%-35% (Moderate)'
    if d < 0.50: return '35%-50% (High)'
    return '>50% (Critical)'

df['Credit_Score_Band'] = df['Credit_Score'].apply(score_band)
df['Income_Band'] = df['Monthly_Income_INR'].apply(inc_band)
df['DTI_Band'] = df['Debt_to_Income_Ratio'].apply(dti_band)
df['Approval_Flag'] = (df['Loan_Approval_Status'] == 'Approved').astype(int)
df['Default_Flag'] = (df['Loan_Default'] == 'Yes').astype(int)

master_csv = os.path.join(BASE_DIR, "Financial_Loan_Credit_Risk_PowerBI_Master.csv")
df.to_csv(master_csv, index=False)
print("Master CSV saved:", master_csv, f"({len(df)} records)")

# Power Query M expression with normalized path
csv_m_path = master_csv.replace('\\', '/')

m_code_lines = [
    "let",
    f'    Source = Csv.Document(File.Contents("{csv_m_path}"),[Delimiter=",", Columns={len(df.columns)}, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{',
    '        {"Customer_ID", type text},',
    '        {"Customer_Name", type text},',
    '        {"Age", Int64.Type},',
    '        {"Gender", type text},',
    '        {"City", type text},',
    '        {"Account_Type", type text},',
    '        {"Account_Balance_INR", type number},',
    '        {"Credit_Score", Int64.Type},',
    '        {"Employment_Type", type text},',
    '        {"Education", type text},',
    '        {"Loan_ID", type text},',
    '        {"Loan_Type", type text},',
    '        {"Loan_Purpose", type text},',
    '        {"Loan_Amount_INR", type number},',
    '        {"Loan_Term_Months", Int64.Type},',
    '        {"Interest_Rate_Percent", type number},',
    '        {"Monthly_Income_INR", type number},',
    '        {"Annual_Income_INR", type number},',
    '        {"Debt_to_Income_Ratio", type number},',
    '        {"Loan_Approval_Status", type text},',
    '        {"Credit_Risk", type text},',
    '        {"Credit_Score_Band", type text},',
    '        {"Income_Band", type text},',
    '        {"DTI_Band", type text},',
    '        {"Approval_Flag", Int64.Type},',
    '        {"Default_Flag", Int64.Type}',
    '    })',
    "in",
    '    #"Changed Type"'
]

# Build DataModelSchema for Power BI
columns_meta = []
for col in df.columns:
    dtype = df[col].dtype
    if 'int' in str(dtype):
        pbi_type = "int64"
    elif 'float' in str(dtype):
        pbi_type = "double"
    else:
        pbi_type = "string"
    columns_meta.append({"name": col, "dataType": pbi_type, "sourceColumn": col})

measures = [
    {"name": "Total Borrowers", "expression": "COUNTROWS('Loan_Risk_Master')"},
    {"name": "Total Requested Loan INR", "expression": "SUM('Loan_Risk_Master'[Loan_Amount_INR])"},
    {"name": "Total Disbursed INR", "expression": "CALCULATE(SUM('Loan_Risk_Master'[Loan_Amount_INR]), 'Loan_Risk_Master'[Loan_Approval_Status] = \"Approved\")"},
    {"name": "Avg Credit Score", "expression": "AVERAGE('Loan_Risk_Master'[Credit_Score])"},
    {"name": "Avg Monthly Income", "expression": "AVERAGE('Loan_Risk_Master'[Monthly_Income_INR])"},
    {"name": "Approved Applications", "expression": "CALCULATE(COUNTROWS('Loan_Risk_Master'), 'Loan_Risk_Master'[Loan_Approval_Status] = \"Approved\")"},
    {"name": "Rejected Applications", "expression": "CALCULATE(COUNTROWS('Loan_Risk_Master'), 'Loan_Risk_Master'[Loan_Approval_Status] = \"Rejected\")"},
    {"name": "Approval Rate %", "expression": "DIVIDE([Approved Applications], [Total Borrowers], 0) * 100"},
    {"name": "Default Rate %", "expression": "DIVIDE(CALCULATE(COUNTROWS('Loan_Risk_Master'), 'Loan_Risk_Master'[Loan_Default] = \"Yes\"), [Total Borrowers], 0) * 100"}
]

data_model_schema = {
    "name": "Financial_Risk_SemanticModel",
    "compatibilityLevel": 1550,
    "model": {
        "culture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True
        },
        "tables": [
            {
                "name": "Loan_Risk_Master",
                "columns": columns_meta,
                "partitions": [
                    {
                        "name": "Loan_Risk_Master-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": m_code_lines
                        }
                    }
                ],
                "measures": measures
            }
        ]
    }
}

layout = {
    "version": "5.3",
    "themeCollection": {
        "baseTheme": {"name": "CY20R01", "version": "5.2.0"}
    },
    "pages": [
        {
            "name": "Page1",
            "displayName": "1. Loan Approval Dashboard",
            "width": 1280,
            "height": 720,
            "visuals": []
        },
        {
            "name": "Page2",
            "displayName": "2. Income Analysis",
            "width": 1280,
            "height": 720,
            "visuals": []
        },
        {
            "name": "Page3",
            "displayName": "3. Credit Score Distribution",
            "width": 1280,
            "height": 720,
            "visuals": []
        }
    ]
}

pbit_path = os.path.join(BASE_DIR, "Financial_Credit_Risk_Dashboard.pbit")
with zipfile.ZipFile(pbit_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("DataModelSchema", json.dumps(data_model_schema, indent=2))
    z.writestr("Layout", json.dumps(layout, indent=2))
    z.writestr("Version", "2.115.0.0")

print("Power BI Template file created successfully at:", pbit_path)
