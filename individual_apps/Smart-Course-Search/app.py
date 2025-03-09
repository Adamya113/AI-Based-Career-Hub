import yaml
from together import Together
from langchain.llms.together import Together as TogetherLLM
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from pinecone import Pinecone
import gradio as gr
from dotenv import load_dotenv
import os

load_dotenv()


API_FILE_PATH = r"API.yml"
COURSES_FILE_PATH = r"courses.json"

def load_api_keys(api_file_path):
    """Loads API keys from a YAML file."""
    with open(api_file_path, 'r') as f:
        api_keys = yaml.safe_load(f)
    return api_keys

def generate_query_embedding(query, together_api_key):
    """Generates embedding for the user query."""
    client = Together(api_key=together_api_key)
    response = client.embeddings.create(
        model="WhereIsAI/UAE-Large-V1", input=query
    )
    return response.data[0].embedding

def initialize_pinecone(pinecone_api_key):
    """Initializes Pinecone with API key."""
    return Pinecone(api_key=pinecone_api_key)

def pinecone_similarity_search(pinecone_instance, index_name, query_embedding, top_k=5):
    """Performs a similarity search in Pinecone."""
    try:
        index = pinecone_instance.Index(index_name)
        results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        if not results.matches:
            return None
        return results
    except Exception as e:
        print(f"Error during similarity search: {e}")
        return None

def create_prompt_template():
    """Creates a prompt template for LLM."""
    template = """You are a helpful AI course advisor. Based on the following context and query, suggest relevant courses.
    For each course, explain:
    1. Why it's relevant to the query
    2. What the student will learn
    3. Who should take this course
    
    If no relevant courses are found, suggest alternative search terms.

    Context: {context}
    User Query: {query}

    Response: Let me help you find the perfect courses for your needs! 🎓
    """
    return PromptTemplate(template=template, input_variables=["context", "query"])

def initialize_llm(together_api_key):
    """Initializes Together LLM."""
    return TogetherLLM(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        together_api_key=together_api_key,
        temperature=0.3,
        max_tokens=500
    )

def create_chain(llm, prompt):
    """Creates a chain using the RunnableSequence approach."""
    chain = (
        {"context": RunnablePassthrough(), "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def format_course_info(metadata):
    """Formats course information with emojis and styling."""
    return f"""
📚 **Course Title:** {metadata.get('title', 'No title')}

📝 **Description:** {metadata.get('text', 'No description')}

🔗 **Course Link:** {metadata.get('course_link', 'No link')}

👨‍🏫 **Instructor:** {metadata.get('instructor', 'Not specified')}

⏱️ **Duration:** {metadata.get('duration', 'Not specified')}

📊 **Level:** {metadata.get('difficulty_level', 'Not specified')}

💰 **Price:** {metadata.get('price', 'Not specified')}
"""

def generate_llm_response(chain, query, retrieved_data):
    """Generates an LLM response with formatted course information."""
    try:
        if not retrieved_data or not retrieved_data.matches:
            return "🔍 I couldn't find any relevant courses matching your query. Please try different search terms."

        context_parts = []
        formatted_courses = []
        
        for match in retrieved_data.matches:
            metadata = match.metadata
            if metadata:
                context_parts.append(
                    f"Title: {metadata.get('title', 'No title')}\n"
                    f"Description: {metadata.get('text', 'No description')}\n"
                    f"Link: {metadata.get('course_link', 'No link')}"
                )
                formatted_courses.append(format_course_info(metadata))

        if not context_parts:
            return "⚠️ I found some matches but couldn't extract course information. Please try again."

        context = "\n\n".join(context_parts)
        llm_analysis = chain.invoke({"context": context, "query": query})

        separator = "=" * 50
        final_response = f"""
{llm_analysis}

🎯 Here are the detailed course listings:
{separator}
{''.join(formatted_courses)}
"""
        return final_response

    except Exception as e:
        print(f"Error generating response: {e}")
        return "❌ I encountered an error while generating the response. Please try again."

def create_gradio_interface(api_keys):
    """Creates a custom Gradio interface with improved styling."""
    # Initialize components
    pinecone_instance = initialize_pinecone(api_keys["pinecone_api_key"])
    llm = initialize_llm(api_keys["together_ai_api_key"])
    prompt = create_prompt_template()
    chain = create_chain(llm, prompt)

    def process_query(query):
        try:
            query_embedding = generate_query_embedding(query, api_keys["together_ai_api_key"])
            results = pinecone_similarity_search(
                pinecone_instance, 
                api_keys["pinecone_index_name"], 
                query_embedding
            )
            response = generate_llm_response(chain, query, results)
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        background-color: #f0f8ff;
    }
    .input-box {
        border: 2px solid #2e86de;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .output-box {
        background-color: #ffffff;
        border: 2px solid #54a0ff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .heading {
        color: #2e86de;
        text-align: center;
        margin-bottom: 20px;
    }
    .submit-btn {
        background-color: #2e86de !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
    }
    .examples {
        margin-top: 20px;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    """

    # Create Gradio interface with custom theme
    theme = gr.themes.Soft().set(
        body_background_fill="#f0f8ff",
        block_background_fill="#ffffff",
        block_border_width="2px",
        block_border_color="#2e86de",
        block_radius="10px",
        button_primary_background_fill="#2e86de",
        button_primary_text_color="white",
        input_background_fill="#ffffff",
        input_border_color="#2e86de",
        input_radius="8px",
    )

    with gr.Blocks(theme=theme, css=custom_css) as demo:
        gr.Markdown(
            """
            # 🎓 Course Recommendation Assistant
            
            Welcome to your personalized course finder! Ask me about any topics you're interested in learning.
            I'll help you discover the perfect courses from Analytics Vidhya's collection.
            
            ## 🌟 Features:
            - 📚 Detailed course recommendations
            - 🎯 Learning path suggestions
            - 📊 Course difficulty levels
            - 💰 Price information
            """,
            elem_classes=["heading"]
        )
        
        with gr.Row():
            with gr.Column():
                query_input = gr.Textbox(
                    label="What would you like to learn? 🤔",
                    placeholder="e.g., 'machine learning for beginners' or 'advanced python courses'",
                    lines=3,
                    elem_classes=["input-box"]
                )
                submit_btn = gr.Button(
                    "🔍 Find Courses",
                    variant="primary",
                    elem_classes=["submit-btn"]
                )

        with gr.Row():
            output = gr.Markdown(
                label="Recommendations 📚",
                elem_classes=["output-box"]
            )

        with gr.Row(elem_classes=["examples"]):
            gr.Examples(
                examples=[
                    ["I want to learn machine learning from scratch"],
                    ["Advanced deep learning courses"],
                    ["Data visualization tutorials"],
                    ["Python programming for beginners"],
                    ["Natural Language Processing courses"]
                ],
                inputs=query_input,
                label="📝 Example Queries"
            )

        submit_btn.click(
            fn=process_query,
            inputs=query_input,
            outputs=output
        )

    return demo

def main():
    try:
        
        api_keys = load_api_keys(API_FILE_PATH)
        
        
        demo = create_gradio_interface(api_keys)
        demo.launch(
            share=True)

    except Exception as e:
        print(f"An error occurred during initialization: {str(e)}")

if __name__ == "__main__":
    main()
