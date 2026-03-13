import plotly.express as px
import streamlit as st

from src.config.config import SCORE_COLORS, EDUCATION_COLORS


def render_score_distribution(df):

    fig = px.bar(
        df,
        x="score_category",
        y="count",
        color="score_category",
        color_discrete_map=SCORE_COLORS,
        title="Candidate Score Distribution"
    )

    fig.update_traces(
        text=df["count"],
        textposition="outside"
    )

    fig.update_layout(
        title={'text': "Candidate Score Distribution", 'x': 0.0, 'xanchor': 'left'},
        xaxis_title="Score Category",
        yaxis_title="Candidates",
        plot_bgcolor="white",
        font=dict(color="#111827"),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#E5E7EB")
    )

    st.plotly_chart(fig, use_container_width=True)


def render_education_score_chart(df):

    fig = px.bar(
        df,
        x="score",
        y="education_level",
        orientation="h",
        color="education_level",
        color_discrete_map=EDUCATION_COLORS,
        title="Average Candidate Score by Education Level"
    )

    fig.update_traces(
        text=df["score"].round(1),
        textposition="outside"
    )

    fig.update_layout(
        title={'text': "Average Candidate Score by Education Level", 'x': 0.0, 'xanchor': 'left'},
        xaxis_title="Average Score",
        yaxis_title="Education Level",
        plot_bgcolor="white",
        font=dict(color="#111827"),
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor="#E5E7EB", range=[0, 100]),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig, use_container_width=True)