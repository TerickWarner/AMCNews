import requests
import datetime
from twilio.rest import Client

CONSTANTS
STOCK = "AMC"
COMPANY_NAME = "AMC"
API_STOCK_KEY = ""
API_NEWS_KEY =""
# OPEN_PRICE_KEY = "1. open"
CLOSE_PRICE_KEY = "4. close"
NEWS_ENDPOINT_URL = "https://newsapi.org/v2/everything"
STOCK_ENDPOINT_URL = "https://www.alphavantage.co/query"
news_list = []

now = datetime.date.today()
TWO_DAYS_AGO = now - datetime.timedelta(days=7)
YESTERDAY = now - datetime.timedelta(days=1)


#GET DATA FOR SPECIFIC STOCK (AMC in this case) USING STOCK_ENDPOINT_URL
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_STOCK_KEY
}
stock_r = requests.get(STOCK_ENDPOINT_URL, params=stock_parameters)
stock_data = stock_r.json()
yesterday_close_price = stock_data['Time Series (Daily)'][str(YESTERDAY)][CLOSE_PRICE_KEY]
two_days_ago_close_price = stock_data['Time Series (Daily)']["2021-06-11"][CLOSE_PRICE_KEY]

#PERCENT CHANGE = ((V2 - V1) / V1) * 100
#V1 = TWO DAYS AGO
#V2 = ONE DAY AGO
def percent_change(V1, V2):
    change = (float(V2) - float(V1))
    percent_change = (change / float(V1)) * 100
    return percent_change

recent_change = percent_change(two_days_ago_close_price, yesterday_close_price)

#IF THE STOCK HASN'T CHANGED MUCH WE DON'T CARE ABOUT THE NEWS
if recent_change >= 5 or recent_change <= -5:
    #Same logic as stocks but with news API
    news_parameters = {
        "apiKey": API_NEWS_KEY,
        "qInTitle": COMPANY_NAME,
        "language": "en",
        "sortBy": "popularity",
        "from": "2021-06-13",
        "to": "2021-06-14"
    }

    news_r = requests.get(NEWS_ENDPOINT_URL, params=news_parameters)
    news_data = news_r.json()

    #create empty list to hold headline and link
    news_list = []
    for i in range(3):
        news_list.append(news_data['articles'][i]["title"])
        news_list.append(news_data['articles'][i]["url"])
    news = '\n'.join(map(str, news_list))

    #Send the message
    client = Client("", "")

    msg = client.messages.create(
        body=f"AMC is UP {recent_change}, here are the top headlines: \n{news}",
        to="17656235043",
        from_="+16122604224"
    )
































#Optional: Format the SMS message like this: 
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# """

