# UPWORK WEB SCRAPING PORTFOLIO

This repository is destinated to future upwork clients with the purpose of gather all my personal python web scraping projects in one place.

## PROJECT 01 - POKEMON GO WEB SCRAPING USING PYTHON

This project consists of a python script that is capable of scrape data from a list of links.

The website choose to be scraped was the following -> [Pokemon go wiki - fandom](https://pokemongo.fandom.com/wiki/)

Firstly a function called "link_scraper" scans the website and returns the list of links relative to each pokemon. This list is used as input parameter by the function called "info_scraper" where all available information about each pokemon is scraped. So, the scraping part of the script is a two step process and a json file is saved as a result by the function "save_json".

![Code overview](https://github.com/fcastro25/upwork_web_scraping_portfolio/blob/main/01.PNG)
Code overview

![Terminal when code is running](https://github.com/fcastro25/upwork_web_scraping_portfolio/blob/main/02.PNG)
Terminal when code is running

![Excerpt from json file of scraped data](https://github.com/fcastro25/upwork_web_scraping_portfolio/blob/main/03.PNG)
Excerpt from json file of scraped data
