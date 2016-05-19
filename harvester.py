import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import csv

def getBreweryLocation(url):
    global driver

    driver.implicitly_wait(4)
    driver.get(url)

    address = ''
    try:
        elements = WebDriverWait(driver, 20).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR,
                                                             'p.memberpage-info-address'))
        )
        for p in driver.find_elements_by_css_selector('p.memberpage-info-address'):
            if address:
                address += ', '
            address += p.text
    except Exception as e:
        print(e)

    return address


def getBreweries():
    with open('brewerylist.html', 'r') as f:
        html = f.read();

    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all('a')

    links = []
    for a in anchors:
        try:
            if 'member-sidebar-item' in a['class'] and a['href']:
                title = a.find('p').contents[0]
                links.append((title, a['href']))
        except Exception:
            pass

    return links

def main():
    global driver

    driver = webdriver.Chrome(executable_path='/Users/jrossi/bin/chromedriver')
    brews = []

    for title, addr in getBreweries():
        print("Getting location of %s" % title)
        loc = getBreweryLocation(addr)
        brews.append({'Title': title, 'Address': loc})

    driver.quit()

    with open('brewerylist.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['Title', 'Address'])
        writer.writeheader()
        for row in brews:
            writer.writerow(row)

    return brews

if __name__ == "__main__":
    main()
