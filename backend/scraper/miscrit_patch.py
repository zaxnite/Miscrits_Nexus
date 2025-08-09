import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def miscrit_patch_scraper():
    results = []
    driver = None
    miscrits_patched = []
    try:
        # Setup Chrome driver
        driver = webdriver.Chrome()
        driver.maximize_window()

        url = "https://www.worldofmiscrits.com/updates"
        print(f"Opening {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        # Wait for the "Miscrit Patches" button
        miscrit_patches_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[span[text()='Miscrit Patches']]"))
        )
        # Click to expand patches list if needed
        miscrit_patches_button.click()
        print("Miscrit Patches button clicked to expand patches list.")

        # Find container holding patch buttons
        container = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[span[text()='Miscrit Patches']]/following-sibling::div")
            )
        )

        # Get all patch buttons inside the container
        patch_buttons = container.find_elements(
            By.XPATH, ".//button[contains(@class, 'text-miscrits-yellow') and contains(@class, 'font-medium')]"
        )

        print(f"Found {len(patch_buttons)} Miscrit patch buttons inside container.")

        for button in patch_buttons:
            patch_name = button.text.strip()
            miscrits_patched.append(patch_name)
            print(f"\nClicking Miscrit patch button: {patch_name}")

            # Scroll to button and click with JS to avoid overlay issues
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)

            time.sleep(0.8)

            try:
                parent = button.find_element(By.XPATH, "./..")

                # Wait for the open content div inside this parent to be visible
                content_panel = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, ".//div[@data-state='open']"))
                )

                # Now wait for at least one <li> to appear inside the content's <ul>
                ul_element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "ul.pl-4.space-y-1.text-miscrits-green")
                    )
                )
                li_elements = WebDriverWait(driver, 2).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.pl-4.space-y-1.text-miscrits-green > li"))
                )

                patch_notes = [li.text for li in li_elements]


                results.append({"Miscrit": patch_name, "Patch_Notes": patch_notes})

            except Exception as e:
                print(f"Failed to extract patch notes for '{patch_name}': {e}")
                results.append({"Miscrit": patch_name, "Patch_Notes": None, "Error": str(e)})


        return miscrits_patched,results

    except Exception as e:
        print(f"Error in scraper: {e}")

    finally:
        if driver:
            driver.quit()
            print("\nBrowser closed after scraping.")

if __name__ == "__main__":
    patch_data,patches = miscrit_patch_scraper()
    print("\nSummary of patches scraped:")
    print(patch_data)
    print(patches[-1].get('Patch_Notes'))
