# Project Apartment

Well, I finally need to buy an apartment... This repository will contain tools that will hopefully help me achieve that.

Problems to solve:

1. Missing data that is relevant to me, like:
    - How far is the nearest metro station
    - How far is the city center
    - How far is my workplace
    - How long would it take me to get to work by public transport
    - How long would it take me to get to the city center by public transport
    - Distance to the nearest park
2. Inaccurate/Vague addresses
3. Duplicates
    - same apartment listed multiple times on a single site
    - same apartment listed across various sites

## Plan

1. Start with scraping [otodom.pl](https://www.otodom.pl) using [scrapy](https://scrapy.org/)
2. Deploy the scraper to [scrapinghub.com](https://scrapinghub.com)
3. Figure out how to extract lat/long locations
4. Try out some simple de-duplication methods
5. See if we can improve address accuracy by looking at duplicates
6. Create a pipeline with post-processors, adding metadata, eg. distance/travel time to the city center
7. Add more scrapers
8. Try to sort offers by my preferences
