from selenium.webdriver.common.by import By
from whatsapp import open_whatsapp, MESSAGES
from config import BOT_NAME

driver = open_whatsapp()
input("From your MAIN phone send: debug check\nWait until you SEE it at the bottom of the Chrome chat, then press Enter...")

print("BOT_NAME =", repr(BOT_NAME))
elements = driver.find_elements(By.CSS_SELECTOR, MESSAGES)
print("total elements:", len(elements))
for el in elements[-6:]:
    label = el.get_attribute("data-pre-plain-text") or ""
    skipped = f"] {BOT_NAME}:" in label
    print(repr(label), "|", repr(el.text.strip()[:40]), "| skipped by filter:", skipped)

input("Enter to close")