import streamlit as st
import time
import re # For regex-based image URL detection

from database.pinecone.PineconeIndex import PineconeIndex
from database.mongo.MongoDB import MongoDB
from agent.cheese_bot.ChatAgent import ChatAgent

from prompt_template import hello


if __name__ == "__main__":
    if "pinecone_index" not in st.session_state:
        st.session_state.pinecone_index = PineconeIndex()
    if "mongo" not in st.session_state:
        st.session_state.mongo = MongoDB()
    if "agent" not in st.session_state:
        st.session_state.agent = ChatAgent(st.session_state.pinecone_index.indexModel, st.session_state.mongo)

    # --- Page Configuration ---
    st.set_page_config(
        page_title="CheesyChat",
        page_icon="🧀",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://shop.kimelo.com/department/cheese/3365',
            'Report a bug': None,
            'About': "## 🧀 CheesyChat \n Your friendly AI assistant for all things cheese!"
        }
    )

    # --- Custom Action Function ---
    def perform_custom_action():
        st.toast("🔄 Custom Action Triggered!", icon="🎉")
        # Example: Reset a part of the session state or re-fetch something
        if "action_counter" not in st.session_state:
            st.session_state.action_counter = 0
        st.session_state.action_counter += 1
        st.info(f"Custom action performed! Counter: {st.session_state.action_counter}")
        # You might want to st.rerun() if this action needs to refresh data displayed elsewhere
        # st.rerun()


    # --- Theme Definitions (CSS Variables) ---
    LIGHT_THEME = """
    <style>
        :root {
            --primary-color: #1c83e1;
            --background-color: #ffffff;
            --secondary-background-color: #f0f2f6;
            --text-color: #31333F;
            --font: "Source Sans Pro", sans-serif;
        }
    </style>
    """

    DARK_THEME = """
    <style>
        :root {
            --primary-color: #ff4b4b;
            --background-color: #0e1117;
            --secondary-background-color: #262730;
            --text-color: #fafafa;
            --font: "Source Sans Pro", sans-serif;
        }
    </style>
    """

    # --- CSS for Fixed Top-Right Action Button and Chat Bubbles ---
    st.markdown("""
    <style>
        /* Container for the fixed button */
        .fixed-top-right-container {
            position: fixed;
            top: 0.8rem;      /* Adjust to avoid overlapping Streamlit's header/menu */
            right: 1rem;
            z-index: 1001;   /* High z-index to be on top of other elements */
        }
    
        /* Style the button itself within the fixed container */
        .fixed-top-right-container .stButton button {
            background-color: var(--primary-color); /* Use theme color */
            color: var(--background-color); /* Contrast text */
            border: 1px solid var(--primary-color);
            padding: 0.3rem 0.8rem;
            border-radius: 0.5rem;
            font-weight: bold;
        }
        .fixed-top-right-container .stButton button:hover {
            opacity: 0.8;
        }
    
        /* Chat bubble styling */
        .stChatMessage {
            border-radius: 10px;
            padding: 10px 15px;
            margin-bottom: 10px;
            /* background-color: var(--secondary-background-color) !important; /* Ensures it uses our theme */
        }
        .stChatMessage[data-testid="stChatMessageContent"] p {
            margin-bottom: 0.5em;
        }
        /* Ensure chat text color uses our theme variable */
        .stChatMessage[data-testid="stChatMessageContent"] {
            color: var(--text-color);
        }
    </style>
    """, unsafe_allow_html=True)

    def is_image_url(text):
        if isinstance(text, str) and text.lower().startswith(('http://', 'https://')):
            if re.search(r'\.(png|jpg|jpeg|gif|webp|svg)(\?|$)', text.lower()):
                return True
        return False

    # --- App Initialization ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": hello, "avatar": "🧀"})

    if "current_theme" not in st.session_state:
        st.session_state.current_theme = "dark"

    # --- Apply Theme CSS ---
    if st.session_state.current_theme == "dark":
        st.markdown(DARK_THEME, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_THEME, unsafe_allow_html=True)


    # --- Top-Right Fixed Action Button ---
    # This uses the "markdown wrapper" trick to create a styled container for the button.
    # st.markdown('<div class="fixed-top-right-container">', unsafe_allow_html=True)
    # if st.button("🔄 Action", key="custom_action_button"):
    #     perform_custom_action()
    # st.markdown('</div>', unsafe_allow_html=True)


    # --- Sidebar ---
    with st.sidebar:
        st.header("🧀 CheesyChat Options")

        # if st.session_state.current_theme == "light":
        #     if st.button("🌙 Switch to Dark Mode", use_container_width=True):
        #         st.session_state.current_theme = "dark"
        #         st.rerun()
        # else:
        #     if st.button("☀️ Switch to Light Mode", use_container_width=True):
        #         st.session_state.current_theme = "light"
        #         st.rerun()
        st.markdown("---")
        if st.button("Clear Chat History", use_container_width=True, type="primary"):
            if "messages" in st.session_state:
                del st.session_state.messages

            if "action_counter" in st.session_state: # Also clear custom action counter for demo
                del st.session_state.action_counter
            st.rerun()
        st.markdown("---")
        st.subheader("About")
        st.info("Demo chatbot built with Streamlit.")


    # --- Main Chat Interface ---
    st.title("🧀 CheesyChat: Your AI Cheese Expert")
    st.caption("Ask me anything about cheese!")

    # Display existing messages
    for message in st.session_state.messages:
        avatar = message.get("avatar", "🤵" if message["role"] == "user" else "🧀")
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"], unsafe_allow_html=True)

    if "count" not in st.session_state:
        st.session_state.count = 0

    # Get user input
    if query := st.chat_input("What cheese are you curious about?"):
        st.session_state.messages.append({"role": "user", "content": query, "avatar": "🤵"})
        with st.chat_message("user", avatar="🤵"):
            st.markdown(query)

        with st.chat_message("assistant", avatar="🧀"):
            message_placeholder = st.empty()
            with st.spinner("The cheese expert is thinking..."):
                stream = st.session_state.agent.get_response(query)
            response = ''
            for text in stream:
                response = text
                message_placeholder.markdown(text, unsafe_allow_html=True)

            # st.session_state.count += 1
            # with open(f"response/{st.session_state.count}.md", "wb") as f:
            #     f.write(response.encode())
            #     f.close()

        st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🧀"})

