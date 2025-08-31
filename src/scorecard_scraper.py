# coding: utf-8
import pandas as pd
from selenium import webdriver
import time
from tabulate import tabulate
from selenium.webdriver.common.by import By
from tqdm import tqdm
from io import StringIO
from pprint import pprint
import numpy as np

match_links_df = pd.read_csv('./data/match_links.csv')

def scrape(url):
    
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
            bd_batting_table = pd.read_html(StringIO(first_round_table_batting.get_attribute('outerHTML')))[0]
            bd_bowling_table = pd.read_html(StringIO(second_round_table_bowling.get_attribute('outerHTML')))[0]
        elif"bangladesh" in second_round_table_title.lower():
            bd_batting_table = pd.read_html(StringIO(second_round_table_batting.get_attribute('outerHTML')))[0]
            bd_bowling_table = pd.read_html(StringIO(first_round_table_bowling.get_attribute('outerHTML')))[0]
        
        bd_batting_table = bd_batting_table[['Batting', 'R', 'B', 'M', '4s', '6s', 'SR']]
        bd_bowling_table = bd_bowling_table[['Bowling', 'O', 'M', 'R', 'W', 'ECON']]
        # remove bs
        bd_batting_table = bd_batting_table[ bd_batting_table['Batting']!=bd_batting_table['R']]
        bd_bowling_table = bd_bowling_table[ bd_bowling_table['Bowling'] != bd_bowling_table['O']]

        #finding captain:
        found_captain = False
        captain = ''
        for batter in bd_batting_table['Batting'].tolist():
            if '(c)' in batter:
                found_captain = True
                captain = batter
        if not found_captain: print("captain not found in batsmen")


        match_details_table = driver.find_element(By.CSS_SELECTOR,
        r"#main-container > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(7) > div.ds-p-0 > table")
        
        match_details_table = pd.read_html(StringIO(match_details_table.get_attribute('outerHTML')))[0]
        md_keys = match_details_table[0].tolist()
        md_values = match_details_table[1].tolist()
        venue = md_values[0]
        details_record = {}
        for i in range(len(md_keys)):
            if i == 0: continue
            details_record[md_keys[i]]=md_values[i]
        details_table = pd.DataFrame([details_record])
        # print(
        #     f"""
        #     {match_title = }
        #     {short_desc = }
        #     {summary_result = }
        #     {venue = }
        #     {first_round_table_title = }
        #     {second_round_table_title = }
        #     {captain = }
        #     """
        # )
        output = {
            'match_title':match_title,
            'short_desc':short_desc,
            'summary_result':summary_result,
            'venue': venue,
            'bd_captain': captain,
            'batting': bd_batting_table,
            'bowling': bd_bowling_table,
            'details': details_table
        }
    else: 
        # print(
        #     f"""
        #     Match Cancello
        #     {match_title = }
        #     {short_desc = }
        #     {summary_result = }
        #     """
        # )
        output = {
            'match_title':match_title,
            'short_desc':short_desc,
            'summary_result':summary_result,
        }
    
    return output

driver = webdriver.Chrome()
driver.implicitly_wait(5)
urls = match_links_df.iloc[:,-1].tolist()
successful, failed = (0,0)
failed_list = []
raw_match_stat_list = []
raw_tables_path = 'data/raw_tables/'
for i, url in tqdm(enumerate(urls), bar_format="{n_fmt}/{total_fmt} [{elapsed}]"):
    
    try:
        raw_match_stats = scrape(url)
        if 'won' in raw_match_stats['summary_result']:
            batting_table_path = f'{raw_tables_path}batting/{i}.csv'
            bowling_table_path = f'{raw_tables_path}bowling/{i}.csv'
            details_table_path = f'{raw_tables_path}details/{i}.csv'
            raw_match_stats['batting'].to_csv(batting_table_path, index=False)
            raw_match_stats['bowling'].to_csv(bowling_table_path, index=False)
            raw_match_stats['details'].to_csv(details_table_path, index=False)
            raw_match_stats['batting'] =batting_table_path
            raw_match_stats['bowling'] = bowling_table_path
            raw_match_stats['details'] = details_table_path
        raw_match_stats['url'] = url
        raw_match_stat_list.append(
            raw_match_stats
        )
        successful += 1
    except:
        print('error in: ',i,    url)
        failed += 1
        failed_list.append(
            {'link':url, 'index': i}
        )

pd.DataFrame(raw_match_stat_list).to_csv('data/raw_match_stats.csv')
print(
    f"""
    {successful = }
    {failed = }
    """
)
driver.quit()
pd.DataFrame(failed_list).to_csv('data/failed_list.csv',
index=False)

