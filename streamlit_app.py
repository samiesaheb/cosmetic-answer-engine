# streamlit_app.py

import streamlit as st
import requests

st.set_page_config(page_title="🧠 Cosmetic Answer Engine", layout="wide")
st.title("🧴 AI-Powered Answer Engine")
st.markdown("Ask anything about ingredients, formulations, or products.")

question = st.text_input("🔍 Your question:", placeholder="What is panthenol used for?")

if question:
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={"question": question, "stream": True},
            stream=True,
        )

        # Output area for streamed response
        full_answer = ""
        answer_box = st.empty()

        for chunk in response.iter_content(chunk_size=64):
            if chunk:
                text = chunk.decode("utf-8")
                full_answer += text
                answer_box.markdown(f"💬 {full_answer}")

    st.success("✅ Done!")

    if "Sources:" in full_answer:
        sources = full_answer.split("Sources:")[-1]
        st.markdown("### 📚 Sources")
        st.markdown(f"```\n{sources.strip()}\n```")
