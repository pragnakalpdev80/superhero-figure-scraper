import csv
import json
import os
import logging

class DataHandler:
    def __init__(self, output_dir="data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_to_csv(self, data, filename="products.csv"):
        """Saves data into the CSV file."""
        if not data:
            logging.warning("No data to save to CSV.")
            return

        filepath = os.path.join(self.output_dir, filename)
        fields = ['price', 'name', 'url']

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=fields)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            logging.info(f"Successfully saved {len(data)} items to {filepath}")
        except Exception as e:
            logging.error(f"Error saving to CSV: {e}")

    def save_to_json(self, data, filename="products.json"):
        """Saves data into the JSON file."""
        if not data:
            logging.warning("No data to save to JSON.")
            return

        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w') as output_file:
                json.dump(data, output_file, indent=4)
            logging.info(f"Successfully saved {len(data)} items to {filepath}")
        except Exception as e:
            logging.error(f"Error saving to JSON: {e}")
