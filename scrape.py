from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import Dict, List

def extract_info(url: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Extracts information from a webpage.

    Args:
        url (str): The URL of the webpage to extract information from.

    Returns:
        dict: A dictionary containing extracted information.
              The keys are 'bar_info' and 'status_texts'.
              'bar_info' is a list of dictionaries, each containing 'width' and 'rgb' values.
              'status_texts' is a list of strings representing status texts.
    """
    # Configure Chrome options for headless mode
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        # Use WebDriver to navigate to the URL
        driver.get(url)

        # Wait for the dynamic content to load
        driver.implicitly_wait(10)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find elements and extract information as needed
        bar_divs = soup.find_all("div", class_="bar")
        status_divs = soup.find_all("div", class_="status_text")

        # Extract width and rgb for each bar div
        bar_info = []
        for i, bar_div in enumerate(bar_divs):
            style = bar_div.get("style")
            width = style.split(';')[0].split(':')[1].strip()
            rgb = style.split('rgb')[1].split(')')[0].strip('()')
            bar_info.append({"width": width, "rgb": rgb, "index": i})  # Add index

        # Extract text from each status_div
        status_texts = []
        for i, status_div in enumerate(status_divs):
            status_texts.append({"text": status_div.text.strip(), "index": i})  # Add index

        # Sort both lists based on index to ensure consistent order
        bar_info.sort(key=lambda x: x["index"])
        status_texts.sort(key=lambda x: x["index"])


        # Remove index information
        bar_info = [{"width": info["width"], "rgb": info["rgb"]} for info in bar_info]
        status_texts = [info["text"] for info in status_texts]

        return {"bar_info": bar_info, "status_texts": status_texts}

    finally:
        # Close the WebDriver instance
        driver.quit()


# Example usage:
# url = "https://www.bouldershabitat.de/"
# extracted_info = extract_info(url)
# print(extracted_info)

import schedule
import time
from datetime import datetime
import json

def extract_info_and_append_to_file(url: str, filename: str) -> None:
    """
    Extracts information from a webpage and appends it to a file.

    Args:
        url (str): The URL of the webpage to extract information from.
        filename (str): The name of the file to append the extracted information to.
    """
    extracted_info = extract_info(url)
    with open(filename, 'a') as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp}: {json.dumps(extracted_info)}\n")

# Schedule the extraction and appending task to run every 5 minutes
url = "https://www.bouldershabitat.de/"
filename = "extracted_info.log"
schedule.every(5).minutes.do(extract_info_and_append_to_file, url, filename)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)  # Wait for 1 second before checking for scheduled tasks again
                                                                        
