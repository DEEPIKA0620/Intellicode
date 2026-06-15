import os
from flask import Flask, render_template, request
import joblib
import numpy as np
import csv
import os

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

@app.route('/')
def home():
    return render_template(
        "index.html",
        prediction=None,
        risk_score=None,
        risk_level=None,
        priority=None,
        history=load_prediction_history(),
        risk_factors=[]
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
    )

if __name__ == "__main__":
    app.run(debug=True)
