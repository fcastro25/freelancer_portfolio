from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json

#set webdriver via selenium
def define_webdriver_using_selenium(link, hide=True, window_size=(800, 800), waiting_time=3):
    options = Options()
    size_string = f'window-size={str(window_size[0])},{str(window_size[1])}'
    options.add_argument(size_string)
    if hide:
        options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
    driver.get(link)
    sleep(waiting_time)

    return driver

#return the "soup" or html content of the website
def scrape_data(link, use_selenium=False):
    if use_selenium:
        driver = define_webdriver_using_selenium(link)
        soup = BeautifulSoup(driver.page_source, 'lxml')
    else:
        soup = BeautifulSoup(requests.get(link).text, "lxml")
    return soup

#get links from all debut pokemon of available regions
def link_scraper(url):
    region_sufix = ["Pokémon_from_Kanto_region",
                    "Pokémon_from_Johto_region",
                    "Pokémon_from_Hoenn_region",
                    "Pokémon_from_Sinnoh_region",
                    "Pokémon_from_Unova_region",
                    "Pokémon_from_Kalos_region",
                    "Pokémon_from_Galar_region"]
    link_ = {}
    for region in region_sufix:
        link = f'{url}Category:{region}'
        soup = scrape_data(link)
        category_page = soup.find("div",{"class":"category-page__members"})
        region_key = region.split(sep='_')[2]
        keys = []
        values = []
        for pokemon in category_page.findAll("div",{"class":"category-page__member-left"}):
            current_pokemon = pokemon.find("a").get("title")
            keys.append(current_pokemon)
            values.append(url + current_pokemon)
        link_[region_key] = dict(zip(keys, values))
    print("-------------------------")
    print("All links scraped!")
    print("-------------------------")
    return link_

def remove_thousand_separator(string):
    if len(string.split(sep=',')) == 2:
        left_part = string.split(sep=',')[0]
        right_part = string.split(sep=',')[-1]
        temp_string = left_part + right_part
    else:
        temp_string = string
    return int(temp_string)

def get_cps(soup):
    cp_stats = soup.find("td",{"data-source":"cp"}).text
    cp_level_1 = remove_thousand_separator(cp_stats.split(sep=' - ')[0])
    cp_level_40 = remove_thousand_separator(cp_stats.split(sep=' - ')[-1].split(sep=' ')[0])
    cp_level_40_wb = remove_thousand_separator(cp_stats.split(sep=' - ')[-1].split(sep='Level 50')[0].split(sep=' ')[-1])
    cp_level_50 = remove_thousand_separator(cp_stats.split(sep=' - ')[-1].split(sep='Level 50:')[-1].split(sep=' ')[0])
    cp_level_50_wb = remove_thousand_separator(cp_stats.split(sep=' - ')[-1].split(sep='Level 50')[-1].split(sep=' ')[-1])

    return cp_level_1, cp_level_40, cp_level_40_wb, cp_level_50, cp_level_50_wb

def get_hps(soup):
    hp_stats = soup.find("td",{"data-source":"hp"}).text
    hp_level_1 = remove_thousand_separator(hp_stats.split(sep=' - ')[0])
    hp_level_40 = remove_thousand_separator(hp_stats.split(sep=' - ')[-1].split(sep=' ')[0])
    hp_level_40_wb = remove_thousand_separator(hp_stats.split(sep=' - ')[-1].split(sep='Level 50')[0].split(sep=' ')[-1])
    hp_level_50 = remove_thousand_separator(hp_stats.split(sep=' - ')[-1].split(sep='Level 50:')[-1].split(sep=' ')[0])
    hp_level_50_wb = remove_thousand_separator(hp_stats.split(sep=' - ')[-1].split(sep='Level 50')[-1].split(sep=' ')[-1])

    return hp_level_1, hp_level_40, hp_level_40_wb, hp_level_50, hp_level_50_wb

def get_fast_attacks(soup,pokemon_types,pokemon_info,region,pokemon):
    pokemon_info[region][pokemon]["fast_attacks"] = {}
    for t in pokemon_types:
        current_type = "pogo-attack-item type-" + t
        s = soup.findAll("div",{"class":current_type})
        for attacks in s:
            if attacks and not attacks.findAll("div")[1].find("div"):
                fast_attack_name = attacks.findAll("div")[1].find("a").text
                fast_attack_damage = int(attacks.find("span",{"title":"Damage"}).text)
                fast_attack_dps = int(attacks.find("span",{"title":"DPS"}).text.split(sep='(')[-1].split(sep=')')[0])
                pokemon_info[region][pokemon]["fast_attacks"][t] = {"name": fast_attack_name,
                                                                    "damage": fast_attack_damage,
                                                                    "dps": fast_attack_dps}

