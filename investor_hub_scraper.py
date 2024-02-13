"""Function to scrape invector hub data"""
import requests
from bs4 import BeautifulSoup
from database import db_stock

def investors_hub_scraper(url):
    """Gets data from Investor Hub and uploads it to the db"""
    #url = "https://investorshub.advfn.com/Gamestop-Corporation-GME-4617"
    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' 
       '(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    #n = 0
    counter = -1# at the end of board you reach a ssection that is just 0 to 1 comments a page
    comment_info = []

    while url is not None and counter != 0 and counter != 1:
        counter = 0

        response = requests.get(url, headers=headers)
        # Check if the request was successful (status code 200
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            comments = soup.find_all("div", {
                "class": "card full-message-card my-4 mt-md-0 mb-md-2 "
                "rounded-0 border-left-0 border-right-0 border-top-0"})

            for comment in comments:
                counter += 1
                time = comment.find("div", {"data-app": "message-timestamp"}).get_text().strip()
                text = comment.find("p", {"class": "mb-0"})
                user = comment.find("a" , {
                    "class": "text-blue-link message-author font-weight-bold pt-0 mt-0"
                    }).get_text().strip()
                replies = comment.find("span", {"class":"reaction-text"}).get_text().strip()
                if replies == "Reply":
                    reply_number = 0
                else:
                    reply_number = replies[0:replies.index(" ")]

                emojis = comment.find_all("span", {"data-app": "emoji-count"})
                ecount = 0
                for e in emojis:
                    ecount = ecount + int(e.get_text().strip())

                text = text.get_text()
                # break into lines and remove leading and trailing space on each
                #lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                #chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                comment_info.append([user,time,text,reply_number*2 + ecount])


        buttons = soup.find_all("a", {"class":"mt-1 mr-2 btn blue-style-btn text-decoration-none"})
        url = None
        for b in buttons:
            if b.get_text().strip() == "Older":
                url = b.get("href")
                break

    db_stock.upload_sns(raw_data = comment_info, site = "investorshub", symbol = "gme")
    print(":)")
