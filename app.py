import os
from flask import Flask, render_template, request, send_file
import joblib
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

# Load trained model
rf = joblib.load("model/defect_model.pkl")

def load_prediction_history():

    file_path = "reports/prediction_history.csv"

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as file:

        reader = csv.reader(file)

        next(reader, None)

        rows = list(reader)

    return rows[-5:]

def generate_feature_chart():

    features = [
        "LOC",
        "Logical LOC",
        "Halstead Volume",
        "Intelligence",
        "Time Estimate"
    ]

    importance = [
        13.2,
        5.65,
        5.51,
        5.49,
        5.36
    ]

    plt.figure(figsize=(8,4))
    plt.barh(features, importance)

    plt.xlabel("Importance (%)")
    plt.title("Top Risk Drivers")

    plt.tight_layout()

    plt.savefig("static/feature_importance.png")

    plt.close()

def get_dashboard_stats():

    file_path = "reports/prediction_history.csv"

    if not os.path.exists(file_path):
        return 0,0,0,0

    with open(file_path,"r") as file:

        reader = csv.DictReader(file)

        rows = list(reader)

    total_predictions = len(rows)

    healthy_count = sum(
        1 for row in rows
        if row["Prediction"] == "Healthy Module"
    )

    defective_count = sum(
        1 for row in rows
        if row["Prediction"] == "Defective Module"
    )

    if total_predictions > 0:

        avg_risk = round(
            sum(float(row["Risk Score"]) for row in rows)
            / total_predictions,
            2
        )

    else:
        avg_risk = 0

    return (
        total_predictions,
        healthy_count,
        defective_count,
        avg_risk
    )    

@app.route('/')
def home():
    total_predictions, healthy_count, defective_count, avg_risk = get_dashboard_stats()
    return render_template(
        "index.html",
        prediction=None,
        risk_score=None,
        risk_level=None,
        priority=None,
        history=load_prediction_history(),
        risk_factors=[],
        top_features=[],
        overall_assessment="",
        total_predictions=total_predictions,
        healthy_count=healthy_count,
        defective_count=defective_count,
        avg_risk=avg_risk,
)

