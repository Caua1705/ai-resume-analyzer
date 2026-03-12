import plotly.express as px
import streamlit as st


def render_score_distribution(score_dist):

    fig = px.bar(
        x=score_dist.index,
        y=score_dist.values,
        labels={"x": "Score Category", "y": "Candidates"},
        title="Candidate Score Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


def render_education_score_chart(media):

    fig = px.bar(
        media,
        x="score",
        y="education_level",
        orientation="h",
        title="Average Candidate Score by Education Level",
        labels={
            "score": "Average Score",
            "education_level": "Education Level"
        }
    )

    fig.update_xaxes(range=[0, 100])

    st.plotly_chart(fig, use_container_width=True)