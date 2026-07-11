import os
from flask import Flask, render_template, request, send_file
import joblib
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
from utils.metrics_extractor import extract_basic_metrics, extract_radon_metrics
from utils.feature_mapper import map_features
UPLOAD_FOLDER = r"C:\Temp\IntelliCodeUploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
from database import (
    save_prediction,
    get_prediction_history,
    get_dashboard_stats
)
from utils.pdf_report import generate_pdf_report
from bulk_pdf_report import generate_bulk_pdf_report

METRIC_NAMES = {
    "loc": "Lines of Code",
    "locode": "Logical Lines of Code",
    "locomment": "Comment Lines",
    "loblank": "Blank Lines",
    "loccodecomment": "LOC + Comments",
    "vg": "Cyclomatic Complexity",
    "evg": "Essential Complexity",
    "ivg": "Design Complexity",
    "n": "Program Length",
    "v": "Halstead Volume",
    "l": "Program Level",
    "d": "Difficulty",
    "i": "Intelligence",
    "e": "Effort",
    "b": "Estimated Bugs",
    "t": "Time Required",
    "uniqop": "Unique Operators",
    "uniqopnd": "Unique Operands",
    "totalop": "Total Operators",
    "totalopnd": "Total Operands",
    "branchcount": "Branch Count"
}

app = Flask(__name__)

# Load trained model
rf = joblib.load("model/defect_model.pkl")
def load_prediction_history():
    return get_prediction_history()

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
        # NEW VARIABLES
        extracted_metrics=None,
        uploaded_filename=None,
        analysis_mode=None,
        all_metrics=None,
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

    # maintainability_index may not be available for manual input
    maintainability_index = None

    save_prediction(
        "Manual Input",
        prediction_text,
        probability,
        risk_level,
        float(request.form["loc"]),
        float(request.form["vg"]),
        maintainability_index
    )

    pdf_path = generate_pdf_report(
    filename="Manual Input",
    prediction=prediction_text,
    risk_score=risk_score,
    risk_level=risk_level,
    loc=float(request.form["loc"]),
    complexity=float(request.form["vg"]),
    mi=None
)

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
        avg_risk=avg_risk,
        pdf_report=pdf_path
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

    df["Module ID"] = range(1, len(df) + 1)

    df["Risk Score"] = (probabilities * 100).round(2)

    df["Prediction"] = [
        "Defective Module" if p == 1
        else "Healthy Module"
        for p in predictions
    ]
    for index, row in df.iterrows():

      if row["Risk Score"] <= 40:
         risk_level = "Low"
      elif row["Risk Score"] <= 60:
         risk_level = "Medium"
      else:
         risk_level = "High"

      save_prediction(
          f"Module {int(row['Module ID'])}",
          row["Prediction"],
          row["Risk Score"] / 100,
          risk_level,
          row["loc"],
          row["v(g)"],
          None
    )
    
    top_risk_modules = (
    df.sort_values(
        by="Risk Score",
        ascending=False
    )
    .head(10)
    .to_dict("records")
    )

    highest_module = df.sort_values(
        by="Risk Score",
        ascending=False
    ).iloc[0]["Module ID"]

    highest_risk = df.sort_values(
        by="Risk Score",
        ascending=False
    ).iloc[0]["Risk Score"]

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

    bulk_pdf_path = generate_bulk_pdf_report(
    filename=file.filename,
    total_modules=total_modules,
    healthy_count=healthy_modules,
    defective_count=defective_modules,
    avg_risk=avg_risk,
    highest_module=highest_module,
    highest_risk=highest_risk,
    top_risk_modules=top_risk_modules
)

    return render_template(
        "bulk_results.html",

        total_modules=total_modules,

        healthy_count=healthy_modules,

        defective_count=defective_modules,

        avg_risk=avg_risk,

        highest_module=highest_module,
        highest_risk=highest_risk,

        table_html=df.head(20).to_html(
            classes="results-table",
            index=False
        ),
        top_risk_modules=top_risk_modules,
        bulk_pdf=bulk_pdf_path
    )

@app.route('/download_csv')
def download_csv():
    return send_file(
        "reports/bulk_predictions.csv",
        as_attachment=True
    )
@app.route("/analyze_python", methods=["POST"])
def analyze_python():

    file = request.files["python_file"]

    if file.filename == "":
        return "No file selected."

    upload_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(upload_path)

    basic_metrics = extract_basic_metrics(upload_path)

    with open(upload_path, "r", encoding="utf-8") as f:
      code = f.read()

    radon_metrics = extract_radon_metrics(code)

    features = map_features(
    basic_metrics,
    radon_metrics
)
    feature_vector = [[

    features["loc"],
    features["vg"],
    features["evg"],
    features["ivg"],
    features["n"],
    features["v"],
    features["l"],
    features["d"],
    features["i"],
    features["e"],
    features["b"],
    features["t"],
    features["locode"],
    features["locomment"],
    features["loblank"],
    features["loccodecomment"],
    features["uniqop"],
    features["uniqopnd"],
    features["totalop"],
    features["totalopnd"],
    features["branchcount"]

]]
    prediction = rf.predict(feature_vector)[0]

    probability = rf.predict_proba(feature_vector)[0][1]

    risk_score = round(probability * 100, 2)

    if risk_score <= 40:
       risk_level = "Low"
       priority = "Priority 3"

    elif risk_score <= 60:
         risk_level = "Medium"
         priority = "Priority 2"

    else:
        risk_level = "High"
        priority = "Priority 1"

    prediction_text = (
         "Defective Module"
         if prediction == 1
         else "Healthy Module"
)

    uploaded_filename = file.filename

    save_prediction(
        file.filename,
        prediction_text,
        probability,
        risk_level,
        features["loc"],
        features["vg"],
        radon_metrics["maintainability_index"]
    )

    pdf_path = generate_pdf_report(
        filename=uploaded_filename,
        prediction=prediction_text,
        risk_score=risk_score,
        risk_level=risk_level,
        loc=basic_metrics.get("loc", features["loc"]),
        complexity=basic_metrics.get("v(g)", features["vg"]),
        mi=radon_metrics.get("maintainability_index")
    )

    print("\n========== PYTHON FILE ANALYSIS ==========")

    print("Prediction :", prediction_text)

    print("Risk Score :", risk_score)

    print("Risk Level :", risk_level)

    print("Priority :", priority)

    print("=========================================\n")

    print("Basic Metrics:")
    print(basic_metrics)

    print("\nRadon Metrics:")
    print(radon_metrics)

    print("\nMapped Features:")
    print(features)

    print("\nFeature Vector:")
    print(feature_vector)

    display_metrics = {}

    for key, value in features.items():
        display_metrics[METRIC_NAMES.get(key, key)] = value

    return render_template(

    "index.html",

    prediction=int(prediction),

    risk_score=risk_score,

    risk_level=risk_level,

    priority=priority,

    extracted_metrics=features,

    all_metrics=display_metrics,

    uploaded_filename=file.filename,

    analysis_mode="python",

    pdf_report=pdf_path

)

@app.route("/download_report")
def download_report():

    return send_file(
        "reports/IntelliCode_Report.pdf",
        as_attachment=True,
        download_name="IntelliCode_Report.pdf"
    )

@app.route("/download_bulk_report")
def download_bulk_report():

    return send_file(
        "reports/IntelliCode_Bulk_Report.pdf",
        as_attachment=True,
        download_name="IntelliCode_Bulk_Report.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
