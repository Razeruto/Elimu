from flask import Blueprint, request, jsonify
import openai

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/ask", methods=["POST"])
def ask_chatbot():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # New engine that's not deprecated
            messages=[{"role": "user", "content": user_message}],
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
        reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"response": reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
