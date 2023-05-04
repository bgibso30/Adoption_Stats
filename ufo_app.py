import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import glob, nltk, os, re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from PIL import Image
from ufo_app2 import *


#Read in data
ufo_df = pd.read_csv('UFOs.csv')

# Create new columns
ufo_df['Date_Time'] = pd.to_datetime(ufo_df['Date_Time'])
ufo_df['Day'] = ufo_df['Date_Time'].dt.day
ufo_df['Month'] = ufo_df['Date_Time'].dt.month
ufo_df['Time'] = ufo_df['Date_Time'].dt.time

# Convert month 
ufo_df['Month'] = ufo_df['Month'] .replace(1,"January")
ufo_df['Month'] = ufo_df['Month'] .replace(2,"February")
ufo_df['Month'] = ufo_df['Month'] .replace(3,"March")
ufo_df['Month'] = ufo_df['Month'] .replace(4,"April")
ufo_df['Month'] = ufo_df['Month'] .replace(5,"May")
ufo_df['Month'] = ufo_df['Month'] .replace(6,"June")
ufo_df['Month'] = ufo_df['Month'] .replace(7,"July")
ufo_df['Month'] = ufo_df['Month'] .replace(8,"August")
ufo_df['Month'] = ufo_df['Month'] .replace(9,"September")
ufo_df['Month'] = ufo_df['Month'] .replace(10,"October")
ufo_df['Month'] = ufo_df['Month'] .replace(11,"November")
ufo_df['Month'] = ufo_df['Month'] .replace(12,"December")

# Cast summary column
ufo_df = ufo_df.astype({'Summary':'string'})


#Sidebar
st.sidebar.header('Bar Chart Settings')
state_count = st.sidebar.slider('Number of bars to display', min_value=5, max_value=25, value=10, step=2)

st.sidebar.header('Word Cloud Settings')
max_word = st.sidebar.slider('Max Words', min_value=10, max_value=200, value=100, step=10)
word_size = st.sidebar.slider('Size of largest word', min_value=50, max_value=350, value=60, step=10)

#Create vertical space
st.sidebar.write(" ")
st.sidebar.write(" ")
image = Image.open('ufo.png')
st.sidebar.image(image, use_column_width=True)


row0_spacer1, row0_1, row0_spacer2, row0_spacer3 = st.columns((.1, 2.3, 1.3, .1))
with row0_1:
    st.title('Visualizing UFO Sightings')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Have you ever wondered how often a UFO is sighted across the country? Check out these interesting statistics from the year 2016!  This is a Streamlit App by [Bria Gibson](https://www.linkedin.com/in/bria-gibson-ba0573188/) ")

#Create vertical space
st.write(" ")
st.write(" ")
st.write(" ")
st.subheader('Count of UFO Sightings') 



state_list= ufo_df[ufo_df['Country'] == 'USA']
state_list = state_list['State'].unique().tolist()
state_list.sort(reverse=False)
state_list.insert(0, "Top States")

state = st.selectbox('Select a State to look at city count', state_list, index=0)




#Graph

if state == "Top States":
    bar_chart = alt.Chart(ufo_df).transform_aggregate(
        Count='count()',
        groupby=['State']
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('Count', order='descending')]
    ).transform_filter(
        alt.datum.rank < state_count + 1
    ).mark_bar().encode(
        y=alt.Y('State:N', sort='-x'),
        x=('Count:Q')
    ).properties(
        width=700,
        height=450
    )
else:
      cities_df = ufo_df[(ufo_df['Country'] == 'USA') & (ufo_df['State'] == state)]
      bar_chart = alt.Chart(cities_df).transform_aggregate(
        Count='count()',
        groupby=['City']
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('Count', order='descending')]
    ).transform_filter(
        alt.datum.rank < state_count + 1
    ).mark_bar().encode(
        y=alt.Y('City:N', sort='-x'),
        x=('Count:Q')
    ).properties(
        width=700,
        height=450
    )

st.altair_chart(bar_chart)

#Create vertical space
st.write(" ")
st.write(" ")
st.subheader('Lets drill into the monthly view...') 

month = st.selectbox('Select a Month', ufo_df['Month'].unique())

df = ufo_df[ufo_df.Month == month]


line_chart = alt.Chart(df).transform_aggregate(
    Count='count()',
    groupby=['Day']
).transform_window(
    rank='rank(count)',
    sort=[alt.SortField('Count', order='descending')]
).transform_filter(
    alt.datum.rank < state_count + 1
).mark_line().encode(
    y=('Count:Q'),
    x = alt.X('Day:N')
).properties(
    width=700,
    height=450
)
st.altair_chart(line_chart)


#Create vertical space
st.write(" ")
st.write(" ")
st.subheader("Now, let's see how these sightings were described...") 

# Word Cloud
month2 = st.selectbox('Choose a Month', ufo_df['Month'].unique())
day = st.selectbox('Choose a Date', ufo_df['Day'].unique())

df2 = ufo_df[(ufo_df.Month == month) & (ufo_df.Day == day)]  

nltk_stop_words = stopwords.words('english')
stop_words = set(nltk_stop_words)


def custom_tokenize(text):
    nltk_stop_words = stopwords.words('english')
    stop_words = set(nltk_stop_words)
    if not text:
        print('The text to be tokenized is a None type. Defaulting to blank string.')
        text = ''
    return word_tokenize(text)
df2['Summary'] = df2.Summary.apply(custom_tokenize)
tokens = df2['Summary']

wc= WordCloud(width=480, height=480, margin=0,max_words=max_word,max_font_size=word_size).generate(df2['Summary'].to_string())
word_cloud = wc.to_file('wordcloud.png')
st.image(wc.to_array(),width=550)






    
