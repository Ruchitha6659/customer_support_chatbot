import streamlit as st
import traceback

from rag import initialize_system, generate_answer

st.set_page_config(
    page_title="HP Laptop Customer Support Chatbot",
    layout="wide"
)

st.title("HP Laptop Customer Support Chatbot")

if "system_ready" not in st.session_state:
    st.session_state.system_ready = False

with st.sidebar:
    if st.button("Initialize System"):
        with st.spinner("Initializing system..."):
            try:
                initialize_system()
                st.session_state.system_ready = True
                st.success("System initialized successfully!")

            except Exception:
                st.session_state.system_ready = False

                st.error("Initialization failed")

                st.code(
                    traceback.format_exc(),
                    language="python"
                )

    if st.session_state.system_ready:
        st.success("System Ready")

query = st.text_input("Question")

if query:
    if not st.session_state.system_ready:
        st.warning("Please initialize the system first!")

    else:
        try:
            answer, sources = generate_answer(query)

            st.header("Answer:")
            st.write(answer)

            if sources:
                st.subheader("Sources:")
                for source in sources:
                    st.write(f"- {source}")

        except Exception:
            st.error("Error while generating answer")

            st.code(
                traceback.format_exc(),
                language="python"
            )