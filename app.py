import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout= 'wide', page_title= 'Startup Analysis')

df = pd.read_csv('startup_cleaned (1).csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')


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
        fig, ax = plt.subplots()
        ax.bar(big_series.index , big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().head()
        st.subheader('Sectors invested')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series , labels = vertical_series.index )
        st.pyplot(fig1)

    with col3:
        stages_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().head()
        st.subheader('Sectors invested')
        fig2, ax2 = plt.subplots()
        ax2.pie(stages_series , labels = stages_series.index )
        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().head()
        st.subheader('Cities')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series , labels = city_series.index )
        st.pyplot(fig3)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year on Year Investement')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)






st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis' , 'Startup' , 'Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')

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




