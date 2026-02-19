from datetime import datetime, timedelta
import requests
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


# -------- Getting today's, yesterday, day before yesterday DATES -----------


time = datetime

today = str(time.today())
day_yesterday = str(time.today() - timedelta(days=1))
day_before_yesterday_time = str(time.today() - timedelta(days=2))


# -------- Getting the stock Prices of yesterday, and day befor yesterday -------


parameters_for_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "T1NR9XP1M8884U0P"
}

data = requests.get(url="https://www.alphavantage.co/query", params=parameters_for_stock)
data.raise_for_status()

yesterday_stock_price = float(data.json()["Time Series (Daily)"][day_yesterday[:10]]['4. close'])
day_before_yesterday_stock_price = float(data.json()["Time Series (Daily)"][day_before_yesterday_time[:10]]['4. close'])

print(yesterday_stock_price)
print(day_before_yesterday_stock_price)

five_percent_or_more = day_before_yesterday_stock_price + (day_before_yesterday_stock_price * 0.05)
five_percent_or_less = day_before_yesterday_stock_price - (day_before_yesterday_stock_price * 0.05)


# ------------ Getting the news of the specific stock of yesterday ---------------


parameter_for_news = {
    'q': COMPANY_NAME,
    "sortBy": "popularity",
    'apiKey': "22d70d8e8b9d45fa89fcbf6a0047ca1c",
    "from": day_yesterday[:10]
}

data = requests.get(url="https://newsapi.org/v2/everything", params=parameter_for_news)
data.raise_for_status()
articles = data.json()["articles"][:3]


# -------- checking if the stock price increased/decreased by 5%  within yesterday adn day before ---------
my_email = "imkp004@gmail.com"
password = "yixxwxxwvytwctzd"



if yesterday_stock_price >= five_percent_or_more or yesterday_stock_price <= five_percent_or_less:

    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        for i in articles:
            connection.sendmail(from_addr=my_email,
                                to_addrs=my_email,
                                msg=f"Subject:{COMPANY_NAME}\nYesterday: {yesterday_stock_price}\nDay Before Yesterday: {day_before_yesterday_stock_price}\n\nHeadline: {i["title"]}\n\nBrief: {i['description']}\n\nLink To News: {i['url']}")




#Formated the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

