# AI-ResumeForge

AI-ResumeForge is an AI-driven tool designed to automate resume tailoring for specific job applications. Leveraging Langchain and the Groq API, this project performs intelligent job description analysis and skill extraction to generate personalized resumes that highlight your most relevant qualifications. Built with FastAPI, AI-ResumeForge provides a robust and scalable API for career optimization. Key technologies include LCEL for defining the AI pipeline and Pydantic for data validation. This project showcases my skills in AI, LLM integration with Groq, API development, and prompt engineering.

This project addresses the challenge of manually tailoring resumes for each job application, which can be a time-consuming and tedious process. AI-ResumeForge automates this process by:

1.  Scraping the job description from a given URL.
2.  Using Langchain and the Groq API to extract key skills and requirements.
3.  Tailoring the provided resume data to match the extracted skills.
4.  Returning a tailored resume as a JSON response.

Key technologies used: Langchain, Groq API, FastAPI, Pydantic.

## Installation

1.  Clone the repository: `git clone [repository URL]`
2.  Navigate to the project directory: `cd ai-resume-forge`
3.  Install dependencies using Poetry: `poetry install`
4.  Set the Groq API key as an environment variable: `export GROQ_API_KEY=[your API key]`

## Usage

1.  Run the FastAPI application: `poetry run uvicorn AgentPro1:app --reload`
2.  Send a POST request to the `/generate` endpoint with the following JSON body:

```json
{
  "job_url": "https://example.com/job-description",
  "resume_data": "Your resume text here",
  "session_id": "unique_session_id"
}
