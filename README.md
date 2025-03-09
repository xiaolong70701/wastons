# WatsonsScraper 🛍️

A Python-based web scraper for extracting product information from **Watsons Taiwan** using **Selenium-Wire** and **Requests**. The scraper retrieves **Authorization tokens**, fetches product details via the Watsons API, and saves the data in a CSV file.

## 📌 Features
✔ **Automated Authorization Retrieval** - Uses `Selenium-Wire` to extract `Authorization` and `PIM-SESSION-ID`.  
✔ **Watsons API Data Scraping** - Fetches product details including **name, price, image URL, and product link**.  
✔ **Progress Bar with `tqdm`** - Displays real-time progress while scraping.  
✔ **CSV Data Storage** - Saves extracted data in a structured CSV format.  
✔ **Customizable Folder Path** - Allows users to specify the save location (defaults to `./data`).  

---

## 📦 **Installation**
Before running the scraper, install the required dependencies:

```bash
pip install selenium-wire requests tqdm
```

Alternatively, if you have added wastons as a package:

```bash
pip install git+https://github.com/xiaolong70701/wastons.git
```

## 🚀 **Example Usage**

Run the following script to scrape Watsons for sunscreen stick (防曬棒) products:

```python
from wastons.scraper import WatsonsScraper

scraper = WatsonsScraper(query="防曬棒")
scraper.run()
```

This will:

1. Retrieve the Authorization token and PIM-SESSION-ID.
2. Scrape product data from the Watsons API.
3. Save the results in a CSV file located in `./data/Watsons_防曬棒.csv`.

## ⚙ **Customization**

### Specify Save Folder

By default, the CSV files are saved in `./data/`. You can specify a different folder:

```python
scraper = WatsonsScraper(query="面膜", save_folder="./my_results")
scraper.run()
```

This will save the output file to `./my_results/Watsons_面膜.csv`.

### Adjust Number of Products per Page

To increase the number of products retrieved per API request:

```python
scraper = WatsonsScraper(query="洗面乳", page_size=50)
scraper.run()
```

This increases the page size from 32 (default) to 50.