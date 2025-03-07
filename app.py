from flask import Flask, request, jsonify, render_template, send_file
import os
import json
from data_extraction import extract_transactions_from_pdf, analyze_statement
from loan_model import process_transactions
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io
import base64

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_plots(transactions_df, analysis_result):
    """Generate visualization plots for the analysis"""
    plots = {}
    
    # Monthly Income vs Expenses
    plt.figure(figsize=(10, 6))
    monthly = transactions_df.groupby(pd.Grouper(key='date', freq='M')).agg({
        'amount': lambda x: [x[x > 0].sum(), abs(x[x < 0].sum())]
    })
    monthly_data = pd.DataFrame(monthly['amount'].tolist(), 
                              columns=['Income', 'Expenses'],
                              index=monthly.index)
    monthly_data.plot(kind='bar')
    plt.title('Monthly Income vs Expenses')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plots['income_expenses'] = base64.b64encode(buf.getvalue()).decode()
    plt.close()
    
    # Transaction Categories
    plt.figure(figsize=(10, 6))
    category_totals = transactions_df.groupby('category')['amount'].sum()
    plt.pie(abs(category_totals), labels=category_totals.index, autopct='%1.1f%%')
    plt.title('Transaction Categories Distribution')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plots['categories'] = base64.b64encode(buf.getvalue()).decode()
    plt.close()
    
    return plots

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format'}), 400
    
    try:
        # Save and process file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Extract transactions
        transactions_df = extract_transactions_from_pdf(filename)
        if transactions_df is None:
            return jsonify({'error': 'Failed to extract transactions'}), 400
        
        # Analyze transactions
        statement_analysis = analyze_statement(transactions_df)
        loan_recommendation = process_transactions(transactions_df)
        
        # Generate plots
        plots = generate_plots(transactions_df, loan_recommendation)
        
        # Prepare response data
        response_data = {
            'statement_analysis': statement_analysis,
            'loan_recommendation': loan_recommendation,
            'plots': plots
        }
        
        return render_template(
            'analysis.html',
            analysis=response_data,
            plots=plots
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)