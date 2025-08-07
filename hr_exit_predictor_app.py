import streamlit as st
from streamlit_option_menu import option_menu

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(page_title="Sidebar Border Fix Test", layout="wide")

# ------------------------------------------------
# FINAL CSS TO REMOVE WHITE BORDER
# ------------------------------------------------
st.markdown("""
    <style>
        /* Sidebar background and layout */
        [data-testid="stSidebar"] {
            background-color: #006983 !important;
        }
        html, body, [data-testid="stAppViewContainer"] > .main {
            background-color: white !important;
            color: black !important;
        }

        /* FINAL FIX: Kill white borders, focus rings, shadows, corners */
        [data-testid="stSidebar"] .nav-link,
        [data-testid="stSidebar"] .nav-link:focus,
        [data-testid="stSidebar"] .nav-link:focus-visible,
        [data-testid="stSidebar"] .nav-link:active,
        [data-testid="stSidebar"] .nav-link-selected,
        [data-testid="stSidebar"] .nav-link-selected:focus,
        [data-testid="stSidebar"] .nav-link-selected:focus-visible,
        [data-testid="stSidebar"] .nav-link-selected:active {
            outline: none !important;
            box-shadow: none !important;
            border: none !important;
            background-image: none !important;
            border-radius: 0px !important;
        }

        /* Global fallback */
        *:focus {
            outline: none !important;
            box-shadow: none !important;
        }
        *:focus-visible {
            outline: none !important;
        }

        /* Selected menu item styling */
        .nav-link-selected {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR MENU
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
# PAGE CONTENT
# ------------------------------------------------
if selected == "Home":
    st.title("🏠 Home")
    st.write("This is the Home section. White border should be completely gone.")

elif selected == "Predictor":
    st.title("📊 Predictor")
    st.write("This is the Predictor section. Again, no white border should be visible.")
