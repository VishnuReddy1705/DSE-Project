import os
import io
import math
from datetime import datetime, timedelta
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
import subprocess
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from db import get_db, init_database, clean_record, DATA_DIR

app = FastAPI(title="FinRisk 360 - Financial Loan & Credit Risk System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure database is initialized on startup
@app.on_event("startup")
def startup_event():
    try:
        init_database(force_reload=False)
        print("MongoDB connection verified & collections ready.")
    except Exception as e:
        print("Warning during startup DB check:", e)

@app.get("/api/health")
def health_check():
    try:
        db = get_db()
        counts = {
            "bank_customers": db.bank_customers.count_documents({}),
            "loan_applications": db.loan_applications.count_documents({}),
            "repayment_history": db.repayment_history.count_documents({}),
            "credit_risk": db.credit_risk.count_documents({}),
            "loan_rejection_reasons": db.loan_rejection_reasons.count_documents({}),
        }
        return {"status": "healthy", "database": "financial_risk_db", "counts": counts}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/api/stats")
def get_stats():
    db = get_db()
    total_customers = db.bank_customers.count_documents({})
    total_loans = db.loan_applications.count_documents({})
    
    # Aggregation for loan metrics
    loans = list(db.loan_applications.find({}, {
        "Loan_Amount_INR": 1,
        "Loan_Approval_Status": 1,
        "Loan_Type": 1,
        "Loan_Purpose": 1,
        "Interest_Rate_Percent": 1
    }))
    
    total_disbursed = sum(l.get("Loan_Amount_INR", 0) or 0 for l in loans if l.get("Loan_Approval_Status") == "Approved")
    total_requested = sum(l.get("Loan_Amount_INR", 0) or 0 for l in loans)
    
    approved_count = sum(1 for l in loans if l.get("Loan_Approval_Status") == "Approved")
    rejected_count = sum(1 for l in loans if l.get("Loan_Approval_Status") == "Rejected")
    approval_rate = round((approved_count / total_loans * 100), 1) if total_loans > 0 else 0
    
    # Credit Risk aggregations
    risks = list(db.credit_risk.find({}, {"Credit_Score": 1, "Credit_Risk": 1, "Loan_Default": 1}))
    total_credit_score = sum(r.get("Credit_Score", 0) or 0 for r in risks)
    avg_credit_score = round(total_credit_score / len(risks), 1) if risks else 0
    
    risk_counts = {"Low": 0, "Medium": 0, "High": 0}
    default_counts = {"Yes": 0, "No": 0}
    score_brackets = {"<580 (Poor)": 0, "580-669 (Fair)": 0, "670-739 (Good)": 0, "740-799 (Very Good)": 0, "800+ (Exceptional)": 0}

    for r in risks:
        rk = r.get("Credit_Risk")
        if rk in risk_counts:
            risk_counts[rk] += 1
        ld = r.get("Loan_Default")
        if ld in default_counts:
            default_counts[ld] += 1
            
        sc = r.get("Credit_Score", 0) or 0
        if sc < 580:
            score_brackets["<580 (Poor)"] += 1
        elif sc < 670:
            score_brackets["580-669 (Fair)"] += 1
        elif sc < 740:
            score_brackets["670-739 (Good)"] += 1
        elif sc < 800:
            score_brackets["740-799 (Very Good)"] += 1
        else:
            score_brackets["800+ (Exceptional)"] += 1

    default_rate = round((default_counts["Yes"] / len(risks) * 100), 1) if risks else 0

    # Loan types and purposes breakdown
    loan_types = {}
    loan_purposes = {}
    for l in loans:
        lt = l.get("Loan_Type", "Other")
        loan_types[lt] = loan_types.get(lt, 0) + 1
        lp = l.get("Loan_Purpose", "Other")
        loan_purposes[lp] = loan_purposes.get(lp, 0) + 1

    # Repayment breakdown
    repayments = list(db.repayment_history.find({}, {"Repayment_Status": 1}))
    repayment_stats = {"On Time": 0, "Late": 0, "Missed": 0}
    for rp in repayments:
        st = rp.get("Repayment_Status", "Other")
        if st in repayment_stats:
            repayment_stats[st] += 1

    return {
        "kpis": {
            "total_customers": total_customers,
            "total_loans": total_loans,
            "total_disbursed_inr": total_disbursed,
            "total_requested_inr": total_requested,
            "approval_rate": approval_rate,
            "approved_count": approved_count,
            "rejected_count": rejected_count,
            "avg_credit_score": avg_credit_score,
            "default_count": default_counts["Yes"],
            "default_rate": default_rate
        },
        "charts": {
            "credit_risk": risk_counts,
            "approval_status": {"Approved": approved_count, "Rejected": rejected_count},
            "loan_types": loan_types,
            "loan_purposes": loan_purposes,
            "repayment_status": repayment_stats,
            "credit_score_brackets": score_brackets
        }
    }

@app.get("/api/customers")
def get_customers(
    search: Optional[str] = "",
    sort_by: Optional[str] = "Customer_ID",
    sort_order: Optional[str] = "asc",
    risk: Optional[str] = None,
    approval: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200)
):
    db = get_db()
    
    # Build match query for customer
    query = {}
    if search:
        search_term = search.strip()
        query["$or"] = [
            {"Customer_Name": {"$regex": search_term, "$options": "i"}},
            {"Customer_ID": {"$regex": search_term, "$options": "i"}},
            {"City": {"$regex": search_term, "$options": "i"}},
            {"Email": {"$regex": search_term, "$options": "i"}},
            {"Phone": {"$regex": search_term, "$options": "i"}},
        ]
        
    direction = 1 if sort_order.lower() == "asc" else -1
    sort_field = sort_by if sort_by in [
        "Customer_ID", "Customer_Name", "Credit_Score", "Account_Balance_INR", "Age", "City"
    ] else "Customer_ID"

    # Fetch matching customers
    cursor = db.bank_customers.find(query, {"_id": 0})
    if sort_field in ["Customer_ID", "Customer_Name", "Credit_Score", "Account_Balance_INR", "Age", "City"]:
        cursor = cursor.sort([(sort_field, direction)])

    all_matches = list(cursor)
    
    # Fast enrichment with loan and credit risk data
    if all_matches:
        cust_ids = [c["Customer_ID"] for c in all_matches]
        
        loans_map = {
            l["Customer_ID"]: l 
            for l in db.loan_applications.find({"Customer_ID": {"$in": cust_ids}}, {"_id": 0, "Customer_ID": 1, "Loan_ID": 1, "Loan_Type": 1, "Loan_Amount_INR": 1, "Loan_Approval_Status": 1})
        }
        
        risk_map = {
            r["Customer_ID"]: r
            for r in db.credit_risk.find({"Customer_ID": {"$in": cust_ids}}, {"_id": 0, "Customer_ID": 1, "Credit_Risk": 1, "Loan_Default": 1, "Credit_Score": 1})
        }
        
        enriched = []
        for c in all_matches:
            cid = c["Customer_ID"]
            loan = loans_map.get(cid, {})
            risk_info = risk_map.get(cid, {})
            
            c_loan_status = loan.get("Loan_Approval_Status", "N/A")
            c_risk = risk_info.get("Credit_Risk", "Unknown")
            
            # Apply risk and approval filters if given
            if risk and risk != "All" and c_risk.lower() != risk.lower():
                continue
            if approval and approval != "All" and c_loan_status.lower() != approval.lower():
                continue
                
            c_data = {
                **c,
                "Loan_ID": loan.get("Loan_ID"),
                "Loan_Type": loan.get("Loan_Type"),
                "Loan_Amount_INR": loan.get("Loan_Amount_INR"),
                "Loan_Approval_Status": c_loan_status,
                "Credit_Risk": c_risk,
                "Loan_Default": risk_info.get("Loan_Default", "No"),
                "Credit_Score": risk_info.get("Credit_Score") or c.get("Credit_Score")
            }
            enriched.append(c_data)
    else:
        enriched = []

    # Handle sorting on joined columns if requested
    if sort_field in ["Credit_Risk", "Loan_Amount_INR", "Loan_Approval_Status"]:
        enriched.sort(key=lambda x: (x.get(sort_field) is None, x.get(sort_field)), reverse=(direction == -1))

    total = len(enriched)
    start = (page - 1) * limit
    paged_results = enriched[start:start + limit]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": math.ceil(total / limit) if total > 0 else 1,
        "customers": paged_results
    }

