import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

def format_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return url
    return "https://" + url

def scrape_website(url):
    url = format_url(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text

def get_sentiment(text):
    prompt = f"Please classify the sentiment of the following text - you can be as neauanced, list in 5 bullet points, keep it very short. Add in an appropriate emoji:\n\n{text}"
    messages = [{"role": "system", "content": "You are a helpful assistant that analyzes the sentiment of text."},
                {"role": "user", "content": prompt}]
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}'}
    data = json.dumps({"model": "gpt-4", "messages": messages, "max_tokens": 100, "n": 1, "stop": None, "temperature": 0.9})
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=data)

    try:
        sentiment = response.json()['choices'][0]['message']['content'].strip()
    except KeyError:
        print("Error in OpenAI API response:", response.content)
        raise Exception("An error occurred while processing the sentiment from the OpenAI API.")
    
    return sentiment

def get_summary(text):
    text = text.replace("'", '"')
    prompt = f"Please provide a brief summary of the following text. Format it in bullet points. Add emojis as appropriate.:\n\n{text}"
    messages = [{"role": "system", "content": "You are a helpful assistant that summarises and analyses web pages."},
                {"role": "user", "content": prompt}]
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}'}
    data = json.dumps({"model": "gpt-4", "messages": messages, "max_tokens": 200, "n": 1, "stop": None, "temperature": 0.5})
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=data)
    
    try:
        summary = response.json()['choices'][0]['message']['content'].strip()
    except KeyError:
        print("Error in OpenAI API response:", response.content)
        raise Exception("An error occurred while processing the summary from the OpenAI API.")
    
    return summary