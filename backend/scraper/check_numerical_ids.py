import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from text_to_file import append_list_to_file


def find_working_miscripedia_indices(start_id: int, end_id: int) -> list[int]:
    """
    Checks a range of numerical Miscripedia routes for valid pages and collects their IDs.
    Initializes and quits the WebDriver once for efficiency.

    Args:
        start_id (int): The starting Miscrit ID to check (inclusive).
        end_id (int): The ending Miscrit ID to check (exclusive, if using range).

    Returns:
        list[int]: A list of Miscrit IDs for which a valid page was found.
    """

    driver = None # Initialize driver to None for the outer try/finally
    working_index = [] # List to store valid Miscrit IDs

    try:
        driver = webdriver.Chrome()
        print("Chrome WebDriver initialized successfully for scanning.")

        for x in range(start_id, end_id): # Loop through the specified range
            target_url = f"https://www.worldofmiscrits.com/miscripedia/{x}"
            print(f"Checking: {target_url}")

            try:
                # Navigate to the URL
                driver.get(target_url)

                
                time.sleep(0.2) # Increased sleep for robustness for SPAs

                full_page_html = driver.page_source
                soup = BeautifulSoup(full_page_html, 'lxml')

            
                not_found_h1 = soup.find('h1', string='Miscrit Not Found')

        
                miscrit_name_h2 = soup.find('h2', class_="text-2xl md:text-3xl lg:text-4xl font-boris text-miscrits-brown")


                # If a Miscrit name H1 is found AND the "Not Found" H1 is NOT found
                if miscrit_name_h2 and not not_found_h1:
                    print(f"    ID {x}: Page EXISTS! Miscrit Name: {miscrit_name_h2.text.strip()}")
                    working_index.append(x)
            except Exception as inner_e:
                print(f"    Error processing {target_url}: {inner_e}")
                # Continue to the next URL even if one fails
            time.sleep(0.2) # Small delay between requests for politeness

    except Exception as outer_e:
        print(f"An unexpected error occurred during WebDriver initialization or loop: {outer_e}")
    finally:
        if driver:
            driver.quit()
            print("\nBrowser closed after scan.")

    return working_index

if __name__ == "__main__":
    start_time = time.time()
    scan_start = 1
    scan_end = 570

    found_miscrit_ids = find_working_miscripedia_indices(scan_start, scan_end)

    if found_miscrit_ids:
        print(f"\n--- Scan Complete ---")
        print(f"Found {len(found_miscrit_ids)} working Miscripedia IDs:")
        append_list_to_file(found_miscrit_ids,"miscrit_id.txt","data")

    else:
        print("\nNo working Miscripedia IDs found in the specified range.")

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")

