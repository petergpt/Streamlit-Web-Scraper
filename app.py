import os
import json
import requests
import re
import streamlit as st
import pandas as pd
from helpers import format_url, scrape_website, get_summary, get_sentiment, get_generated_url
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_url(url):
    content = scrape_website(url)
    summary = get_summary(content)
    sentiment = get_sentiment(summary)
    return url, summary, sentiment

st.title("URL Summarizer")

url_mapping = {
    "BBC": "www.bbc.co.uk/news",
    "The Guardian": "www.theguardian.com/uk",
    "The Telegraph": "www.telegraph.co.uk",
    "The Sun": "www.thesun.co.uk",
    "Daily Mail": "https://www.dailymail.co.uk",
    "Mirror": "www.mirror.co.uk",
    "The Times": "www.thetimes.co.uk",
    "Independent": "www.independent.co.uk",
    "Express": "www.express.co.uk",
    "Financial Times": "www.ft.com"
}

source_option = st.radio("Choose a source option:", ("Enter a URL or keyword", "Select from pre-listed UK news websites"))

selected_urls = [None, None, None]
url_inputs = ["", "", ""]

if source_option == "Enter a URL or keyword":
    url_inputs[0] = st.text_input("Enter URL or keyword for Summary 1:")
    url_inputs[1] = st.text_input("Enter URL or keyword for Summary 2:")
    url_inputs[2] = st.text_input("Enter URL or keyword for Summary 3:")
else:
    for i in range(3):
        selected_website = st.selectbox(f"Choose from the pre-listed UK news websites for Summary {i+1}:", [None] + list(url_mapping.keys()), key=i)
        if selected_website:
            selected_urls[i] = url_mapping[selected_website]

if st.button("Submit"):
    urls = []
    for url_input, selected_url in zip(url_inputs, selected_urls):
        if url_input:
            url_input = get_generated_url(url_input)
            urls.append(url_input)
        else:
            urls.append(selected_url)

    results = {}
    progress_bar = st.progress(0)
    progress = 0

    with ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results[url] = future.result()
            except Exception as e:
                results[url] = (url, None, str(e))
            
            progress += 1
            progress_bar.progress(progress / len(urls))

    # Prepare the table data
    table_data = []

    for i, url in enumerate(urls):
        if not url:
            table_data.append({"URL": f"Summary {i+1} (No URL provided)", "Sentiment": "N/A", "Summary": "N/A"})
            continue

        summary, sentiment = results[url][1], results[url][2]
        
        table_data.append({"URL": url, "Sentiment": sentiment, "Summary": summary})

    # Create and display the table
    df = pd.DataFrame(table_data, index=range(1, len(table_data) + 1))
    st.table(df)