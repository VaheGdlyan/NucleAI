import streamlit as st
import requests
import pandas as pd
import altair as alt
from utils.ui_helpers import glass_card

API_URL = "http://127.0.0.1:8000/api/radiation-data"

def render():
    st.markdown(
        """
        <div class="fade-in" style="display: flex; align-items: flex-end; gap: 15px; margin-bottom: 1rem;">
            <img src="app/static/logo.png" width="260">
            <span style="color: #9a9a9a; font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 500; margin-bottom: 6px;">| Reality Check</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("")
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        try:
            with st.spinner("Fetching IAEA safety metrics..."):
                response = requests.get(API_URL)
                response.raise_for_status()
                data = response.json()
                
            points = data["data"]
            df = pd.DataFrame(points)
            
            # Altair Chart
            chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
                x=alt.X('source:N', sort='-y', title='Source / Activity', axis=alt.Axis(labelAngle=-45, labelColor='#f0f0f0', titleColor='#9a9a9a', labelFontSize=12)),
                y=alt.Y('dose_usv:Q', scale=alt.Scale(type='symlog'), title='Radiation Dose (μSv) - Log Scale', axis=alt.Axis(labelColor='#f0f0f0', titleColor='#9a9a9a', labelFontSize=12)),
                color=alt.Color('category:N', legend=None, scale=alt.Scale(range=['#d4af37', '#00bfff', '#3fb950', '#e05252'])),
                tooltip=['source', 'dose_usv', 'category', 'context']
            ).properties(
                height=500
            ).configure_view(
                strokeWidth=0
            ).configure_axis(
                grid=True,
                gridColor='rgba(255,255,255,0.1)',
                domainColor='rgba(255,255,255,0.2)'
            ).configure_mark(
                opacity=0.9
            )

            glass_card(
                "<h3 style='color:var(--text-primary); margin-bottom: 0;'>Radiation Dose Comparison</h3>"
                f"<p style='color:var(--text-muted); margin-top: 5px;'>Comparing everyday activities to nuclear energy (Unit: {data['unit']})</p>"
            )
            
            st.altair_chart(chart, use_container_width=True, theme=None)

            st.markdown("<br><h3 style='color:var(--gold);'>🔍 Context & Facts</h3>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, row in df.iterrows():
                with cols[i % 3]:
                    glass_card(
                        f"<h4 style='color:var(--text-primary); margin:0; font-size:16px;'>{row['source']}</h4>"
                        f"<p style='color:var(--gold); font-size:12px; margin-bottom:10px;'>{row['category']} • {row['dose_usv']} μSv</p>"
                        f"<p style='font-size:14px; margin:0;'>{row['context']}</p>"
                    )
                    st.write("") # slight spacing between rows
                    
        except Exception as e:
            st.error(f"Failed to load data from backend: {e}")

if __name__ == "__main__":
    from styles.global_css import inject_global_css
    inject_global_css()
    render()
