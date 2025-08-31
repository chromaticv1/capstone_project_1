from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from src.scrape_links_css_selectors import *
from itertools import product
from tqdm import tqdm


months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

url = "https://www.espncricinfo.com/team/bangladesh-25/match-schedule-fixtures-and-results?format=2"

# start and handle popup
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(16)
popup_container_csss = "#wzrk_wrapper > div.wzrk-alert.wiz-show-animate"
popup_container = driver.find_element(By.CSS_SELECTOR, popup_container_csss)
popup_buttons = popup_container.find_elements(By.CSS_SELECTOR, 'button')
for b in popup_buttons:
    if 'not now' in b.get_attribute('innerHTML').lower():
        b.click()


def change_year_and_month(year_to: int, month_to: str):

    navigator_month_button = driver.find_element(
        By.CSS_SELECTOR, navigator_month_button_csss)

    def change_year(year_to):

        year_left_button = driver.find_element(
            By.CSS_SELECTOR, year_left_button_csss)

        year_right_button = driver.find_element(
            By.CSS_SELECTOR, year_right_button_csss)

        keypad_year = driver.find_element(By.CSS_SELECTOR, keypad_year_csss)

        year_from = int(keypad_year.text)

        number_of_steps = abs(year_from-year_to)

        if year_from > year_to:

            for i in range(number_of_steps):

                year_left_button.click()

        if year_from < year_to:

            for i in range(number_of_steps):

                year_right_button.click()

    def change_month(month_to):

        months_keypad = driver.find_element(
            By.CSS_SELECTOR, months_keypad_csss)
        month_buttons = months_keypad.find_elements(By.TAG_NAME, 'div')

        actual_buttons = [b for b in month_buttons if len(b.text) == 3]

        actual_buttons[3].click()

        for b in actual_buttons:

            if b.text.lower() == month_to:
                b.click()

    navigator_month_button.click()
    change_year(year_to)
    change_month(month_to)
    apply_button = driver.find_element(By.CSS_SELECTOR, apply_button_csss)
    apply_button.click()

years = range(2020,2025+1)

year_and_monthIndices = [x for x in product(years,range(12)) if not ((x[0]==2020 and x[1]<6) or (x[0]==2025 and x[1]>7))]

years_and_months = (map(lambda x:(x[0], months[x[1]]), year_and_monthIndices))

match_links = {}
for pair in tqdm(years_and_months):
    driver.implicitly_wait(1)
    year, month = pair
    change_year_and_month(year,month)
    try:
        time.sleep(1)
        match_cards = driver.find_elements(By.CLASS_NAME, 'ds-no-tap-higlight')
        links = []
        for card in match_cards:
            links.append(card.get_attribute('href'))
        match_links[str(year)+'-'+month] = links
    except:
        print(f'no matches found in {year, month}')

driver.quit()

na_ml = {}
for t in match_links.keys():
    if len(match_links[t]) != 0: na_ml[t] = match_links[t]

match_records = []
for pair in na_ml.keys():
    year, month = (pair[0:4], pair[-3:])
    for link in na_ml[pair]:
        record={
            'year': year,
            'month': month,
            'link': link
        }
        match_records.append(record)
import pandas as pd
match_links_df = pd.DataFrame(match_records)
match_links_df.to_csv('./data/match_links.csv', index=False)
