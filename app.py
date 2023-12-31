import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout= 'wide', page_title= 'Startup Analysis', page_icon = "🐥")

df = pd.read_csv('startup_cleaned (1).csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month_name()

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
        temp_df['x_axis'] = temp_df['month'].astype('str') + ' ' + temp_df['year'].astype('str')
        temp_df.drop(columns=['year', 'month'], inplace=True)
        temp_df.set_index('x_axis', inplace=True)
        st.line_chart(data=temp_df)


    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        temp_df.drop(columns=['year', 'month'], inplace=True)
        temp_df.set_index('x_axis', inplace=True)
        st.line_chart(data=temp_df)



    category = df.groupby('vertical')[['vertical', 'amount']].head(5)
    category.set_index('vertical', inplace = True)
    st.subheader('Top 5 Sectors')
    fig6 = px.pie(
        labels=category.head().values,
        names= category.head().index,
        color_discrete_sequence=px.colors.sequential.ice)
    st.plotly_chart(fig6)


    st.subheader('Top Startup')
    grouped_df = df.groupby(['year', 'startup'])['amount'].sum().reset_index()
    selected_year= st.slider('Choose a year', 2015,2020,2015)

    if selected_year == 2015:
        top_5= grouped_df.query('year == 2015')

        st.dataframe(top_5)
    elif selected_year == 2016:
        top_5 = grouped_df.query('year == 2016').head(5)
        st.dataframe(top_5)
    elif selected_year == 2017:
        top_5 = grouped_df.query('year == 2017').head(5)
        st.dataframe(top_5)
    elif selected_year == 2018:
        top_5 = grouped_df.query('year == 2018').head(5)
        st.dataframe(top_5)
    elif selected_year == 2019:
        top_5 = grouped_df.query('year == 2019').head(5)
        st.dataframe(top_5)
    elif selected_year == 2020:
        top_5 = grouped_df.query('year == 2020').head(5)
        st.dataframe(top_5)


    st.subheader('Top Investors')
    grouped_df_inv = df.groupby(['year', 'investors'])['amount'].sum().reset_index()
    selected_year_inv = st.slider('Choose year', 2015, 2020, 2015)
    if selected_year_inv == 2015:
        top_5 = grouped_df_inv.query('year == 2015')
        st.dataframe(top_5)
    elif selected_year_inv == 2016:
        top_5 = grouped_df_inv.query('year == 2016').head(5)
        st.dataframe(top_5)
    elif selected_year_inv == 2017:
        top_5 = grouped_df_inv.query('year == 2017').head(5)
        st.dataframe(top_5)
    elif selected_year_inv == 2018:
        top_5 = grouped_df_inv.query('year == 2018').head(5)
        st.dataframe(top_5)
    elif selected_year_inv == 2019:
        top_5 = grouped_df_inv.query('year == 2019').head(5)
        st.dataframe(top_5)
    elif selected_year_inv == 2020:
        top_5 = grouped_df_inv.query('year == 2020').head(5)
        st.dataframe(top_5)



#function for displaying startup analysis
def load_startup_details(startup):

    st.title(startup)             #name of the startup
    last5_df_start = df[df['startup'].str.contains(startup)].head()[['date','vertical','subvertical','city','round','amount']]#load investor details
    st.dataframe(last5_df_start)
    #stages  (funding rounds)
    stage = df[df['startup'].str.contains(startup)].groupby('round')['amount'].sum().head(4) * 10000
    st.subheader('Stage')
    st.dataframe(stage)

    #investors

    inv = df[df['startup'].str.contains(startup)]['investors']
    st.subheader('Investor(s)')
    st.dataframe(inv)

#function for showing investment details
def load_investor_details(investor):
    st.title(investor)  #displaying investor name
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]#load investor details
    st.subheader('Most recent investments')
    st.dataframe(last5_df)

    col1 , col , col2 = st.columns([0.2,0.07,0.2], gap = 'small')  #to reduce the space taken by the bar chart, we can divide the page into two columns
    with col1:
        #biggest investments - bar chart
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        st.bar_chart(data = big_series)


    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().head(4)
        st.subheader('Sectors invested')
        fig1 = px.pie(
            hole=0.4,
            labels=vertical_series.index,
            names= vertical_series.index,
            color_discrete_sequence= px.colors.sequential.Tealgrn_r)
        st.plotly_chart(fig1)


    col3, cole ,col4 = st.columns([0.2,0.07,0.2], gap='small')
    with col3:
        stages_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().head(4)
        st.subheader('Stages invested')
        fig2 = px.pie(
            hole=0.4,
            labels=stages_series.index,
            names= stages_series.index,
            color_discrete_sequence=px.colors.sequential.Tealgrn
        )

        st.plotly_chart(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().head(2)
        st.subheader('Cities')
        fig3 = px.pie(
            hole=0.4,
            labels=city_series.index,
            names= city_series.index,
            color_discrete_sequence=px.colors.sequential.Teal
        )

        st.plotly_chart(fig3)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year on Year Investement')
    st.line_chart(year_series)

    #find similar investors



st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis' , 'Startup' , 'Investor'])

if option == 'Overall Analysis':
        load_overall_analysis()

elif option == 'Startup':
    st.title('Startup Analysis')
    selected_startup = st.sidebar.selectbox('Select Startup', df['startup'].unique().tolist())
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_details(selected_startup)

else:
    st.title('Investor Analysis')
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(sorted(set(df['investors'].str.split(',').sum()))))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)




