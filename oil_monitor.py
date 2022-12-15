from selenium import webdriver
import paho.mqtt.publish as publish
import json
from selenium.webdriver.common.by import By
import time
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')

browser = webdriver.Chrome(options=chrome_options)
browser.implicitly_wait(3)

user_name = os.getenv('OIL_DEVICE_USER')
password = os.getenv('OIL_DEVICE_PASS')
mqtt_server = os.getenv('MQTT_SERVER')
mqtt_user = os.getenv('MQTT_USER')
mqtt_password = os.getenv('MQTT_PASS')

while True:
    browser.get("https://app.smartoilgauge.com/app.php")
    browser.find_element(By.ID, "inputUsername").send_keys(user_name)
    browser.find_element(By.ID, "inputPassword").send_keys(password)
    browser.find_element(By.CSS_SELECTOR, "button.btn").click()
    browser.implicitly_wait(3)

    var = browser.find_element(By.XPATH, '//p[contains(text(), "/")]').text
    fill_level = browser.find_element(By.XPATH,
                                      "//div[@class='ts_col ts_level']//div[@class='ts_col_val']//p"
                                      ).get_attribute("innerHTML")
    fill_level = fill_level.split(r"/")
    current_fill_level = fill_level[0]
    current_fill_proportion = round((float(str(fill_level[0])) / float(str(fill_level[1]))) * 100, 1)
    battery_status = browser.find_element(By.XPATH,
                                          "//div[@class='ts_col ts_battery']//div[@class='ts_col_val']//p"
                                          ).get_attribute("innerHTML")
    days_to_low = browser.find_element(By.XPATH,
                                       "//div[@class='ts_col ts_days_to_low']//div[@class='ts_col_val']//p"
                                       ).get_attribute("innerHTML")

    print(current_fill_level)
    print(current_fill_proportion)
    print(battery_status)
    print(days_to_low)

    msgs = [{"topic": "oilgauge/tanklevel",
             "payload": json.dumps({
                 "current_fill_level": current_fill_level,
                 "current_fill_proportion": current_fill_proportion,
                 "battery_status": battery_status,
                 "days_to_low": days_to_low
             })
             }]
    browser.quit()
    publish.multiple(msgs, hostname=mqtt_server, port=1883, auth={'username': mqtt_user, 'password': mqtt_password})
    time.sleep(3600)
