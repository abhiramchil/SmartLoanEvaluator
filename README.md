# Smart Loan Evaluator 🏦

An intelligent system that automates bank statement analysis and loan decision-making using machine learning.

## Features 🌟

- **PDF Bank Statement Analysis**: Automatically extracts and processes transaction data from PDF bank statements
- **Smart Transaction Categorization**: Uses ML to categorize transactions into meaningful categories
- **Financial Health Analysis**: Calculates key financial metrics and patterns
- **Loan Risk Assessment**: ML-powered evaluation of loan worthiness
- **Interactive Dashboard**: User-friendly web interface for uploading statements and viewing insights
- **Detailed Reporting**: Generates comprehensive financial health reports

## Tech Stack 💻

- **Backend**: Python, Flask
- **ML/Data Processing**: scikit-learn, pandas, tabula-py
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: CSV (for MVP phase)

## Installation 🛠️

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python app.py
```

## Project Structure 📁

```
SmartLoanEvaluator/
├── app.py                 # Main Flask application
├── loan_model.py          # ML model for loan evaluation
├── data_extraction.py     # PDF parsing and data extraction
├── transaction_analysis.py # Transaction processing and analysis
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── uploads/             # Temporary storage for uploaded files
└── models/              # Trained ML models
```

## Usage 📝

1. Access the web interface at `http://localhost:5000`
2. Upload a bank statement PDF
3. View the automated analysis and loan recommendation
4. Download detailed reports

## Development Status 🚧

This is an MVP (Minimum Viable Product) demonstrating the core functionality of automated bank statement analysis and loan evaluation. Future enhancements will include:

- Advanced ML models for better accuracy
- Support for more bank statement formats
- Database integration
- API endpoints for integration
- Enhanced security features

## License 📄

MIT License 