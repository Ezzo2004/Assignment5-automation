from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import pandas as pd
import os

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)
driver.maximize_window() 
driver.get("https://www.ebay.com/globaldeals/tech")

existing_titles = set()

file_name = "ebay_tech_deals.csv"

if os.path.exists(file_name):
    existing_df = pd.read_csv(file_name)
    existing_titles = set(existing_df["title"].astype(str))
product_data = []

wait = WebDriverWait(driver, 10)

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    product_container = driver.find_elements(By.XPATH, "//div[contains(@itemtype,'Product')]")
    for product in product_container:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = product.find_element(By.XPATH, ".//span[@itemprop='name']").text

        if title in existing_titles:
            continue
        
        price = product.find_element(By.XPATH, ".//span[@itemprop='price']").text
        try:
            original_price = product.find_element(By.XPATH, ".//span[contains(@class,'itemtile-price-strikethrough')]").text
        except:
            original_price = "N/A"
        try:
            shipping = product.find_element(By.XPATH, ".//span[contains(@class,'itemtile-delivery')]").text
        except:
            shipping = "N/A"
        url = product.find_element(By.XPATH, ".//a[@itemprop='url']").get_attribute("href")
        product_data.append({"timestamp": timestamp, "title": title, "price": price, "original_price": original_price, "shipping": shipping, "url": url})

        existing_titles.add(title) # update set so duplicates during scrolling are skipped

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


driver.quit()
import os


df = pd.DataFrame(product_data)

if os.path.exists(file_name):
    df.to_csv(file_name, mode="a", header=False, index=False)
else:
    df.to_csv(file_name, index=False)