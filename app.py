import streamlit as st
import pandas as pd
import numpy as np
df = pd.read_csv('startup_funding.csv')
#data cleaning
df['Investors Name'] = df['Investors Name'].fillna('Undisclosed')

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis' , 'Startup' , 'Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
elif option == 'Startup':
    st.title('Startup Analysis')
    st.sidebar.selectbox('Select Startup', df['Startup Name'].unique().tolist())
    btn1 = st.sidebar.button('Find Startup Details')

else:
    st.title('Investor Analysis')
    st.sidebar.selectbox('Select Investor', sorted(df['Investors Name'].unique().tolist()))
    btn2 = st.sidebar.button('Find Investor Details')




