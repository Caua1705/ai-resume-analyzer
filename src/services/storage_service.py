import uuid
from src.core.supabase_client import supabase


def upload_curriculo(pdf_bytes: bytes, job_name: str):

    file_id = str(uuid.uuid4())
    file_path = f"{job_name}/{file_id}.pdf"

    supabase.storage.from_("curriculos").upload(
        file_path,
        pdf_bytes,
        {"content-type": "application/pdf"}
    )

    return file_path