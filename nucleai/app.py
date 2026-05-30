import streamlit as st
from styles.global_css import inject_global_css

st.set_page_config(layout="wide", page_title="NucleAI", page_icon="⚛️", initial_sidebar_state="expanded")

inject_global_css()

# Sidebar Setup
with st.sidebar:
    st.image("assets/logo.png", width=140)
    st.markdown("<br>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "💬 Mythbuster",
            "📊 Radiation Check",
            "⚡ Grid & Safety",
            "🩺 Beyond Energy",
        ],
        label_visibility="hidden"
    )

# Page Routing
if page == "💬 Mythbuster":
    import pages._1_Mythbuster as p
    p.render()
elif page == "📊 Radiation Check":
    import pages._2_Reality_Check as p
    p.render()
elif page == "⚡ Grid & Safety":
    import pages._3_Grid_Safety as p
    p.render()
elif page == "🩺 Beyond Energy":
    import pages._4_Beyond_Energy as p
    p.render()
