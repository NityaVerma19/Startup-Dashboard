import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# theme1 = sns.color_palette("mako", 1)

st.set_page_config(layout= 'wide', page_title= 'Startup Analysis')

df = pd.read_csv('startup_cleaned (1).csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month


#function for displaying overall analysis
def load_overall_analysis():
    st.title('Overall Analysis')

    #total invested amount
    total = round(df['amount'].sum())

    #max amount infused in a startup
    max_funding = round(df.groupby('startup')['amount'].max().sort_values(ascending= False).head(1).values[0] * 10)

    #average ticket size
    avg_funding = round(df.groupby('startup')['amount'].sum().mean() * 1000)


    col1, col2, col3 = st.columns(3, gap = 'medium')
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Maximum', str(max_funding) + 'Cr')
    with col3:
        st.metric('Average', str(avg_funding) + 'Cr')


    st.header('Month on Month Graph')
    selected_option = st.selectbox('Select type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        temp_df.drop(columns=['year', 'month'], inplace=True)
        temp_df.set_index('x_axis', inplace=True)
        st.line_chart(data=temp_df , color = sns.color_palette("mako", 1))


    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        temp_df.drop(columns=['year', 'month'], inplace=True)
        temp_df.set_index('x_axis', inplace=True)
        st.line_chart(data=temp_df, color = sns.color_palette("mako"))



#function for showing investment details
def load_investor_details(investor):
    st.title(investor)  #displaying investor name
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]#load investor details
    st.subheader('Most recent investments')
    st.dataframe(last5_df)

    col1, col2, col3, col4 = st.columns(4, gap = 'small')  #to reduce the space taken by the bar chart, we can divide the page into two columns
    with col1:
        #biggest investments - bar chart
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        st.bar_chart(data = big_series, color = sns.color_palette("mako", 1))


    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().head(4)
        st.subheader('Sectors invested')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series , labels = vertical_series.index , colors = sns.color_palette("mako", 4))
        st.pyplot(fig1)

    with col3:
        stages_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().head(4)
        st.subheader('Stages invested')
        fig2, ax2 = plt.subplots()
        ax2.pie(stages_series , labels = stages_series.index , colors = sns.color_palette("mako", 4))
        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().head(4)
        st.subheader('Cities')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series , labels = city_series.index , colors = sns.color_palette("mako", 4))
        st.pyplot(fig3)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year on Year Investement')
    st.line_chart(year_series, color= sns.color_palette("mako", 1))

    #find similar investors

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis' , 'Startup' , 'Investor'])

if option == 'Overall Analysis':
        load_overall_analysis()

elif option == 'Startup':
    st.title('Startup Analysis')
    st.sidebar.selectbox('Select Startup', df['startup'].unique().tolist())
    btn1 = st.sidebar.button('Find Startup Details')

else:
    st.title('Investor Analysis')
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(sorted(set(df['investors'].str.split(',').sum()))))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)




