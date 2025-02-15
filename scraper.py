import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
site_to_scrape  = "https://jobs.dou.ua/vacancies/?category=Python"
driver.get(site_to_scrape)

work_data = []

def scrape_jobs():
    job_container = driver.find_elements(By.CLASS_NAME, "l-vacancy")
    for job in job_container:
        position = job.find_element(By.CLASS_NAME, "vt").text
        company = job.find_element(By.CLASS_NAME, "company").text
        city = job.find_element(By.CLASS_NAME, "cities").text
        try:
            salary = job.find_element(By.CLASS_NAME, "salary").text
        except:
            salary = None
        work_data.append({"position": position, "company": company, "city or remote": city, "salary": salary})

scrape_jobs()

while True:
    try:
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".more-btn a")
        actions = ActionChains(driver)
        actions.move_to_element(load_more_button).perform()
        load_more_button.click()
        time.sleep(2)
        scrape_jobs()
    except:
        print("No more jobs")
        break

df = pd.DataFrame(work_data)
df.to_csv("jobs.csv", index=False)
driver.quit()