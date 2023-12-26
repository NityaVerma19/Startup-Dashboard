import streamlit as st
import pandas as pd
import numpy as np
df = pd.read_csv('startup_cleaned (1).csv')

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
    st.sidebar.selectbox('Select Investor', sorted(sorted(set(df['investors'].str.split(',').sum()))))
    btn2 = st.sidebar.button('Find Investor Details')




