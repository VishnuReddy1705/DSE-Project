import os
import glob
import pandas as pd
from pymongo import MongoClient, ASCENDING

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "financial_risk_db"

def get_db():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client[DB_NAME]

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def clean_record(row):
    record = {}
    for k, v in row.items():
        if pd.isna(v):
            record[k] = None
        else:
            # Cast common types if necessary
            if isinstance(v, (int, float, str, bool)):
                record[k] = v
            else:
                record[k] = str(v)
    return record

def init_database(force_reload=False):
    db = get_db()
    
    collection_mapping = {
        "bank_customers": "01_bank_customers_*.csv",
        "loan_applications": "02_loan_applications_*.csv",
        "repayment_history": "03_repayment_history_*.csv",
        "credit_risk": "04_credit_risk_*.csv",
        "loan_rejection_reasons": "05_loan_rejection_reasons_*.csv"
    }

    results = {}

    for coll_name, pattern in collection_mapping.items():
        coll = db[coll_name]
        count = coll.count_documents({})
        
        if count == 0 or force_reload:
            if force_reload:
                coll.delete_many({})
            
            # Find file in DATA_DIR
            matched_files = glob.glob(os.path.join(DATA_DIR, pattern))
            if not matched_files:
                # Also check original Downloads folder fallback
                dl_dir = r"C:\Users\omvis\Downloads\financial_loan_credit_risk_datasets"
                matched_files = glob.glob(os.path.join(dl_dir, pattern))
                
            if matched_files:
                csv_path = matched_files[0]
                df = pd.read_csv(csv_path)
                records = [clean_record(row) for row in df.to_dict(orient="records")]
                if records:
                    coll.insert_many(records)
                results[coll_name] = len(records)
            else:
                results[coll_name] = 0
        else:
            results[coll_name] = count

    # Create Indexes for fast querying
    db.bank_customers.create_index([("Customer_ID", ASCENDING)], unique=True)
    db.bank_customers.create_index([("Customer_Name", ASCENDING)])
    db.loan_applications.create_index([("Loan_ID", ASCENDING)])
    db.loan_applications.create_index([("Customer_ID", ASCENDING)])
    db.credit_risk.create_index([("Customer_ID", ASCENDING)])
    db.credit_risk.create_index([("Loan_ID", ASCENDING)])
    db.repayment_history.create_index([("Customer_ID", ASCENDING)])
    db.repayment_history.create_index([("Loan_ID", ASCENDING)])
    db.loan_rejection_reasons.create_index([("Customer_ID", ASCENDING)])

    return results

if __name__ == "__main__":
    print("Initializing MongoDB collections...")
    res = init_database(force_reload=True)
    print("Database initialization complete:", res)
