from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


def is_captcha_present(driver):
    try:
        # Look for common CAPTCHA markers
        # Example 1: iframe with title
        driver.find_element(By.XPATH, "//iframe[contains(@title, 'not a robot')]")
        return True
    except:
        pass

    try:
        # Example 2: div with common captcha class
        driver.find_element(By.XPATH, "//*[contains(@class, 'captcha')]")
        return True
    except:
        pass

    try:
        # Example 3: Consent/Captcha warning text
        if "not a robot" in driver.page_source.lower() or "captcha" in driver.page_source.lower():
            return True
    except:
        pass

    return False


def get_papers_from_google_scholar(website_url):
    website = website_url
    path = r"D:\\_F_drive\\study_material\\machine_learning\\Practice\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # chrome_options.add_argument()
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(website)
    time.sleep(5)  # Wait for the page to load

    
    if is_captcha_present(driver):
        print("⚠️ CAPTCHA detected. Waiting for it to be solved manually...")
        while is_captcha_present(driver):
            print("⏳ Still detecting CAPTCHA...waiting 5 seconds.")
            time.sleep(5)
        print("✅ CAPTCHA solved. Continuing script.")
    else:
        print("✅ No CAPTCHA detected. Proceeding...")
    # driver.maximize_window()


    cookies = driver.get_cookies()
    driver.quit()

    # Step 3: Reopen browser in headless mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size for consistent rendering
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Reload the page (CAPTCHA should already be solved in most cases)
    driver.get(website)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(website)  # Reload the page with cookies


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[@class='gsc_a_t']"))
    )

    researcher_name = driver.find_element(By.XPATH, "//div[@id='gsc_prf_in']").text
    print("Researcher Name:", researcher_name)

    papers = driver.find_elements(By.XPATH, "//td[@class='gsc_a_t']")
    paper_count = 20 if len(papers) > 20 else len(papers)

    titles = []
    authors = []
    journals = []
    abstracts = []
    years = []

    for index in range(paper_count):
        try:
            paper = driver.find_elements(By.XPATH, "//td[@class='gsc_a_t']")[index]
            print(f"Processing paper {index + 1}/{paper_count}...")
            title_elem = paper.find_element(By.XPATH, "./a[@class='gsc_a_at']")
            titles.append(title_elem.text)
            years.append(paper.find_element(By.XPATH, "//span[@class='gsc_a_h gsc_a_hc gs_ibl']").text)
            authors.append(paper.find_element(By.XPATH, "./div[1]").text)
            journals.append(paper.find_element(By.XPATH, "./div[2]").text)

            title_elem.click()
            time.sleep(1)

            try:
                abstract_elem = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "gsh_csp"))
                )
                abstracts.append(abstract_elem.text)
            except:
                abstracts.append("No abstract/snippet available")

            # Close popup
            close_button = driver.find_element(By.XPATH, "//a[@id='gs_hdr_bck']")
            close_button.click()
            time.sleep(1)

        except Exception as e:
            print(f"❌ Error at index {index}: {e}")
            titles.append("Error")
            authors.append("Error")
            years.append("Error")
            journals.append("Error")
            abstracts.append("Error")

    print(f"\n✅ Total papers processed: {len(titles)}")

    print(len(titles), "papers found.")
    print(len(authors), "authors found.")
    print(len(journals), "journals found.")
    print(len(years), "years found.")
    print(len(abstracts), "abstracts found.")

    print(driver.title)



    print(f"\n✅ Total papers processed: {len(titles)}")

    driver.quit()  # Optional cleanup

    papers_df = pd.DataFrame({
        "Title": titles,
        "Years": years,
        "Abstract": abstracts
    })

    # papers_df.to_csv("web_scrap_google_scholar_papers_"+researcher_name+".csv", index=False)
    return papers_df, researcher_name


if __name__ == "__main__":
    # Example usage
    url = "https://scholar.google.com/citations?user=pp_w84AAAAAJ&hl=en&oi=ao"
    papers_df = get_papers_from_google_scholar(url)
    print(papers_df.head())