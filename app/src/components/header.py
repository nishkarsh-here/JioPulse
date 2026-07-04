import streamlit as st


def theme_toggle_button(key):
    theme = st.session_state.get("theme", "dark")
    icon = ':material/light_mode:' if theme == 'dark' else ':material/dark_mode:'
    if st.button("", type='tertiary', icon=icon, key=key, width='stretch', help="Switch theme"):
        st.session_state.theme = "light" if theme == "dark" else "dark"
        st.rerun()


def header_home():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px">
            <img src='{logo_url}' style='height:100px;' />
            <h1 style='text-align:center; color:#FCE4E8'>JIO<br/>PULSE</h1>
        </div>   
                
                """, unsafe_allow_html=True)


def header_dashboard():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:10px">
            <img src='{logo_url}' style='height:85px;' />
            <h2 style='text-align:left; color:#C8102E'>JIO<br/>PULSE</h1>
        </div>   
                
                """, unsafe_allow_html=True)
