import pandas as pd

def load_excel():

    uploaded = st.file_uploader(
        "Excel yükle"
    )

    if uploaded is None:
        st.stop()

    return pd.read_excel(uploaded)
