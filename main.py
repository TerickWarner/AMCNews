import requests
import datetime
from twilio.rest import Client

#STOCK CONSTANTS
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
API_STOCK_KEY = "AJMMVMF4GSJ21JHX"
API_NEWS_KEY ="74fb92969ae644e0959a6d9839743de9"
# OPEN_PRICE_KEY = "1. open"
CLOSE_PRICE_KEY = "4. close"
NEWS_ENDPOINT_URL = "https://newsapi.org/v2/everything"

#DATE VARIABLES/CONSTANTS
# now = datetime.date.today()
# one_day_ago = now - datetime.timedelta(days=3)
# TODAY = now.strftime("%Y-%m-%d")
# YESTERDAY = one_day_ago.strftime("%Y-%m-%d")


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={API_STOCK_KEY}'
stock_r = requests.get(stock_url)
stock_data = stock_r.json()

yesterday_close = stock_data['Time Series (Daily)']["2021-06-09"][CLOSE_PRICE_KEY]
today_close = stock_data['Time Series (Daily)']["2021-06-10"][CLOSE_PRICE_KEY]
print(yesterday_close)
print(today_close)

#turn into function
change = (float(today_close) - float(yesterday_close))
percent_change = (change / float(yesterday_close)) * 100
print(percent_change)




#this gets what i want but would be easier to get using parameters object instead of typing out the paramenters you want in the url
#news_url = f"https://newsapi.org/v2/everything?qInTitle={COMPANY_NAME}&language=en&sortBy=popularity&from=2021-06-09&to=2021-06-10&apiKey={API_NEWS_KEY}"



news_parameters = {
    "apiKey": API_NEWS_KEY,
    "qInTitle": COMPANY_NAME,
    "language": "en",
    "sortBy": "popularity",
    "from": "2021-06-09",
    "to": "2021-06-10"
}

news_r = requests.get(NEWS_ENDPOINT_URL, params=news_parameters)
news_data = news_r.json()





## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
client = Client("AC8eca76f0c0ae93fa0c594606eb325dd4", "179bea591a73283c0b26ebe2a6d3e944")

# msg = client.messages.create(
#     body="Monday Baby, Fuck",
#     to="17656235043",
#     from_="+16122604224"
# )

news_list = []
if percent_change > 1:
    for i in range(3):
        news_list.append(news_data['articles'][i]["title"])
        news_list.append(news_data['articles'][i]["url"])























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

