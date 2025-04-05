import requests
import json
from config import API_BASE_URL

def handle_response(response, key="result"):
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)
    
    if response.status_code != 200:
        raise ValueError(f"API Error {response.status_code}: {response.text}")
    
    if not response.text.strip():
        raise ValueError("Empty response from API")
    
    try:
        data = response.json()
        if isinstance(data, dict):
            return data
        else:
            return {key: data}
    except requests.exceptions.JSONDecodeError:
        # Wrap plain text response in a dictionary using the provided key.
        return {key: response.text}

def summarize_text(text, summary_type="Concise", summary_length=30):
    url = f"{API_BASE_URL}/summarizer/summarize"
    payload = {"text": text, "summary_type": summary_type, "summary_length": summary_length}
    response = requests.post(url, json=payload)
    # Expect the summarizer to return a summary.
    return handle_response(response, key="summary")

def chat_with_ai(message):
    url = f"{API_BASE_URL}/chatbot/ask"
    payload = {"message": message}
    response = requests.post(url, json=payload)
    # Expect the chatbot to return its answer under "response".
    return handle_response(response, key="response")

def grade_assignment(question, answer):
    url = f"{API_BASE_URL}/grading/grade"
    payload = {"question": question, "answer": answer}
    response = requests.post(url, json=payload)
    # Expect the grading API to return a JSON object with keys 'percentage_grade' and 'feedback'
    return handle_response(response, key="feedback")


def get_recommendations(interest):
    url = f"{API_BASE_URL}/recommendations/get_courses"
    payload = {"interest": interest}
    response = requests.post(url, json=payload)
    # Expect a list of recommended courses.
    return handle_response(response, key="recommended_courses")

def get_study_plan(subjects, duration):
    url = f"{API_BASE_URL}/study_planner/plan"
    payload = {"subjects": subjects, "duration": duration}
    response = requests.post(url, json=payload)
    # Expect the study plan under "study_plan".
    return handle_response(response, key="study_plan")

def track_engagement(activities, time_spent):
    url = f"{API_BASE_URL}/engagement/track"
    payload = {"activities": activities, "time_spent": time_spent}
    response = requests.post(url, json=payload)
    # Expect the API to return a JSON object with keys 'average_time_spent', 'performance_score', and 'feedback'
    return handle_response(response, key="engagement")

def register_user(username, password):
    url = f"{API_BASE_URL}/auth/register"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    # Expect a registration message.
    return handle_response(response, key="message")

def login_user(username, password):
    url = f"{API_BASE_URL}/auth/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    # Expect an access token on successful login.
    return handle_response(response, key="access_token")
