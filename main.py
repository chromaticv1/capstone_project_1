import os
if 'data' not in os.listdir(): os.mkdir('data')
if 'raw_tables' not in os.listdir('data'): os.mkdir('data/raw_tables')
if 'batting' not in os.listdir('data/raw_tables/'): os.mkdir('data/raw_tables/batting')
if 'bowling' not in os.listdir('data/raw_tables/'): os.mkdir('data/raw_tables/bowling')
if 'details' not in os.listdir('data/raw_tables/'): os.mkdir('data/raw_tables/details')
from src import scrape_links
from src import scorecard_scraper
from src import match_stats_wrangler