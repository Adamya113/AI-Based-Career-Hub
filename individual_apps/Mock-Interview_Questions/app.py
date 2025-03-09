# import streamlit as st
# from function import GetLLMResponse

# from langchain_community.llms import OpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI

    
# # Page configuration
# st.set_page_config(page_title="Interview Practice Bot",
#                    page_icon="📚",
#                    layout="wide",
#                    initial_sidebar_state="collapsed")




# def main():        
#     roles_and_topics = {      
  
#     "Front-End Developer": ["HTML/CSS", "JavaScript and Frameworks (React, Angular, Vue.js)", "Responsive Design", "Browser Compatibility"],
#     "Back-End Developer": ["Server-Side Languages (Node.js, Python, Ruby, PHP)", "Database Management (SQL, NoSQL)", "API Development", "Server and Hosting Management"],
#     "Full-Stack Developer": ["Combination of Front-End and Back-End Topics", "Integration of Systems", "DevOps Basics"],
#     "Mobile Developer": ["Android Development (Java, Kotlin)", "iOS Development (Swift, Objective-C)", "Cross-Platform Development (Flutter, React Native)"],
#     "Data Scientist": ["Statistical Analysis", "Machine Learning Algorithms", "Data Wrangling and Cleaning", "Data Visualization"],
#     "Data Analyst": ["Data Collection and Processing", "SQL and Database Querying", "Data Visualization Tools (Tableau, Power BI)", "Basic Statistics"],
#     "Machine Learning Engineer": ["Supervised and Unsupervised Learning", "Model Deployment", "Deep Learning", "Natural Language Processing"],
#     "DevOps Engineer": ["Continuous Integration/Continuous Deployment (CI/CD)", "Containerization (Docker, Kubernetes)", "Infrastructure as Code (Terraform, Ansible)", "Cloud Platforms (AWS, Azure, Google Cloud)"],
#     "Cloud Engineer": ["Cloud Architecture", "Cloud Services (Compute, Storage, Networking)", "Security in the Cloud", "Cost Management"],
#     "Cybersecurity Analyst": ["Threat Detection and Mitigation", "Security Protocols and Encryption", "Network Security", "Incident Response"],
#     "Penetration Tester": ["Vulnerability Assessment", "Ethical Hacking Techniques", "Security Tools (Metasploit, Burp Suite)", "Report Writing and Documentation"],
#     "Project Manager": ["Project Planning and Scheduling", "Risk Management", "Agile and Scrum Methodologies", "Stakeholder Communication"],
#     "UX/UI Designer": ["User Research", "Wireframing and Prototyping", "Design Principles", "Usability Testing"],
#     "Quality Assurance (QA) Engineer": ["Testing Methodologies", "Automation Testing", "Bug Tracking", "Performance Testing"],
#     "Blockchain Developer": ["Blockchain Fundamentals", "Smart Contracts", "Cryptographic Algorithms", "Decentralized Applications (DApps)"],
#     "Digital Marketing Specialist": ["SEO/SEM", "Social Media Marketing", "Content Marketing", "Analytics and Reporting"],
#     "AI Research Scientist": ["AI Theory", "Algorithm Development", "Neural Networks", "Natural Language Processing"],
#     "AI Engineer": ["AI Model Deployment", "Machine Learning Engineering", "Deep Learning", "AI Tools and Frameworks"],
#     "Generative AI Specialist (GenAI)": ["Generative Models", "GANs (Generative Adversarial Networks)", "Creative AI Applications", "Ethics in AI"],
#     "Generative Business Intelligence Specialist (GenBI)": ["Automated Data Analysis", "Business Intelligence Tools", "Predictive Analytics", "AI in Business Strategy"]


#     }

#     levels = ['Beginner','Intermediate','Advanced']

#     Question_Difficulty = ['Easy','Medium','Hard']
    

#     st.header("Select AI:")
#     model = st.radio("Model", [ "Gemini","Open AI",])
#     st.write("Selected option:", model)
    
    
    
#     # Header and description
#     st.title("Mock -Interview Practice Bot 📚")
#     st.text("Choose the role and topic for your Interview.")
    
#     # User input for quiz generation
#     ## Layout in columns
#     col4, col1, col2 = st.columns([1, 1, 1])
#     col5, col3 = st.columns([1, 1])


#     with col4:
#         selected_level = st.selectbox('Select level of understanding', levels)
    
#     with col1:
#         selected_topic_level = st.selectbox('Select Role', list(roles_and_topics.keys()))
    
