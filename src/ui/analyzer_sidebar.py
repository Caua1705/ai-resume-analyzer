import streamlit as st

from src.ui.analyzer_layout import render_section_divider
from src.config.settings import MAX_RESUME_UPLOAD


def render_sidebar(jobs, uploader_key):

    with st.sidebar:

        st.title("📄 Resume Analysis")

        selected_job = st.selectbox(
            "Select Job",
            jobs,
            format_func=lambda j: j.name,
        )

        render_section_divider()

        st.markdown("**Upload Resumes (PDF)**")
        st.caption(f"Maximum {MAX_RESUME_UPLOAD} files")

        files = st.file_uploader(
            "Drag or select files",
            type="pdf",
            accept_multiple_files=True,
            label_visibility="collapsed",
            key=f"uploader_{uploader_key}",
        )

        if files:
            st.caption(f"{len(files)} file(s) selected")

        analyze = st.button(
            "🚀 Analyze Resumes",
            type="primary",
            use_container_width=True,
        )

    return selected_job, files, analyze