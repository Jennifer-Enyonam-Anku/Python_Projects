import streamlit as st
from streamlit_option_menu import option_menu

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(page_title="Overlay Hack Test", layout="wide")

# ------------------------------------------------
# STYLE: Dark sidebar + overlay mask
# ------------------------------------------------
st.markdown("""
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #006983 !important;
            position: relative;
            z-index: 1;
        }

        html, body, [data-testid="stAppViewContainer"] > .main {
            background-color: white !important;
            color: black !important;
        }

        /* Menu item style overrides */
        .nav-link-selected {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
        }

        /* 🔧 Overlay mask to hide white corners */
        [data-testid="stSidebar"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            background-color: #006983;
            border-radius: 0px;
            z-index: 2;
            pointer-events: none;
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
# MAIN CONTENT
# ------------------------------------------------
if selected == "Home":
    st.title("🏠 Home")
    st.write("Overlay mask is active. White border should now be visually gone.")

elif selected == "Predictor":
    st.title("📊 Predictor")
    st.write("Click between tabs. Confirm if the white corner border is hidden.")
