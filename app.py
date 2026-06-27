import streamlit as st
from NewsAnalyzer import NewsAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()
finnhub_api_key = os.getenv("FINNHUB_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

news_analyzer = NewsAnalyzer(
    finnhub_api_key=finnhub_api_key,
    openai_api_key=openai_api_key
    )

st.title("Stock News Analyzer")
st.write("Analyze the sentiment of news articles related to a specific stock.")
company_symbol = st.text_input("Company symbol", "NVDA")
sentiment = news_analyzer.calculate_sentiment(company_symbol)
summary = news_analyzer.generate_news_summary(company_symbol)
st.write("Positive articles:", sentiment["positive_count"])
st.write("Negative articles:", sentiment["negative_count"])
st.write("Neutral articles:", sentiment["neutral_count"])
formatted_score = f"{sentiment['score_scaled']:.2f}"
st.write("Sentiment score (scaled -100 to 100):", formatted_score)
st.write(summary)
