import streamlit as st

def glass_card(content_html: str, extra_class: str = "") -> None:
    """Render HTML inside a glassmorphism card."""
    st.markdown(
        f'<div class="glass {extra_class} fade-in">{content_html}</div>',
        unsafe_allow_html=True
    )

def section_title(title: str, subtitle: str = "") -> None:
    """Render a styled section heading with optional subtitle."""
    sub = f'<p style="color:var(--text-muted);font-size:15px;margin-top:4px;">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<div class="fade-in" style="margin-bottom:1.5rem;">'
        f'<h2 style="font-family:Syne,sans-serif;color:var(--gold);margin:0;">{title}</h2>'
        f'{sub}</div>',
        unsafe_allow_html=True
    )

def metric_badge(label: str, value: str, color: str = "var(--gold)") -> None:
    """Render a small inline metric badge."""
    st.markdown(
        f'<div class="fade-in" style="display:inline-block;background:rgba(255,255,255,0.05);'
        f'border:1px solid {color};border-radius:8px;padding:6px 14px;margin:4px;">'
        f'<span style="color:var(--text-muted);font-size:11px;text-transform:uppercase;'
        f'letter-spacing:0.08em;">{label}</span><br>'
        f'<span style="color:{color};font-size:18px;font-weight:600;">{value}</span>'
        f'</div>',
        unsafe_allow_html=True
    )
