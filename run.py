import os
import logging

from service.scrape import SuperHeroFigureScraper
from service.data_handling import DataHandler

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/report.log",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    filemode='a')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logger.info("=== Scrapping for superhero action figures started. ===")
    scraper = SuperHeroFigureScraper(headless=False)
    data = scraper.run(max_pages=2)
    logging.info(f"Total Products: {len(data)}")
    logger.info("Data saving to files.")
    handler = DataHandler(output_dir="data")
    handler.save_to_csv(data=data)
    handler.save_to_json(data=data)
    logger.info("=== Data Extraction Successful. ===")
