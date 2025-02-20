import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from selenium.webdriver.support.select import Select


class JobScraper:
    """Scrape list of vacancies from Dou"""

    def __init__(self) -> None:
        self.BASE_URL = "https://jobs.dou.ua/"
        chrome_options = Options()
        service = Service(ChromeDriverManager().install())
        chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options, service=service)
        self.jobs = []

    def open_site(self) -> None:
        """Open Jobs Dou with vacancies"""

        self.driver.get(self.BASE_URL)

    def get_categories(self) -> tuple:
        """Extracts job categories from the dropdown menu"""

        self.open_site()
        time.sleep(2)
        categories_dropdown = self.driver.find_element(By.NAME, "category")
        select = Select(categories_dropdown)
        categories = {i: option.text for i, option
                      in enumerate(select.options, start=1)}
        return select, categories

    def chose_category(self, category_name: str) -> None:
        """Choose category from dropdown menu in terminal"""

        select, categories = self.get_categories()

        if category_name in categories.values():
            select.select_by_visible_text(category_name)
            time.sleep(2)

    def scrape_jobs(self) -> None:
        """Extract vacancies from Dou"""

        job_container = self.driver.find_elements(By.CLASS_NAME, "l-vacancy")
        for job in job_container:
            position = job.find_element(By.CLASS_NAME, "vt").text
            company = job.find_element(By.CLASS_NAME, "company").text
            try:
                city = job.find_element(By.CLASS_NAME, "cities").text
            except NoSuchElementException:
                city = None
            try:
                salary = job.find_element(By.CLASS_NAME, "salary").text
            except NoSuchElementException:
                salary = None
            link = job.find_element(By.CSS_SELECTOR,
                                    "a.vt").get_attribute("href")
            self.jobs.append({"position": position,
                              "company": company,
                              "city or remote": city,
                              "salary": salary,
                              "link": link})

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
                break

    def save_to_csv(self, filename: str) -> None:
        """Save vacancies to CSV"""
        df = pd.DataFrame(self.jobs).drop_duplicates()
        df.to_csv(filename, index=False)
        print(f"Saved data to {filename}.csv")

    def run_scraping(self, category_name) -> None:
        """Run scraping jobs"""
        self.open_site()
        self.chose_category(category_name)
        self.scrape_jobs()
        self.load_more_btn()
        self.save_to_csv("jobs.csv")
        print("Finished")
        self.driver.quit()


if __name__ == "__main__":
    scraper = JobScraper()
    scraper.run_scraping()
