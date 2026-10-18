from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

ACTIVITY = {
    "1": 1.2,
    "2": 1.375,
    "3": 1.55,
    "4": 1.725,
    "5": 1.9
}


def bmi_category(bmi):
    if bmi < 18.5:
        return "Недостаток массы"
    elif bmi < 25:
        return "Норма"
    elif bmi < 30:
        return "Избыточный вес"
    else:
        return "Ожирение"


@app.route("/calc")
def calc():
    try:
        weight = float(request.args.get("weight"))
        height = float(request.args.get("height"))
        age = int(request.args.get("age"))
    except (TypeError, ValueError):
        return jsonify({"error": "Вес, рост и возраст должны быть числами"}), 400

    gender = request.args.get("gender", "m")
    activity = request.args.get("activity", "1")

    if weight <= 0 or height <= 0 or age <= 0:
        return jsonify({"error": "Значения должны быть больше нуля"}), 400
    if activity not in ACTIVITY:
        return jsonify({"error": "Неверный уровень активности"}), 400

    bmi = weight / (height / 100) ** 2

    # формула Миффлина - Сан Жеора
    bmr = 10 * weight + 6.25 * height - 5 * age
    if gender == "f":
        bmr -= 161
    else:
        bmr += 5

    calories = bmr * ACTIVITY[activity]

    return jsonify({
        "bmi": round(bmi, 1),
        "category": bmi_category(bmi),
        "bmr": round(bmr),
        "calories": round(calories)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
