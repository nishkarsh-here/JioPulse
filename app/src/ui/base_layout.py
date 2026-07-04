import streamlit as st



def get_theme():
    """Current UI theme for the logged-in dashboards. Defaults to dark,
    matching the app's original look, and only ever changes via the
    theme toggle button (see header.theme_toggle_button)."""
    return st.session_state.get("theme", "dark")


def style_background_home():

    st.markdown("""
        <style>

                .stApp {
                    background: #C8102E !important;
                }

                .stApp div[data-testid="stColumn"]{
                    background-color:#FCE4E8 !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important;
                    }

                .stApp div[data-testid="stColumn"] [data-testid="stHeading"]{
                    color:#1A0E13 !important;
                    }
        </style>

                """
            ,unsafe_allow_html=True)


def style_background_dashboard():
    theme = get_theme()

    if theme == "light":
        app_bg = "#F7F5F6"
        text_color = "#241A20"
        input_bg = "#FFFFFF"
        border_color = "#E5D9DC"
    else:
        app_bg = "#181318"
        text_color = "#F5EEF0"
        input_bg = "#241A20"
        border_color = "#3A2C33"

    st.markdown(f"""
        <style>

                .stApp {{
                    background: {app_bg} !important;
                }}

                .stApp [data-testid="stHeading"], .stApp label, .stApp p, .stApp li,
                .stApp [data-testid="stMarkdownContainer"] {{
                    color:{text_color} !important;
                }}

                .stApp [data-testid="stTextInput"] input,
                .stApp [data-testid="stTextArea"] textarea,
                .stApp [data-baseweb="select"] > div {{
                    background-color:{input_bg} !important;
                    color:{text_color} !important;
                    border-color:{border_color} !important;
                }}

                .stApp [data-testid="stVerticalBlockBorderWrapper"],
                .stApp [data-testid="stExpander"] {{
                    border-color:{border_color} !important;
                }}

        </style>

                """
            ,unsafe_allow_html=True)




def style_base_layout():
# asdasd
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');


         /* Hide Top Bar of streamlit */

            #MainMenu, footer, header {
                visibility: hidden;
            }

            .block-container {
                padding-top:1.5rem !important;
            }

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height:1.1 1important;
                margin-bottom:0rem !important;
            }


            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height:0.9 !important;
                margin-bottom:0rem !important;
            }

            h3, h4, p {
                font-family: 'Outfit', sans-serif;
            }


            button{
                border-radius: 1.5rem !important;
                background-color: #C8102E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="secondary"]{
                border-radius: 1.5rem !important;
                background-color: #E5097F !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="tertiary"]{
                border-radius: 1.5rem !important;
                background-color: #33262E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button:hover{
                transform :scale(1.05)}
        </style>

                """
            ,unsafe_allow_html=True)