#     with col2:
#         selected_topic = st.selectbox('Select Topic', roles_and_topics[selected_topic_level])
    
    

    
    
#     with col5:
#         selected_Question_Difficulty = st.selectbox('Select Question Difficulty', Question_Difficulty)

#     with col3:
#         num_quizzes = st.slider('Number of Questions', min_value=1, max_value= 10, value=1)
    
#     submit = st.button('Generate Questions')
#     st.write(selected_topic_level, selected_topic, num_quizzes, selected_Question_Difficulty, selected_level, model)
    
#     # Final Response
#     if submit:
#         questions,answers = GetLLMResponse(selected_topic_level, selected_topic, num_quizzes, selected_Question_Difficulty, selected_level, model)
       
#         with st.spinner("Generating Quizzes..."):
#             questions,answers =  GetLLMResponse(selected_topic_level, selected_topic, num_quizzes, selected_Question_Difficulty, selected_level, model)
#             st.success("Quizzes Generated!")


            
#             # Display questions and answers in a table
#             if questions:
#                 st.subheader("Quiz Questions and Answers:")
#                 # Prepare data for the table
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.subheader("Questions")
                    
#                     st.write(questions)
                
#                 with col2:
#                     st.subheader("Answers")

#                     st.write(answers)

               
    
#             else:
#                 st.warning("No Quiz Questions and Answers")
                
#     else:
#         st.warning("Click the 'Generate Quizzes' button to create quizzes.")





    
    


# if __name__ == "__main__":
#     main()




import openai
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import re

def generate_question(role, topic, difficulty_level):
    prompt = f"Generate an interview question for the role of {role} on the topic of {topic} with difficulty level {difficulty_level}."
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GOOGLE_API_KEY"])
    response = llm.invoke(prompt)
    response = response.content
 
    return response

def evaluate_answer(question, user_answer):
    prompt = f"Question: {question}\nUser's Answer: {user_answer}\nEvaluate the answer and provide feedback. Also, provide the best possible answer."
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GOOGLE_API_KEY"])
    response = llm.invoke(prompt)
    response = response.content
 
    return response







# ----------------------

import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_question(role, topic, difficulty_level):
    prompt = f"Generate an interview question for the role of {role} on the topic of {topic} with difficulty level {difficulty_level}."
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GOOGLE_API_KEY"])
    response = llm.invoke(prompt)
    response = response.content
 
    return response

def evaluate_answer(question, user_answer):
    prompt = f"Question: {question}\nUser's Answer: {user_answer}\nEvaluate the answer, give a score out of 100, and provide feedback. Also, provide the best possible answer."
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GOOGLE_API_KEY"])
    response = llm.invoke(prompt)
   
    evaluation = response.content
    # Extract score and feedback from the evaluation
     # Extract score using regular expressions
    score_match = re.search(r'(\d+)/100', evaluation)
    score = int(score_match.group(1)) if score_match else 0

    # Extract feedback
    feedback = evaluation.split('\n', 1)[1] if '\n' in evaluation else evaluation
    return score, feedback

def generate_report():
    st.write("### Interview Report")
    for i in range(st.session_state['total_questions']):
        st.write(f"**Question {i+1}:** {st.session_state['questions'][i]}")
        st.write(f"**Your Answer:** {st.session_state['answers'][i]}")
        st.write(f"**Score:** {st.session_state['scores'][i]}")
        st.write(f"**Feedback:** {st.session_state['feedback'][i]}")
        st.write("---")

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state['questions'] = []
if 'answers' not in st.session_state:
    st.session_state['answers'] = []
if 'feedback' not in st.session_state:
    st.session_state['feedback'] = []
if 'scores' not in st.session_state:
    st.session_state['scores'] = []
if 'current_question' not in st.session_state:
    st.session_state['current_question'] = 0
if 'total_questions' not in st.session_state:
    st.session_state['total_questions'] = 10
if 'question_answered' not in st.session_state:
    st.session_state['question_answered'] = False
if 'interview_started' not in st.session_state:
    st.session_state['interview_started'] = False

st.title("Mock Interview Bot")

