import openai
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

openai.api_key = "hidden"

@app.route('/')
def home():
    return render_template('chat.html')

def recommend_diet(age, gender, weight, height):
    weight = float(weight)
    height = float(height)
    bmi = weight / ((height / 100) ** 2)

    if gender == "male":
        if bmi > 25:
            return "paleo"
        else:
            return "primal"
    else:
        if bmi > 24:
            return "ketogenic"
        else:
            return "whole30"

def generate_meal_plan(diet_type):
    try:
        response = openai.Completion.create(
          engine="text-davinci-003",
          prompt=f"Create a one-day meal plan for a {diet_type} diet.",
          max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

@app.route('/get-meal-plan', methods=['POST'])
def get_meal_plan():
    try:
        data = request.json
        age = int(data['age'])
        gender = data['gender']
        weight = float(data['weight'])
        height = float(data['height'])

        recommended_diet = recommend_diet(age, gender, weight, height)
        meal_plan = generate_meal_plan(recommended_diet)

        # Include both the recommended diet and the meal plan in the response
        return jsonify({'dietType': recommended_diet, 'mealPlan': meal_plan})
    except ValueError as e:
        return jsonify({"error": "Invalid input: " + str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
