from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import os
import schedule
import time

# printing todays date
from datetime import date
today = date.today()
d=today.strftime("%m-%d-%y")
# print("date =",d)

# googlenews_url="https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en".format(d)
# print(googlenews_url)
# html=requests.get(googlenews_url)
# bsobj = soup(html.content,'lxml')
# print(bsobj)
# for link in bsobj.findAll('a',class_='gPFEn'):
#     print("Title : {}".format(link.text))

def scrape_news():
    # bbc_url="https://www.bbc.com/news/world".format(d)
    ndtv_url="https://www.ndtv.com/world-news#pfrom=home-ndtvworld_nav".format(d)
    # print(ndtv_url)
    html=requests.get(ndtv_url)
    bsobj = soup(html.content,'lxml')
    # print(bsobj)
    data = {'': [],'Unnamed: 0': [],'title': [],'article': [],'label': []}
    index = 0
    for link in bsobj.findAll('h2',class_="newsHdng"):
        # print("Title : {}".format(link.text))
        data[""].append(index)
        data["title"].append(link.text)
        data["label"].append('REAL')
        index += 1

    for news in bsobj.findAll('p'):
        # print("Article : {}".format(news.text.strip()))
        data["article"].append(news.text.strip())
        data["Unnamed: 0"].append(len("article"))

    # df=pd.DataFrame.from_dict(data)
    # df.to_csv("data.csv",index=False)
    # return pd.DataFrame(data)

# if __name__=="__main__":
#     df = scrape_news()
    df = pd.DataFrame(data)
    output_file = "data.csv"
    
    # Check if the file exists and append new data
    if os.path.exists(output_file):
        df.to_csv(output_file, mode='a', index=False, header=False)
    else:
        # If the file doesn't exist, write the DataFrame normally
        df.to_csv(output_file, index=False)

#schedule the job to run every minutes


# scheduler = BlockingScheduler()
# scheduler.add_job(scrape_news, 'interval', minutes=1)
# scheduler.start()


schedule.every(1).minutes.do(scrape_news)
while True:
    schedule.run_pending()
    time.sleep(1)

# schedule.every().day.at("00:00").do(scrape_news)
