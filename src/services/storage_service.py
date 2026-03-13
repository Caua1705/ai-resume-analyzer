import uuid

from src.core.supabase_client import supabase
from src.config.settings import SUPABASE_BUCKET


def upload_resume(pdf_bytes: bytes, job_name: str) -> str:

    file_id = uuid.uuid4()
    file_path = f"{job_name}/{file_id}.pdf"

    supabase.storage.from_(SUPABASE_BUCKET).upload(
        file_path,
        pdf_bytes,
        {"content-type": "application/pdf"},
    )

    return file_path