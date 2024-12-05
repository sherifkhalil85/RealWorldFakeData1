import streamlit as st
import plotly.express as px 
import pandas as pd

st.set_page_config(
    layout="wide",
    page_title='Tips HomePage',
    page_icon='🪙'
)

df1= pd.read_csv('C:\sherif\DS course\python sessions\session 38_ Streamlit\Data World projects\Real World Fake Data Season1\Financial Consumer Complaints.csv')
df2=pd.read_csv('C:\sherif\DS course\python sessions\session 38_ Streamlit\Data World projects\Real World Fake Data Season1\Call Center.csv')



#Side bar
st.sidebar.success('select page above')
st.markdown('<h1 style="text-align: center; color : stategrey;">Home Page For Dash Board</h1>', unsafe_allow_html= True)



st.write('Call center transactions:',len(df2))
st.write('Total complaints:',len(df1))






