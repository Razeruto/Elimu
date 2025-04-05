from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.config import Config  # Import Config from backend folder
import openai

app = Flask(__name__)
CORS(app)

# Load configuration from backend/config.py
app.config.from_object(Config)

# Initialize JWT
jwt = JWTManager(app)

# Load OpenAI API Key
openai.api_key = Config.OPENAI_API_KEY

# Import routes from the backend/routes directory
from backend.routes.summarizer import summarizer_bp
from backend.routes.chatbot import chatbot_bp
from backend.routes.grading import grading_bp
from backend.routes.recommendations import recommendations_bp
from backend.routes.study_planner import study_planner_bp
from backend.routes.engagement import engagement_bp
from backend.routes.auth import auth_bp

# Register Blueprints with their URL prefixes
app.register_blueprint(summarizer_bp, url_prefix="/summarizer")
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
app.register_blueprint(grading_bp, url_prefix="/grading")
app.register_blueprint(recommendations_bp, url_prefix="/recommendations")
app.register_blueprint(study_planner_bp, url_prefix="/study_planner")
app.register_blueprint(engagement_bp, url_prefix="/engagement")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)
