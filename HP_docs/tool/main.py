import streamlit as st
from HP_docs.tool.rag import initialize_system, generate_answer

st.title("HP Laptop Customer Support Chatbot")

if "system_ready" not in st.session_state:
    st.session_state.system_ready = False

if st.sidebar.button("Initialize System"):
    with st.spinner("Initializing system..."):
        try:
            initialize_system()
            st.session_state.system_ready = True
            st.sidebar.success("System initialized!")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

if st.session_state.system_ready:
    st.sidebar.write("System Ready")

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
                    st.write(source)

        except Exception as e:
            st.error(f"Error: {e}")