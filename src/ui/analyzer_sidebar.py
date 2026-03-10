import streamlit as st

def render_sidebar(jobs, uploader_key):

    with st.sidebar:

        st.title("📄 Análise de currículos")

        vaga = st.selectbox(
            "Selecionar vaga",
            jobs,
            format_func=lambda j: j.name
        )

        st.markdown("<hr style='margin-top:10px;margin-bottom:15px;'>", unsafe_allow_html=True)

        st.markdown("**Enviar currículos (PDF)**")
        st.caption("Máximo de 10 arquivos")

        arquivos = st.file_uploader(
            "Arraste ou selecione arquivos",
            type="pdf",
            accept_multiple_files=True,
            label_visibility="collapsed",
            key=f"uploader_{uploader_key}"
        )

        if arquivos:
            st.caption(f"{len(arquivos)} arquivo(s) selecionado(s)")

        analisar = st.button(
            "🚀 Analisar currículos",
            type="primary",
            use_container_width=True
        )

    return vaga, arquivos, analisar