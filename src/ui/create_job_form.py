import streamlit as st


def render_create_job_form():

    st.title("📌 Create New Job")

    st.markdown(
        "Fill in the information below to create a job position that will be used to analyze resumes."
    )

    st.markdown("---")

    with st.container():

        with st.form("create_job_form"):

            name = st.text_input(
                "Job title",
                placeholder="Example: Data Science Intern"
            )

            st.markdown("### Job Description")

            main_activities = st.text_area(
                "Main Responsibilities",
                placeholder="Describe the main responsibilities of the role...",
                height=150
            )

            prerequisites = st.text_area(
                "Requirements",
                placeholder="Example: Python, SQL, statistics...",
                height=150
            )

            differentials = st.text_area(
                "Nice to Have",
                placeholder="Example: experience with AI, personal projects, portfolio...",
                height=150
            )

            submitted = st.form_submit_button(
                "🚀 Create Job",
                use_container_width=True
            )

    return submitted, name, main_activities, prerequisites, differentials