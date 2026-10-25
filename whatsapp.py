import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_PROFILE_PATH, PHONE_NUMBER , BOT_NAME

MESSAGE_BOX = "footer div[contenteditable='true']"
MESSAGES = "div.copyable-text[data-pre-plain-text]"

def open_whatsapp():
    options = Options()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}") 
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://web.whatsapp.com/send?phone={PHONE_NUMBER}")
    
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, MESSAGE_BOX))
    )
    return driver

def send_message(driver, text):
    box = driver.find_element(By.CSS_SELECTOR, MESSAGE_BOX)
    box.click()
    lines = text.split("\n")
    for i, line in enumerate(lines):
        box.send_keys(line)
        if i < len(lines) - 1:
            box.send_keys(Keys.SHIFT, Keys.ENTER)  
    box.send_keys(Keys.ENTER)

def read_messages(driver):
    
    elements = driver.find_elements(By.CSS_SELECTOR, MESSAGES)
    replies = []
    for ele in elements:
        text = ele.text.strip()
        label = ele.get_attribute("data-pre-plain-text") or ""
        if not text:
            continue
        if f"] {BOT_NAME}:" in label:   # sent by the bot, skip
            continue
        replies.append(text)
    return replies

if __name__ == "__main__":
    driver = open_whatsapp()
    send_message(driver, "test: reply 'done' ")
    print("reply from phone and press enter here")
    time.sleep(3)
    print(read_messages(driver)[-3:])
    input("Enter to close")