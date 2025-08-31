import pandas as pd
from selenium import webdriver
import time
from tabulate import tabulate
from selenium.webdriver.common.by import By
from tqdm import tqdm
from io import StringIO

match_links_df = pd.read_csv('./data/match_links.csv')


driver = webdriver.Chrome()
urls = match_links_df.iloc[25:35,-1].tolist()
url = urls[0]
    
driver.get(url)

match_title = driver.find_element(By.CSS_SELECTOR, r"#main-container > div:nth-child(2) > div > div > div > div.ds-grow.ds-flex.ds-items-center > div > h1").text
short_desc = driver.find_element(By.CSS_SELECTOR, r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(1) > div:nth-child(2) > div.ds-w-full.ds-bg-fill-content-prime.ds-overflow-hidden > div > div:nth-child(1) > div > div > div > div > div.ds-flex.ds-justify-between.ds-items-center > div.ds-truncate > span.ds-flex.ds-items-center > div").text
summary_result = driver.find_element(By.CSS_SELECTOR, r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(1) > div:nth-child(2) > div.ds-w-full.ds-bg-fill-content-prime.ds-overflow-hidden > div > div:nth-child(1) > div > div > div > div > p > span").text

if 'won' in summary_result.lower():

    first_round_table_title = driver.find_element(By.CSS_SELECTOR, r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div.ds-w-full.ds-bg-fill-content-prime.ds-overflow-hidden.ds-border-line.ds-mb-2.ds-border > div.ds-flex.ds-px-4.ds-border-b.ds-border-line.ds-py-3.ds-bg-ui-fill-translucent-hover > div > span > span.ds-text-title-xs.ds-font-bold.ds-capitalize").text
    first_round_table_batting = driver.find_element(By.CSS_SELECTOR, r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div.ds-w-full.ds-bg-fill-content-prime.ds-overflow-hidden.ds-border-line.ds-mb-2.ds-border > div.ds-p-0 > table.ds-w-full.ds-table.ds-table-xs.ds-table-auto.ci-scorecard-table")
    first_round_table_bowling = driver.find_element(By.CSS_SELECTOR, r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div.ds-w-full.ds-bg-fill-content-prime.ds-overflow-hidden.ds-border-line.ds-mb-2.ds-border > div.ds-p-0 > table:nth-child(2)")
    second_round_table_title = driver.find_element(By.CSS_SELECTOR, r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(3) > div > div.ds-flex.ds-px-4.ds-border-b.ds-border-line.ds-py-3.ds-bg-ui-fill-translucent-hover > div > span > span.ds-text-title-xs.ds-font-bold.ds-capitalize").text
    second_round_table_batting = driver.find_element(By.CSS_SELECTOR, r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(3) > div > div.ds-p-0 > table.ds-w-full.ds-table.ds-table-xs.ds-table-auto.ci-scorecard-table")
    second_round_table_bowling = driver.find_element(By.CSS_SELECTOR, r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(3) > div > div.ds-p-0 > table:nth-child(2)")
    second_round_table_bowling.text

    if"bangladesh" in first_round_table_title.lower():
        if "bangladesh" in second_round_table_title.lower(): print("mindfuck at", url)
        bd_batting_table = pd.read_html(StringIO(first_round_table_batting.get_attribute('outerHTML')))[0]
        bd_bowling_table = pd.read_html(StringIO(second_round_table_bowling.get_attribute('outerHTML')))[0]
    elif" bangladesh" in second_round_table_title.lower():
        bd_batting_table = pd.read_html(StringIO(second_round_table_batting.get_attribute('outerHTML')))[0]
        bd_bowling_table = pd.read_html(StringIO(first_round_table_bowling.get_attribute('outerHTML')))[0]
    else:
        print("error finding tables ", url)
    
    bd_batting_table = bd_batting_table[['Batting', 'R', 'B', 'M', '4s', '6s', 'SR']]
    bd_bowling_table = bd_bowling_table[['Bowling', 'O', 'M', 'R', 'W', 'ECON']]
    # remove bs
    bd_batting_table = bd_batting_table[ bd_batting_table['Batting']!=bd_batting_table['R']]
    bd_bowling_table = bd_bowling_table[ bd_bowling_table['Bowling'] != bd_bowling_table['O']]

    #finding captain:
    found_captain = False
    for batter in bd_batting_table['Batting'].tolist():
        if '(c)' in batter: found_captain = True
    if not found_captain: print("captain not found in batsmen")


    match_details_table = driver.find_element(By.CSS_SELECTOR,
    r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(7) > div.ds-p-0 > table")

    print(
        f"""
        {match_title = }
        {short_desc = }
        {summary_result = }
        {first_round_table_title = }
        {second_round_table_title = }
        """
    )
else: 
    print(
        f"""
        Match Cancello
        {match_title = }
        {short_desc = }
        {summary_result = }
        """
    )