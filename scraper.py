import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time


class JobScraper:
    """Scrape list of python vacancies from Dou"""

    def __init__(self) -> None:
        self.url = "https://jobs.dou.ua/vacancies/?category=Python"
        self.driver = webdriver.Chrome()
        self.jobs = []

    def open_site(self) -> None:
        """Open Jobs Dou with python vacancies"""

        self.driver.get(self.url)

    def scrape_jobs(self) -> None:
        """Extract Python vacancies from Dou"""

        job_container = self.driver.find_elements(By.CLASS_NAME, "l-vacancy")
        for job in job_container:
            position = job.find_element(By.CLASS_NAME, "vt").text
            company = job.find_element(By.CLASS_NAME, "company").text
            city = job.find_element(By.CLASS_NAME, "cities").text
            try:
                salary = job.find_element(By.CLASS_NAME, "salary").text
            except:
                salary = None
            self.jobs.append({"position": position,
                              "company": company,
                              "city or remote": city,
                              "salary": salary})

    def load_more_btn(self) -> None:
        """Click on Load More button"""
        while True:
            try:
                load_more_button = self.driver.find_element(By.CSS_SELECTOR,
                                                            ".more-btn a")
                actions = ActionChains(self.driver)
                actions.move_to_element(load_more_button).perform()
                load_more_button.click()
                time.sleep(2)
                self.scrape_jobs()
            except:
                print("No more jobs")
                break

    def save_to_csv(self, filename: str) -> None:
        """Save Python vacancies to CSV"""
        df = pd.DataFrame(self.jobs)
        df.to_csv(filename, index=False)
        print(f"Saved data to {filename}.csv")

    def run_scraping(self) -> None:
        """Run scraping jobs"""
        self.open_site()
        self.scrape_jobs()
        self.load_more_btn()
        self.save_to_csv("jobs.csv")
        print("Finished")


if __name__ == "__main__":
    scraper = JobScraper()
    scraper.run_scraping()
