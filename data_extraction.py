import pandas as pd
import tabula
import os
from datetime import datetime

def extract_transactions_from_pdf(pdf_path):
    """
    Extract transaction data from PDF bank statements.
    Returns a pandas DataFrame with standardized transaction data.
    """
    try:
        # Extract all tables from PDF
        tables = tabula.read_pdf(pdf_path, pages='all', encoding='ISO-8859-1')
        
        # Combine all tables into one DataFrame
        combined_df = pd.concat(tables, ignore_index=True)
        
        # Clean and standardize column names
        combined_df.columns = [col.strip().lower().replace(' ', '_') for col in combined_df.columns]
        
        # Try to identify date, description, and amount columns
        date_col = next((col for col in combined_df.columns if 'date' in col), None)
        desc_col = next((col for col in combined_df.columns if any(x in col for x in ['desc', 'narr', 'part'])), None)
        debit_col = next((col for col in combined_df.columns if any(x in col for x in ['debit', 'withdrawal'])), None)
        credit_col = next((col for col in combined_df.columns if any(x in col for x in ['credit', 'deposit'])), None)
        
        if not all([date_col, desc_col]):
            raise ValueError("Could not identify required columns in the statement")
        
        # Create standardized DataFrame
        transactions = pd.DataFrame()
        transactions['date'] = pd.to_datetime(combined_df[date_col], errors='coerce')
        transactions['description'] = combined_df[desc_col]
        
        # Handle amounts
        if debit_col and credit_col:
            transactions['amount'] = combined_df[credit_col].fillna(0) - combined_df[debit_col].fillna(0)
        elif debit_col:
            transactions['amount'] = -combined_df[debit_col].fillna(0)
        elif credit_col:
            transactions['amount'] = combined_df[credit_col].fillna(0)
        
        # Clean up
        transactions = transactions.dropna(subset=['date', 'amount'])
        transactions = transactions.sort_values('date')
        
        return transactions
    
    except Exception as e:
        print(f"Error extracting transactions: {str(e)}")
        return None

def categorize_transaction(description):
    """
    Basic transaction categorization based on keywords.
    """
    description = description.lower()
    
    categories = {
        'salary': ['salary', 'payroll', 'wage'],
        'rent': ['rent', 'lease'],
        'utilities': ['electric', 'water', 'gas', 'internet', 'phone'],
        'loan_payment': ['loan', 'mortgage', 'emi'],
        'employee_expenses': ['payroll', 'salary expense'],
        'supplies': ['supplies', 'inventory', 'stock'],
        'insurance': ['insurance', 'coverage'],
        'tax': ['tax', 'gst', 'vat'],
        'other': []
    }
    
    for category, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            return category
    
    return 'other'

def analyze_statement(transactions_df):
    """
    Analyze transactions to extract key financial metrics.
    """
    if transactions_df is None or transactions_df.empty:
        return None
        
    analysis = {
        'total_deposits': transactions_df[transactions_df['amount'] > 0]['amount'].sum(),
        'total_withdrawals': abs(transactions_df[transactions_df['amount'] < 0]['amount'].sum()),
        'average_balance': transactions_df['amount'].mean(),
        'transaction_count': len(transactions_df),
        'date_range': {
            'start': transactions_df['date'].min().strftime('%Y-%m-%d'),
            'end': transactions_df['date'].max().strftime('%Y-%m-%d')
        }
    }
    
    # Categorize transactions
    transactions_df['category'] = transactions_df['description'].apply(categorize_transaction)
    
    # Category-wise analysis
    category_analysis = {}
    for category in transactions_df['category'].unique():
        cat_df = transactions_df[transactions_df['category'] == category]
        category_analysis[category] = {
            'total': cat_df['amount'].sum(),
            'count': len(cat_df),
            'average': cat_df['amount'].mean()
        }
    
    analysis['category_analysis'] = category_analysis
    
    return analysis 