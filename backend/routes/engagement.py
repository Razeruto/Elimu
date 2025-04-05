from flask import Blueprint, request, jsonify
import openai
import json

engagement_bp = Blueprint("engagement", __name__)

@engagement_bp.route("/track", methods=["POST"])
def track_engagement():
    data = request.json
    activities = data.get("activities", [])
    time_spent_values = data.get("time_spent", [])
    
    if not activities or not time_spent_values:
        return jsonify({"error": "Both activities and time_spent data are required"}), 400
    if len(activities) != len(time_spent_values):
        return jsonify({"error": "The number of activities and time_spent values must match"}), 400

    try:
        avg_time = sum(time_spent_values) / len(time_spent_values)
        # Build prompt with both lists as inputs
        prompt = (
            f"Given the following study activities: {activities} and their corresponding time spent (in minutes): {time_spent_values}, "
            "calculate the average study time, simulate a performance score between 70 and 95, and provide motivational feedback. "
            "Return your result as a JSON object with the keys 'average_time_spent', 'performance_score', and 'feedback'."
        )

        messages = [
            {"role": "system", "content": "You are a helpful assistant that analyzes study activities and provides motivational feedback."},
            {"role": "user", "content": prompt}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0
        )

        generated_text = response["choices"][0]["message"]["content"].strip()

        try:
            result = json.loads(generated_text)
        except json.JSONDecodeError:
            # Fallback if parsing fails
            result = {"average_time_spent": avg_time, "performance_score": None, "feedback": generated_text}

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
