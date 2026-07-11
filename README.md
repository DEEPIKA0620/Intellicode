# IntelliCode

> **AI-Powered Software Defect Prediction Platform**

IntelliCode is an AI-powered web application that predicts software defects using Machine Learning and software metrics. It enables developers to analyze software quality through manual metric input, Python source code analysis, and bulk CSV prediction while providing Explainable AI insights, dashboard analytics, MySQL storage, and professional PDF reports.

---

## Features

### Manual Software Metrics Prediction
- Predict software defects using software metrics.
- Displays:
  - Prediction Result
  - Risk Score
  - Risk Level
  - Priority Level
  - Explainable AI Assessment

### Python Source Code Analysis
- Upload Python (.py) files
- Automatic software metric extraction
- Cyclomatic Complexity calculation
- Halstead Metrics calculation
- Maintainability Index calculation
- AI-based defect prediction
- Professional PDF report generation

### Bulk CSV Prediction
- Upload PROMISE dataset or custom software metric datasets
- Predict defects for multiple modules
- Summary dashboard
- Module distribution visualization
- Top high-risk module identification
- Download bulk analysis report

### Explainable AI
- Feature Importance
- Risk Assessment
- Risk Drivers
- AI Recommendations

### Dashboard Analytics
- Total Predictions
- Healthy Modules
- Defective Modules
- Average Risk Score
- Recent Prediction History

### Database Integration
- MySQL storage
- Prediction history
- Dashboard statistics

### Report Generation
- Individual Software Analysis Report (PDF)
- Bulk Analysis Report (PDF)

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Flask, Python |
| Machine Learning | Scikit-learn, Random Forest |
| Static Code Analysis | Radon |
| Database | MySQL |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib |
| PDF Generation | ReportLab |

---

## Project Structure

```text
IntelliCode/
│
├── app.py
├── database.py
├── model.pkl
├── requirements.txt
│
├── utils/
│   ├── metrics_extractor.py
│   ├── feature_mapper.py
│   ├── pdf_report.py
│   ├── bulk_pdf_report.py
│   └── ...
│
├── templates/
│   ├── index.html
│   └── bulk_results.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── feature_importance.png
│   └── bulk_pie_chart.png
│
├── uploads/
├── reports/
└── dataset/
```

---

## System Workflow

```text
             User
               │
               ▼
   Manual Entry / Python File / CSV Upload
               │
               ▼
      Software Metric Extraction
               │
               ▼
         Feature Mapping
               │
               ▼
     Random Forest Prediction
               │
               ▼
        Explainable AI Analysis
               │
       ┌───────┴────────┐
       ▼                ▼
    MySQL          PDF Report
       │
       ▼
 Interactive Dashboard
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/IntelliCode.git
```

```bash
cd IntelliCode
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure MySQL

Create a database named:

```sql
CREATE DATABASE intellicode;
```

Import the required tables.

---

### Run the Application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## Screenshots

Add screenshots inside a `screenshots` folder.

```
screenshots/
│
├── home.png
├── manual_prediction.png
├── python_analysis.png
├── bulk_prediction.png
├── dashboard.png
└── pdf_report.png
```

Example:

```markdown
![Home](screenshots/home.png)
```

---

## Future Enhancements

- User Authentication
- Cloud Deployment
- REST API
- Docker Support
- CI/CD Integration
- Multiple Machine Learning Models
- Real-time Monitoring Dashboard
- Email Report Generation

---

## Learning Outcomes

This project demonstrates practical implementation of:

- Machine Learning
- Software Defect Prediction
- Static Code Analysis
- Explainable AI
- Flask Web Development
- MySQL Integration
- Report Generation
- Data Visualization
- Full-Stack AI Application Development

---

## Author

**Deepika B R**

B.Tech Information Technology

Agni College of Technology

---

## License

This project is intended for educational and research purposes.
