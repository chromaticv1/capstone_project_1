from pathlib import Path

required_dirs = [
    'data/raw_tables/batting',
    'data/raw_tables/bowling',
    'data/raw_tables/details',
    'data/player_tables/batting',
    'data/player_tables/bowling'
]
for dir in required_dirs:
    Path.mkdir(
        Path(dir), parents=True, exist_ok= True
    )
should_scrape_links, should_scrape_scorecards, should_do_wrangling = (False, False, True)
should_scrape_links = ('y' in input("Scrape links? y/[n]: ")) or False
should_scrape_scorecards = ('y' in input("Scrape scorecards from those links? y/[n]: ")) or False
should_do_wrangling = ('y' in input("Wrangle scraped data? y/[n]: ")) or True

if should_scrape_links:
    from src import scrape_links
if should_scrape_scorecards:
    from src import scorecard_scraper
if should_do_wrangling:
    from src import match_stats_wrangler
    from src import player_stats_wrangler
    from src import tableau_wrangler