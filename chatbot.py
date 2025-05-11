import os
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama.chat_models import ChatOllama
# from langchain_ollama.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from chat_history import save_chat_log
from vector_embeddings import load_vector_store
import streamlit as st


def get_chain():
    template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are an intelligent and helpful assistant, you are supposed to answer the user questions in a detailed answer format from the provided context, make sure to provide all the details. If the answer is not in the provided context just say, "answer is not available in the context". Do not give incorrect information.
        
        Context : {context}
        Question : {question}
        
        Answer : 
        
        """
    )
    
    model = ChatOllama(model="tinyllama", temperature=0.3)
    return load_qa_chain(model, chain_type="stuff", prompt=template)





def handle_user_input(user_question):
    st.info("Processing your question...")
    

    db = load_vector_store()
        
    docs = db.similarity_search(user_question)
        
    
    chain = get_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    
    st.write("Reply:", response["output_text"])
    save_chat_log(user_question, response["output_text"])
        
