from langchain_community.llms import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st



def get_answers(questions,model):


    answer_prompt = (f"I want you to become a teacher answer this specific Question: {questions}. You should gave me a straightforward and consise explanation and answer to each one of them")

    
    if model == "Open AI":
        llm = OpenAI(temperature=0.8, openai_api_key=st.secrets["OPENAI_API_KEY"])
        answers = llm(answer_prompt)
        # return questions
        
    elif model == "Gemini":
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GOOGLE_API_KEY"])
        answers = llm.invoke(answer_prompt)
        answers = answers.content
        # return questions.content

    return(answers)    




def GetLLMResponse(selected_topic_level, selected_topic, num_quizzes, selected_Question_Difficulty, selected_level, model):


    for i in range(num_quizzes):
        question_prompt = (f'You are an AI interview assistant that helps generate customized interview questions for various technical and non-technical roles. Your task is to create a set of interview questions based on the {selected_topic_level} and topic : {selected_topic}.Ensure the questions match the indicated level of understanding:{selected_level} and difficulty:{selected_Question_Difficulty}. Generate only 1 question.')
        
        
        if model == "Open AI":
            llm = OpenAI(temperature=0.7, openai_api_key=st.secrets["OPENAI_API_KEY"])
            questions = llm(question_prompt)
            
            
        elif model == "Gemini":
            llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GOOGLE_API_KEY"])
            questions = llm.invoke(question_prompt)
            questions = questions.content
            # return questions.content
    
        # answers = "testing"
    
        answers = get_answers(questions,model)
    

    return(questions,answers)
    