import os
import time
import requests
import csv
import random
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from seleniumwire import webdriver
from selenium.webdriver.edge.service import Service

class WatsonsScraper:
    def __init__(self, query, page_size=32, edge_path="/usr/local/bin/msedgedriver", save_folder="./data"):
        """
        Initializes the WatsonsScraper class.

        :param query: The search query for Watsons product search.
        :param page_size: Number of products per API page.
        :param edge_path: Path to the Edge WebDriver.
        """
        self.query = query
        self.page_size = page_size
        self.edge_path = edge_path
        self.save_folder = save_folder
        self.authorization_token = None
        self.pim_session_id = None
        self.products = []

        os.makedirs(self.save_folder, exist_ok=True)

    def get_auth_and_pim(self):
        """
        Uses Selenium-Wire to retrieve the Authorization token and PIM-SESSION-ID.
        """
        service = Service(self.edge_path)
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=service, options=options)

        site_url = f"https://www.watsons.com.tw/search?text={self.query}"
        driver.get(site_url)
        time.sleep(10)

        authorization_token, pim_session_id = None, None

        for request in driver.requests[::-1]:
            if "api.watsons.com.tw/api/v2/" in request.url:
                headers = request.headers
                if "Authorization" in headers:
                    authorization_token = headers["Authorization"]
                    break

        for cookie in driver.get_cookies():
            if cookie["name"] == "PIM-SESSION-ID":
                pim_session_id = cookie["value"]

        driver.quit()

        if authorization_token:
            authorization_token = authorization_token.split()[1]

        self.authorization_token = authorization_token
        self.pim_session_id = pim_session_id

    def get_products(self):
        """
        Uses requests to retrieve product information from Watsons API and extracts product specifications.
        """
        if not self.authorization_token or not self.pim_session_id:
            print("Missing Authorization token or PIM-SESSION-ID. Unable to proceed.")
            return []

        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://www.watsons.com.tw/",
            "Authorization": f"Bearer {self.authorization_token}",
        }
        cookies = {"PIM-SESSION-ID": self.pim_session_id}

        session.headers.update(headers)
        session.cookies.update(cookies)

        base_url = "https://api.watsons.com.tw/api/v2/wtctw/products/search"
        all_products = []
        current_page = 0
        total_products = None

        with tqdm(desc="Search Products Info", unit="Product", dynamic_ncols=True) as pbar, ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                api_url = f"{base_url}?fields=FULL&query={self.query}&pageSize={self.page_size}&currentPage={current_page}&sort=mostRelevant&brandRedirect=true&ignoreSort=false&lang=zh_TW&curr=TWD"
                response = session.get(api_url)

                if response.status_code != 200:
                    print(f"API request failed with status code: {response.status_code}")
                    break

                data = response.json()
                products = data.get("products", [])

                if not products:
                    print("No more products available. Ending scraping.")
                    break

                if total_products is None:
                    total_products = data.get("pagination", {}).get("totalResults", len(products))
                    pbar.total = total_products

                # Create product list
                product_list = []
                future_to_product = {}

                for product in products:
                    name = product.get("name", "No Name")
                    price = product.get("price", {}).get("value", "No Price")
                    img_url = product.get("images", [{}])[0].get("url", "No Image")
                    product_url = f"https://www.watsons.com.tw/{product.get('url', '')}"

                    # Create product dictionary
                    product_data = {
                        "Name": name,
                        "Price": price,
                        "Image URL": img_url,
                        "Product Link": product_url,
                        "Specification": "",
                        "Dimensions": "",
                        "Weight": "",
                    }

                    product_list.append(product_data)

                    # Use multihthreadings
                    future = executor.submit(self.get_product_specs, product_url, headers)
                    future_to_product[future] = product_data

                    pbar.update(1)

                # Get product info
                for future in future_to_product:
                    spec_data = future.result()
                    product = future_to_product[future]
                    product["Specification"] = spec_data["Specification"]
                    product["Dimensions"] = spec_data["Dimensions"]
                    product["Weight"] = spec_data["Weight"]

                all_products.extend(product_list)

                current_page += 1
                time.sleep(random.uniform(1, 3))

            self.products = all_products
            return all_products

    def get_product_specs(self, product_url, headers):
        """
        Retrieves product specifications from the product page.
        Extracts "規格", "深、寬、高", and "淨重" as separate fields.
        If a field is missing, it returns an empty string instead of "N/A".

        :param product_url: The URL of the product page.
        :param headers: HTTP headers (same as get_products).
        :return: A dictionary with "Specification", "Dimensions", and "Weight".
        """
        try:
            response = requests.get(product_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to retrieve product page: {product_url} (Status code: {response.status_code})")
                return {"Specification": "", "Dimensions": "", "Weight": ""}

            soup = BeautifulSoup(response.text, "html.parser")

            # Find Specification sheet
            spec_table = soup.find("table", class_="ecTable")
            if not spec_table:
                return {"Specification": "", "Dimensions": "", "Weight": ""}

            specs = {"Specification": "", "Dimensions": "", "Weight": ""}
            for row in spec_table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()

                    if key == "規格":
                        specs["Specification"] = value
                    elif key == "深、寬、高":
                        specs["Dimensions"] = value
                    elif key == "淨重":
                        specs["Weight"] = value

            return specs

        except Exception as e:
            print(f"Error retrieving specifications for {product_url}: {e}")
            return {"Specification": "", "Dimensions": "", "Weight": ""}
        
    def save_to_csv(self):
        """
        Saves the scraped product data to a CSV file inside the specified folder.
        """
        if not self.products:
            print("No products to save. Run the scraper first.")
            return

        filename = os.path.join(self.save_folder, f"Watsons_{self.query}.csv")
        keys = ["Name", "Price", "Image URL", "Product Link", "Specification", "Dimensions", "Weight"]

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.products)

        print(f"Saved {len(self.products)} products to {filename}")

    def run(self):
        """
        Executes the full scraping process: retrieving credentials, scraping products, and saving to CSV.
        """
        self.get_auth_and_pim()
        self.get_products()
        self.save_to_csv()
