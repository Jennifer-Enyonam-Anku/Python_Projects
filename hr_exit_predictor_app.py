import streamlit as st
from streamlit_option_menu import option_menu

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(page_title="Backdrop Fix", layout="wide")

# ------------------------------------------------
# CUSTOM CSS WITH BACKDROP SQUARE
# ------------------------------------------------
st.markdown("""
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #006983 !important;
            position: relative;
        }

        html, body, [data-testid="stAppViewContainer"] > .main {
            background-color: white !important;
            color: black !important;
        }

        /* Backdrop block behind menu items */
        [data-testid="stSidebar"]::before {
            content: "";
            position: absolute;
            top: 70px; /* push below the top padding */
            left: 0;
            width: 100%;
            height: 120px; /* enough to cover 2 items */
            background-color: #006983;
            z-index: 0;
        }

        /* Menu styles */
        .nav-link {
            z-index: 1;
            position: relative;
        }

        .nav-link-selected {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR
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
    st.title("🏠 Home")
    st.write("A square block is rendered behind the menu to visually mask white edges.")

elif selected == "Predictor":
    st.title("📊 Predictor")
    st.write("The visual glitch should now be hidden by the background square.")