@app.route('/predict', methods=['POST'])
def predict():
    # Sample software metrics
    sample = [[
float(request.form["loc"]),
float(request.form["vg"]),
float(request.form["evg"]),
float(request.form["ivg"]),
float(request.form["n"]),
float(request.form["v"]),
float(request.form["l"]),
float(request.form["d"]),
float(request.form["i"]),
float(request.form["e"]),
float(request.form["b"]),
float(request.form["t"]),
float(request.form["locode"]),
float(request.form["locomment"]),
float(request.form["loblank"]),
float(request.form["loccodecomment"]),
float(request.form["uniqop"]),
float(request.form["uniqopnd"]),
float(request.form["totalop"]),
float(request.form["totalopnd"]),
float(request.form["branchcount"])
]]


    prediction = rf.predict(sample)[0]
    probability = rf.predict_proba(sample)[0][1]
    print("Prediction:", prediction)
    print("Probability:", probability)
    risk_score = round(probability * 100, 2)
    generate_feature_chart()
    # Determine risk factors
    risk_factors = []

    if float(request.form["vg"]) > 20:
        risk_factors.append(f"⚠ High Cyclomatic Complexity ({request.form['vg']})")

    if float(request.form["loc"]) > 300:
        risk_factors.append(f"⚠ Large LOC ({request.form['loc']})")

    if float(request.form["v"]) > 1000:
        risk_factors.append(f"⚠ High Halstead Volume ({request.form['v']})")

    if float(request.form["branchcount"]) > 30:
        risk_factors.append(f"⚠ High Branch Count ({request.form['branchcount']})")

    if len(risk_factors) == 0:
        risk_factors.append("✅ No major risk factors detected")

    # Determine risk level and priority from risk score
    if risk_score <= 40:
        risk_level = "Low"
        priority = "Priority 3"
    elif risk_score <= 60:
        risk_level = "Medium"
        priority = "Priority 2"
    else:
        risk_level = "High"
        priority = "Priority 1"

    prediction_text = "Defective Module" if prediction == 1 else "Healthy Module"

    top_features = [
        ("LOC", 13.2),
        ("Logical LOC", 5.65),
        ("Halstead Volume", 5.51),
        ("Intelligence", 5.49),
        ("Time Estimate", 5.36)
    ]

    if risk_score >= 70:
        overall_assessment = """
        This module exhibits elevated software complexity and
        defect-prone characteristics. Additional testing,
        code review, and quality assurance efforts are strongly
        recommended before deployment.
        """
    elif risk_score >= 40:
        overall_assessment = """
        This module shows moderate risk indicators.
        Targeted testing and focused code review are
        recommended to improve software reliability.
        """
    else:
        overall_assessment = """
        The software metrics indicate a stable and maintainable
        module with a relatively low probability of defects.
        Standard testing procedures should be sufficient.
        """

    # Save prediction to history
    file_path = "reports/prediction_history.csv"
    os.makedirs("reports", exist_ok=True)
    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Risk Score", "Risk Level", "Priority", "Prediction"])
        writer.writerow([risk_score, risk_level, priority, prediction_text])

    history = load_prediction_history()
    total_predictions, healthy_count, defective_count, avg_risk = get_dashboard_stats()
    return render_template(
        "index.html",
        prediction=int(prediction),
        prediction_text=prediction_text,
        risk_score=risk_score,
        risk_level=risk_level,
        priority=priority,
        history=history,
        risk_factors=risk_factors,
        top_features=top_features,
        overall_assessment=overall_assessment,
        total_predictions=total_predictions,
        healthy_count=healthy_count,
        defective_count=defective_count,
        avg_risk=avg_risk
    )

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['csv_file']

    if file.filename == '':
        return "No file selected"

    df = pd.read_csv(file)
    # Replace ? with NaN
    df.replace("?", np.nan, inplace=True)

    # Convert everything to numeric
    df = df.apply(pd.to_numeric, errors="coerce")

    # Fill missing values
    df.fillna(df.median(), inplace=True)

    # Remove columns not used by model
    df = df.drop(columns=["id", "defects"], errors="ignore")

    print(df.columns.tolist())

    predictions = rf.predict(df)

    probabilities = rf.predict_proba(df)[:, 1]

    df["Risk Score"] = (probabilities * 100).round(2)

    df["Prediction"] = [
        "Defective Module" if p == 1
        else "Healthy Module"
        for p in predictions
    ]

    output_file = "reports/bulk_predictions.csv"

    os.makedirs("reports", exist_ok=True)
    df.to_csv(output_file, index=False)

    total_modules = len(df)

    defective_modules = len(
        df[df["Prediction"] == "Defective Module"]
    )

    healthy_modules = len(
        df[df["Prediction"] == "Healthy Module"]
    )

    avg_risk = round(
        df["Risk Score"].mean(),
        2
    )
    # Generate pie chart
    plt.figure(figsize=(5,5))

    plt.pie(
        [healthy_modules, defective_modules],
        labels=["Healthy", "Defective"],
        autopct="%1.1f%%"
    )

    plt.title("Module Distribution")

    plt.savefig("static/bulk_pie_chart.png")

    plt.close()

    return render_template(
        "bulk_results.html",

        total_modules=total_modules,

        healthy_count=healthy_modules,

        defective_count=defective_modules,

        avg_risk=avg_risk,

        table_html=df.to_html(
            classes="results-table",
            index=False
        )
    )

@app.route('/download_report')
def download_report():
    return send_file(
        "reports/bulk_predictions.csv",
        as_attachment=True
    )
if __name__ == "__main__":
    app.run(debug=True)
