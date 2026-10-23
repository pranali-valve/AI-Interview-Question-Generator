
import streamlit as st


# Configure the page.
st.set_page_config(
    page_title="AI Interview Question Generator",
    page_icon="🎯",
    layout="wide",   
)


# Main heading.
st.title("🎯 AI Interview Question Generator")

st.write(
    "Prepare for your next interview with AI-generated "
    "questions, answers, explanations, and examples."
)

st.divider()

st.subheader("What can this app do?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Interview Questions")
    st.write(
        "Generate interview questions based on your job role, "
        "experience level, and skills."
    )

    st.markdown("### 💡 Sample Answers")
    st.write(
        "Learn how to answer each question with clear explanations "
        "and practical examples."
    ) 

with col2:
    st.markdown("### 🎓 Difficulty Levels")
    st.write(
        "Prepare with Easy, Medium, and Hard questions "
        "suited to your experience."
    )

    st.markdown("### 🔄 Follow-up Questions")
    st.write(
        "Explore related questions to deepen your understanding."
    )

st.divider()

st.info(
    "Your interview preparation workspace is ready. "
    "The input form is coming next."
)
