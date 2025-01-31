import pandas as pd
import pdfplumber
import re

def extract_transactions_from_pdf(pdf_path):
    transactions = []
    account_holder = "Unknown"
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if "Mr." in text or "Mrs." in text:
                account_holder_match = re.search(r'(Mr\.|Mrs\.)\s+(.*?)\n', text)
                if account_holder_match:
                    account_holder = account_holder_match.group(2).strip()
            
            lines = text.split('\n')
            for line in lines:
                match = re.search(r'(\d{2}-[A-Za-z]{3}-\d{4})\s+(\d{2}-[A-Za-z]{3}-\d{4})\s+(.*?)\s+(\d{6}|null)?\s*(-?\d+,?\d*\.\d{2})?\s*(-?\d+,?\d*\.\d{2})?\s*(-?\d+,?\d*\.\d{2})?', line)
                if match:
                    transaction_date, value_date, particulars, cheque_no, debit, credit, balance = match.groups()
                    transactions.append([
                        transaction_date, value_date, particulars, cheque_no if cheque_no else "N/A",
                        float(debit.replace(",", "")) if debit else 0.0,
                        float(credit.replace(",", "")) if credit else 0.0,
                        float(balance.replace(",", "")) if balance else 0.0
                    ])
    
    df = pd.DataFrame(transactions, columns=["Transaction Date", "Value Date", "Particulars", "Cheque No", "Debit", "Credit", "Balance"])
    return account_holder, df

if __name__ == "__main__":
    pdf_path = "example_bank_statement.pdf"  # Change this
    account_holder, df_pdf = extract_transactions_from_pdf(pdf_path)
    
    print(f"Account Holder: {account_holder}\n")
    print("Extracted Transactions:")
    print(df_pdf.head())