import streamlit as st
from streamlit_option_menu import option_menu

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(page_title="Sidebar Mask Test", layout="wide")

# ------------------------------------------------
# STYLING BLOCK
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

        .square-block {
            height: 80px;
            width: 100%;
            background-color: #ffffff;
            border: none;
            margin-top: -10px;
            margin-bottom: 0;
            padding: 0;
        }

        /* Optional: tighten sidebar padding */
        .css-6qob1r.eczjsme3 {
            padding-top: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR CONTENT
# ------------------------------------------------
with st.sidebar:
    # 🔹 MENU
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

    # 🔹 BACKGROUND MASK BELOW MENU
    st.markdown('<div class="square-block"></div>', unsafe_allow_html=True)

# ------------------------------------------------
# PAGE DISPLAY
# ------------------------------------------------
if selected == "Home":
    st.title("🏠 Home")
    st.write("This square now sits under the menu to visually mask any white corners.")

elif selected == "Predictor":
    st.title("📊 Predictor")
    st.write("Navigate between tabs — the square remains as a visual mask.")