@app.get("/api/customer/{customer_id}")
def get_customer_details(customer_id: str):
    db = get_db()
    cid = customer_id.strip().upper()
    
    # 1. Bank Customers
    cust = db.bank_customers.find_one({"Customer_ID": cid}, {"_id": 0})
    if not cust:
        # Fallback search by Loan_ID or Customer_Name
        loan_ref = db.loan_applications.find_one({"Loan_ID": cid}, {"_id": 0})
        if loan_ref:
            cid = loan_ref["Customer_ID"]
            cust = db.bank_customers.find_one({"Customer_ID": cid}, {"_id": 0})
        else:
            cust = db.bank_customers.find_one({"Customer_Name": {"$regex": f"^{cid}$", "$options": "i"}}, {"_id": 0})
            if cust:
                cid = cust["Customer_ID"]
                
    if not cust:
        raise HTTPException(status_code=404, detail=f"Customer with ID or Name '{customer_id}' not found.")

    # 2. Loan Applications
    loan = db.loan_applications.find_one({"Customer_ID": cid}, {"_id": 0}) or {}
    loan_id = loan.get("Loan_ID")

    # 3. Credit Risk
    risk = db.credit_risk.find_one({"Customer_ID": cid}, {"_id": 0}) or {}

    # 4. Rejection reasons
    rejection = db.loan_rejection_reasons.find_one({"Customer_ID": cid}, {"_id": 0}) or {}

    # 5. Repayment history (sorted by installment number)
    repayments = list(db.repayment_history.find({"Customer_ID": cid}, {"_id": 0}).sort("Installment_Number", 1))

    return {
        "customer": cust,
        "loan": loan,
        "credit_risk": risk,
        "rejection": rejection,
        "repayments": repayments
    }

