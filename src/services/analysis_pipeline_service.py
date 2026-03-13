from src.services.pdf_service import extrair_texto_pdf
from src.services.storage_service import upload_curriculo
from src.services.resume_analysis_llm_service import LLMResumeAnalyzer
from src.config.config import OPENAI_API_KEY


def run_resume_analysis_pipeline(
    arquivos,
    vaga,
    edu_repo,
    resume_repo,
    analise_repo
):

    textos = []

    for arquivo in arquivos:
        texto = extrair_texto_pdf(arquivo.getvalue())
        textos.append(texto)

    analyzer = LLMResumeAnalyzer(OPENAI_API_KEY)
    responses = analyzer.analyze(vaga, textos)

    for i, arquivo in enumerate(arquivos):

        texto = textos[i]
        resp = responses[i]

        file_path = upload_curriculo(
            arquivo.getvalue(),
            vaga.name
        )

        resume = resume_repo.add_resume(
            file_path,
            texto,
            vaga.id
        )

        analise_repo.add_analysis(
            resume_id=resume.id,
            job_id=vaga.id,
            education_level_id=edu_repo.get_by_name(resp.education_level).id,
            score=resp.score,
            opinion=resp.opinion,
            strengths=resp.strengths,
            weaknesses=resp.weaknesses,
            languages=resp.languages
        )