import streamlit as st
from streamlit_option_menu import option_menu

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(page_title="Sidebar Test", layout="wide")

# ------------------------------------------------
# FINAL CSS FIX TO REMOVE WHITE BORDER
# ------------------------------------------------
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #006983 !important;
        }
        html, body, [data-testid="stAppViewContainer"] > .main {
            background-color: white !important;
            color: black !important;
        }

        /* ✅ FINAL FIX: REMOVE WHITE OUTLINES ON SELECTED MENU ITEM */
        .nav-link,
        .nav-link:focus,
        .nav-link:focus-visible,
        .nav-link:active,
        .nav-link-selected,
        .nav-link.nav-link-selected:focus,
        .nav-link.nav-link-selected:focus-visible,
        .nav-link.nav-link-selected:active {
            outline: none !important;
            box-shadow: none !important;
            border: none !important;
            background-image: none !important;
        }

        .nav-link-selected {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
            border-top-left-radius: 8px !important;
            border-bottom-left-radius: 8px !important;
        }

        .nav-link {
            border-radius: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR MENU (TEST)
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
# PAGE DISPLAY
# ------------------------------------------------
if selected == "Home":
    st.title("🏠 Home Page")
    st.write("This is the Home section. White border should not be visible.")

elif selected == "Predictor":
    st.title("📊 Predictor Page")
    st.write("This is the Predictor section. Still no white border.")