def get_charged_attacks(soup,pokemon_types,pokemon_info,region,pokemon):
    pokemon_info[region][pokemon]["charged_attacks"] = {}
    for t in pokemon_types:
        current_type = "pogo-attack-item type-" + t
        s = soup.findAll("div",{"class":current_type})
        for attacks in s:
            if attacks and attacks.findAll("div")[1].find("div"):
                charged_attack_name = attacks.findAll("div")[1].find("a").text
                charged_attack_damage = int(attacks.find("span",{"title":"Damage"}).text)
                charged_attack_dps = int(attacks.find("span",{"title":"DPS"}).text.split(sep='(')[-1].split(sep=')')[0])
                charged_attack_bars = len(attacks.findAll("div")[1].findAll("div"))
                pokemon_info[region][pokemon]["charged_attacks"][t] = {"name": charged_attack_name,
                                                                    "damage": charged_attack_damage,
                                                                    "dps": charged_attack_dps,
                                                                    "bars":charged_attack_bars}

#pokemon info scraper
def info_scraper(link_map):
    region = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Galar"]
    pokemon_types = ["Bug","Dark","Dragon","Electric","Fairy","Fighting","Fire","Flying","Ghost","Grass","Ground","Ice","Normal","Poison","Psychic","Rock","Steel","Water"]
    pokemon_info = {}
    for region in region:
        pokemon_info[region] = {}
        for pokemon in link_map[region]:
            pokemon_link = link_map[region][pokemon]
            soup = scrape_data(pokemon_link)
            dex_number = soup.find("div",{"class":"pogo-nav"}).find("div",{"class":"pogo-nav-item3"}).find("div",{"class":"n1"}).text
            description = soup.find("div",{"class":"pogo-dexbox-desc"}).text.replace('\n','')
            pokemon_type = soup.find("section",{"class":"pi-smart-group-body pi-border-color"}).findAll("div",{"class":"pi-smart-data-value pi-data-value pi-font pi-item-spacing pi-border-color"})
            if len(pokemon_type)==2:
                pkm_type = [pokemon_type[0].find("a").get("title"), pokemon_type[1].find("a").get("title")]
            else:
                pkm_type = [pokemon_type[0].find("a").get("title")]
            base_stats = soup.find("table",{"class":"pi-horizontal-group"}).findAll("td")
            buddy_distance = soup.find("div",{"data-source":"buddy-d"}).text
            cp_level_1, cp_level_40, cp_level_40_wb, cp_level_50, cp_level_50_wb = get_cps(soup)
            hp_level_1, hp_level_40, hp_level_40_wb, hp_level_50, hp_level_50_wb = get_hps(soup)
            pokemon_info[region][pokemon] = {"dex_number": dex_number,
                                             "description": description,
                                             "type": pkm_type,
                                             "buddy_distance": buddy_distance,
                                             "base_stats":{"attack": int(base_stats[0].text),
                                                           "defense": int(base_stats[1].text),
                                                           "stamina": int(base_stats[2].text)},
                                             "cp_stats": {"cp (level 1)": cp_level_1,
                                                          "cp (level 40)": cp_level_40,
                                                          "cp (level 40 with weather boost)": cp_level_40_wb,
                                                          "cp (level 50)": cp_level_50,
                                                          "cp (level 50 with weather boost)": cp_level_50_wb},
                                             "hp_stats": {"hp (level 1)": hp_level_1,
                                                          "hp (level 40)": hp_level_40,
                                                          "hp (level 40 with weather boost)": hp_level_40_wb,
                                                          "hp (level 50)": hp_level_50,
                                                          "hp (level 50 with weather boost)": hp_level_50_wb}}
            
            get_fast_attacks(soup,pokemon_types,pokemon_info,region,pokemon)
            get_charged_attacks(soup,pokemon_types,pokemon_info,region,pokemon)
            
            print('pokemon: ' + pokemon + ' [info scraped]')
    return pokemon_info

#exports the scraped data in a json file
def save_json(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4)

#function calls
base_url = "https://pokemongo.fandom.com/wiki/"
link_map = link_scraper(base_url)
pokemon_info = info_scraper(link_map)
save_json(pokemon_info, 'pokemon_go_db.json')