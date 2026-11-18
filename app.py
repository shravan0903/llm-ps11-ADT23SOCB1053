
import streamlit as st

from utils.chatbot import ask_college_chatbot


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="MIT ADT College Enquiry Chatbot",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
.block-container {
    max-width: 950px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.stChatMessage {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🎓 MIT ADT University")

    st.divider()

    st.subheader("About the Chatbot")

    st.write(
        """
        This chatbot helps students get information
        about MIT Art, Design and Technology University.

        It uses the 2026–27 Admission Handbook
        as its knowledge source.
        """
    )

    st.divider()

    st.subheader("What can I ask?")

    st.markdown("""
    - Course eligibility
    - Admission procedure
    - Fee structure
    - Scholarships
    - Hostel facilities
    - Required documents
    - Seat intake
    - International admissions
    """)

    st.divider()

    st.subheader("Example Questions")

    st.markdown("""
    1. What is CSE eligibility?
    2. What is the hostel fee?
    3. What scholarships are available?
    4. What documents are required for UG?
    5. How can I apply for admission?
    """)

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("MIT ADT University Enquiry Assistant")
    st.caption("Academic Year 2026–27")


# =====================================================
# MAIN HEADER
# =====================================================

st.title("🎓 MIT ADT College Enquiry Chatbot")

st.caption(
    "Your virtual assistant for university admission "
    "and student enquiries."
)

st.divider()


# =====================================================
# WELCOME MESSAGE
# =====================================================

if not st.session_state.messages:

    with st.chat_message("assistant"):

        st.markdown("""
        Hello! 👋

        Welcome to the **MIT ADT University Enquiry Chatbot**.

        I can help you with:

        - Course eligibility and fees
        - Admission procedure
        - Scholarships and concessions
        - Hostel facilities and fees
        - Required admission documents
        - Seat intake and university information

        **How can I help you today?**
        """)


# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =====================================================
# CHAT INPUT
# =====================================================

user_question = st.chat_input(
    "Ask your question about MIT ADT University..."
)


# =====================================================
# PROCESS USER QUESTION
# =====================================================

if user_question:

    previous_history = st.session_state.messages.copy()

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):

        try:

            with st.spinner("Finding information..."):

                response_stream, retrieval_time = ask_college_chatbot(
                    user_question,
                    previous_history
                )

            response = st.write_stream(response_stream)

            if not response:
                response = (
                    "I could not generate a response. "
                    "Please try asking again."
                )
                st.markdown(response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            with st.expander("Response details"):
                st.write(
                    f"Knowledge retrieval time: "
                    f"{retrieval_time:.4f} seconds"
                )

        except Exception as e:

            st.error(
                "Sorry, something went wrong while processing "
                "your question. Please try again."
            )

            print("Chatbot Error:", str(e))

            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "Sorry, I encountered an error while "
                    "processing your question. Please try again."
                )
            })


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "MIT ADT University College Enquiry Chatbot | "
    "Python | Streamlit | Gemini"
)

st.caption(
    "Knowledge Source: MIT ADT Admission Handbook 2026–27"
)
