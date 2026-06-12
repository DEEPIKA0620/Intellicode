import os

from flask import Flask, render_template, request
import joblib
import numpy as np
import csv
import os

app = Flask(__name__)

# Load trained model
rf = joblib.load("model/defect_model.pkl")

@app.route('/')
def home():
    return render_template(
        "index.html",
        risk_score=None,
        risk_level=None,
        priority=None
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

    if risk_score <= 30:
        risk_level = "Low"
        priority = "Priority 3"
    elif risk_score <= 70:
        risk_level = "Medium"
        priority = "Priority 2"
    else:
        risk_level = "High"
        priority = "Priority 1"
    # Save prediction to history
    file_path = "reports/prediction_history.csv"
    os.makedirs("reports", exist_ok=True)
    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Risk Score", "Risk Level", "Priority", "Prediction"])
        writer.writerow([risk_score, risk_level, priority, int(prediction)])

    return render_template(
        "index.html",
        prediction=int(prediction),
        risk_score=risk_score,
        risk_level=risk_level,
        priority=priority
    )

if __name__ == "__main__":
    app.run(debug=True)
