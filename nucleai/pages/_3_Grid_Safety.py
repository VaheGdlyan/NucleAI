import streamlit as st
import requests
import pandas as pd
import altair as alt
from utils.ui_helpers import glass_card, metric_badge, section_title

API_URL = "http://127.0.0.1:8000/api/energy-safety"

def render():
    st.markdown(
        """
        <div class="fade-in" style="display: flex; align-items: flex-end; gap: 15px; margin-bottom: 1rem;">
            <img src="app/static/logo.png" width="260">
            <span style="color: #9a9a9a; font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 500; margin-bottom: 6px;">| Grid &amp; Safety</span>
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
            with st.spinner("Loading energy data..."):
                response = requests.get(API_URL)
                response.raise_for_status()
                data = response.json()

            armenia_mix = data["armenia_mix"]
            safety_records = data["safety_records"]
            carbon_footprints = data["carbon_footprints"]

            # ── Section 1: Armenia Energy Mix ──────────────────────────────────
            section_title(
                "🇦🇲 Armenia's Energy Grid (2023)",
                "Metsamor NPP provides ~40% of all national electricity — a critical baseload anchor"
            )

            df_mix = pd.DataFrame(armenia_mix)

            mix_chart = alt.Chart(df_mix).mark_arc(innerRadius=70, outerRadius=120).encode(
                theta=alt.Theta("percentage:Q"),
                color=alt.Color(
                    "source:N",
                    scale=alt.Scale(
                        domain=[d["source"] for d in armenia_mix],
                        range=[d["color"] for d in armenia_mix]
                    ),
                    legend=None
                ),
                tooltip=["source:N", "percentage:Q", "twh:Q"]
            ).properties(
                width=340, height=340,
                title=alt.TitleParams(text="Electricity Generation Share", color="#9a9a9a", fontSize=13)
            )

            center_text = alt.Chart(pd.DataFrame([{"x": 0, "y": 0, "text": "8.5 TWh", "sub": "Total / Year"}])).mark_text(
                align="center", baseline="middle", fontSize=22, fontWeight="bold", color="#d4af37"
            ).encode(text="text:N")

            final_mix_chart = mix_chart + center_text

            c1, c2 = st.columns([1, 1])
            with c1:
                st.altair_chart(final_mix_chart, use_container_width=True, theme=None)
            with c2:
                st.write("")
                st.write("")
                for item in armenia_mix:
                    glass_card(
                        f"<div style='display:flex;align-items:center;gap:12px;'>"
                        f"<div style='width:12px;height:36px;border-radius:4px;background:{item['color']};flex-shrink:0;'></div>"
                        f"<div>"
                        f"<p style='color:var(--text-primary);font-weight:600;margin:0;font-size:14px;'>{item['source']}</p>"
                        f"<p style='color:var(--text-muted);margin:0;font-size:13px;'>{item['percentage']}% · {item['twh']} TWh/yr</p>"
                        f"</div></div>"
                    )
                    st.write("")

                glass_card(
                    "<p style='color:#e05252;font-size:13px;margin:0;line-height:1.6;'>"
                    "⚠️ Without Metsamor, electricity prices in Armenia would rise <strong style='color:#f0f0f0;'>40–60%</strong>."
                    "</p>"
                )

            st.write("")
            st.write("")

            # ── Section 2: Deaths Per TWh ───────────────────────────────────────
            section_title(
                "💀 Safety by the Numbers",
                "Deaths per TWh of electricity generated — includes accidents, air pollution, and mining"
            )

            df_safety = pd.DataFrame(safety_records).sort_values("deaths_per_twh", ascending=False)

            safety_chart = alt.Chart(df_safety).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
                x=alt.X("source:N", sort="-y", title=None,
                        axis=alt.Axis(labelAngle=-30, labelColor="#f0f0f0", labelFontSize=12, domainColor="rgba(255,255,255,0.1)")),
                y=alt.Y("deaths_per_twh:Q", title="Deaths per TWh",
                        axis=alt.Axis(labelColor="#9a9a9a", titleColor="#9a9a9a", gridColor="rgba(255,255,255,0.06)")),
                color=alt.condition(
                    alt.datum.source == "Nuclear",
                    alt.value("#d4af37"),
                    alt.value("rgba(255,255,255,0.15)")
                ),
                tooltip=[
                    alt.Tooltip("source:N", title="Energy Source"),
                    alt.Tooltip("deaths_per_twh:Q", title="Deaths per TWh", format=".2f")
                ]
            ).properties(height=380).configure_view(strokeWidth=0).configure_axis(
                grid=True, gridColor="rgba(255,255,255,0.06)", domainColor="rgba(255,255,255,0.1)"
            )

            st.altair_chart(safety_chart, use_container_width=True, theme=None)

            # Key insight badges
            b1, b2, b3 = st.columns(3)
            with b1:
                metric_badge("Coal kills", "24.6 / TWh", "#e05252")
            with b2:
                metric_badge("Nuclear kills", "0.07 / TWh", "#d4af37")
            with b3:
                metric_badge("Nuclear is", "351× safer than coal", "#3fb950")

            st.write("")
            st.write("")

            # ── Section 3: CO₂ Lifecycle Footprint ─────────────────────────────
            section_title(
                "🌍 Lifecycle CO₂ Emissions",
                "Grams of CO₂ equivalent per kWh generated — including manufacturing, fuel, and decommissioning"
            )

            df_co2 = pd.DataFrame(carbon_footprints).sort_values("grams_co2_per_kwh", ascending=False)

            co2_chart = alt.Chart(df_co2).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
                x=alt.X("source:N", sort="-y", title=None,
                        axis=alt.Axis(labelAngle=-30, labelColor="#f0f0f0", labelFontSize=12, domainColor="rgba(255,255,255,0.1)")),
                y=alt.Y("grams_co2_per_kwh:Q", title="g CO₂ / kWh",
                        axis=alt.Axis(labelColor="#9a9a9a", titleColor="#9a9a9a", gridColor="rgba(255,255,255,0.06)")),
                color=alt.condition(
                    alt.datum.source == "Nuclear",
                    alt.value("#d4af37"),
                    alt.value("rgba(255,255,255,0.15)")
                ),
                tooltip=[
                    alt.Tooltip("source:N", title="Energy Source"),
                    alt.Tooltip("grams_co2_per_kwh:Q", title="g CO₂/kWh", format=".0f")
                ]
            ).properties(height=380).configure_view(strokeWidth=0).configure_axis(
                grid=True, gridColor="rgba(255,255,255,0.06)", domainColor="rgba(255,255,255,0.1)"
            )

            st.altair_chart(co2_chart, use_container_width=True, theme=None)

            co2_b1, co2_b2, co2_b3 = st.columns(3)
            with co2_b1:
                metric_badge("Coal emits", "820 g CO₂/kWh", "#e05252")
            with co2_b2:
                metric_badge("Nuclear emits", "12 g CO₂/kWh", "#d4af37")
            with co2_b3:
                metric_badge("As clean as", "Wind energy", "#3fb950")

        except Exception as e:
            st.error(f"Failed to load data from backend: {e}")

if __name__ == "__main__":
    from styles.global_css import inject_global_css
    inject_global_css()
    render()
