import streamlit as st
from streamlit_option_menu import option_menu

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(page_title="Sidebar Block Test", layout="wide")

# ------------------------------------------------
# PHYSICAL BLOCK INSERTED USING STREAMLIT
# ------------------------------------------------
with st.sidebar:
    # Background color styling
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #006983 !important;
            }
            html, body, [data-testid="stAppViewContainer"] > .main {
                background-color: white !important;
                color: black !important;
            }
            .square-block {
                height: 120px;
                width: 100%;
                background-color: #006983;
                border: none;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # 🔲 THIS IS THE VISIBLE SQUARE
    st.markdown('<div class="square-block"></div>', unsafe_allow_html=True)

    # MENU BELOW SQUARE
    selected = option_menu(
        menu_title=None,
        options=["Home", "Predictor"],
        icons=["house", "bar-chart"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#006983"},
            "icon": {"color": "#3edad8", "font-size": "22px"},
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#002c66",
                "color": "#ffffff"
            },
            "nav-link-selected": {
                "background-color": "#00b4d8",
                "color": "#ffffff"
            },
        },
    )

# ------------------------------------------------
# PAGE DISPLAY
# ------------------------------------------------
if selected == "Home":
    st.title("🏠 Home")
    st.write("The square is above the menu in the sidebar. Do you see it?")

elif selected == "Predictor":
    st.title("📊 Predictor")
    st.write("You can still navigate. The block should remain above the menu.")
