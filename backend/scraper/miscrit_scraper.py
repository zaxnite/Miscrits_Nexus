import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def stat_calc (stat: int) -> int:
    stat = str(stat)
    count = 5 - stat.count("amber")
    return count


def miscrit_info (miscrit_page: int) -> dict:


    driver = None 

    try:
        driver = webdriver.Chrome()
        print("Chrome WebDriver initialized successfully for scanning.")

        # for x in (miscrit_ids): # Loop through the specified range
        target_url = f"https://www.worldofmiscrits.com/miscripedia/{miscrit_page}"
        print(f"Checking: {target_url}")

        try:
            # Navigate to the URL
            driver.get(target_url)

            
            time.sleep(0.4) # Increased sleep for robustness for SPAs

            full_page_html = driver.page_source
            soup_whole = BeautifulSoup(full_page_html, 'lxml')
            soup = soup_whole.find('div',class_="absolute inset-0 flex flex-col md:flex-row px-3 md:px-16 lg:px-24 pt-20")
    
            miscrit_name_h2 = soup.find('h2', class_="text-2xl md:text-3xl lg:text-4xl font-boris text-miscrits-brown")
            miscrit_rarity = soup.find('p',class_ = "text-lg font-bold")
            img_class = "max-w-full max-h-[180px] h-auto w-auto object-contain pixelated"
            img_tag = soup.find('img', class_=img_class)
            if img_tag and img_tag.has_attr('src'):
                full_src = img_tag['src']
                # Extract part after 'miscrits/' in the URL
                miscrit_image = full_src.split("miscrits/")[-1]
            else:
                miscrit_image = None
            spans = soup.find_all('span', class_="px-2 py-1 bg-miscrits-yellow/20 text-miscrits-yellow text-xs rounded-full border border-miscrits-yellow/30")
            effects = [span.get_text(strip=True) for span in spans]
            miscrit_effect = effects if effects else ["None"]
            miscrit_location = soup.find_all('span',class_="text-sm text-miscrits-brown")[1]
            miscrit_type_html = soup.find_all('span',class_="text-sm text-miscrits-brown")[0]
            miscrit_type = str(miscrit_type_html.get_text())
            miscrit_abilities_unformated = soup.find_all('span',class_="text-sm text-miscrits-brown overflow-wrap-anywhere")
            miscrit_evos = soup.find_all('span',class_='text-xs text-center text-miscrits-yellow mt-1 w-full truncate')
            miscrit_evo_list = []
            for i in range(0,4):
                miscrit_evo_list.append(miscrit_evos[i].get_text())
            miscrit_evolutions = '/'.join(miscrit_evo_list)
            miscrit_health = stat_calc(soup.find_all('div',class_="flex justify-start")[0])
            miscrit_speed = stat_calc(soup.find_all('div',class_="flex justify-start")[1])
            miscrit_ea = stat_calc(soup.find_all('div',class_="flex justify-start")[2])
            miscrit_ed = stat_calc(soup.find_all('div',class_="flex justify-start")[3])
            miscrit_pa = stat_calc(soup.find_all('div',class_="flex justify-start")[4])
            miscrit_pd = stat_calc(soup.find_all('div',class_="flex justify-start")[5])
            miscrit_abilities = []
            for i in range (0,len(miscrit_abilities_unformated)):
                miscrit_abilities.append(miscrit_abilities_unformated[i].get_text())

            miscrit_data = {"Miscrit_ID":miscrit_page,"Name": miscrit_name_h2.get_text(), "Rarity":miscrit_rarity.get_text(),"Location":miscrit_location.get_text(),"Type":miscrit_type.replace(' / ', '/'),"Evolutions":miscrit_evolutions,
                            "Health":miscrit_health,"Speed":miscrit_speed,"Elemental Attack":miscrit_ea,"Elemental Defense":miscrit_ed,"Physical Attack":miscrit_pa,"Physical Defense":miscrit_pd,"Abilities":miscrit_abilities, "Image": miscrit_image,'Status Effect': miscrit_effect}
            return(miscrit_data)
        except Exception as inner_e:
            print(f"    Error processing {target_url}: {inner_e}")
            
            
    except Exception as outer_e:
        print(f"An unexpected error occurred during WebDriver initialization or loop: {outer_e}")
        
    finally:
        if driver:
            driver.quit()
            print("\nBrowser closed after scan.")

if __name__ == "__main__":
    print(miscrit_info(201))