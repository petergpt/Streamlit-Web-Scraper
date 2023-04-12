import os
import json
import requests
import re
import streamlit as st
from helpers import format_url, scrape_website, get_summary

def get_generated_url(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates URLs based on user input."},
        {"role": "user", "content": prompt}
    ]
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}'}
    data = json.dumps({"model": "gpt-4", "messages": messages, "max_tokens": 50, "n": 1, "stop": None, "temperature": 0.5})
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=data)

    try:
        generated_text = response.json()['choices'][0]['message']['content'].strip()
    except KeyError:
        print("Error in OpenAI API response:", response.content)
        raise Exception("An error occurred while processing the generated URL from the OpenAI API.")
    
    # Extract URL from the generated text
    url_match = re.search(r'https?://[^\s]+', generated_text)
    if url_match:
        return url_match.group(0)
    else:
        raise Exception("No URL was found in the generated text.")

st.title("URL Summarizer")

source_option = st.radio("Choose a source option:", ("Enter a URL or keyword", "Select from pre-listed UK news websites"))

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

if source_option == "Enter a URL or keyword":
    url_input = st.text_input("Enter a URL or keyword:")
    selected_url = None
else:
    selected_website = st.selectbox("Choose from the pre-listed UK news websites:", list(url_mapping.keys()))
    selected_url = url_mapping[selected_website]
    url_input = None

if st.button("Submit"):
    if url_input:
        with st.spinner("Generating URL based on input..."):
            url_input = get_generated_url(url_input)

        url = url_input
    else:
        url = selected_url

    st.write(f"Processing URL: {url}")

    try:
        with st.spinner("Scraping website and generating summary..."):
            content = scrape_website(url)
            summary = get_summary(content)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    else:
        st.subheader("Summary")
        st.write(summary)