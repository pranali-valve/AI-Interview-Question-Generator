
import streamlit as st

from generator import generate_interview_questions


st.set_page_config(
    page_title="AI Interview Question Generator",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 AI Interview Question Generator")

st.write(
    "Prepare for your next interview with AI-generated "
    "questions, answers, explanations, and examples."
)

st.divider()

st.subheader("Tell us about your interview preparation")

with st.form("interview_form"):
    job_role = st.text_input(
        "Job Role",
        placeholder="e.g. Python Developer",
    )

    experience = st.selectbox(
        "Experience Level",
        [
            "Beginner",
            "Fresher",
            "1–3 Years",
            "3–5 Years",
            "5+ Years",
        ],
    )

    skills_input = st.text_input(
        "Skills",
        placeholder="e.g. Python, SQL, Machine Learning",
        help="Enter skills separated by commas.",
    )

    number_of_questions = st.slider(
        "Number of Questions",
        min_value=1,
        max_value=10,
        value=5,
    )

    submitted = st.form_submit_button(
        "Generate Interview Questions",
        type="primary",
        use_container_width=True,
    )


if submitted:
    st.session_state.pop("interview_result", None)

    skills = [
        skill.strip()
        for skill in skills_input.split(",")
        if skill.strip()
    ]

    try:
        # Show a helpful error if required inputs are missing.
        if not job_role.strip():
            raise ValueError("Please enter a Job Role.")

        if not skills:
            raise ValueError("Please enter at least one Skill.")

        # Call Gemini through the reusable generator module.
        with st.spinner(
            "Generating your interview questions with Gemini AI..."
        ):
            result = generate_interview_questions(
                role=job_role,
                experience=experience,
                skills=skills,
                number_of_questions=number_of_questions,
            )

        st.session_state["interview_result"] = result

    except ValueError as error:
        st.error(str(error))

    except RuntimeError as error:
        st.error(str(error))

    except Exception as error:
        # Do not display API keys or sensitive configuration.
        st.error(
            "Something went wrong. Please try again. "
            f"Error type: {type(error).__name__}"
        )


# Display the generated result whenever it is available.
result = st.session_state.get("interview_result")

if result:
    st.divider()
    st.header("Your Interview Questions")

    st.caption(
        f"Role: {result['role']} | "
        f"Total Questions: {len(result['questions'])}"
    )

    for index, question in enumerate(result["questions"], start=1):
        with st.expander(
            f"Question {index}: {question['question']}",
            expanded=(index == 1),
        ):
            st.markdown(
                f"**Difficulty:** {question['difficulty']}"
            )

            st.markdown("### Sample Answer")
            st.write(question["answer"])

            st.markdown("### Explanation")
            st.write(question["explanation"])

            st.markdown("### Practical Example")
            st.write(question["example"])

            st.markdown("### Follow-up Questions")
            for follow_up in question["follow_up_questions"]:
                st.markdown(f"- {follow_up}")

    st.success("Your interview preparation set is ready!")
