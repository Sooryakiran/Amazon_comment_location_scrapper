import requests as rq
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

file = open("output.csv" ,"a")

options = Options()
options.add_argument('--headless')

binary = FirefoxBinary('/usr/bin/firefox')  # path to firefox
firefoxProfile = FirefoxProfile()

firefoxProfile.set_preference('permissions.default.image', 2)
browser = webdriver.Firefox(firefoxProfile,firefox_binary=binary)

def get_location(profile_url):

    browser.get(profile_url)


    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "customer-profile-name-header"))

    )
    finally:
        pass
    data =browser.page_source
    # print(data)
    data2 = BeautifulSoup(data ,features="lxml" )
    data3 = data2.findAll("div", {"class": "bio-occupation-location"})
    if len(data3) ==0 :
        print("\tNo location data. Skipping...")
        return None

    else:
        data3 = data3[0]
        location = data3.findAll("span")
        location = location[0].text
        print("\t" + location)
        return location

def get_data(url):
    global file
    parts = url.split("/dp/")
    reviews_url = parts[0] + "/product-reviews/" + parts[1]
    i =1
    done = False
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 15_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


    while(not done):
        target = reviews_url+ "ref=cm_cr_getr_d_paging_btm_next_" + str(i) + "?ie=UTF8&reviewerType=all_reviews&pageNumber=" + str(i)
        # print(target)
        data = rq.get(target,headers = headers)
        data = data.text
        # print(data)
        soup = BeautifulSoup(data,features="lxml")
        divs = soup.findAll("div", {"data-hook": "review"})
        for div in divs:
            profile = div.findAll("a", {"class": "a-profile"})
            required = div.findAll("a", {"data-hook": "review-title"})
            required = str(required[0])
            required = required.split(">")[1]
            required = required.split("<")[0]
            print("Comment title: " + required)
            profile_data = str(profile[0])

            profile_data = profile_data.split('href="')[1]
            profile_data = profile_data.split('"')[0]
            profile_url = "https://www.amazon.in/" + profile_data
            location = get_location(profile_url)
            if location == None:
                pass
            else:
                file.write(required +"\t" + location + "\n")
                file.flush()
            # print(profile_url)

        i = i +1
        print("Page %d" %(i-1))
        print(len(divs))
        if len(divs) ==0 :
            done = True

    # print(data)

url = "https://www.amazon.in/OnePlus-Mirror-Black-128GB-Storage/dp/B07DJD1Y3Q/"

get_data(url=url)
