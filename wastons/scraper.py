import os
import time
import requests
import csv
from tqdm import tqdm
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
        self.save_folder = save_folder  # Default to ./data
        self.authorization_token = None
        self.pim_session_id = None
        self.products = []  # Stores scraped products

        # Ensure the save folder exists
        os.makedirs(self.save_folder, exist_ok=True)  # Create the folder if it doesn't exist

    def get_auth_and_pim(self):
        """
        Uses Selenium-Wire to retrieve the Authorization token and PIM-SESSION-ID.
        """
        service = Service(self.edge_path)
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=service, options=options)

        site_url = f"https://www.watsons.com.tw/search?text={self.query}"
        driver.get(site_url)
        time.sleep(10)  # Wait for API requests to be made

        # Variables to store the retrieved credentials
        authorization_token = None
        pim_session_id = None

        # Extract headers from API requests
        for request in driver.requests[::-1]:  # Iterate from the latest request
            if "api.watsons.com.tw/api/v2/" in request.url:
                headers = request.headers
                if "Authorization" in headers:
                    authorization_token = headers["Authorization"]
                    break  # Use the latest found Authorization

        # Retrieve PIM-SESSION-ID from cookies
        for cookie in driver.get_cookies():
            if cookie["name"] == "PIM-SESSION-ID":
                pim_session_id = cookie["value"]

        driver.quit()

        # Ensure the authorization token is correctly formatted
        if authorization_token:
            authorization_token = authorization_token.split()[1]  # Extract token value after "Bearer"

        self.authorization_token = authorization_token
        self.pim_session_id = pim_session_id

    def get_products(self):
        """
        Uses requests to retrieve product information from Watsons API.
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
        total_products = None  # Used for progress bar initialization

        with tqdm(desc="Search Products Info", unit="Product", dynamic_ncols=True) as pbar:
            while True:
                # Construct API URL
                api_url = f"{base_url}?fields=FULL&query={self.query}&pageSize={self.page_size}&currentPage={current_page}&sort=mostRelevant&brandRedirect=true&ignoreSort=false&lang=zh_TW&curr=TWD"
                response = session.get(api_url)

                # Handle API request failure
                if response.status_code != 200:
                    print(f"API request failed with status code: {response.status_code}")
                    break

                data = response.json()
                products = data.get("products", [])

                if not products:
                    print("No more products available. Ending scraping.")
                    break

                # Update total product count for tqdm (only set once)
                if total_products is None:
                    total_products = data.get("pagination", {}).get("totalResults", len(products))
                    pbar.total = total_products  # Set total products in tqdm progress bar

                # Extract product information
                for product in products:
                    name = product.get("name", "No Name")
                    price = product.get("price", {}).get("value", "No Price")
                    img_url = product.get("images", [{}])[0].get("url", "No Image")
                    product_url = f"https://www.watsons.com.tw/{product.get('url', '')}"

                    all_products.append({
                        "Name": name,
                        "Price": price,
                        "Image URL": img_url,
                        "Product Link": product_url,
                    })

                    pbar.update(1)  # Update progress bar

                current_page += 1
                time.sleep(1)  # Pause between requests to prevent rate limiting

        self.products = all_products  # Store for later use
        return all_products

    def save_to_csv(self):
        """
        Saves the scraped product data to a CSV file inside the specified folder.
        """
        if not self.products:
            print("No products to save. Run the scraper first.")
            return
        
        filename = os.path.join(self.save_folder, f"Watsons_{self.query}.csv")  # Save to the specified folder
        keys = self.products[0].keys()  # Get column names

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