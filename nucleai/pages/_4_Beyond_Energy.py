import streamlit as st
import requests
from utils.ui_helpers import glass_card, metric_badge, section_title

API_URL = "http://127.0.0.1:8000/api/beyond-energy"

# Category icon map
ICONS = {
    "PET Scans (early cancer detection)": "🔬",
    "SPECT Imaging (heart/bone diagnostics)": "❤️",
    "Iodine-131 targeted therapy (thyroid cancer)": "🎯",
    "Brachytherapy (prostate/cervical cancer)": "💊",
}

def render():
    st.markdown(
        """
        <div class="fade-in" style="display: flex; align-items: flex-end; gap: 15px; margin-bottom: 1rem;">
            <img src="app/static/logo.png" width="260">
            <span style="color: #9a9a9a; font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 500; margin-bottom: 6px;">| Beyond Energy</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([0.5, 9, 0.5])
    with col2:
        try:
            with st.spinner("Loading application data..."):
                response = requests.get(API_URL)
                response.raise_for_status()
                data = response.json()

            medical_apps = data["medical_apps"]
            agricultural_facts = data["agricultural_facts"]
            space_facts = data["space_facts"]

            # ── Section 1: Nuclear Medicine ─────────────────────────────────────
            section_title(
                "🩺 Nuclear Medicine",
                "Radiation saves millions of lives every year through advanced diagnostics and targeted therapies"
            )

            glass_card(
                "<p style='color:var(--text-muted);font-size:14px;line-height:1.8;margin:0;'>"
                "Armenia faces significant challenges in cancer detection and treatment. Nuclear medicine technologies "
                "like PET scans, SPECT imaging, and targeted radiotherapy represent a transformational opportunity "
                "for improving health outcomes nationwide — and nuclear energy infrastructure makes them possible."
                "</p>"
            )
            st.write("")

            med_cols = st.columns(2)
            for idx, app in enumerate(medical_apps):
                icon = ICONS.get(app["application"], "⚛️")
                with med_cols[idx % 2]:
                    glass_card(
                        f"<div>"
                        f"<p style='font-size:22px;margin:0 0 6px 0;'>{icon}</p>"
                        f"<h4 style='color:var(--text-primary);margin:0 0 4px 0;font-size:15px;'>{app['application']}</h4>"
                        f"<div style='display:flex;gap:12px;margin:8px 0;'>"
                        f"<span style='background:rgba(212,175,55,0.12);border:1px solid rgba(212,175,55,0.3);"
                        f"border-radius:6px;padding:3px 10px;font-size:12px;color:var(--gold);'>"
                        f"{app['annual_procedures_millions']}M procedures/yr</span>"
                        f"<span style='background:rgba(63,185,80,0.12);border:1px solid rgba(63,185,80,0.3);"
                        f"border-radius:6px;padding:3px 10px;font-size:12px;color:#3fb950;'>"
                        f"{app['success_rate_pct']}% success rate</span>"
                        f"</div>"
                        f"<p style='color:var(--text-muted);font-size:13px;margin:0;line-height:1.6;'>{app['context']}</p>"
                        f"</div>"
                    )
                    st.write("")

            st.write("")

            # ── Section 2: Agriculture & Food Security ──────────────────────────
            section_title(
                "🌾 Agriculture & Food Security",
                "Radiation technology protects crops, eliminates pests, and feeds billions worldwide"
            )

            ag_cols = st.columns(3)
            ag_icons = ["🦟", "🍎", "🌾"]
            ag_titles = ["Sterile Insect Technique", "Food Irradiation", "Mutation Breeding"]
            for idx, fact in enumerate(agricultural_facts):
                with ag_cols[idx]:
                    # Split off the title (first sentence ending at ':')
                    parts = fact.split(":", 1)
                    title_display = ag_titles[idx]
                    body_display = parts[1].strip() if len(parts) > 1 else fact
                    glass_card(
                        f"<p style='font-size:28px;margin:0 0 8px 0;'>{ag_icons[idx]}</p>"
                        f"<h4 style='color:var(--gold);font-size:14px;margin:0 0 8px 0;'>{title_display}</h4>"
                        f"<p style='color:var(--text-muted);font-size:13px;line-height:1.7;margin:0;'>{body_display}</p>"
                    )

            st.write("")
            st.write("")

            # ── Section 3: Space & Science ──────────────────────────────────────
            section_title(
                "🚀 Deep Space Exploration",
                "Without nuclear power, exploring the outer solar system is physically impossible"
            )

            space_icons = ["⚛️", "🛰️", "🌌"]
            space_cols = st.columns(3)
            for idx, fact in enumerate(space_facts):
                parts = fact.split(":", 1)
                title_display = parts[0].strip()
                body_display = parts[1].strip() if len(parts) > 1 else fact
                with space_cols[idx]:
                    glass_card(
                        f"<p style='font-size:28px;margin:0 0 8px 0;'>{space_icons[idx]}</p>"
                        f"<h4 style='color:var(--gold);font-size:14px;margin:0 0 8px 0;'>{title_display}</h4>"
                        f"<p style='color:var(--text-muted);font-size:13px;line-height:1.7;margin:0;'>{body_display}</p>"
                    )

            st.write("")
            st.write("")

            # ── Summary Impact Metrics ──────────────────────────────────────────
            section_title("📊 Nuclear Technology — Global Impact")
            imp_cols = st.columns(4)
            with imp_cols[0]:
                metric_badge("Medical Procedures", "40M / year", "#d4af37")
            with imp_cols[1]:
                metric_badge("Crop Varieties Developed", "3,200+", "#3fb950")
            with imp_cols[2]:
                metric_badge("Space Missions Powered", "Voyager, Cassini…", "#00bfff")
            with imp_cols[3]:
                metric_badge("Thyroid Cancer Cure Rate", ">95% with I-131", "#3fb950")

        except Exception as e:
            st.error(f"Failed to load data from backend: {e}")

if __name__ == "__main__":
    from styles.global_css import inject_global_css
    inject_global_css()
    render()
