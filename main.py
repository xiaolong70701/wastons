from wastons import WatsonsScraper

if __name__ == "__main__":
    query = input("Please enter product name:")
    scraper = WatsonsScraper(query=query)
    products = scraper.run()