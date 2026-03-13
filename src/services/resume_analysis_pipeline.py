from src.services.pdf_service import extract_pdf_text
from src.services.storage_service import upload_resume
from src.services.resume_llm_service import LLMResumeAnalyzer
from src.config.settings import OPENAI_API_KEY


def run_resume_analysis_pipeline(
    files,
    job,
    education_repo,
    resume_repo,
    analysis_repo,
):

    texts = []

    for file in files:
        text = extract_pdf_text(file.getvalue())
        texts.append(text)

    analyzer = LLMResumeAnalyzer(OPENAI_API_KEY)
    responses = analyzer.analyze(job, texts)

    for i, file in enumerate(files):

        text = texts[i]
        response = responses[i]

        file_path = upload_resume(
            file.getvalue(),
            job.name,
        )

        resume = resume_repo.add_resume(
            file_path,
            text,
            job.id,
        )

        analysis_repo.add_analysis(
            resume_id=resume.id,
            job_id=job.id,
            education_level_id=education_repo.get_by_name(
                response.education_level
            ).id,
            score=response.score,
            opinion=response.opinion,
            strengths=response.strengths,
            weaknesses=response.weaknesses,
            languages=response.languages,
        )