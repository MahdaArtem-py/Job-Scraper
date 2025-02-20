# Job Scraper with PyQt6 and Selenium

This project is a job scraper that extracts job listings from the Dou.ua job board, featuring a graphical user interface (GUI) built with **PyQt6**. The scraper is powered by **Selenium** and can be used to fetch job vacancies based on categories, scrape job details, and save the results to a CSV file.

## Features

- **GUI for Interaction**: 
  - Load job categories from the Dou.ua job board.
  - Select a category from a list to scrape job postings.
  - Start the scraping process and display the status in the GUI.
  
- **Job Scraping**:
  - Scrapes job details such as position, company, location, and salary.
  
- **Export**: 
  - Saves the scraped job listings to a CSV file for further analysis.

## Requirements

- Python 3.7+
- PyQt6
- Selenium
- Pandas
- WebDriver Manager
- ChromeDriver (automatically handled by WebDriver Manager)

### Install Dependencies

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