if not st.session_state['interview_started']:
    roles_and_topics = {      
  
    "Front-End Developer": ["HTML/CSS", "JavaScript and Frameworks (React, Angular, Vue.js)", "Responsive Design", "Browser Compatibility"],
    "Back-End Developer": ["Server-Side Languages (Node.js, Python, Ruby, PHP)", "Database Management (SQL, NoSQL)", "API Development", "Server and Hosting Management"],
    "Full-Stack Developer": ["Combination of Front-End and Back-End Topics", "Integration of Systems", "DevOps Basics"],
    "Mobile Developer": ["Android Development (Java, Kotlin)", "iOS Development (Swift, Objective-C)", "Cross-Platform Development (Flutter, React Native)"],
    "Data Scientist": ["Statistical Analysis", "Machine Learning Algorithms", "Data Wrangling and Cleaning", "Data Visualization"],
    "Data Analyst": ["Data Collection and Processing", "SQL and Database Querying", "Data Visualization Tools (Tableau, Power BI)", "Basic Statistics"],
    "Machine Learning Engineer": ["Supervised and Unsupervised Learning", "Model Deployment", "Deep Learning", "Natural Language Processing"],
    "DevOps Engineer": ["Continuous Integration/Continuous Deployment (CI/CD)", "Containerization (Docker, Kubernetes)", "Infrastructure as Code (Terraform, Ansible)", "Cloud Platforms (AWS, Azure, Google Cloud)"],
    "Cloud Engineer": ["Cloud Architecture", "Cloud Services (Compute, Storage, Networking)", "Security in the Cloud", "Cost Management"],
    "Cybersecurity Analyst": ["Threat Detection and Mitigation", "Security Protocols and Encryption", "Network Security", "Incident Response"],
    "Penetration Tester": ["Vulnerability Assessment", "Ethical Hacking Techniques", "Security Tools (Metasploit, Burp Suite)", "Report Writing and Documentation"],
    "Project Manager": ["Project Planning and Scheduling", "Risk Management", "Agile and Scrum Methodologies", "Stakeholder Communication"],
    "UX/UI Designer": ["User Research", "Wireframing and Prototyping", "Design Principles", "Usability Testing"],
    "Quality Assurance (QA) Engineer": ["Testing Methodologies", "Automation Testing", "Bug Tracking", "Performance Testing"],
    "Blockchain Developer": ["Blockchain Fundamentals", "Smart Contracts", "Cryptographic Algorithms", "Decentralized Applications (DApps)"],
    "Digital Marketing Specialist": ["SEO/SEM", "Social Media Marketing", "Content Marketing", "Analytics and Reporting"],
    "AI Research Scientist": ["AI Theory", "Algorithm Development", "Neural Networks", "Natural Language Processing"],
    "AI Engineer": ["AI Model Deployment", "Machine Learning Engineering", "Deep Learning", "AI Tools and Frameworks"],
    "Generative AI Specialist (GenAI)": ["Generative Models", "GANs (Generative Adversarial Networks)", "Creative AI Applications", "Ethics in AI"],
    "Generative Business Intelligence Specialist (GenBI)": ["Automated Data Analysis", "Business Intelligence Tools", "Predictive Analytics", "AI in Business Strategy"]


    }




    
    role = st.selectbox('Select Role', list(roles_and_topics.keys()))
    topic = st.selectbox('Select Topic', roles_and_topics[role])
    difficulty_level = st.selectbox("Select difficulty level:", ["Easy", "Medium", "Hard"])

    if st.button("Start Interview"):
        if role and topic and difficulty_level:
            st.session_state['questions'] = [generate_question(role, topic, difficulty_level) for _ in range(st.session_state['total_questions'])]
            st.session_state['current_question'] = 0
            st.session_state['interview_started'] = True
            st.session_state['question_answered'] = False

if st.session_state['interview_started']:
    current_question = st.session_state['current_question']
    if current_question < st.session_state['total_questions']:
        st.write(f"Question {current_question + 1}: {st.session_state['questions'][current_question]}")
        
        if not st.session_state['question_answered']:
            answer = st.text_area("Your Answer:", key=f"answer_{current_question}")
            if st.button("Submit Answer"):
                if answer:
                    st.session_state['answers'].append(answer)
                    score, feedback = evaluate_answer(st.session_state['questions'][current_question], answer)
                    st.session_state['scores'].append(score)
                    st.session_state['feedback'].append(feedback)
                    st.session_state['question_answered'] = True
                    st.write(f"Score: {score}")
                    st.write(f"Feedback: {feedback}")
        
        if st.session_state['question_answered']:
            if st.button("Next Question"):
                st.session_state['current_question'] += 1
                st.session_state['question_answered'] = False
    else:
        st.write("Interview Complete! Generating Report...")
        generate_report()

