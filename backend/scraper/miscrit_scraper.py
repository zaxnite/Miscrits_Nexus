import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def stat_calc(stat: int) -> int:
    """Calculate stat value based on amber count"""
    stat = str(stat)
    count = 5 - stat.count("amber")
    return count


def convert_status_effects(effect_string: str) -> str:
    """
    Convert abbreviated status effects to their full forms
    Returns 'None' for empty/null values
    """
    if not effect_string or effect_string.strip() == "" or effect_string.lower() == "none":
        return "None"
        
    replacements = {
        "Hot": "Heal over Time",
        "Dot": "Damage over Time", 
        "SI": "Sleep Immunity",
        "CI": "Confuse Immunity",
        "PI": "Paralyze Immunity",
        "A I": "Antiheal Immunity"
    }
    
    effects = effect_string.split(",")
    converted = []
    
    for effect in effects:
        effect = effect.strip()
        if effect in replacements:
            converted.append(replacements[effect])
        else:
            converted.append(effect)
            
    return ", ".join(converted) if converted else "None"


def miscrit_info(miscrit_page: int) -> dict:
    """
    Scrape miscrit information from the website
    Returns a dictionary containing all miscrit data
    """
    driver = None 

    try:
        # Initialize WebDriver
        driver = webdriver.Chrome()
        print("Chrome WebDriver initialized successfully for scanning.")

        target_url = f"https://www.worldofmiscrits.com/miscripedia/{miscrit_page}"
        print(f"Checking: {target_url}")

        try:
            # Navigate and parse page
            driver.get(target_url)
            time.sleep(0.4)  # Wait for SPA to load
            
            # Parse HTML
            full_page_html = driver.page_source
            soup_whole = BeautifulSoup(full_page_html, 'lxml')
            soup = soup_whole.find('div', class_="absolute inset-0 flex flex-col md:flex-row px-3 md:px-16 lg:px-24 pt-20")
            
            if not soup:
                print(f"    Page structure not found for {target_url}")
                return None
            
            # Basic Information
            miscrit_name = soup.find('h2', class_="text-2xl md:text-3xl lg:text-4xl font-boris text-miscrits-brown").get_text()
            miscrit_rarity = soup.find('p', class_="text-lg font-bold").get_text()
            
            # Image Processing
            img_class = "max-w-full max-h-[180px] h-auto w-auto object-contain pixelated"
            img_tag = soup.find('img', class_=img_class)
            miscrit_image = img_tag['src'].split("miscrits/")[-1] if img_tag and img_tag.has_attr('src') else None
            
            # Status Effects
            status_spans = soup.find_all('span', class_="px-2 py-1 bg-miscrits-yellow/20 text-miscrits-yellow text-xs rounded-full border border-miscrits-yellow/30")
            effects = [span.get_text(strip=True) for span in status_spans]
            miscrit_effect = convert_status_effects(",".join(effects) if effects else "None")
            
            # Type and Location
            misc_spans = soup.find_all('span', class_="text-sm text-miscrits-brown")
            miscrit_type = str(misc_spans[0].get_text()).replace(' / ', '/')
            miscrit_location = misc_spans[1].get_text()
            
            # Evolution Information
            evo_spans = soup.find_all('span', class_='text-xs text-center text-miscrits-yellow mt-1 w-full truncate')
            miscrit_evolutions = '/'.join([evo_spans[i].get_text() for i in range(4)])
            
            # Stats Calculation
            stat_divs = soup.find_all('div', class_="flex justify-start")
            stats = {
                "Health": stat_calc(stat_divs[0]),
                "Speed": stat_calc(stat_divs[1]),
                "Elemental Attack": stat_calc(stat_divs[2]),
                "Elemental Defense": stat_calc(stat_divs[3]),
                "Physical Attack": stat_calc(stat_divs[4]),
                "Physical Defense": stat_calc(stat_divs[5])
            }
            
            # Abilities
            ability_spans = soup.find_all('span', class_="text-sm text-miscrits-brown overflow-wrap-anywhere")
            miscrit_abilities = [span.get_text() for span in ability_spans]

            # Compile all data
            miscrit_data = {
                "Miscrit_ID": miscrit_page,
                "Name": miscrit_name,
                "Rarity": miscrit_rarity,
                "Location": miscrit_location,
                "Type": miscrit_type,
                "Evolutions": miscrit_evolutions,
                "Health": stats["Health"],
                "Speed": stats["Speed"],
                "Elemental Attack": stats["Elemental Attack"],
                "Elemental Defense": stats["Elemental Defense"],
                "Physical Attack": stats["Physical Attack"],
                "Physical Defense": stats["Physical Defense"],
                "Abilities": miscrit_abilities,
                "Status Effects": miscrit_effect,
                "Image_Name": miscrit_image
            }
            
            return miscrit_data

        except Exception as inner_e:
            print(f"    Error processing {target_url}: {inner_e}")
            return None
            
    except Exception as outer_e:
        print(f"An unexpected error occurred during WebDriver initialization or loop: {outer_e}")
        return None
        
    finally:
        if driver:
            driver.quit()
            print("\nBrowser closed after scan.")


if __name__ == "__main__":
    print(miscrit_info(556))