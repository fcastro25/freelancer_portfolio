# MY FREELANCER PORTFOLIO

This page aims to serve as a portfolio for projects made by me. These projects serve as evidence of my expertise in the areas I work in.

## WEB SCRAPING PROJECTS

### PROJECT 01 - POKEMON GO WEB SCRAPING USING PYTHON

This project consists of a Python script capable of scraping data from a list of links using the BeautifulSoup library.

The chosen website to be scraped was the following -> [Pokemon go wiki - fandom](https://pokemongo.fandom.com/wiki/)

1. Firstly, a function named **link_scraper** scans the website and retrieves the list of links associated with each Pokémon;
2. This list of links serves as an input parameter for the function named **info_scraper**;
3. Within the **info_scraper** function, all available information about each Pokémon is scraped from the respective links;
4. Finally, the function **save_json** saves the scraped data as a JSON file.

<details>
  <summary> <b> Project prints... </b> <i>(click to expand!)</i> </summary>
  <br>

![Code overview](https://github.com/fcastro25/upwork_web_scraping_portfolio/blob/main/01.PNG)
Code overview

![Terminal when code is running](https://github.com/fcastro25/upwork_web_scraping_portfolio/blob/main/02.PNG)
Terminal when code is running

![Excerpt from json file of scraped data](https://github.com/fcastro25/upwork_web_scraping_portfolio/blob/main/03.PNG)
Excerpt from json file of scraped data

---
  
</details>
