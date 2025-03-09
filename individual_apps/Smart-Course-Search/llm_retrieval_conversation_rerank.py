import json
import os
from dotenv import load_dotenv
import yaml
from together import Together
from langchain.llms.together import Together as TogetherLLM
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from pinecone import Pinecone
from typing import List, Dict
import cohere
load_dotenv()


API_FILE_PATH = r"API.yml"
COURSES_FILE_PATH = r"courses.json"

# Global list to store conversation history
conversation_history: List[Dict[str, str]] = []

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

def pinecone_similarity_search(pinecone_instance, index_name, query_embedding, top_k=10):
    """Performs a similarity search in Pinecone and increase top k for reranking."""
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
    template = """You are a helpful AI assistant that provides information on courses. 
    Based on the following context, conversation history, and new user query, 
    suggest relevant courses and explain why they might be useful, or respond accordingly if the user query is unrelated. 
    If no relevant courses are found, please indicate that.

    Conversation History:
    {conversation_history}

    Context: {context}
    User Query: {query}

    Response: Let me help you find relevant courses based on your query.
    """
    return PromptTemplate(template=template, input_variables=["context", "query", "conversation_history"])

def initialize_llm(together_api_key):
    """Initializes Together LLM."""
    return TogetherLLM(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        together_api_key=together_api_key,
        temperature=0,
        max_tokens=250
    )

def create_chain(llm, prompt):
    """Creates a chain using the new RunnableSequence approach."""
    chain = (
        {"context": RunnablePassthrough(), "query": RunnablePassthrough(), "conversation_history": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def initialize_cohere_client(cohere_api_key):
    """Initializes the Cohere client."""
    return cohere.ClientV2(api_key=cohere_api_key)


def rerank_results(cohere_client, query, documents, top_n=3):
    """Reranks documents using Cohere."""
    try:
        results = cohere_client.rerank(
            query=query,
            documents=documents,
            top_n=top_n,
            model="rerank-english-v3.0",
        )
        return results
    except Exception as e:
        print(f"Error reranking results: {e}")
        return None

def generate_llm_response(chain, query, retrieved_data, history, cohere_client):
    """Generates an LLM response based on context and conversation history."""
    try:
        if not retrieved_data or not retrieved_data.matches:
            return "I couldn't find any relevant courses matching your query. Please try a different search term."

        # Prepare documents for reranking
        documents = []
        for match in retrieved_data.matches:
            metadata = match.metadata
            if metadata:
                documents.append(
                    { "text" :f"Title: {metadata.get('title', 'No title')}\nDescription: {metadata.get('text', 'No description')}\nLink: {metadata.get('course_link', 'No link')}"
                    }
                )

        if not documents:
            return "I found some matches but couldn't extract course information. Please try again."
        
         # Rerank the documents
        reranked_results = rerank_results(cohere_client, query, documents)

        if not reranked_results:
              return "I couldn't rerank the results, please try again."
        
          # Prepare context from reranked results
        context_parts = []
        for result in reranked_results.results:
            context_parts.append(documents[result.index]["text"])
            
        context = "\n\n".join(context_parts)
            
        # Format conversation history
        formatted_history = "\n".join(f"User: {item['user']}\nAssistant: {item['assistant']}" for item in history) if history else "No previous conversation."

        response = chain.invoke({"context": context, "query": query, "conversation_history":formatted_history})
        return response

    except Exception as e:
        print(f"Error generating response: {e}")
        return "I encountered an error while generating the response. Please try again."
    

def check_context_similarity(query_embedding, previous_query_embedding, threshold=0.7):
    """Checks if the new query is related to the previous one."""
    if not previous_query_embedding:
        return False  # First query, no previous embedding to compare

    from numpy import dot
    from numpy.linalg import norm

    cos_sim = dot(query_embedding, previous_query_embedding) / (norm(query_embedding) * norm(previous_query_embedding))
    return cos_sim > threshold

def main():
    global conversation_history
    previous_query_embedding = None

    try:
        
        api_keys = load_api_keys(API_FILE_PATH)
        together_api_key = api_keys["together_ai_api_key"]
        pinecone_api_key = api_keys["pinecone_api_key"]
        index_name = api_keys["pinecone_index_name"]
        cohere_api_key = api_keys["cohere_api_key"]
        print("Initializing services...")
        
        # Initialize Pinecone
        pinecone_instance = initialize_pinecone(pinecone_api_key)

        # Initialize Together LLM
        llm = initialize_llm(together_api_key)

         # Initialize Cohere client
        cohere_client = initialize_cohere_client(cohere_api_key)


        
        prompt = create_prompt_template()

        # Create chain
        chain = create_chain(llm, prompt)

        print("Ready to process queries!")

        while True:
           
            user_query = input("\nEnter your query (or 'quit' to exit): ").strip()
            
            if user_query.lower() == 'quit':
                break

            if not user_query:
                print("Please enter a valid query.")
                continue

            try:
                print("Generating query embedding...")
                query_embedding = generate_query_embedding(user_query, together_api_key)

                # Check context similarity
                if previous_query_embedding and check_context_similarity(query_embedding, previous_query_embedding):
                     print("Continuing the previous conversation...")
                else:
                    print("Starting a new conversation...")
                    conversation_history = []  # Clear history for a new conversation
                
                print("Searching for relevant courses...")
                pinecone_results = pinecone_similarity_search(
                    pinecone_instance, index_name, query_embedding
                )

                print("Generating response...")
                llm_response = generate_llm_response(chain, user_query, pinecone_results, conversation_history, cohere_client)

                print("\nResponse:")
                print(llm_response)
                print("\n" + "="*50)

                # Update conversation history
                conversation_history.append({"user": user_query, "assistant": llm_response})
                previous_query_embedding = query_embedding  # Save for next turn
               
            except Exception as e:
                print(f"Error processing query: {e}")
                print("Please try again with a different query.")

    except Exception as e:
        print(f"An error occurred during initialization: {str(e)}")

if __name__ == "__main__":
    main()