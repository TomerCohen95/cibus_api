
from playwright.sync_api import sync_playwright


def get_balance(
    user: str,
    password: str,
    from_date: str,
    to_date: str,
) -> str:
    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False)
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
        # assert page.url == "https://www.mysodexo.co.il/new_my/new_my_orders.aspx"

        page.fill('input[name="ctl00$cphMain$txtFrom"]', from_date)
        page.fill('input[name="ctl00$cphMain$txtTo"]', to_date)
        price = page.query_selector_all('.price')[-1].inner_text()

        context.close()
        browser.close()
        return price

get_balance(
        user="",
        password="",
        from_date="02/01/2022",
        to_date="06/01/2022",
    )
