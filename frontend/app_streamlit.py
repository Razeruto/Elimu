import streamlit as st
from utils import summarize_text, chat_with_ai, grade_assignment, get_recommendations, get_study_plan, track_engagement, register_user, login_user

st.set_page_config(page_title="Elimu Msaidizi", layout="wide")

st.title("📚 Elimu Msaidizi - AI-Powered Education")

menu = st.sidebar.selectbox("Select Feature", ["Summarizer", "Chatbot", "Grading", "Course Recommendations", "Study Planner", "Engagement Tracking", "User Authentication"])

# Summarizer
if menu == "Summarizer":
    st.header("📄 Document Summarizer")
    text = st.text_area("Enter text to summarize")
    summary_type = st.selectbox("Select summary type", ["Concise", "Detailed", "Bullet Points", "Academic", "Simple Language"])
    summary_length = st.slider("Summary Length (%)", 10, 100, 30)

    if st.button("Summarize"):
        result = summarize_text(text, summary_type, summary_length)
        st.subheader("Summary:")
        st.write(result.get("summary", result.get("error", "Error generating summary.")))

# Chatbot
elif menu == "Chatbot":
    st.header("💬 AI Chatbot")
    user_input = st.text_input("Ask something:")
    if st.button("Send"):
        response = chat_with_ai(user_input)
        st.subheader("AI Response:")
        st.write(response.get("response", response.get("error", "Error in chatbot.")))

# Grading
elif menu == "Grading":
    st.header("📝 Automated Grading")
    assignment_question = st.text_area("Enter assignment question")
    student_answer = st.text_area("Enter student answer")
    
    if st.button("Grade"):
        if not assignment_question or not student_answer:
            st.error("Both the assignment question and answer are required.")
        else:
            result = grade_assignment(assignment_question, student_answer)
            st.subheader("Grading Result:")
            st.write(f"💡 Feedback: {result.get('feedback', result.get('error', 'Error in grading.'))}")

elif menu == "Course Recommendations":
    st.header("🎓 Course Recommendations")
    interest = st.text_input("Enter your area of interest:")
    if st.button("Get Recommendations"):
        courses = get_recommendations(interest)
        st.subheader("Recommended Courses:")
        recommended = courses.get("recommended_courses", [])
        # If the response is a string, display it directly.
        if isinstance(recommended, str):
            st.write(recommended)
        else:
            for course in recommended:
                if isinstance(course, dict):
                    st.write(f"📌 {course.get('title', 'No title')} - {course.get('description', 'No description')}")
                else:
                    st.write(course)
# Study Planner
elif menu == "Study Planner":
    st.header("📅 Personalized Study Planner")
    subjects = st.text_area("Enter subjects (comma-separated)").split(",")
    duration = st.selectbox("Select duration", ["1 week", "2 weeks", "1 month"])
    if st.button("Generate Plan"):
        plan = get_study_plan(subjects, duration)
        st.subheader("Your Study Plan:")
        st.write(plan.get("study_plan", plan.get("error", "Error generating plan.")))

# Engagement Tracking
elif menu == "Engagement Tracking":
    st.header("📊 Engagement & Motivation Tracking")
    
    # Ask how many activities to input
    num_entries = st.number_input("How many study activities would you like to enter?", min_value=1, value=1, step=1)
    activities = []
    time_spent_values = []
    
    # Input fields for each activity and its time spent
    for i in range(int(num_entries)):
        activity = st.text_input(f"Activity {i+1} Description", key=f"activity_{i}")
        time_spent = st.number_input(f"Time Spent on Activity {i+1} (minutes)", min_value=1, value=30, key=f"time_{i}")
        activities.append(activity)
        time_spent_values.append(time_spent)
    
    if st.button("Track Engagement"):
        # Filter out empty activity descriptions
        valid_activities = [act for act in activities if act.strip() != ""]
        valid_time_spent = [time_spent_values[i] for i, act in enumerate(activities) if act.strip() != ""]
    
        if not valid_activities:
            st.error("Please enter at least one activity description.")
        elif len(valid_activities) != len(valid_time_spent):
            st.error("Mismatch in activities and time spent values.")
        else:
            # Call the updated track_engagement from utils.py with two parameters.
            result = track_engagement(valid_activities, valid_time_spent)
            st.subheader("Analysis:")
            st.write(f"🕒 Average Study Time: {result.get('average_time_spent', 'N/A')} minutes")
            st.write(f"📈 Performance Score: {result.get('performance_score', 'N/A')}")
            st.write(f"💡 AI Feedback: {result.get('feedback', result.get('error', 'No feedback generated.'))}")

# User Authentication
elif menu == "User Authentication":
    st.header("🔐 User Authentication")
    auth_choice = st.radio("Choose Action", ["Register", "Login"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_choice == "Register":
        if st.button("Register"):
            result = register_user(username, password)
            st.write(result.get("message", result.get("error", "Error in registration.")))

    elif auth_choice == "Login":
        if st.button("Login"):
            result = login_user(username, password)
            st.write(result.get("access_token", result.get("error", "Invalid credentials.")))
