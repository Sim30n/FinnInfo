import finnhub
import re
import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os


class NewsAnalyzer:
    def __init__(self, finnhub_api_key, openai_api_key):
        self.finnhub_client = finnhub.Client(api_key=finnhub_api_key)
        self.openai_client = OpenAI(api_key=openai_api_key)

    def send_prompt(self, prompt):
        response = self.openai_client.chat.completions.create(
            model="gpt-5-2025-08-07",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        }
                    ],
                }
            ],
        )
        return response.choices[0].message.content

    def generate_sentiment_prompt(self, company_symbol, news_summary):
        prompt = f"""
        You are a financial analysis assistant. Your task is to analyze a short news summary related to the stock **{company_symbol}** and determine whether the news is **Positive**, **Negative**, or **Neutral** from an **investor's perspective**.

        Your analysis must focus **exclusively** on how the news affects **{company_symbol}** — do not consider the impact on any other stocks, sectors, or companies unless they directly influence {company_symbol}'s outlook.

        Consider factors such as:
        - Financial performance or outlook
        - Management actions or statements
        - Regulatory or legal developments
        - Product or service announcements
        - Market sentiment directly related to {company_symbol}
        - Industry-wide changes only if they clearly affect {company_symbol}

        Output format:
        - Sentiment: Positive / Negative / Neutral
        - Reason: [A concise explanation (1–3 sentences) of why this news is positive, negative, or neutral for {company_symbol}'s investors.]

        Example Input:
        "Tesla announced record vehicle deliveries in the second quarter, exceeding analyst expectations and boosting investor confidence."

        Example Output:
        - Sentiment: Positive
        - Reason: The record-breaking deliveries and exceeding analyst expectations indicate strong demand and performance, which is favorable for investors.

        Now analyze the following news summary:
        {news_summary}
        """
        return prompt

    def calculate_sentiment(self, company_symbol):
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        data = self.finnhub_client.company_news(company_symbol, _from=yesterday, to=today)
        sentiment_list = []
        sentiment_dict = {
            "positive_count": None,
            "negative_count": None,
            "neutral_count": None,
            "score_scaled": None
        }
        for item in data:
            news_summary = item["summary"]
            prompt = self.generate_sentiment_prompt(company_symbol, news_summary)
            if news_summary:
                result = self.send_prompt(prompt)
                sentiment = re.search(r"- Sentiment:\s*(Positive|Negative|Neutral)", result)
                sentiment_list.append(sentiment.group(1) if sentiment else "Unknown")
        sentiment_dict["positive_count"] = sentiment_list.count("Positive")
        sentiment_dict["negative_count"] = sentiment_list.count("Negative")
        sentiment_dict["neutral_count"] = sentiment_list.count("Neutral")
        score_raw = (sentiment_dict["positive_count"] * 1) + (sentiment_dict["negative_count"] * -1) + (sentiment_dict["neutral_count"] * 0)
        total = sentiment_dict["positive_count"] + sentiment_dict["negative_count"] + sentiment_dict["neutral_count"]
        score_normalized = score_raw / total
        sentiment_dict["score_scaled"] = score_normalized * 100
        return sentiment_dict

    def generate_news_summary(self, company_symbol):
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        data = self.finnhub_client.company_news(company_symbol, _from=yesterday, to=today)

        news_summary_prompt = f"""
        Here is a list of news articles related to the stock **{company_symbol}**.
        Make a maximum of 5 sentences summary from all the news articles. Focus on the
        most relevant and impactful information that would be of interest to investors.
        The news are separated by a "-------" character.
        """
        for item in data:
            news_summary = item["summary"]
            if news_summary:
                news_summary_prompt += f"\n-------\n{news_summary}"
        summary = self.send_prompt(news_summary_prompt)
        return summary


if __name__ == "__main__":
    load_dotenv()
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    news_analyzer = NewsAnalyzer(
        finnhub_api_key=finnhub_api_key,
        openai_api_key=openai_api_key
        )
    # Nvidia = NVDA
    # Microsoft = MSFT
    company_symbol = "PATH"
    sentiment = news_analyzer.calculate_sentiment(company_symbol)
    summary = news_analyzer.generate_news_summary(company_symbol)

    print(f"Positive Sentiments: {sentiment['positive_count']}")
    print(f"Negative Sentiments: {sentiment['negative_count']}")
    print(f"Neutral Sentiments: {sentiment['neutral_count']}")
    print(f"Score: {sentiment['score_scaled']}")

    print("Summary of News Articles:")
    print(summary)
