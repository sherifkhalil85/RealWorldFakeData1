
import streamlit as st
import plotly.express as px 

st.set_page_config(
    layout="wide",
    page_title = 'Simple DashBoard'
)

df = px.data.tips()

## side bar 
x = st.sidebar.checkbox('Show Data', False, key=1)
day = st.sidebar.selectbox("Select Day", df['day'].unique())
time = st.sidebar.selectbox('select Meal Time', df['time'].unique())


size = st.sidebar.radio('Select How many Dishes', sorted(df['size'].unique()),3, horizontal=True)


if x:
    st.header('DataSet Sample')
    st.dataframe(df.head(8))

# page content
col1, col2, col3 = st.columns([5,2, 5])
with col1:
    new_df1 = df[df['day'] == day]
    fig = px.histogram(new_df1, x = 'total_bill', color = 'sex',
                       title=f'totalt bill for {day}day'.title(), width = 700)
    st.plotly_chart(fig,use_container_width=True)
    new_df1 = df[df['size'] == size]
    fig = px.pie(new_df1, names = 'time', color = 'sex',
                 title=f'count of each meal time according to {size} dishes'.title()).update_traces(textinfo='value')
    st.plotly_chart(fig,use_container_width=True)
    
with col3:
    new_df2 = df[df['time'] == time]
    fig = px.scatter(new_df2, x='total_bill', y = 'tip', size = 'size', size_max=20,color = 'sex',
                     title=f'correlation between total bill and tips on {time}')
    st.plotly_chart(fig,use_container_width=True)
    fig = px.sunburst(df, path= ['day', 'time', 'size'], color = 'tip',
                      title=f'counting over day, time and size over tips'.title())
    st.plotly_chart(fig,use_container_width=True)