class NewCustomerPayload(BaseModel):
    # Personal & Bank
    Customer_Name: str
    Age: int = Field(..., ge=18, le=100)
    Gender: str
    City: str
    Email: str
    Phone: str
    Account_Type: str
    Account_Balance_INR: float
    KYC_Status: str = "Verified"
    Employment_Type: str
    Education: str
    Marital_Status: str
    
    # Loan
    Loan_Type: str
    Loan_Purpose: str
    Loan_Amount_INR: float
    Loan_Term_Months: int
    Interest_Rate_Percent: float
    Monthly_Income_INR: float
    Monthly_Expenses_INR: float = 0.0
    Coapplicant_Income_INR: float = 0.0
    Existing_Loan_Amount_INR: float = 0.0
    Existing_EMI_INR: float = 0.0
    
    # Credit History & Risk
    Credit_Score: int = Field(..., ge=300, le=900)
    Previous_Loans: int = 0
    Previous_Defaults: int = 0
    Late_Payments: int = 0
    Delayed_Payment_Days: int = 0
    Outstanding_Debt_INR: float = 0.0

@app.post("/api/customer")
def add_new_customer(payload: NewCustomerPayload):
    db = get_db()
    
    # Compute next Customer_ID
    all_custs = list(db.bank_customers.find({}, {"Customer_ID": 1}))
    max_cust_num = 0
    for c in all_custs:
        cid_str = c.get("Customer_ID", "")
        if cid_str.startswith("BANK"):
            try:
                num = int(cid_str.replace("BANK", ""))
                if num > max_cust_num:
                    max_cust_num = num
            except ValueError:
                pass
    next_customer_id = f"BANK{str(max_cust_num + 1).zfill(4)}"

    # Compute next Loan_ID
    all_loans = list(db.loan_applications.find({}, {"Loan_ID": 1}))
    max_loan_num = 0
    for l in all_loans:
        lid_str = l.get("Loan_ID", "")
        if lid_str.startswith("LN"):
            try:
                num = int(lid_str.replace("LN", ""))
                if num > max_loan_num:
                    max_loan_num = num
            except ValueError:
                pass
    next_loan_id = f"LN{str(max_loan_num + 1).zfill(4)}"

    # Compute next Repayment_ID prefix
    all_rp = list(db.repayment_history.find({}, {"Repayment_ID": 1}).sort("Repayment_ID", -1).limit(10))
    max_rp_num = 0
    for r in all_rp:
        rid_str = r.get("Repayment_ID", "")
        if rid_str.startswith("RP"):
            try:
                num = int(rid_str.replace("RP", ""))
                if num > max_rp_num:
                    max_rp_num = num
            except ValueError:
                pass
    if max_rp_num == 0:
        max_rp_num = 6000

    # Calculate financial ratios
    annual_income = payload.Monthly_Income_INR * 12
    total_monthly_income = payload.Monthly_Income_INR + payload.Coapplicant_Income_INR
    # Estimated monthly EMI: simple formula P * (r/12) / (1 - (1+r/12)^-n)
    monthly_r = (payload.Interest_Rate_Percent / 100) / 12
    n_months = max(1, payload.Loan_Term_Months)
    if monthly_r > 0:
        est_emi = (payload.Loan_Amount_INR * monthly_r * ((1 + monthly_r)**n_months)) / (((1 + monthly_r)**n_months) - 1)
    else:
        est_emi = payload.Loan_Amount_INR / n_months
    est_emi = round(est_emi, 2)

    total_debt_service = est_emi + payload.Existing_EMI_INR
    dti = round(total_debt_service / max(1.0, total_monthly_income), 3)

    # Risk evaluation
    if payload.Credit_Score >= 720 and dti <= 0.40 and payload.Previous_Defaults == 0:
        credit_risk = "Low"
    elif payload.Credit_Score >= 620 and dti <= 0.50 and payload.Previous_Defaults <= 1:
        credit_risk = "Medium"
    else:
        credit_risk = "High"

    loan_default = "Yes" if credit_risk == "High" and payload.Previous_Defaults > 0 else "No"

    # Approval / Rejection logic
    rejection_code = None
    rejection_reason = "Not Applicable - Loan Approved"
    approval_status = "Approved"

    if payload.Previous_Defaults > 0:
        approval_status = "Rejected"
        rejection_code = "R01"
        rejection_reason = "Previous loan default recorded"
    elif payload.Monthly_Income_INR < 20000:
        approval_status = "Rejected"
        rejection_code = "R02"
        rejection_reason = "Insufficient monthly income"
    elif dti > 0.50:
        approval_status = "Rejected"
        rejection_code = "R03"
        rejection_reason = "High proposed debt-to-income ratio"
    elif payload.Credit_Score < 600:
        approval_status = "Rejected"
        rejection_code = "R04"
        rejection_reason = "Credit score below the minimum eligibility threshold"
    elif payload.Employment_Type == "Unemployed":
        approval_status = "Rejected"
        rejection_code = "R05"
        rejection_reason = "No current employment income"

    today_str = datetime.now().strftime("%Y-%m-%d")

    # 1. Bank Customers document
    bank_cust_doc = {
        "Customer_ID": next_customer_id,
        "Customer_Name": payload.Customer_Name.strip(),
        "Age": payload.Age,
        "Gender": payload.Gender,
        "City": payload.City.strip(),
        "Email": payload.Email.strip(),
        "Phone": payload.Phone.strip(),
        "Account_Type": payload.Account_Type,
        "Account_Balance_INR": float(payload.Account_Balance_INR),
        "Account_Opening_Date": today_str,
        "Credit_Score": int(payload.Credit_Score),
        "Loan_Status": approval_status,
        "Monthly_Transactions": 12,
        "KYC_Status": payload.KYC_Status,
        "Employment_Type": payload.Employment_Type,
        "Education": payload.Education,
        "Marital_Status": payload.Marital_Status
    }

    # 2. Loan Application document
    loan_app_doc = {
        "Loan_ID": next_loan_id,
        "Customer_ID": next_customer_id,
        "Application_Date": today_str,
        "Loan_Type": payload.Loan_Type,
        "Loan_Purpose": payload.Loan_Purpose,
        "Loan_Amount_INR": float(payload.Loan_Amount_INR),
        "Loan_Term_Months": payload.Loan_Term_Months,
        "Interest_Rate_Percent": float(payload.Interest_Rate_Percent),
        "Monthly_Income_INR": float(payload.Monthly_Income_INR),
        "Annual_Income_INR": float(annual_income),
        "Coapplicant_Income_INR": float(payload.Coapplicant_Income_INR),
        "Monthly_Expenses_INR": float(payload.Monthly_Expenses_INR),
        "Existing_Loan_Amount_INR": float(payload.Existing_Loan_Amount_INR),
        "Existing_EMI_INR": float(payload.Existing_EMI_INR),
        "Outstanding_Debt_INR": float(payload.Outstanding_Debt_INR),
        "Debt_to_Income_Ratio": float(dti),
        "Previous_Loans": payload.Previous_Loans,
        "Previous_Defaults": payload.Previous_Defaults,
        "Late_Payments": payload.Late_Payments,
        "Delayed_Payment_Days": payload.Delayed_Payment_Days,
        "Loan_Approval_Status": approval_status,
        "Rejection_Reason_Code": rejection_code,
        "Rejection_Reason": rejection_reason
    }

    # 3. Credit Risk document
    credit_risk_doc = {
        "Loan_ID": next_loan_id,
        "Customer_ID": next_customer_id,
        "Credit_Score": int(payload.Credit_Score),
        "Debt_to_Income_Ratio": float(dti),
        "Previous_Loans": payload.Previous_Loans,
        "Previous_Defaults": payload.Previous_Defaults,
        "Late_Payments": payload.Late_Payments,
        "Delayed_Payment_Days": payload.Delayed_Payment_Days,
        "Outstanding_Debt_INR": float(payload.Outstanding_Debt_INR),
        "Monthly_Income_INR": float(payload.Monthly_Income_INR),
        "Credit_Risk": credit_risk,
        "Loan_Default": loan_default
    }

    # 4. Loan Rejection Reason document
    rejection_doc = {
        "Loan_ID": next_loan_id,
        "Customer_ID": next_customer_id,
        "Loan_Approval_Status": approval_status,
        "Rejection_Reason_Code": rejection_code,
        "Rejection_Reason": rejection_reason
    }

    # 5. Repayment History schedule (6 installments)
    repayment_records = []
    base_date = datetime.now()
    installment_amount = round(payload.Loan_Amount_INR / 6, 2)
    for i in range(1, 7):
        max_rp_num += 1
        rp_id = f"RP{str(max_rp_num).zfill(6)}"
        due_d = (base_date + timedelta(days=30 * i)).strftime("%Y-%m-%d")
        
        # If approved, schedule as On Time / future; if rejected or high risk, simulate realistic status
        if approval_status == "Approved":
            paid_d = due_d
            days_late = 0
            rp_status = "On Time"
        else:
            paid_d = None
            days_late = 0
            rp_status = "Not Disbursed"

        repayment_records.append({
            "Repayment_ID": rp_id,
            "Loan_ID": next_loan_id,
            "Customer_ID": next_customer_id,
            "Installment_Number": i,
            "Due_Date": due_d,
            "Paid_Date": paid_d,
            "Due_Amount_INR": installment_amount,
            "Paid_Amount_INR": installment_amount if approval_status == "Approved" else 0.0,
            "Days_Late": days_late,
            "Repayment_Status": rp_status
        })

    # Insert all documents into MongoDB
    db.bank_customers.insert_one(bank_cust_doc)
    db.loan_applications.insert_one(loan_app_doc)
    db.credit_risk.insert_one(credit_risk_doc)
    db.loan_rejection_reasons.insert_one(rejection_doc)
    db.repayment_history.insert_many(repayment_records)

    # Sync back to CSV in data directory for seamless persistent synchronization
    try:
        append_to_csv("01_bank_customers_1000.csv", bank_cust_doc)
        append_to_csv("02_loan_applications_1000.csv", loan_app_doc)
        append_to_csv("04_credit_risk_1000.csv", credit_risk_doc)
        append_to_csv("05_loan_rejection_reasons_1000.csv", rejection_doc)
        for rp in repayment_records:
            append_to_csv("03_repayment_history_6000.csv", rp)
    except Exception as e:
        print("Note: CSV backup append warning:", e)

    return {
        "success": True,
        "message": f"Customer {payload.Customer_Name} added successfully!",
        "Customer_ID": next_customer_id,
        "Loan_ID": next_loan_id,
        "Loan_Approval_Status": approval_status,
        "Credit_Risk": credit_risk,
        "Rejection_Reason": rejection_reason
    }

