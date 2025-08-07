import streamlit as st
from streamlit_option_menu import option_menu

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(page_title="Test Sidebar", layout="wide")

# ------------------------------------------------
# CUSTOM STYLING (MINIMAL STRIP DOWN)
# ------------------------------------------------
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #006983 !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            border-right: none;
        }
        html, body, [data-testid="stAppViewContainer"] > .main {
            background-color: white !important;
            color: black !important;
        }

        /* ✅ Final attempt to kill all white borders on active menu items */
        [data-testid="stSidebar"] .nav-link:focus,
        [data-testid="stSidebar"] .nav-link:focus-visible,
        [data-testid="stSidebar"] .nav-link:active,
        [data-testid="stSidebar"] .nav-link-selected {
            outline: none !important;
            box-shadow: none !important;
            border: none !important;
            background-image: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR TEST
# ------------------------------------------------
with st.sidebar:
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
# SIMPLE PAGE RENDERING
# ------------------------------------------------
if selected == "Home":
    st.title("🏠 Home Test")
    st.write("You are on the Home page.")

elif selected == "Predictor":
    st.title("📊 Predictor Test")
    st.write("You are on the Predictor page.")
