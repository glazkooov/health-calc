import os
import psycopg2
import psycopg2.extras
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

CALC_URL = os.getenv("CALC_URL", "http://localhost:5001")


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


@app.route("/api/records", methods=["GET"])
def get_records():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM measurements ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    for r in rows:
        r["height"] = float(r["height"])
        r["weight"] = float(r["weight"])
        r["bmi"] = float(r["bmi"])
        r["created_at"] = r["created_at"].strftime("%d.%m.%Y %H:%M")
    return jsonify(rows)


@app.route("/api/calc", methods=["POST"])
def calc():
    data = request.get_json() or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"error": "Введите имя"}), 400

    params = {
        "weight": data.get("weight"),
        "height": data.get("height"),
        "age": data.get("age"),
        "gender": data.get("gender", "m"),
        "activity": data.get("activity", "1")
    }

    try:
        resp = requests.get(CALC_URL + "/calc", params=params, timeout=5)
    except requests.RequestException:
        return jsonify({"error": "Сервис расчета недоступен"}), 502

    result = resp.json()
    if resp.status_code != 200:
        return jsonify(result), resp.status_code

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO measurements (name, gender, age, height, weight, bmi, category, calories) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (name, params["gender"], params["age"], params["height"], params["weight"],
         result["bmi"], result["category"], result["calories"])
    )
    result["id"] = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(result), 201


@app.route("/api/records/<int:rid>", methods=["DELETE"])
def delete_record(rid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM measurements WHERE id = %s", (rid,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"deleted": rid})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
