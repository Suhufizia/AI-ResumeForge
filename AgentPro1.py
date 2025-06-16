from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough
from typing import Dict, List
import os  # Import the os module

app = FastAPI()

# In-memory storage for chat history (replace with a database for production)
chat_history: Dict[str, List[str]] = {}

# 1. Web Scraping (Simplified)
def scrape_job_description(url: str) -> str:
    return f"This is a job description from {url}. Requires skills in Python, FastAPI, and LangChain."

# Get the Groq API key from the environment variable
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")

# Initialize the ChatGroq model
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# 2. Data Processing Chain
data_processing_template = PromptTemplate(
    input_variables=["job_description"],
    template="Extract key skills and requirements from the following job description:\n{job_description}"
)
data_processing_chain = LLMChain(llm=model, prompt=data_processing_template, output_key="skills")

# 3. Resume Generation Chain
resume_template = PromptTemplate(
    input_variables=["skills", "resume_data"],
    template="""
    You are an expert resume writer. Tailor the resume using the following skills and requirements: {skills}.
    Here is some resume data for inspiration: {resume_data}
    """
)
resume_chain = LLMChain(llm=model, prompt=resume_template, output_key="tailored_resume")

# 4. Overall Chain using LCEL
chain = (
    {"job_description": RunnablePassthrough(), "resume_data": RunnablePassthrough()}
    | data_processing_chain
    | {"skills": lambda x: x["skills"], "resume_data": lambda x: x["resume_data"]}
    | resume_chain
)

# 5. Chat History
memory = ConversationBufferMemory(memory_key="chat_history", input_key="job_description")

class JobInput(BaseModel):
    job_url: str
    resume_data: str
    session_id: str

@app.post("/generate")
async def generate_resume(job_input: JobInput):
    job_description = scrape_job_description(job_input.job_url)
    resume_data = job_input.resume_data

    result = chain.invoke({"job_description": job_description, "resume_data": resume_data})

    return {"tailored_resume": result["tailored_resume"]}
