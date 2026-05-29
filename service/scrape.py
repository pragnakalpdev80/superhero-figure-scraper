import logging
from playwright.sync_api import sync_playwright


class SuperHeroFigureScraper:
    def __init__(self, headless=True):
        """Base URL set up."""
        self.base_url = "https://www.bigbadtoystore.com" 
        self.url = "https://www.bigbadtoystore.com/Search?HideInStock=false&HidePreorder=false&HideSoldOut=false&InventoryStatus=i,p,so&PageSize=100&SortOrder=Relevance&SearchText=superhero%20action%20figures"
        self.headless = headless
        self.extracted_data = []
        
    def run(self, max_pages=2):
        """Runs the URL and calls the extraction method and changes the page"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(self.url)
            current_page = 1
            
            while current_page <=max_pages:
                logging.info(f"Data extracted from page {current_page} started.")
                self.extract(page=page)
                logging.info(f"Extracted data from page {current_page}.")

                if current_page < max_pages:    
                    next_page = page.locator(".PagedList-skipToNext").get_by_role("link")
                    if next_page.count() == 0:
                        logging.warning("Next page not found")
                        break  
                    try:                          
                        next_page.click()  
                        current_page+=1
                        page.goto(page.url)
                        logging.info(f"Redirecting to the page {current_page}")

                    except Exception as exc:
                        print(exc)
                else:
                    logging.info(f"Extracted data from all pages.")
                    break

            return self.extracted_data

    def extract(self, page):
        """Extracts name, price and URL of the products."""
        products = page.locator(".product-card").all()

        for product in products:
            try:
                name_locator = product.locator(".product-card-title")
                name = name_locator.text_content(timeout=2000).strip()

            except Exception as exc:
                name = "N/A"
                logging.warning("Name not found for product")

            try:
                price_locator = product.locator(".product-card-price")
                price = price_locator.text_content(timeout=2000).strip()
            
            except Exception as exc:
                logging.warning(f"Price not found for {name} ")
                price = "N/A"
            
            try:
                relative_url = product.get_attribute("href")
                url = f"{self.base_url}{relative_url}"

            except Exception as exc:
                logging.warning(f"URL not found for {name} ")
                url = "N/A"
            
            self.extracted_data.append({
                "name": name,
                "price": price,
                "url": url
            })
            

        

