import mysql.connector


def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="intellicode"
    )
    return connection

def save_prediction(filename, prediction, probability, risk_level,
                    loc, complexity, mi):

    connection = connect_db()
    cursor = connection.cursor()

    query = """
    INSERT INTO predictions
    (filename, prediction, probability, risk_level,
     loc, complexity, mi)

    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        filename,
        prediction,
        probability,
        risk_level,
        loc,
        complexity,
        mi
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

def get_prediction_history():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT *
    FROM predictions
    ORDER BY timestamp DESC
    """

    cursor.execute(query)
    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return records

def get_dashboard_stats():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE prediction = 'Healthy Module'
    """)
    healthy_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE prediction = 'Defective Module'
    """)
    defective_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT AVG(probability)
        FROM predictions
    """)
    avg = cursor.fetchone()[0]

    avg_risk = round((avg or 0) * 100, 2)

    cursor.close()
    connection.close()

    return (
        total_predictions,
        healthy_count,
        defective_count,
        avg_risk
    )

if __name__ == "__main__":
    try:
        save_prediction(
            "sample.py",
            "Defective",
            0.91,
            "High",
            120,
            8.4,
            71.5
        )

        print("✅ Prediction saved successfully!")

    except Exception as e:
        print("❌ Error")
        print(e)