def append_to_csv(filename, record):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        rec_copy = {k: v for k, v in record.items() if k != "_id"}
        df_new = pd.DataFrame([rec_copy])
        df_new.to_csv(filepath, mode="a", header=False, index=False)

@app.get("/api/dataset/{dataset_name}")
def get_dataset(
    dataset_name: str,
    search: Optional[str] = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=5, le=100),
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "asc"
):
    db = get_db()
    valid_collections = {
        "bank_customers": "01_bank_customers_1000.csv",
        "loan_applications": "02_loan_applications_1000.csv",
        "repayment_history": "03_repayment_history_6000.csv",
        "credit_risk": "04_credit_risk_1000.csv",
        "loan_rejection_reasons": "05_loan_rejection_reasons_1000.csv"
    }

    if dataset_name not in valid_collections:
        raise HTTPException(status_code=400, detail=f"Invalid dataset '{dataset_name}'. Available: {list(valid_collections.keys())}")

    coll = db[dataset_name]
    
    # Query builder
    query = {}
    if search:
        search_term = search.strip()
        # Build search across primary fields
        or_clauses = []
        sample_doc = coll.find_one({}, {"_id": 0})
        if sample_doc:
            for k, v in sample_doc.items():
                if isinstance(v, str):
                    or_clauses.append({k: {"$regex": search_term, "$options": "i"}})
        if or_clauses:
            query["$or"] = or_clauses

    direction = 1 if sort_order.lower() == "asc" else -1
    cursor = coll.find(query, {"_id": 0})
    if sort_by:
        cursor = cursor.sort([(sort_by, direction)])

    total_rows = coll.count_documents(query)
    start = (page - 1) * page_size
    records = list(cursor.skip(start).limit(page_size))

    # Get column names
    first_record = coll.find_one({}, {"_id": 0}) or {}
    columns = list(first_record.keys())

    return {
        "dataset_name": dataset_name,
        "total_records": total_rows,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total_rows / page_size) if total_rows > 0 else 1,
        "columns": columns,
        "records": records
    }

