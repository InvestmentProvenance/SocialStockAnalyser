"""
this is a scraper for the site stockTwits. however it is not efficient so have decided 
not to include it for data gathering.

stockTwits requires javascript interaction for seeing the page that investorshub didn't
if i tried to load it using just beuatiful soup then only the top couple comments
would be displayed. therefore i used selenium to scroll down and view more comments. 
the html of the selenium element object was then parsed using beautiful soup.

this worked reasonable well (if somewhat slowly) for the first couple hundred comments.
it was when it scrolled down much further, this selenium object became increasingly bigger
as it stored the entire page as one object. therefore interaction became increasingly 
slower every time you scrolled down. this cumulative affect made it unreasonably slow.
no longer functional. 

after running it for about 40 min it managed to scrape 6000 comments dating back to 
january 2024 which it successfully wrote to the database

chose delete these comments from the database as in the analysis it would have implied
that there was a sudden increase in interest in jan 2024, which is not true.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from database import db_stock
import os

site = "https://stocktwits.com/symbol/GME"
limit = 300 # number of scroll pages



#host = os.environ.get("DB_HOST","investdata.c5cwsai4kiot.us-east-1.rds.amazonaws.com")
#user = os.environ.get("DB_USER","admin")
#password = os.environ.get("DB_PASSWORD","12345678")
#database = os.environ.get("DB_NAME","your_database_name")


# Initialize the webdriver
driver = webdriver.Chrome()
# Navigate to the webpage
driver.get(site)


SCROLL_PAUSE_TIME = 0.5
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
driver.set_page_load_timeout(60)

n = 0
endReached = False
while n < limit and endReached == False: #untill end reached or some arbitrary limit
    n = n + 1
    # Scroll down to bottom

    try :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            endReached = True
        last_height = new_height

    except: # this is just to catch if it doesnt load in time.
       print(":/")

    if n%10 == 0:# displays progress
        print(n)
    

    
title_elements = driver.find_elements(By.CLASS_NAME, "symbol-active-tab-feed")
s = title_elements[0].get_attribute("innerHTML");
soup = BeautifulSoup(s,"html.parser")

posts = soup.find_all("div", {"class": "StreamMessage_main___aESy grid"})
#posts = soup.find_all("div", {"class": "css-175oi2r"})-twitter

comments = []
for post in posts:
    user = post.find("span", {"class":"StreamMessage_username-default__gka83 font-bold" }).get_text()
    text = post.find("div", {"class":"RichTextMessage_body__Fa2W1 whitespace-pre-wrap"}).get_text()
    post_time = post.find("time", {"class":"StreamMessage_timestamp__CP2QT text-stream-text ml-2 text-[11px]"})
    post_time = post_time.get("datetime").replace('Z', '+00:00')
    post_time = datetime.datetime.fromisoformat(post_time)
    
    replies = post.find("button", {"aria-label":"Reply"}).get_text()
    likes = post.find("button", {"aria-label":"Like message"}).get_text()
    score = (0 if replies == "" else 2*int(replies)) + (0 if likes == "" else int(likes))

    comments.append([user,post_time,text,score,"stocktwits.com","GME"])
    #(username, timestamp, body, score, site, symbol)


driver.quit()

db_stock.upload_sns(raw_data = comments)
