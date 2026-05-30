import streamlit as st

def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        /* Load background.png as fixed full-screen cover */
        .stApp {
            background-image: url("app/static/background.png");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }

        /* Dark cinematic overlay for readability */
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            background: linear-gradient(
                135deg,
                rgba(0, 0, 0, 0.82) 0%,
                rgba(5, 10, 20, 0.75) 50%,
                rgba(0, 0, 0, 0.88) 100%
            );
            z-index: 0;
            pointer-events: none;
        }

        /* Hide default Streamlit chrome */
        #MainMenu, footer { visibility: hidden; }
        header { background: transparent !important; }
        .block-container { padding-top: 1.5rem; position: relative; z-index: 1; background: transparent !important; }

        /* Glassmorphism base class */
        .glass {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            padding: 1.5rem 2rem;
            transition: all 0.3s ease;
        }
        .glass:hover {
            border-color: rgba(255, 255, 255, 0.18);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55);
        }
        
        .placeholder-glass {
            background: rgba(255, 255, 255, 0.01) !important;
            backdrop-filter: blur(4px) !important;
            -webkit-backdrop-filter: blur(4px) !important;
            border: 1px solid rgba(255, 255, 255, 0.03) !important;
            box-shadow: none !important;
            padding: 1rem !important;
        }

        /* Typography */
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', 'Segoe UI', 'Helvetica Neue', sans-serif;
            color: #e8e8e8;
        }

        h1, h2, h3 {
            font-family: 'Syne', sans-serif;
            letter-spacing: -0.02em;
        }

        /* Color tokens */
        :root {
            --gold: #d4af37;
            --gold-dim: rgba(212, 175, 55, 0.15);
            --blue-glow: #00bfff;
            --red-alert: #e05252;
            --green-safe: #3fb950;
            --surface: rgba(255, 255, 255, 0.04);
            --border: rgba(255, 255, 255, 0.10);
            --text-primary: #f0f0f0;
            --text-muted: #9a9a9a;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(8, 8, 12, 0.85) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--border);
        }
        [data-testid="stSidebar"] * { color: var(--text-primary) !important; }

        /* Buttons */
        .stButton > button {
            background: transparent !important;
            color: var(--gold) !important;
            border: 1px solid var(--gold) !important;
            border-radius: 8px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 13px !important;
            transition: all 0.25s ease !important;
        }
        .stButton > button:hover {
            background: var(--gold-dim) !important;
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.3) !important;
        }

        /* Search input styling (replaces chat input) */
        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            background: transparent !important;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 14px !important;
            box-shadow: none !important;
            transition: all 0.3s ease;
            padding: 4px 8px !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: var(--gold) !important;
            background: rgba(255, 255, 255, 0.05) !important;
        }
        div[data-testid="stTextInput"] input {
            color: var(--text-primary) !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 16px !important;
            background: transparent !important;
        }

        /* User and AI message bubbles */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            margin-bottom: 0.75rem !important;
            backdrop-filter: blur(8px);
        }

        /* Fade-in animation */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(12px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeInUp 0.4s ease forwards;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
