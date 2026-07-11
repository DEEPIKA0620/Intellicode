IntelliCode
AI-Powered Software Defect Prediction Platform

IntelliCode is an AI-powered web application that predicts software defects using software metrics extracted from source code or CSV datasets. The platform combines Machine Learning, Static Code Analysis, Explainable AI, MySQL, and PDF reporting to help developers identify defect-prone modules before deployment.

Features
Manual Software Metrics Prediction
Predict software defects by entering software metrics manually.
Displays:
Prediction result
Risk Score
Risk Level
AI Recommendations
Explainable AI insights
Python Source Code Analysis

Upload a Python (.py) file and IntelliCode automatically:

Extracts software metrics
Computes Maintainability Index
Calculates Cyclomatic Complexity
Maps extracted metrics to the machine learning feature set
Predicts software defects
Generates a professional PDF report
Bulk CSV Prediction

Upload software metric datasets in CSV format to:

Predict defects for hundreds or thousands of modules
Generate module-wise predictions
View Top High-Risk Modules
Visualize module distribution using charts
Download a professional Bulk Analysis Report
Explainable AI

The platform provides transparent predictions through:

Risk Score
Risk Level
Feature Importance
AI Assessment
Testing Recommendations
Dashboard Analytics
Total Predictions
Healthy Modules
Defective Modules
Average Risk Score
Recent Predictions

All prediction history is stored in MySQL.

PDF Report Generation

Supports:

Individual Software Analysis Report
Bulk Prediction Report

Reports include:

Prediction Summary
Software Metrics
AI Assessment
Recommendations
Risk Analysis

Tech Stack
Frontend
HTML5
CSS3
JavaScript

Backend
Flask
Python

Machine Learning
Scikit-learn
Random Forest Classifier
Static Code Analysis
Radon

Data Processing
Pandas
NumPy

Visualization
Matplotlib

Database
MySQL

PDF Generation
ReportLab

Project Structure
IntelliCode/
│
├── app.py
├── database.py
├── model/
│   ├── random_forest_model.pkl
│   └── feature_importance.png
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
├── dataset/
└── requirements.txt
System Workflow
                User
                  │
                  ▼
      Manual / Python / CSV Upload
                  │
                  ▼
      Software Metrics Extraction
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
      ┌───────────┴────────────┐
      ▼                        ▼
   MySQL Storage         PDF Report
      │                        │
      └───────────┬────────────┘
                  ▼
          Interactive Dashboard
Installation
Clone Repository
git clone https://github.com/yourusername/IntelliCode.git
cd IntelliCode
Create Virtual Environment
python -m venv venv

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Configure MySQL

Create a database named:

CREATE DATABASE intellicode;

Create the predictions table.

(You can include your SQL schema here or in a separate .sql file.)

Run the Application
python app.py

Visit:

http://127.0.0.1:5000




This project demonstrates practical implementation of:

Machine Learning for Software Engineering
Static Code Analysis
Software Quality Prediction
Explainable AI
Flask Web Development
MySQL Database Integration
PDF Report Generation
Data Visualization
Full-Stack AI Application Development
Author

Deepika B R

B.Tech Information Technology

Agni College of Technology

License

This project is developed for educational and research purposes.