@app.get("/api/dataset/{dataset_name}/export")
def export_dataset(dataset_name: str):
    db = get_db()
    valid = ["bank_customers", "loan_applications", "repayment_history", "credit_risk", "loan_rejection_reasons"]
    if dataset_name not in valid:
        raise HTTPException(status_code=400, detail="Invalid dataset")
    
    records = list(db[dataset_name].find({}, {"_id": 0}))
    df = pd.DataFrame(records)
    
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    
    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = f"attachment; filename={dataset_name}.csv"
    return response

@app.post("/api/sync")
def sync_database():
    try:
        counts = init_database(force_reload=True)
        return {"success": True, "message": "Database synchronized successfully with CSV datasets!", "counts": counts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/powerbi/launch")
def launch_powerbi():
    pbi_exe = r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
    pbit_file = os.path.join(os.path.dirname(__file__), "Financial_Credit_Risk_Dashboard.pbit")
    
    if not os.path.exists(pbit_file):
        raise HTTPException(status_code=404, detail="Power BI Template file not found")
        
    if os.path.exists(pbi_exe):
        try:
            subprocess.Popen([pbi_exe, pbit_file])
            return {"success": True, "message": "Launched Microsoft Power BI Desktop with Financial_Credit_Risk_Dashboard.pbit"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    else:
        # Fallback to os.startfile for Windows association
        try:
            os.startfile(pbit_file)
            return {"success": True, "message": "Triggered Power BI file opening"}
        except Exception as e:
            return {"success": False, "error": str(e)}

@app.get("/api/powerbi/download-pbit")
def download_pbit():
    pbit_file = os.path.join(os.path.dirname(__file__), "Financial_Credit_Risk_Dashboard.pbit")
    if not os.path.exists(pbit_file):
        raise HTTPException(status_code=404, detail="Power BI Template file not found")
    return FileResponse(pbit_file, filename="Financial_Credit_Risk_Dashboard.pbit", media_type="application/octet-stream")

@app.get("/api/powerbi/download-master")
def download_master_csv():
    master_file = os.path.join(os.path.dirname(__file__), "Financial_Loan_Credit_Risk_PowerBI_Master.csv")
    if not os.path.exists(master_file):
        raise HTTPException(status_code=404, detail="Master CSV file not found")
    return FileResponse(master_file, filename="Financial_Loan_Credit_Risk_PowerBI_Master.csv", media_type="text/csv")

@app.get("/api/powerbi/analytics")
def get_powerbi_analytics():
    master_file = os.path.join(os.path.dirname(__file__), "Financial_Loan_Credit_Risk_PowerBI_Master.csv")
    if not os.path.exists(master_file):
        raise HTTPException(status_code=404, detail="Master dataset not found")
    
    df = pd.read_csv(master_file)
    
    # 1. Loan Approval Dashboard
    total_apps = len(df)
    approved_df = df[df['Loan_Approval_Status'] == 'Approved']
    rejected_df = df[df['Loan_Approval_Status'] == 'Rejected']
    
    approval_rate = round(len(approved_df) / total_apps * 100, 1) if total_apps else 0
    total_disbursed = float(approved_df['Loan_Amount_INR'].sum())
    total_requested = float(df['Loan_Amount_INR'].sum())
    avg_dti = round(float(df['Debt_to_Income_Ratio'].mean() * 100), 1)

    # Approval by Purpose
    purpose_grp = df.groupby(['Loan_Purpose', 'Loan_Approval_Status']).size().unstack(fill_value=0).to_dict(orient='index')
    
    # Approval by Employment
    emp_grp = df.groupby(['Employment_Type', 'Loan_Approval_Status']).size().unstack(fill_value=0).to_dict(orient='index')
    
    # Rejection Reasons
    rej_counts = df[df['Rejection_Reason_Code'].notna()]['Rejection_Reason_Code'].value_counts().to_dict()
    code_names = {
        "R01": "Previous Default",
        "R02": "Low Income (<₹20k)",
        "R03": "High DTI (>50%)",
        "R04": "Credit Score (<600)",
        "R05": "Unemployed"
    }
    rejection_pareto = {f"{k} ({code_names.get(k, k)})": int(v) for k, v in rej_counts.items()}

    # 2. Income Analysis
    # Income brackets
    inc_bands = ["<₹25k (Low)", "₹25k-₹50k (Lower-Mid)", "₹50k-₹75k (Mid)", "₹75k-₹1L (Upper-Mid)", ">₹1L (Affluent)"]
    inc_band_stats = {}
    for b in inc_bands:
        b_df = df[df['Income_Band'] == b]
        if len(b_df) > 0:
            app_rate = round((b_df['Loan_Approval_Status'] == 'Approved').sum() / len(b_df) * 100, 1)
            mean_inc = round(float(b_df['Monthly_Income_INR'].mean()), 0)
            mean_loan = round(float(b_df['Loan_Amount_INR'].mean()), 0)
            mean_dti = round(float(b_df['Debt_to_Income_Ratio'].mean() * 100), 1)
            inc_band_stats[b] = {
                "count": len(b_df),
                "approval_rate": app_rate,
                "mean_income": mean_inc,
                "mean_loan": mean_loan,
                "mean_dti": mean_dti
            }

    # Avg income by education
    edu_inc = df.groupby('Education')['Monthly_Income_INR'].mean().round(0).to_dict()

    # 3. Credit Score Distribution
    score_bands = ["<580 (Poor)", "580-669 (Fair)", "670-739 (Good)", "740-799 (Very Good)", "800+ (Exceptional)"]
    score_band_stats = {}
    for sb in score_bands:
        s_df = df[df['Credit_Score_Band'] == sb]
        if len(s_df) > 0:
            default_rate = round((s_df['Loan_Default'] == 'Yes').sum() / len(s_df) * 100, 1)
            app_count = (s_df['Loan_Approval_Status'] == 'Approved').sum()
            avg_debt = round(float(s_df['Outstanding_Debt_INR'].mean()), 0)
            score_band_stats[sb] = {
                "count": len(s_df),
                "default_rate": default_rate,
                "approved_count": int(app_count),
                "avg_debt": avg_debt
            }

    # Histogram buckets (50 pt increments)
    hist_buckets = {}
    for low in range(300, 900, 50):
        high = low + 50
        label = f"{low}-{high}"
        h_count = len(df[(df['Credit_Score'] >= low) & (df['Credit_Score'] < high)])
        hist_buckets[label] = h_count

    return {
        "loan_approval_dashboard": {
            "kpis": {
                "total_applications": total_apps,
                "approved_count": len(approved_df),
                "rejected_count": len(rejected_df),
                "approval_rate": approval_rate,
                "total_disbursed_inr": total_disbursed,
                "total_requested_inr": total_requested,
                "avg_dti": avg_dti
            },
            "by_purpose": purpose_grp,
            "by_employment": emp_grp,
            "rejections": rejection_pareto
        },
        "income_analysis": {
            "kpis": {
                "avg_monthly_income": round(float(df['Monthly_Income_INR'].mean()), 0),
                "median_monthly_income": round(float(df['Monthly_Income_INR'].median()), 0),
                "max_monthly_income": round(float(df['Monthly_Income_INR'].max()), 0),
                "coapplicant_rate": round(float((df['Coapplicant_Income_INR'] > 0).mean() * 100), 1)
            },
            "by_income_band": inc_band_stats,
            "by_education": edu_inc
        },
        "credit_score_distribution": {
            "kpis": {
                "avg_credit_score": round(float(df['Credit_Score'].mean()), 1),
                "median_credit_score": round(float(df['Credit_Score'].median()), 1),
                "subprime_count": int((df['Credit_Score'] < 600).sum()),
                "prime_count": int((df['Credit_Score'] >= 720).sum())
            },
            "histogram": hist_buckets,
            "by_score_band": score_band_stats
        }
    }

# Mount static folder
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>FinRisk 360 API running</h1>")
