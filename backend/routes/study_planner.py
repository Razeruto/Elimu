from flask import Blueprint, request, jsonify
import openai

study_planner_bp = Blueprint("study_planner", __name__)

@study_planner_bp.route("/plan", methods=["POST"])
def generate_study_plan():
    data = request.json
    subjects = data.get("subjects", [])
    duration = data.get("duration", "2 weeks")

    if not subjects:
        return jsonify({"error": "No subjects provided"}), 400

    try:
        prompt = f"Create a structured study plan for the following subjects: {', '.join(subjects)} for {duration}."

        messages = [
            {"role": "system", "content": "You are a helpful assistant that creates study plans."},
            {"role": "user", "content": prompt}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # New engine that's not deprecated
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        generated_text = response["choices"][0]["message"]["content"].strip()
        return generated_text
    except Exception as e:
        return f"Error: {str(e)}"

        study_plan = response["choices"][0]["message"]["content"].strip()
        return jsonify({"study_plan": study_plan})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
