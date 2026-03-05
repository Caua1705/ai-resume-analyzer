from langchain_core.prompts import ChatPromptTemplate


def build_resume_analysis_prompt():

    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a senior technical recruiter specialized in evaluating candidates for software engineering, data, and technology roles. "
            "Your job is to objectively analyze resumes and provide structured evaluations."
        ),
        (
            "human",
            """
Evaluate the following resume based on the job description.

JOB DESCRIPTION
Name: {job_name}
Main Activities: {main_activities}
Prerequisites: {prerequisites}
Differentials: {differentials}

RESUME
{curriculo}

INSTRUCTIONS

Analyze the candidate and return a structured evaluation considering:

• How well the candidate matches the prerequisites  
• Relevant experience related to the job activities  
• Technical background and education  
• Languages mentioned in the resume  
• Overall fit for the position  

SCORING RULES

Score must be between 0 and 100.

General guideline:
0–30 → Very weak fit  
31–50 → Weak fit  
51–70 → Moderate fit  
71–85 → Good fit  
86–100 → Excellent fit  

EDUCATION LEVEL

For the field **education_level**, you MUST choose ONLY ONE of the following values:

High School  
Associate Degree  
Technical Degree  
Bachelor's Degree  
Postgraduate  
Master's Degree  
Doctorate  
Course / Certification  
Not Informed  

Choose the **highest education level found in the resume**.

LANGUAGES

List the languages mentioned in the resume (for example: English, Portuguese, Spanish).

OUTPUT REQUIREMENTS

Your response MUST strictly follow the structured schema provided.
Do not add explanations outside the structured output.
"""
        )
    ])