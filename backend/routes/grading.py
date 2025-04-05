from flask import Blueprint, request, jsonify
import openai

grading_bp = Blueprint("grading", __name__)

@grading_bp.route("/grade", methods=["POST"])
def grade_assignment():
    data = request.json
    assignment_question = data.get("question", "")
    assignment_answer = data.get("answer", "")

    if not assignment_question or not assignment_answer:
        return jsonify({"error": "Both assignment question and answer are required"}), 400

    try:
        # Construct prompt that asks the model to answer the question and then grade the given answer.
        prompt = (
            f"Assignment Question:\n{assignment_question}\n\n"
            f"Student's Answer:\n{assignment_answer}\n\n"
            "Based on the provided answer, first answer the assignment question and then grade the student's answer in percentage terms. "
            "Also provide feedback and suggest improvements if necessary. "
            "Format your response as a JSON object with the keys 'percentage_grade' and 'feedback'."
        )

        messages = [
            {
                "role": "system", 
                "content": "You are an educational assistant who first answers assignment questions and then grades the student's answer, providing percentage feedback and suggestions for improvement."
            },
            {"role": "user", "content": prompt}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the latest model
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0
        )

        generated_text = response["choices"][0]["message"]["content"].strip()

        # Try to parse the response as JSON. If it fails, return the raw text.
        try:
            result = response_json = openai.util.convert_to_dict(generated_text)
            # Alternatively, use json.loads if generated_text is valid JSON.
            # import json
            # result = json.loads(generated_text)
        except Exception:
            result = {"percentage_grade": "Grade not available", "feedback": generated_text}

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

