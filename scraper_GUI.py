from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton,
                             QVBoxLayout, QLabel, QListWidget)
import sys
from scraper import JobScraper


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.scraper = JobScraper()
        self.init_GUI()

    def init_GUI(self):
        self.setWindowTitle("Job Scraper")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Press 'Load Categories' to fetch job categories")
        layout.addWidget(self.label)

        self.load_button = QPushButton("Load Categories")
        self.load_button.clicked.connect(self.load_categories)
        layout.addWidget(self.load_button)

        self.category_list = QListWidget()
        layout.addWidget(self.category_list)

        self.scrape_button = QPushButton("Scrape")
        self.scrape_button.setEnabled(False)
        self.scrape_button.clicked.connect(self.start_scraping)
        layout.addWidget(self.scrape_button)

        self.setLayout(layout)

    def load_categories(self):
        select, categories = self.scraper.get_categories()
        self.category_list.clear()
        for index, name in categories.items():
            self.category_list.addItem(name)
        self.scrape_button.setEnabled(True)
        self.label.setText("Select a category and press 'Start Scraping'")

    def start_scraping(self):
        """Start scraping based on the selected category."""
        selected_items = self.category_list.selectedItems()
        if selected_items:
            category = selected_items[0].text()
            self.scraper.driver.quit()
            self.scraper = JobScraper()
            self.scraper.chose_category(category)
            self.scraper.run_scraping(category)
            self.label.setText(f"Scraping completed for: {category}")
        else:
            self.label.setText("Please select a category!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
