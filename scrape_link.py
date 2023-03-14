import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils import get_soup


def adobestock(url):
    soup = get_soup(url)

    # get script element with id "image-detail-json
    script = soup.find("script", {"id": "image-detail-json"})
    # get the content of the script element
    script_content = script.contents[0]

    # get image id from url (last part of url)
    image_id = url[url.rfind("/") + 1:]

    # parse the content as json
    _json = json.loads(script_content)

    title = _json[image_id]["title"]
    contributor = _json[image_id]["author"]

    # shorten the title to a max. of 50 characters, don't cut words
    if len(title) > 50:
        title = title[:50]
        title = title[:title.rfind(" ")] + " <em>[...]</em>"

    # create string with format: <a href="url" target="_blank">contributor - title</a>
    link = '<a href="' + url + '" target="_blank">' + contributor + " - " + title + '</a>'

    return link


def flaticon(url):
    # create a ChromeOptions object and set it to run in headless mode
    options = Options()
    options.add_argument("--headless")

    # create a Selenium webdriver with the headless ChromeOptions and navigate to the page
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)

    # wait for the page to fully load
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    # find the consent banner
    consent_banner = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="onetrust-consent-sdk"]')))

    # execute JavaScript to remove the banner
    driver.execute_script("arguments[0].remove()", consent_banner)

    # scroll to the button element
    button = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="icon-lincense"]/div/div/div/button')))
    driver.execute_script("arguments[0].scrollIntoView();", button)

    # click the button using JavaScript
    driver.execute_script("arguments[0].click();", button)

    # wait for the popup to become visible and extract the attribution text
    popup = wait.until(ec.visibility_of_element_located((By.ID, "modal-attribution-new")))
    popup_soup = BeautifulSoup(popup.get_attribute("innerHTML"), "html.parser")
    attribution_text = popup_soup.find("span", {"class": "attribution__text"}).text

    # close the browser and return the attribution text
    driver.quit()
    return attribution_text


def fallback(url):
    return '<a href="' + url + '" target="_blank">' + url + '</a>'
