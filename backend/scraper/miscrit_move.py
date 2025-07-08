from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def parse_moves(lines: list[str]) -> dict:
    info = {"Name": lines[0]}
    i = 1
    try:
        if lines[i] == "AP:":
            info["Element"] = "Utility"
            info["AP"] = 0
            info["Accuracy"] = lines[i+3]
            info["Description"] = lines[i+4]
            if len(lines) > i+6:
                info["Enchant"] = lines[i+6]
        else:
            info["Element"] = lines[i]
            info["AP"] = lines[i+2]
            info["Accuracy"] = lines[i+4]
            info["Description"] = lines[i+5]
            if len(lines) > i+7:
                info["Enchant"] = lines[i+7]
    except IndexError:
        info["Error"] = "Tooltip structure incomplete"
    return info

def scrape_moves_info(miscrit_id: int, moves: list[str]) -> list[dict]:
    """
    Extracts tooltip info for a list of move names from a Miscrit Miscripedia page.

    Args:
        miscrit_id (int): Miscripedia page ID.
        moves (list[str]): List of move image alt texts.

    Returns:
        list[dict]: List of move data dictionaries (each with Miscrit_ID as first key).
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)
    results = []

    try:
        driver.get(f"https://www.worldofmiscrits.com/miscripedia/{miscrit_id}")
        time.sleep(3)
        move_links = driver.find_elements(By.CSS_SELECTOR, "a.hover\\:bg-amber-800\\/10")

        for alt in moves:
            move_found = False
            for move in move_links:
                try:
                    img = move.find_element(By.TAG_NAME, "img")
                    if img.get_attribute("alt") == alt:
                        actions.move_to_element(move).perform()
                        time.sleep(0.5)

                        tooltip = wait.until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-state='open'] div.space-y-2"))
                        )
                        lines = tooltip.text.strip().splitlines()
                        parsed = parse_moves(lines)
                        move_data = {"Miscrit_ID": miscrit_id,"Move_Name":alt, **parsed}  # Miscrit_ID comes first
                        results.append(move_data)
                        move_found = True
                        break
                except Exception:
                    continue
            if not move_found:
                results.append({
                    "Miscrit_ID": miscrit_id,
                    "Name": alt,
                    "Error": "Move not found"
                })

        return results

    except Exception as e:
        print(f"Error while scraping moves for Miscrit {miscrit_id}: {e}")
        return []
    finally:
        driver.quit()

