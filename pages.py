def stock_page():

def order_page():

def miad_page():

def dead_stock_page():

def profitability_page():

def category_page():

def report_page()

def render_page(data):

    selected = st.session_state["page"]

    if selected == "stok":
        stock_page()

    elif selected == "miad":
        miad_page()

    elif selected == "rapor":
        report_page()
