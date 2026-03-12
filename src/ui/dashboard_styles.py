import streamlit as st

def aplicar_estilo_metricas(cores):

    st.markdown(f"""
    <style>
        .stMetric {{
            background-color: #ffffff;
            border-radius: 10px;
            padding: 12px;
            box-shadow: 0 0 5px rgba(0,0,0,0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            color: #111827;
        }}

        .stMetric:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}

        [data-testid="stColumn"]:nth-of-type(1) .stMetric {{
            border-left: 6px solid {cores.get("col1", "#000")};
        }}

        [data-testid="stColumn"]:nth-of-type(2) .stMetric {{
            border-left: 6px solid {cores.get("col2", "#000")};
        }}

        [data-testid="stColumn"]:nth-of-type(3) .stMetric {{
            border-left: 6px solid {cores.get("col3", "#000")};
        }}

        [data-testid="stColumn"]:nth-of-type(4) .stMetric {{
            border-left: 6px solid {cores.get("col4", "#000")};
        }}
    </style>
    """, unsafe_allow_html=True)