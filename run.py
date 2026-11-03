import uvicorn
import os
import sys

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 60)
    print(" FinRisk 360 - Financial Loan & Credit Risk System")
    print(" Database: MongoDB localhost:27017/financial_risk_db")
    print(" Dashboard URL: http://localhost:8000")
    print("=" * 60)
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info", reload=False)
