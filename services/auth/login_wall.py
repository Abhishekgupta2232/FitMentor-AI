import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    st.markdown(
        """
        <style>
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #2563eb !important;
            color: #ffffff !important;
            border: 1px solid #3b82f6 !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #1d4ed8 !important;
            border-color: #60a5fa !important;
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.35) !important;
        }
        </style>
        <div style="width: 100%; text-align: center; margin-top: 10px; margin-bottom: -8px;">
            <div style="font-size: 3.1rem; font-weight: 700; line-height: 1.1; color: #ffffff; margin: 0; padding: 0;">
                FitMentor <span style="color: #38bdf8;">AI</span>
            </div>
            <div style="font-size: 1.35rem; font-weight: 500; line-height: 1.3; color: #cbd5e1; margin-top: 6px; padding: 0;">
                Your Real-Time AI Gym Coach
            </div>
            <div style="font-size: 0.98rem; font-weight: 400; line-height: 1.4; color: #94a3b8; margin-top: 42px; margin-bottom: 0; padding: 0;">
                Welcome! Please Enter Username To Start.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("Login Form", clear_on_submit=True):
        username = st.text_input("Name (Unique)", placeholder="Unique Name e.g. Abhishek Gupta")
        submit_button = st.form_submit_button("Start Session", width="stretch")

    if submit_button:
        if not username:
            st.error("Name Can't Be Empty.")
            return False

        user = get_or_create_user(username)
        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]
        st.rerun()

    return False