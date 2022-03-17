from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import json
import os
import smtplib
import requests
from bs4 import BeautifulSoup


def checkcrypto():
    with open("C:\Important Keys\cmc.txt", "r") as f:
        cmc = CoinMarketCapAPI(f.read())
    btc = cmc.cryptocurrency_info(symbol='BTC')
    btc = repr(btc.data)
    btc = btc.replace("\'", '\"')
    btc = btc.replace("None", "\"None\"")
    btc = json.loads(btc)
    btc = str(btc["BTC"]["description"])
    btc = btc.replace("Bitcoin (BTC) is a cryptocurrency . Users are able to generate BTC through the process of mining.", "")
    # assumes price of btc doesn't go over 100k and daily change doesn't exceed 10% at same time
    # if btc hits 100k magically there is one space at the end for wiggle room
    # if it were to go up 10% in a day then there is also that space
    btc = btc[45:139]
    return btc
    #print(btc)

def getnews():
    toreturn = []

    url = 'https://www.bbc.com/news'
    response = requests.get(url)
  
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('h3')
    unwanted = ['BBC World News TV', 'BBC World Service Radio',
                'News daily newsletter', 'Mobile app', 'Get in touch']
  
    for x in list(dict.fromkeys(headlines)):
        if x.text.strip() not in unwanted:
            toreturn.append(x.text.strip())
    toreturn = [toreturn[0:4]]    
    return toreturn
    

def send(message):
    with open("C:\Important Keys\phonenum.txt", "r") as f:
        phonenum = f.read()
    email = os.getenv("EMAIL_USER")
    passw = os.getenv("EMAIL_PASSW")
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(email, passw)

    header = f'To: {phonenum}@txt.bell.ca \nFrom:{email}\nSubject: Morning News\n'
    msg = f'{header}\n {message} \n\n'
    smtpserver.sendmail(email, f"{phonenum}@txt.bell.ca", msg)
"""
Crypto News
----------------
Regular News

"""

def main():
    news = getnews()
    news = str(news).replace("(", "")
    news = news.replace("\"", "")
    news = news.replace("\'", "")
    news = news.replace(",", ",\n\n")
    news = news[2:-2]

    message = f"{checkcrypto()}\n-----------------------------\n{news}"
    send(message)

main()