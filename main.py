from playwright.sync_api import sync_playwright
import random
import sys
from datetime import datetime, timedelta
import yagmail


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login?service=https://web-vpn.sues.edu.cn/login?cas_login=true
    page.goto(
        "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login?service=https://web-vpn.sues.edu.cn/login?cas_login=true")

    # Click input[name="username"]
    page.click("input[name=\"username\"]")

    # Fill input[name="username"]
    page.fill("input[name=\"username\"]", sys.argv[1])

    # Click input[name="password"]
    page.click("input[name=\"password\"]")

    # Fill input[name="password"]
    page.fill("input[name=\"password\"]", sys.argv[2])

    # Click input[name="submit"]
    page.click("input[name=\"submit\"]")
    # assert page.url == "https://web-vpn.sues.edu.cn/"

    # Click div[id="group-4"] >> text="健康信息填报"
    with page.expect_popup() as popup_info:
        page.click("div[id=\"group-4\"] >> text=\"健康信息填报\"")
    page1 = popup_info.value

    # Click input[name="tw"]
    page1.click("input[name=\"tw\"]")

    # Click input[name="tw"]
    page1.click("input[name=\"tw\"]")

    # Triple click input[name="tw"]
    page1.click("input[name=\"tw\"]", click_count=3)

    # Fill input[name="tw"]
    temperature = str(round(random.uniform(36.0, 36.7), 1))
    page1.fill("input[name=\"tw\"]", temperature)

    # Click text="提交"
    page1.click("text=\"提交\"")

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

    return temperature


# time
time_utc = datetime.utcnow()
time_peking = (time_utc + timedelta(hours=8))


def send_email(title, _contents):
    yag = yagmail.SMTP(user='suesedu@aliyun.com', password=sys.argv[3],
                       host='smtp.aliyun.com')
    send_contents = _contents
    to = sys.argv[1] + "@sues.edu.cn"
    yag.send(to, title, send_contents)


try:
    with sync_playwright() as playwright:
        title = "Success"
        content = str(time_peking) + " temperature:" + str(run(playwright))
        send_email(title, content)

except Exception as e:
    title = "FAIL!!!"
    content = str(e)
    send_email(title, content)
