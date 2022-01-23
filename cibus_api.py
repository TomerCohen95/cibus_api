import os
from collections import namedtuple

from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

import time

import email_sender


def get_balance(
        user: str,
        password: str,
        from_date: str,
        to_date: str,
) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(accept_downloads=True)
        # Open new page
        page = context.new_page()

        page.goto("https://www.cibus-sodexo.co.il/")

        page.frame(url="https://www.mysodexo.co.il/?mob=1").click(
            '[placeholder="שם משתמש"]'
        )
        page.frame(url="https://www.mysodexo.co.il/?mob=1").fill(
            '[placeholder="שם משתמש"]', user
        )

        page.frame(url="https://www.mysodexo.co.il/?mob=1").click('[placeholder="סיסמה"]')
        page.frame(url="https://www.mysodexo.co.il/?mob=1").fill(
            '[placeholder="סיסמה"]', password
        )

        with page.expect_navigation():
            page.frame(url="https://www.mysodexo.co.il/?mob=1").click("text=כניסה")

        page.goto("https://www.mysodexo.co.il/new_my/new_my_orders.aspx")

        page.fill('input[name="ctl00$cphMain$txtFrom"]', from_date)

        page.fill('input[name="ctl00$cphMain$txtTo"]', to_date)
        page.keyboard.press('Enter')
        page.keyboard.press('Enter')
        time.sleep(2)
        prices_list = page.query_selector_all('.price')
        price = 360 - int(float(prices_list[-1].inner_text())) if prices_list else 360

        context.close()
        browser.close()
        return str(price)


FilterDates = namedtuple('FilterDates', 'from_date,to_date')


def this_sunday():
    return datetime.now() - timedelta(days=((datetime.now().isoweekday()) % 7))


def this_friday():
    return this_sunday() + timedelta(days=5)


dates = FilterDates(from_date=this_sunday(), to_date=this_friday())

price = get_balance(
    user=os.getenv('CIBUS_ACCOUNT'),
    password=os.getenv('CIBUS_PASSWORD'),
    from_date=dates.from_date.strftime('%d/%m/%Y'),
    to_date=dates.to_date.strftime('%d/%m/%Y'),
)

email_sender.send_email(text=price)
