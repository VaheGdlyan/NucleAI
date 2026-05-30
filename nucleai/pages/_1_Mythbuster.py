import streamlit as st
import requests
from utils.ui_helpers import glass_card

API_URL = "http://127.0.0.1:8000/api/mythbuster"

def handle_submit():
    st.session_state.submit_query = st.session_state.search_input
    st.session_state.search_input = ""

def render():
    # Render logo inline instead of fixed
    st.markdown(
        """
        <div class="fade-in" style="margin-bottom: 1rem;">
            <img src="app/static/logo.png" width="260">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "submit_query" not in st.session_state:
        st.session_state.submit_query = ""

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input(
            "Search", 
            placeholder="Ask a question about nuclear energy...", 
            label_visibility="collapsed",
            key="search_input",
            on_change=handle_submit
        )

        st.write("")

        # Placeholder message area
        if not st.session_state.messages and not st.session_state.submit_query:
            glass_card(
                "<p style='color:var(--text-muted);text-align:center;padding:1rem 0; font-size:14px; margin:0;'>"
                "Ask a question above to begin. The AI will respond using verified IAEA data.</p>",
                "placeholder-glass"
            )

    col_chat1, col_chat2, col_chat3 = st.columns([1, 3, 1])
    with col_chat2:
        # Display history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if "sources" in msg and msg["sources"]:
                    with st.expander("📚 Grounding Citations"):
                        for source in msg["sources"]:
                            st.markdown(f"- `{source}`")

        # Handle new submission
        query_to_process = st.session_state.submit_query
        if query_to_process:
            st.session_state.submit_query = ""
            
            st.session_state.messages.append({"role": "user", "content": query_to_process})
            with st.chat_message("user"):
                st.markdown(query_to_process)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing IAEA documents..."):
                    try:
                        response = requests.post(API_URL, json={"query": query_to_process})
                        response.raise_for_status()
                        data = response.json()
                        answer = data.get("answer", "Error: No answer returned.")
                        sources = data.get("sources", [])
                        
                        st.markdown(answer)
                        if sources:
                            with st.expander("📚 Grounding Citations"):
                                for source in sources:
                                    st.markdown(f"- `{source}`")
                        
                        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
                    except Exception as e:
                        st.error(f"Error connecting to backend: {e}")

if __name__ == "__main__":
    from styles.global_css import inject_global_css
    inject_global_css()
    render()
