from flask import Blueprint, request, jsonify
import openai
import os

recommendations_bp = Blueprint("recommendations", __name__)

openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure API key is set

@recommendations_bp.route("/get_courses", methods=["POST"])
def recommend_courses():
    data = request.json
    user_interest = data.get("interest", "")

    if not user_interest:
        return jsonify({"error": "No interest provided"}), 400

    try:
        prompt = f"""
        Based on the interest '{user_interest}', recommend 3 relevant university courses. 
        Provide each course in JSON format with 'title' and 'description'.
        Example:
        [
            {{"title": "Introduction to AI", "description": "Learn the basics of artificial intelligence."}},
            {{"title": "Data Science 101", "description": "Explore data analysis and machine learning concepts."}},
            {{"title": "Python for Beginners", "description": "Master the fundamentals of Python programming."}}
        ]
        """

        # Define the messages variable with the user prompt
        messages = [
            {"role": "system", "content": "You are a helpful assistant that recommends university courses."},
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

        # Extract JSON response
        recommended_courses = response["choices"][0]["message"]["content"]
        
        return jsonify({"recommended_courses": recommended_courses})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

