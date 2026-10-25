import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_PROFILE_PATH, PHONE_NUMBER, BOT_PREFIX

MESSAGE_BOX = "footer div[contenteditable='true']"
MESSAGES = "div.copyable-text[data-pre-plain-text]"


def open_whatsapp():
    options = Options()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")
    options.page_load_strategy = "eager"  # don't wait for every WhatsApp asset; we wait for the message box below
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://web.whatsapp.com/send?phone={PHONE_NUMBER}")

    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, MESSAGE_BOX))
    )
    return driver


def _bmp_only(text):
    """ChromeDriver's send_keys crashes on characters outside the BMP (most emoji)."""
    return "".join(ch for ch in text if ord(ch) <= 0xFFFF)


def send_message(driver, text):
    box = driver.find_element(By.CSS_SELECTOR, MESSAGE_BOX)
    box.click()
    # Every bot message starts with BOT_PREFIX so the bot can recognise (and ignore) its own messages.
    full = _bmp_only(f"{BOT_PREFIX} {text}")
    lines = full.split("\n")
    for i, line in enumerate(lines):
        box.send_keys(line)
        if i < len(lines) - 1:
            box.send_keys(Keys.SHIFT, Keys.ENTER)
    box.send_keys(Keys.ENTER)


def read_messages(driver):
    return [text for _, text in read_messages_with_ids(driver)]


# One browser round trip reads every message, instead of 3-4 round trips PER message.
_READ_JS = """
return Array.from(document.querySelectorAll(arguments[0])).map(function (el) {
  var row = el.closest('[data-id]');
  return [row ? row.getAttribute('data-id') : null,
          el.getAttribute('data-pre-plain-text') || '',
          ((el.innerText || el.textContent) || '').trim()];
});
"""


def read_messages_with_ids(driver):
    """Returns (message_id, text) for every message that doesn't start with the bot tag."""
    rows = driver.execute_script(_READ_JS, MESSAGES)
    out = []
    for msg_id, label, text in rows:
        if not text or text.startswith(BOT_PREFIX):  # empty, or sent by the bot
            continue
        out.append((msg_id or label + text, text))
    return out


if __name__ == "__main__":
    driver = open_whatsapp()
    send_message(driver, "test: reply 'done'")
    input("Reply from your phone, then press Enter here...")
    time.sleep(3)
    print(read_messages(driver)[-3:])
    input("Enter to close")
    driver.quit()