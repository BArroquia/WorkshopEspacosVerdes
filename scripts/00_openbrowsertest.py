from playwright.sync_api import sync_playwright, Playwright
import pandas as pd
import time
import random


playwright = sync_playwright().start()

browser = playwright.chromium.launch()
page = browser.new_page()
page.goto("https://playwright.dev/")
time.sleep(5)
page.screenshot(path="data/raw/example.png")
browser.close()

playwright.stop()