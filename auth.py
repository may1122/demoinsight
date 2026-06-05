import streamlit as st
from config import DEMO_USERS

def login_screen():

    if st.session_state.get("authenticated"):
        return

    username = st.text_input("Kullanıcı")

    password = st.text_input(
        "Şifre",
        type="password"
    )

    if st.button("Giriş"):

        if username in DEMO_USERS:

            if DEMO_USERS[username]["password"] == password:

                st.session_state["authenticated"] = True

                st.session_state["membership"] = \
                    DEMO_USERS[username]["membership"]

                st.rerun()

    st.stop()
