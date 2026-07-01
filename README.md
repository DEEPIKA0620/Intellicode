# 🚀 IntelliCode – AI-Powered Software Defect Prediction & Code Quality Intelligence Platform

## 📌 Overview

IntelliCode is an AI-powered Software Defect Prediction and Code Quality Intelligence Platform designed to help developers identify defect-prone software modules before deployment.

Using Machine Learning trained on the NASA PROMISE JM1 dataset, IntelliCode analyzes software metrics and predicts whether a software module is likely to contain defects. The platform also provides risk scoring, testing priorities, prediction history tracking, and Explainable AI insights to assist developers in making informed software quality decisions.

---

## 🎯 Project Objectives

* Predict software defects using Machine Learning.
* Identify high-risk software modules early.
* Improve software testing efficiency.
* Provide explainable AI-based decision support.
* Assist developers and QA teams in prioritizing testing efforts.

---

## ✨ Features

### 🔍 Software Defect Prediction

Predicts whether a software module is:

* ✅ Healthy Module
* ⚠️ Defective Module

using software quality metrics.

---

### 📊 Risk Assessment Dashboard

Displays:

* Risk Score (%)
* Risk Level (Low / Medium / High)
* Testing Priority
* Prediction Result

---

### 🤖 Explainable AI

Provides transparent explanations for predictions using Random Forest Feature Importance.

Example:

* LOC
* Logical LOC
* Halstead Volume
* Intelligence
* Time Estimate

The system explains why the prediction was generated and highlights key risk drivers.

---

### 📋 AI Risk Assessment

Generates professional software quality insights including:

* Primary Risk Drivers
* Recommended Actions
* Overall Assessment

This helps developers understand and mitigate potential software risks.

---

### 📈 Prediction History Tracking

Stores predictions in CSV format and displays:

* Risk Score
* Risk Level
* Testing Priority
* Prediction Result

allowing users to review recent analyses.

---

## 🧠 Machine Learning Model

### Algorithm Used

Random Forest Classifier

### Why Random Forest?

* High accuracy
* Handles complex feature interactions
* Robust against overfitting
* Provides feature importance for Explainable AI

---

## 📂 Dataset

### NASA PROMISE JM1 Dataset

The model is trained using the NASA JM1 Software Defect Dataset containing software quality metrics such as:

* LOC
* Cyclomatic Complexity
* Essential Complexity
* Design Complexity
* Halstead Metrics
* Branch Count
* Program Length
* Development Effort

and many other software engineering measurements.

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask

### Machine Learning

* Scikit-Learn
* NumPy
* Pandas
* Joblib

### Frontend

* HTML5
* CSS3
* Jinja2 Templates

### Version Control

* Git
* GitHub

---

## 📁 Project Structure

```text
IntelliCode/
│
├── app.py
│
├── model/
│   └── defect_model.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── reports/
│   └── prediction_history.csv
│
├── notebooks/
│   └── model_training.ipynb
│
├── dataset/
│   └── jm1.csv
│
└── README.md
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/IntelliCode.git

cd IntelliCode
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 📸 Current Dashboard Features

✅ Software Defect Prediction

✅ Risk Score Visualization

✅ Risk Level Classification

✅ Testing Priority Assignment

✅ Prediction Result Dashboard

✅ Explainable AI

✅ AI Risk Assessment

✅ Prediction History Tracking

✅ Recent Predictions Table

✅  Basic Python File Metrics Extraction

---

## 📊 Current Project Status

### Phase 1 – Core Defect Prediction System

Completed ✅

* Data Preprocessing
* Model Training
* Random Forest Prediction Engine
* Flask Integration
* Dashboard UI

### Phase 2 – Explainable AI

Completed ✅

* Feature Importance Analysis
* AI Explanation Panel
* Risk Assessment Engine
* Prediction History Logging

---

## 🚀 Upcoming Features (Phase 3)

### Risk Analytics Dashboard

* Total Predictions
* Defect Distribution
* Risk Trends

### Interactive Charts

* Pie Charts
* Bar Charts
* Risk Analytics Visualizations

### CSV Upload Prediction

Predict multiple software modules at once using CSV files.

### Advanced Explainable AI

* SHAP Values
* Local Explanations
* Feature Contribution Graphs

### Deployment

* Render
* Railway
* PythonAnywhere

---

## 🎓 Educational Value

This project demonstrates practical skills in:

* Machine Learning
* Software Engineering
* Explainable AI
* Data Analysis
* Web Development
* Flask Application Development
* GitHub Project Management

---

## 👩‍💻 Author

**Deepika**

B.Tech Information Technology

Aspiring Data Scientist & Software Engineer

---

## ⭐ IntelliCode Vision

To evolve from a Software Defect Prediction Tool into a complete AI-Powered Software Quality Intelligence Platform capable of helping development teams build more reliable, maintainable, and defect-free software.
