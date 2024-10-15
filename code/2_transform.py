import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

states = pd.read_csv('cache/states.csv')
data = pd.read_csv('cache/data.csv')
col21 = pd.read_csv('cache/col_2021.csv')
col22 = pd.read_csv('cache/col_2022.csv')
col23 = pd.read_csv('cache/col_2023.csv')
col24 = pd.read_csv('cache/col_2024.csv')



#convert states to abbreviations using states.csv
data["If you're in the U.S., what state do you work in?"] = (data["If you're in the U.S., what state do you work in?"]).apply(lambda x: states[states['State'] == x]['Abbreviation'].values[0] if x in states['State'].values else x)
#st.write(data["If you're in the U.S., what state do you work in?"])

#clean country for usa
data['country'] = data['What country do you work in?'].apply(pl.clean_country_usa)

#Engineer a new column consisting of the city, a comma, the 2-character state abbreviation, another comma and _country For example: "Syracuse, NY, United States". name this column _full_city
data['full_city'] = data['What city do you work in?'] + ', ' + data["If you're in the U.S., what state do you work in?"] + ', ' + data['country']

#concat col_2021, col_2022, col_2023, col_2024 into one dataframe
col_data = pd.concat([col21, col22, col23, col24], ignore_index=True)

#create the dataframe combined by matching the survey_states_combined to cost of living data matching on the year and _full_city columns
combined = data.merge(col_data, left_on=['year', 'full_city'], right_on=['year', 'City'], how='inner')

# normalize each annual salary based on cost of living. How do you do this? A COL 90 means the cost of living is 90% of the average, so $100,000 in a COL city of 90 is the equivalent buying power of(100/90) * $100,000 == $111,111.11
combined['annual_salary_cleaned'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)
combined['annual_salary_adjusted'] = combined.apply(lambda row: row['annual_salary_cleaned'] * (100 / row['Cost of Living Index']), axis=1)

#save the combined dataframe to a csv file
combined.to_csv('cache/combined.csv', index=False)

#create a pivot table for average adjusted salary with full city and 'How old are you?' 
pivot = combined.pivot_table(index=['full_city', 'How old are you?'], values='annual_salary_adjusted', aggfunc='mean')
pivot.to_csv('cache/annual_salary_adjusted_by_location_age.csv')

#create a pivot table to show annual salary adjusted by location and education
pivot = combined.pivot_table(index=['full_city', 'What is your highest level of education completed?'], values='annual_salary_adjusted', aggfunc='mean')
pivot.to_csv('cache/annual_salary_adjusted_by_location_education.csv')


