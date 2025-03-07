import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def calculate_financial_metrics(transactions_df):
    """
    Calculate key financial metrics from transaction data.
    """
    metrics = {}
    
    # Monthly metrics
    monthly_groups = transactions_df.groupby(pd.Grouper(key='date', freq='M'))
    
    # Income stability
    monthly_deposits = monthly_groups.apply(lambda x: x[x['amount'] > 0]['amount'].sum())
    metrics['avg_monthly_income'] = monthly_deposits.mean()
    metrics['income_stability'] = monthly_deposits.std() / monthly_deposits.mean() if len(monthly_deposits) > 1 else 1
    
    # Expense patterns
    monthly_expenses = monthly_groups.apply(lambda x: abs(x[x['amount'] < 0]['amount'].sum()))
    metrics['avg_monthly_expenses'] = monthly_expenses.mean()
    metrics['expense_to_income_ratio'] = metrics['avg_monthly_expenses'] / metrics['avg_monthly_income'] if metrics['avg_monthly_income'] > 0 else float('inf')
    
    # Balance trends
    metrics['avg_daily_balance'] = transactions_df['amount'].cumsum().mean()
    metrics['min_balance'] = transactions_df['amount'].cumsum().min()
    
    # Debt indicators
    loan_payments = transactions_df[transactions_df['category'] == 'loan_payment']
    metrics['existing_loan_payments'] = len(loan_payments)
    metrics['total_loan_amount'] = abs(loan_payments['amount'].sum()) if not loan_payments.empty else 0
    
    # Business health indicators
    metrics['revenue_growth'] = (monthly_deposits.iloc[-1] - monthly_deposits.iloc[0]) / monthly_deposits.iloc[0] if len(monthly_deposits) > 1 else 0
    
    return metrics

def evaluate_loan_worthiness(metrics):
    """
    Evaluate loan worthiness based on financial metrics.
    Returns a score between 0 and 1, and a detailed analysis.
    """
    score = 0
    analysis = []
    
    # Income stability (weight: 0.25)
    income_stability_score = max(0, 1 - metrics['income_stability'])
    score += 0.25 * income_stability_score
    analysis.append({
        'factor': 'Income Stability',
        'score': income_stability_score,
        'details': f"{'Stable' if income_stability_score > 0.7 else 'Unstable'} income pattern"
    })
    
    # Expense ratio (weight: 0.25)
    expense_ratio_score = max(0, 1 - metrics['expense_to_income_ratio'])
    score += 0.25 * expense_ratio_score
    analysis.append({
        'factor': 'Expense to Income Ratio',
        'score': expense_ratio_score,
        'details': f"Uses {metrics['expense_to_income_ratio']*100:.1f}% of income"
    })
    
    # Balance health (weight: 0.2)
    balance_score = 1 if metrics['min_balance'] > 0 else max(0, 1 + metrics['min_balance']/metrics['avg_monthly_income'])
    score += 0.2 * balance_score
    analysis.append({
        'factor': 'Balance Health',
        'score': balance_score,
        'details': 'Maintains healthy balance' if balance_score > 0.7 else 'Balance issues detected'
    })
    
    # Existing debt (weight: 0.15)
    debt_score = 1 - min(1, metrics['total_loan_amount']/(12*metrics['avg_monthly_income']))
    score += 0.15 * debt_score
    analysis.append({
        'factor': 'Existing Debt',
        'score': debt_score,
        'details': f"Has {metrics['existing_loan_payments']} existing loan payments"
    })
    
    # Business growth (weight: 0.15)
    growth_score = min(1, max(0, metrics['revenue_growth']))
    score += 0.15 * growth_score
    analysis.append({
        'factor': 'Business Growth',
        'score': growth_score,
        'details': f"Revenue growth: {metrics['revenue_growth']*100:.1f}%"
    })
    
    recommendation = {
        'score': score,
        'decision': 'Approved' if score >= 0.7 else 'Needs Review' if score >= 0.5 else 'Rejected',
        'analysis': analysis,
        'metrics': metrics
    }
    
    return recommendation

def process_transactions(transactions_df):
    """
    Process transactions and evaluate loan worthiness.
    """
    if transactions_df is None or transactions_df.empty:
        return None
    
    # Calculate financial metrics
    metrics = calculate_financial_metrics(transactions_df)
    
    # Evaluate loan worthiness
    recommendation = evaluate_loan_worthiness(metrics)
    
    return recommendation 