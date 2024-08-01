import streamlit as st
from streamlit_gsheets import GSheetsConnection
# ydata profiling
import pandas as pd
from ydata_profiling import ProfileReport
import matplotlib.pyplot as plt
# report untuk streamlit
from streamlit_pandas_profiling import st_profile_report
import plotly.express as px


# ----------------CONFIG--------------
st.set_page_config(
    page_title="Citilink User Satisfaction Level Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------- Judul Dashboard
st.markdown("<h1 style='text-align: center;'><font color='Green'>Citilink User Sat</font><font color='MediumSeaGreen'>isfaction Level D</font><font color='YellowGreen'>ashboard</font></h1>",
            unsafe_allow_html=True)
st.markdown("---")

# ------- Sidebar
with st.sidebar:
    st.subheader("Satisfaction Data")
    st.markdown("---")

## ----- Buat button
if st.sidebar.button("Connect Data"):

    ## Read Data
    conn = st.connection("gsheet", type=GSheetsConnection)

    df = conn.read(
        spreadsheet = st.secrets.gsheet_aviation["spreadsheet"],
        worksheet = "1617068575"
    )

    st.write("Data Has Successfully loaded")
    value_consider = ['Inflight_wifi_service', 'Ease_of_Online_booking', 'Gate_location', 'Food_and_drink',
                 'Online_boarding','Seat_comfort','Inflight_entertainment','On-board_service','Leg_room_service',
                 'Baggage_handling','Checkin_service','Inflight_service','Cleanliness']

    tabs = st.tabs(["Male", 
                "Female", "Data"])

    # menambahkan konten 
    with tabs[0]:

        #satisfaction plot
        st.write("Male Satisfaction")
        fig, ax = plt.subplots()
        df.loc[df['Gender']  == 'Male', ['satisfaction']].value_counts().plot(kind='barh', y='Gender', color = ['m','b'])
        st.write(fig)

        pivot_table_Male = df[df.Gender == 'Male'].pivot_table(values = value_consider, index = 'Gender',
                                                               aggfunc = 'sum').transpose().sort_values(by='Male')
        
        #Things to notice
        st.write('Things that you need improve')
        st.write(pivot_table_Male.head(3))

        st.write('Things that you need maintain')
        st.write(pivot_table_Male.tail(3))


    with tabs[1]:
        st.write("Female Satisfaction")

        #satisfaction plot
        fig, ax = plt.subplots()
        df.loc[df['Gender']  == 'Female', ['satisfaction']].value_counts().plot(kind='barh', y='Gender', color = ['m','b'])
        st.write(fig)

        pivot_table_Female = df[df.Gender == 'Female'].pivot_table(values = value_consider, index = 'Gender',
                                                               aggfunc = 'sum').transpose().sort_values(by='Female')
        
        #Things to notice
        st.write('Things that you need improve')
        st.write(pivot_table_Female.head(3))

        st.write('Things that you need maintain')
        st.write(pivot_table_Female.tail(3))

    with tabs[2]:
        st.write(df.head(20))
        st.link_button("Sources", "https://www.kaggle.com/datasets/tetanggabaik/flight-user-satisfaction-level-citilink-indonesia?select=renew.xlsx")

        

else:
    st.info("Click Button in the left sidebar to load the Data")


