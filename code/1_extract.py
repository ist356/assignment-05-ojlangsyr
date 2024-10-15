import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here

data = pd.read_csv('https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv')
data['year'] = (data['Timestamp']).apply(pl.extract_year_mdy)
data.to_csv('cache/data.csv', index=False)

states = pd.read_csv('https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv')
states.to_csv('cache/states.csv', index=False)

years = data['year'].unique()

for year in years:
    col_year = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    col_year = col_year[1]
    col_year['year'] = year
    col_year.to_csv(f'cache/col_{year}.csv', index=False)




st.dataframe(data)











states = pd.read_csv('https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv')
states.to_csv('cache/states.csv', index=False)