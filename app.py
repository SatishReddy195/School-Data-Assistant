import streamlit as st

from assistant import ask_school_data_assistant


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="School Data Assistant",
    page_icon="🏫",
    layout="centered",
)


# =========================================================
# Application Header
# =========================================================

st.title("🏫 School Data Assistant")

st.write(
    "Ask questions about students, marks, fees, "
    "attendance, complaints, sports, and teachers."
)


# =========================================================
# Example Questions
# =========================================================

with st.expander("Example questions"):

    st.markdown(
        """
        - How many students are there?
        - How many female students are in class 8?
        - Show me the marks of student STU2026001.
        - Show Mathematics marks for STU2026001.
        - What is the average attendance?
        - How much fee is outstanding?
        - What is the total revenue?
        - What is the overall student pass percentage?
        - How many complaints are pending?
        - How many students participate in sports?
        - How many teachers are there?
        """
    )


# =========================================================
# Initialize Conversation History
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# Display Previous Messages
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# =========================================================
# Chat Input
# =========================================================

question = st.chat_input(
    "Ask a question about school data..."
)


# =========================================================
# Process New Question
# =========================================================

if question:

    # -----------------------------------------------------
    # Display principal's question
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # -----------------------------------------------------
    # Generate assistant response
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Checking school data..."
        ):

            answer = ask_school_data_assistant(
                question
            )

        st.markdown(answer)

    # -----------------------------------------------------
    # Save assistant response
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )