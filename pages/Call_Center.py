
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    layout='wide',
    page_title='Real World dashboard',
    page_icon=":100:")

################## Loading Data ###########

df= pd.read_csv("data/Call Center.csv")
df['call_timestamp']= pd.to_datetime(df['call_timestamp'], errors='coerce')
df['TFB']= (df['csat_score']>=7).astype(int)
df['submited survey']= df['csat_score'].notna().astype(int)

df['Weekday']=df['call_timestamp'].dt.strftime('%a')
df['year']=df['call_timestamp'].dt.year
df['week']= df['call_timestamp'].dt.isocalendar().week
df['month']= df['call_timestamp'].dt.month


######## Header ########
###

with st.container():

    col1,col2,col3=st.columns([4,5,4])
    with col2:
        st.header('Real World Dashbaord')

tab1,tab2,tab3,tab4,tab5=st.tabs(['📊Overview','📈 Describtive Stats',' Operations','SLA & Sentiment','Satisfaction'])

with tab1:
     
        
    st.markdown('<h3 style="text-align: center; color : SlateGray;">Overview</h3>', unsafe_allow_html=True) 


    ###### Side Bar

    st.sidebar.success('please select page above')
    overview= st.selectbox('please select Overview veiw', ['Metrics','Graphical summary'])


    if overview == 'Metrics':
        with st.container():
            col1,col2,col3 = st.columns([5,0.5,6])
            with col1: 
                st.metric('Total Transaction'.title(), len(df))
                st.metric('Average call duration in minutes'.title(), f"{df['call duration in minutes'].mean():.2f}")

                df1=df.groupby('channel').agg(Total_transactions=('id','count'),surveys=('submited survey','sum'),
                SAT=('TFB','sum') )
                df1['SAT%']= (df1['SAT']/df1['surveys'])*100
                df1['SAT%']= df1['SAT%'].map(lambda x : f"{x:.2f}%")
                st.dataframe(df1,use_container_width= True)


            with col3:
                st.metric('Total submitted surveys'.title(),df['submited survey'].sum())
                st.metric('Satisfaction'.title(),  f"{(df['TFB'].sum()/df['submited survey'].sum())*100:.2f}%")

                df1=df.groupby('city').agg(Total_transactions=('id','count'),surveys=('submited survey','sum'),
                SAT=('TFB','sum'))
                df1['SAT%']= (df1['SAT']/df1['surveys'])*100
                df1['SAT%']= df1['SAT%'].map(lambda x : f"{x:.2f}%")
                st.dataframe(df1,use_container_width= True)

     # Pie for sentiment / histogram for Call duration / bar for call reason           
    if overview == 'Graphical summary':
        col1,col2,col3=st.columns([5,5,5])
        with col1:
            #sentiment

            fig= px.pie(df, names = 'sentiment' ,title='sentiment analysis',template='presentation')
            col1.plotly_chart(fig,use_container_width= True)

        with col2:
            df2=df.groupby('reason').agg(Total_transactions=('id','count'),surveys=('submited survey','sum')).reset_index()
            fig1=px.histogram(df2, x='reason', y='Total_transactions',title='Call reasons',template='simple_white')

            col2.plotly_chart(fig1,use_container_width= True)

        with col3:
            fig2= px.box(df, y='call duration in minutes',color='channel', title='call duration distribution', 
                               template='simple_white')
            col3.plotly_chart(fig2, use_container_width=True)

        with st.container():
            col1,col2,col3=st.columns([0.25,11.5,0.25])
            with col2:

                fig2= px.histogram(df, x='call duration in minutes', color='channel',title='call duration distribution', 
                               template='presentation',nbins=60,marginal='box')
                col2.plotly_chart(fig2, use_container_width=True)
                

with tab2:
    with st.container():
        col1,col2,col3=st.columns([6,1,6])
        with col1:
            st.dataframe(df[['csat_score','call duration in minutes']].describe() )
            
        with col3:
            df_drop=df.drop(columns=['id','customer_name'])
            st.dataframe(df_drop.describe(include="O").T)
            

with tab3:
    col1,col2,col3=st.columns([8,.5,.5])
    
    with col1:
        dfday_duration= df.groupby('call_timestamp').agg(transactions= ('id','count'),
                                                        AVG_call_duration=('call duration in minutes','mean')).reset_index()
        dfday_duration['formatted_duration'] = dfday_duration['AVG_call_duration'].apply(lambda x: f"{x:.2f}")
        overall_avg = dfday_duration['AVG_call_duration'].mean()
        
        st.subheader(f"Overall Average Call Duration: {overall_avg:.2f}")
        
        fig= px.line(dfday_duration, x='call_timestamp',y= 'AVG_call_duration',template='simple_white',
                     text='formatted_duration')

        
        fig.update_traces(textposition="top center", text=dfday_duration['formatted_duration'])
       
        col1.plotly_chart(fig,use_container_width=True)
    
        st.write("Daily Figures:")
        st.write(dfday_duration,hide_index=True)
        
        
        

with tab4:
    
    with st.container():
        Scope= st.radio('select scope: ',['response_time', 'sentiment'] )
        col1,col2,col3 = st.columns([6,.1,3])
        
        df_pivot = df.pivot_table(index='call_timestamp', columns=Scope, values='id', aggfunc='count', fill_value=0)

        with col1:
            
            fig=px.bar(df_pivot,y= df_pivot.columns,x=df_pivot.index, color=Scope,barmode='stack',
                       template='presentation', title= f"Daily {Scope} Trend".title() )
            col1.plotly_chart(fig,use_container_width=True)
            
        with col3:   
            fig1=px.pie(df, names=Scope , color=Scope,template='presentation', title=f" {Scope} analysis".title() )
            col3.plotly_chart(fig1,use_container_width=True)
            
            
with tab5:
    col1,col2,col3=st.columns([6,.1,.1])
    with col1:
        df1=df.groupby('call_timestamp').agg(Total_transactions=('id','count'),surveys=('submited survey','sum'),
                SAT=('TFB','sum')).reset_index()
        
        df1['SAT%']= (df1['SAT']/df1['surveys'])
        df1_filtered = df1[df1['SAT'] != 0] 
        
        
        fig1=px.line(df1_filtered,x= 'call_timestamp', y='SAT%' , template='presentation',
                     text=df1_filtered['SAT%'].apply(lambda x: f"{x:.2%}")) 
        fig1.update_yaxes(tickformat='.0%')
        fig1.update_traces(textposition="top center")

        col1.plotly_chart(fig1, use_container_width=True) 
        
        df2=df.groupby(['call_timestamp','csat_score']).agg(surveys=('submited survey','sum')
                                                 ).reset_index()
        fig2=px.bar(df2,x='call_timestamp',y='surveys',color='csat_score', color_discrete_sequence=px.colors.qualitative.Bold)
        col1.plotly_chart(fig2, use_container_width=True) 
        
