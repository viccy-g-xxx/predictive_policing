from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd

import sys, os

sys.path.append(os.getcwd())


def fetch_fir_reports(test_url, driver):

    driver.get(test_url)

    Select(
        driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$ddFIRYear")
    ).select_by_value("2019")

    Select(
        driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$ddlDistrict")
    ).select_by_value("13225")

    Select(
        driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$ddlPoliceStation")
    ).select_by_value("13225008")

    driver.find_element(
        By.XPATH,
        "//input[@name='ctl00$ContentPlaceHolder1$btnStatusSearch' and @value='Search']",
    ).click()

    tag_present = EC.presence_of_element_located((By.ID, "tblDisplayRecords"))
    wait = WebDriverWait(driver, 10)
    wait.until(tag_present)

    table_links = driver.find_elements(
        By.XPATH, '//table[@id="tblDisplayRecords"]/tbody/tr'
    )

    n = len(table_links)
    fir_texts = []
    first_page_data = []

    for index in range(n):
        print(index)

        fir = table_links[index]

        fir.find_elements(
            By.ID, f"ContentPlaceHolder1_rptDisplayRecords_lnkFIRViewDetail_{index}"
        )[0].click()

        driver.switch_to.window(driver.window_handles[1])

        tag_present = EC.presence_of_element_located(
            (By.NAME, "RptView$ctl06$ctl00$Next$ctl00$ctl00")
        )
        wait = WebDriverWait(driver, 10)
        wait.until(tag_present)

        time.sleep(2)

        first_page_content = driver.find_element(
            By.XPATH, "//td[contains(@id, 'oReportCell')]"
        ).text
        first_page_data.append(first_page_content)

        time.sleep(5)
        driver.find_element(
            By.XPATH, "//input[@name='RptView$ctl06$ctl00$Next$ctl00$ctl00']"
        ).click()

        tag_present = EC.presence_of_element_located(
            (By.XPATH, "//span[contains(@class, '556')]")
        )
        wait = WebDriverWait(driver, 10)
        wait.until(tag_present)
        time.sleep(2)

        full_fir_text = driver.find_element(
            By.XPATH, "//span[contains(@class, '556')]"
        ).text
        print(full_fir_text)

        fir_texts.append(full_fir_text)

        driver.switch_to.window(driver.window_handles[0])
        # refresh table
        table_links = driver.find_elements(
            By.XPATH, '//table[@id="tblDisplayRecords"]/tbody/tr'
        )

    return fir_texts, first_page_data


if __name__ == "__main__":
    test_url = "https://haryanapolice.gov.in/ViewFIR/FIRStatusSearch?From=LFhlihlx%2fW49VSlBvdGc4w%3d%3d"

    service = Service("./chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    fir_texts, first_page_data = fetch_fir_reports(test_url, driver)
    corpus = pd.DataFrame(
        zip(fir_texts, first_page_data), columns=["fir_text", "metadata_html"]
    )
    corpus.to_csv("test_files.csv")

    driver.close()
