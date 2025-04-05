from flask import Blueprint, request, jsonify
import openai

summarizer_bp = Blueprint("summarizer", __name__)

summary_prompts = {
    "Concise": "Summarize this text briefly.",
    "Detailed": "Summarize this text in a detailed yet concise manner.",
    "Bullet Points": "Summarize this text in bullet points.",
    "Academic": "Summarize this text formally with key points.",
    "Simple Language": "Summarize this text using simple, easy-to-understand language."
}

@summarizer_bp.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "").strip()
    summary_type = data.get("summary_type", "Concise")
    summary_length = data.get("summary_length", 30)

    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"{summary_prompts.get(summary_type, 'Summarize this text.')}\n\nText: {text}"
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}]

    try:
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
        summary = response["choices"][0]["message"]["content"].strip()

        return jsonify({"summary": summary, "summary_type": summary_type, "summary_length": summary_length})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
