from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import sys, os

sys.path.append(os.getcwd())

test_url = "https://haryanapolice.gov.in/ViewFIR/FIRStatusSearch?From=LFhlihlx%2fW49VSlBvdGc4w%3d%3d"


def fetch_fir_reports(test_url):
    service = Service("./eda/chromedriver")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

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

    table_links = driver.find_elements(
        By.XPATH, '//table[@id="tblDisplayRecords"]/tbody/tr'
    )

    n = len(table_links)
    fir_texts = []

    for fir, index in zip(table_links, range(n)):

        fir.find_elements(
            By.ID, "ContentPlaceHolder1_rptDisplayRecords_lnkFIRViewDetail_{index}"
        )[0].click()
        driver.switch_to.window(driver.window_handles[1])

        driver.find_element(
            By.XPATH, "//input[@name='RptView$ctl06$ctl00$Next$ctl00$ctl00']"
        ).click()

        full_fir_text = driver.find_element(
            By.XPATH, "//span[contains(@class, '556')]"
        ).text

        fir_texts.append(full_fir_text)

        driver.switch_to.window(driver.window_handles[0])

    return fir_texts
