from auth import login_screen
from data_utils import load_excel
from analytics import prepare_data
from components import render_header
from pages import render_page

login_screen()

df = load_excel()

data = prepare_data(df)

render_header(data)

render_page(data)
