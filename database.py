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