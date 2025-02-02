import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EdTech & Career Counselling",
    page_icon="🎓",
    layout="wide"
)

# --- STYLING (CUSTOM CSS) ---
st.markdown("""
    <style>
        body {
            background-color: #f4f6f9;
        }
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
        }
        .sub-title {
            font-size: 22px;
            font-weight: 500;
            color: #34495e;
            text-align: center;
        }
        .custom-button {
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-size: 18px;
            width: 100%;
            cursor: pointer;
        }
        .custom-button:hover {
            background-color: #2980b9;
        }
        .box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
# st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2944/2944397.png", width=150)
st.sidebar.title("📚 EdTech & Counselling")
menu = st.sidebar.radio("Navigate", [
    "Home", "Mock Interview", "AI Counsellor", 
    "Progress Monitoring", "Recruitment"
])

# --- HOME PAGE ---
if menu == "Home":
    st.markdown("<h1 class='main-title'>Welcome to EdTech & Career Counselling</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Empowering your learning and career journey with AI-powered guidance.</p>", unsafe_allow_html=True)
    
    # Login Section
    with st.container():
        st.subheader("🔑 Login to Access Your Dashboard")
        col1, col2 = st.columns([1, 2])
        with col1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", key="login_btn"):
                st.success(f"Welcome, {username}!")

    # Features Section
    st.subheader("🚀 Key Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='box'><h3>📊 Personalized Learning</h3><p>Get a custom learning plan tailored to your skills and goals.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='box'><h3>🏆 AI-Powered Mock Interview</h3><p>Take tests to assess and improve your knowledge.</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='box'><h3>🤖 AI Career Counsellor</h3><p>Receive personalized career advice based on your skills.</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='custom-button'>Explore Features</div>", unsafe_allow_html=True)

# --- Mock Interview ---
elif menu == "Mock Interview":
    st.title("📝 Mock Interview")
    st.write("Take AI-powered assessments to evaluate your skills.")
    hf_space_url = "https://bonbibi-mock-interview-questions.hf.space"
    st.components.v1.iframe(hf_space_url, width=1200, height=1000, scrolling=True)


# --- AI COUNSELLOR ---
elif menu == "AI Counsellor":
    st.title("🤖 AI Career Counsellor")    
    hf_counsellor_url = "https://temo12-careergps.hf.space"
    st.components.v1.iframe(hf_counsellor_url, width=1000, height=500, scrolling=True)


# --- PROGRESS MONITORING ---
elif menu == "Progress Monitoring":
    st.title("📊 Progress Tracking")
    st.write("View your test results and skill growth.")
    st.line_chart([10, 20, 15, 30, 40, 35])  # Placeholder graph

# --- RECRUITMENT OPPORTUNITIES ---
elif menu == "Recruitment":
    st.title("💼 Recruitment Opportunities")
    st.write("Find job openings that match your skills.")
    hf_recruitment_url = "https://charulp2499-jobscrapper.hf.space"
    st.components.v1.iframe(hf_recruitment_url, width=1400, height=1500, scrolling=True)

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.info("© 2025 Amdocs GenAI Participant")
