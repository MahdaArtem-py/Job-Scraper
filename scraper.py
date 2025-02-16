import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.select import Select


class JobScraper:
    """Scrape list of vacancies from Dou"""

    def __init__(self) -> None:
        self.BASE_URL = "https://jobs.dou.ua/"
        self.driver = webdriver.Chrome()
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
        print("\nAvailable Categories:")
        for index, name in categories.items():
            print(f"{index}. {name}")
        return select, categories

    def chose_category(self):
        """Choose category from dropdown menu in terminal"""

        select, categories = self.get_categories()

        while True:
            try:
                choice = int(input("\nChoose a category: "))
                if choice in categories:
                    select.select_by_visible_text(categories[choice])
                    time.sleep(2)
                    return
                else:
                    print("\nInvalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def scrape_jobs(self) -> None:
        """Extract vacancies from Dou"""

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
        """Save vacancies to CSV"""
        df = pd.DataFrame(self.jobs)
        df.to_csv(filename, index=False)
        print(f"Saved data to {filename}.csv")

    def run_scraping(self) -> None:
        """Run scraping jobs"""
        self.open_site()
        self.chose_category()
        self.scrape_jobs()
        self.load_more_btn()
        self.save_to_csv("jobs.csv")
        print("Finished")


if __name__ == "__main__":
    scraper = JobScraper()
    scraper.run_scraping()
