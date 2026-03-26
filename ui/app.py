import streamlit as st
from llm.explainer  import explain_threat
from llm.remediator import get_remediation
from llm.chatbot    import set_context, ask_chatbot
from llm.report_gen import generate_report
from llm.memory     import save_memory                  # ← new import
from api.receiver   import get_threats_from_model

st.set_page_config(page_title="Cloud Security LLM Assistant", layout="wide")
st.title("Cloud Security Posture Management — LLM Assistant")

threats = get_threats_from_model()
set_context(threats)
threat_choices = [f"{t['threat']} ({t['score']:.0%})" for t in threats]

tab1, tab2, tab3 = st.tabs(["Threat Analysis", "Security Chatbot", "Generate Report"])

with tab1:
    st.subheader("Threat Analysis")
    selected = st.selectbox("Select a detected threat", threat_choices)
    if st.button("Analyze"):
        idx = threat_choices.index(selected)
        t = threats[idx]
        with st.spinner("Analyzing..."):
            explanation = explain_threat(t['threat'], t['score'])
            remediation = get_remediation(t['threat'])
        st.text_area("Explanation", explanation, height=150)
        st.text_area("Remediation Steps", remediation, height=180)

with tab2:
    st.subheader("Security Chatbot")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask about the detected threats...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = ask_chatbot(user_input, st.session_state.messages)
            st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # ↓ Memory and clear buttons — bottom of chatbot tab
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 End Session & Save Memory"):
            if st.session_state.messages:
                save_memory(st.session_state.messages)
                st.success("Session memory saved! The assistant will remember this next time.")
                st.session_state.messages = []
            else:
                st.warning("No messages to save.")
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

with tab3:
    st.subheader("Generate Report")
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            report = generate_report(threats)
        st.text_area("Security Report", report, height=400)
        st.download_button("Download Report", report, file_name="security_report.txt")