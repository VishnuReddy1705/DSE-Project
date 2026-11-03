# FinRisk 360 - Financial Loan & Credit Risk Management Dashboard

FinRisk 360 is a full-stack, enterprise-grade financial loan and credit risk intelligence dashboard. It directly interconnects and synchronizes across the 5 datasets from `financial_loan_credit_risk_datasets` into a live MongoDB database, providing unified search, automated risk scoring, multi-dataset 360° borrower profiles, analytics charts, and a dataset explorer.

---

## 🏗 Architecture & Connected Datasets

All records across the following 5 datasets are imported and indexed in MongoDB (`financial_risk_db`):

| # | Dataset / Collection | Primary / Foreign Keys | Description |
|---|---|---|---|
| **01** | `bank_customers` | `Customer_ID` (PK) | Customer profile, demographics, account type, balance, KYC, employment, marital status |
| **02** | `loan_applications` | `Loan_ID` (PK), `Customer_ID` (FK) | Loan amounts, terms, interest rates, monthly/annual income, EMI, debt-to-income (DTI) |
| **03** | `repayment_history` | `Repayment_ID` (PK), `Loan_ID` (FK), `Customer_ID` (FK) | 6 monthly installment schedules per borrower, payment dates, amounts, days late, status |
| **04** | `credit_risk` | `Loan_ID` (FK), `Customer_ID` (FK) | Credit score, debt-to-income ratio, risk tier (Low / Medium / High), default prediction |
| **05** | `loan_rejection_reasons` | `Loan_ID` (FK), `Customer_ID` (FK) | Loan approval status, rejection reason codes (R01–R05), and official justification |

---

## ✨ Core Features

1. **Live Common Key Search & Sorting (Initial Dashboard Page)**:
   - Search by Borrower Name (`Customer_Name`), Customer ID (`Customer_ID`), Loan ID (`Loan_ID`), or City.
   - Dynamic sorting by Customer Name, Customer ID, Credit Score, Account Balance, Age, and City.
   - Filter chips for Credit Risk (`Low`, `Medium`, `High`) and Approval Status (`Approved`, `Rejected`).

2. **Customer 360° Profile (When Clicked)**:
   - Clicking any borrower profile opens an all-inclusive 360° drawer showing **all 5 connected datasets** for that person:
     - **Sheet 01**: Banking Demographics & Account Details
     - **Sheet 02**: Loan Application Details (Amount, Terms, DTI, Co-applicant, EMI)
     - **Sheet 04**: Credit Risk & Default Prediction
     - **Sheet 05**: Loan Evaluation Status & Rejection Explanation
     - **Sheet 03**: Complete Installment Schedule & Payment Track Record

3. **Add New Customer with Full 5-Dataset Synchronization**:
   - Comprehensive form modal collecting all required parameters.
   - Automatically computes:
     - Sequential `Customer_ID` (e.g. `BANK1001`) and `Loan_ID` (e.g. `LN1001`).
     - Debt-to-Income (DTI) and monthly EMI amortization.
     - Credit Risk Tier (`Low`, `Medium`, `High`).
     - Loan Approval / Rejection decision with reason codes (`R01` to `R05`).
     - 6-month repayment installment schedule.
   - Atomically writes to MongoDB across all 5 collections and appends to the dataset CSV files to guarantee complete synchronization.

4. **Visual Analytics & Financial Charts**:
   - **Credit Risk Classification**: Interactive doughnut chart breaking down Low vs. Medium vs. High risk borrowers.
   - **Loan Approval vs. Rejection**: Doughnut chart of accepted applications versus rejected applications.
   - **Loan Distribution by Category**: Bar chart showing volume across Business, Home, Vehicle, Personal, and Education loans.
   - **Repayment Track Record**: Performance breakdown across On-Time, Late, and Missed installments.
   - **KPI Summary Cards**: Disbursed portfolio value (₹ Cr), Average credit score, Total borrowers, Approval rate, and Default rate.

5. **Datasets Explorer Icon**:
   - A dedicated **Datasets Explorer** icon button on the top navigation bar.
   - Neatly explores all 10,000+ records across all 5 datasets in an interactive tabular view.
   - Supports search across any column, click-to-sort headers, page-size selection, and direct **Export CSV** download.

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- MongoDB Server running on `localhost:27017`

### Start Server
```powershell
cd "C:\Users\omvis\.gemini\antigravity\scratch\financial-risk-dashboard"
python run.py
```
Open your browser at: **[http://localhost:8000](http://localhost:8000)**
