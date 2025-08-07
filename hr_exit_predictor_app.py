import streamlit as st
from streamlit_option_menu import option_menu

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(page_title="Overlay Hack Fix", layout="wide")

# ------------------------------------------------
# CORNER MASKING ONLY
# ------------------------------------------------
st.markdown("""
    <style>
        /* Sidebar base */
        [data-testid="stSidebar"] {
            background-color: #006983 !important;
            position: relative;
        }

        html, body, [data-testid="stAppViewContainer"] > .main {
            background-color: white !important;
            color: black !important;
        }

        /* Selected menu item style */
        .nav-link-selected {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
        }

        /* 🔧 Overlay corner patches */
        .corner-mask {
            content: "";
            position: absolute;
            width: 12px;
            height: 12px;
            background-color: #006983;
            z-index: 1000;
        }

        .corner-top-left {
            top: 0;
            left: 0;
            border-top-left-radius: 8px;
        }

        .corner-bottom-left {
            bottom: 0;
            left: 0;
            border-bottom-left-radius: 8px;
        }
    </style>

    <script>
        // Inject divs into sidebar after it renders
        window.addEventListener('DOMContentLoaded', function () {
            const sidebar = parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                const topCorner = document.createElement('div');
                topCorner.className = 'corner-mask corner-top-left';
                const bottomCorner = document.createElement('div');
                bottomCorner.className = 'corner-mask corner-bottom-left';
                sidebar.appendChild(topCorner);
                sidebar.appendChild(bottomCorner);
            }
        });
    </script>
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
    st.write("Corner mask is active. White edge should now be hidden visually.")

elif selected == "Predictor":
    st.title("📊 Predictor")
    st.write("Test the tab switch — no more white corner should be visible.")
