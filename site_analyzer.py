import os
import re
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from collections import Counter
import streamlit as st

# Function to check the URL
def sanitize_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url
    
# Function to fetch soup from URL
def soup_from_url(url):
    request = Request(url)
    response = urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# Function to process text
def text_proc(soup):
    text = soup.text
    for ch in ['\n', '\t', '\r']:
        text = text.replace(ch, ' ')
    text = re.sub('[^а-яА-Яa-zA-Z]+', ' ', text).strip().lower()
    return text

# Function to create DataFrame with lower and upper limit filters
def df_lim(text, low_limit, upp_limit):
    freqs = dict(Counter(text.split()))
    freqs = dict(sorted(
        freqs.items(), 
        key=lambda item: item[1], 
        reverse=True
    ))
    # Filtering words within the specified range
    freqs = [(k, v) for k, v in freqs.items() if low_limit <= v <= upp_limit]
    df = pd.DataFrame(
        freqs,
        columns=['word', 'count']
    )
    df = df.set_index('word')
    return df

# Streamlit app UI
st.header('Website Word Analyzer 📖', divider='rainbow')

url = st.text_input('Input URL', '')
if url:
    url = sanitize_url(url)
    st.write('Your url is ', url)

    # Slider for both lower and upper limits
    low_limit, upp_limit = st.slider(
        'Select word count limits',
        0, 100, (1, 10)
    )
    st.write('Lower limit:', low_limit)
    st.write('Upper limit:', upp_limit)

    # Processing part
    soup = soup_from_url(url)
    text = text_proc(soup)
    df = df_lim(text, low_limit, upp_limit)

    # Output a table with top 5
    st.divider()
    st.write('Top-5 words from the site')
    st.write(df.head(5))

    # Output a barchart
    st.divider()
    st.write('Barchart')
    st.bar_chart(df)
